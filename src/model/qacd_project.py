from contextlib import contextmanager
from enum import IntEnum, unique
import numpy as np
from operator import itemgetter
import os
import re
from sklearn.cluster import MiniBatchKMeans
import tables
import warnings

from .correction_models import correction_models
from .display_options import DisplayOptions
from .elements import element_properties
from .preset_ratios import preset_ratios
from . import utils


@unique
class State(IntEnum):
    INVALID = -1    # Filename not set.
    EMPTY = 1       # Filename set.
    RAW = 2         # Added raw element maps, including total.
    FILTERED = 3    # Filtered element maps, including total.
    NORMALISED = 4  # Normalised element maps.
    H_FACTOR = 5    # Calculation of h factor for each normalised pixel.


class QACDProject:
    def __init__(self):
        self._state = State.INVALID
        self._filename = None
        self._display_options = None

        # Cached data to avoid recalculating/re-reading from file.
        self._elements = None
        self._valid_preset_ratios = None
        self._ratios = {}  # dict of name -> tuple of
                           #   (formula, correction_model, preset)
        self._phases = {}  # dict of name -> tuple of (source, ...).  Extra
                           # items depend on source, see create_phase_*
        self._regions = {}  # dict of name -> shape string.

        # Regular expression to match input CSV filenames.
        self._csv_file_re = re.compile('^([A-Z][a-z]?) K series.csv$')

        # Compression filters for pytables chunked arrays.
        self._compression_filters = tables.Filters(complevel=5, complib='blosc')

        # numpy array dtypes.
        self._raw_dtype = np.int32
        self._indices_dtype = np.int8

        # Common elements for simpler analysis.
        self.common_elements = ('Al', 'Ca', 'Fe', 'Mg', 'Si')

        warnings.simplefilter('ignore', tables.NaturalNameWarning)

    def _add_array_stats(self, h5node, array, mask=None):
        # Add statistics of the specified array to the specified h5 file node.
        # If a mask is specified, it is applied to the array before calculating
        # the stats.
        is_bool_array = array.dtype == np.bool

        if mask is not None:
            array = np.ma.masked_array(array, mask=mask)

        if not is_bool_array:
            h5node._v_attrs.min = array.min()
            h5node._v_attrs.max = array.max()

        if array.dtype != self._indices_dtype and not is_bool_array:
            h5node._v_attrs.mean = array.mean()
            h5node._v_attrs.median = np.ma.median(array)
            h5node._v_attrs.std = array.std()

        if is_bool_array:
            number_valid = np.count_nonzero(array)
            number_invalid = array.size - number_valid
        else:
            number_invalid = np.ma.count_masked(array)
            number_valid = array.size - number_invalid
        h5node._v_attrs.invalid = number_invalid
        h5node._v_attrs.valid = number_valid

    def _get_array(self, full_node_name, masked=True, want_stats=False,
                   h5file=None):
        # masked and want_stats are booleans.
        if h5file:
            return self._get_array_impl(h5file, full_node_name, masked,
                                        want_stats)
        else:
            with self._h5file_ro() as h5file:
                return self._get_array_impl(h5file, full_node_name, masked,
                                            want_stats)

    def _get_array_impl(self, h5file, full_node_name, masked, want_stats):
        # masked and want_stats are booleans.
        if full_node_name not in h5file:
            raise RuntimeError('No such node: {}'.format(full_node_name))

        group_node = h5file.get_node(full_node_name)
        array = h5file.get_node(group_node, 'data').read()
        if masked:
            if full_node_name + '/mask' in h5file:
                mask = h5file.get_node(group_node, 'mask').read()
            else:
                # Derive mask from data array.
                mask = array == 0
            array = np.ma.masked_array(array, mask=mask)

        if array.dtype in [self._raw_dtype, self._indices_dtype]:
            np.ma.set_fill_value(array, -1)
        elif array.dtype == np.bool:
            np.ma.set_fill_value(array, False)
        else:
            np.ma.set_fill_value(array, np.nan)

        if want_stats:
            keys = group_node._v_attrs._f_list('user')
            stats = {key: group_node._v_attrs[key] for key in keys}
            return array, stats
        else:
            return array

    def _get_filtered_total_mask(self, h5file):
        node = h5file.get_node('/filtered/total/mask')
        mask = node.read()
        return mask

    def _get_pixel_grid(self):
        shape = self.shape
        x, y = np.meshgrid(np.arange(shape[1]) + 0.5, np.arange(shape[0]) + 0.5)
        return x, y

    @contextmanager
    def _h5file(self):
        # All writing to h5 file is done in a 'with self._h5file() as f' block.
        # State should also be changed within such a block to ensure it is
        # correctly written to file.
        if self._state == State.INVALID:
            h5file = tables.open_file(self._filename, mode='w',
                title='QACD-quack file', filters=self._compression_filters)
            h5file.root._v_attrs.file_version = 1
        else:
            h5file = tables.open_file(self._filename, mode='r+')
            assert(State[h5file.root._v_attrs.state] == self._state)
        try:
            yield h5file
            h5file.root._v_attrs.state = self._state.name
        finally:
            h5file.close()

    @contextmanager
    def _h5file_ro(self, ignore_state=False):
        # Read only access to h5 file.
        h5file = tables.open_file(self._filename, mode='r')
        if not ignore_state:
            assert(State[h5file.root._v_attrs.state] == self._state)
        try:
            yield h5file
        finally:
            h5file.close()

    def calculate_region_ellipse(self, centre, size):
        # Calculate and return boolean array corresponding to ellipse region.
        # Does not store the region.  centre and size are 2-tuples.
        x, y = self._get_pixel_grid()
        return utils.calculate_region_ellipse(x, y, centre, size)

    def calculate_region_polygon(self, points):
        # Calculate and return boolean array corresponding to polygon region.
        # Does not store the region.  points is a numpy array of shape (n, 2).
        x, y = self._get_pixel_grid()
        return utils.calculate_region_polygon(x, y, points)

    def calculate_region_rectangle(self, corner0, corner1):
        # Calculate and return boolean array corresponding to rectangle region.
        # Does not store the region.  corner0 and corner1 are 2-tuples.
        x, y = self._get_pixel_grid()
        return utils.calculate_region_rectangle(x, y, corner0, corner1)

    def create_h_factor(self, progress_callback=None):
        if self._state != State.NORMALISED:
            raise RuntimeError('Project does not contain normalised data')

        if progress_callback:
            progress_callback(0.0, 'Calculating h-factor')

        with self._h5file() as h5file:
            Z_mean = None
            A_mean = None
            for element in self.elements:
                normalised = self.get_normalised(element, masked=False,
                                                 h5file=h5file)
                Z, A = element_properties[element][1:3]

                if Z_mean is None:
                    Z_mean = normalised*Z
                    A_mean = normalised*A
                else:
                    Z_mean += normalised*Z
                    A_mean += normalised*A

            h_factor = 1.2*A_mean / (Z_mean**2)

            h_factor_group = h5file.create_group( \
                '/', 'h_factor', title='H factor (Philibert 1963)')
            h5file.create_carray(h_factor_group, 'data', obj=h_factor)
            h5file.create_soft_link(h_factor_group, 'mask',
                                    '/filtered/total/mask')

            mask = self._get_filtered_total_mask(h5file)
            self._add_array_stats(h_factor_group, h_factor, mask=mask)

            self._state = State.H_FACTOR

        if progress_callback:
            progress_callback(1.0, 'Finished')

    def create_phase_map_by_thresholding(self, name, elements_and_thresholds,
                                         phase_map=None):
        # Create a phase map (boolean array) of pixels that are within the
        # (lower, upper) filtered values for one or more elements.
        # elements_and_thresholds is a sequence of (element, lower, upper)
        # tuples.
        # The phase_map itself can be specified, in which case this is used and
        # no validation of it is performed.
        if self._state < State.FILTERED:
            raise RuntimeError('Cannot create phase map, no filtered data present')
        if name in self._phases:
            raise RuntimeError('Phase name {} already used'.format(name))
        if len(elements_and_thresholds) < 1:
            raise RuntimeError('No elements and thresholds specified')

        if phase_map is None:
            # Create phase map.
            for tuple_ in elements_and_thresholds:
                if len(tuple_) != 3:
                    raise RuntimeError('Invalid element and threshold: {}'.format(tuple_))
                element, lower, upper = tuple_

                within_limits = self.get_filtered_within_limits(element, lower, upper)

                if phase_map is None:
                    phase_map = within_limits
                else:
                    phase_map = np.logical_and(phase_map, within_limits)
        else:
            # Check phase map shape and dtype.
            if phase_map.dtype != np.bool:
                raise RuntimeError('Incorrect dtype for phase {}'.format(name))
            raw_total = self.get_raw_total(masked=False)
            if phase_map.shape != raw_total.shape:
                raise RuntimeError('Incorrect shape for phase {}'.format(name))

        # Store phase map.
        with self._h5file() as h5file:
            if '/phase' in h5file:
                all_phases = h5file.get_node('/phase')
            else:
                all_phases = h5file.create_group('/', 'phase', 'Phase maps')

            phase_group = h5file.create_group(all_phases, name)
            phase_data = h5file.create_carray(phase_group, 'data', obj=phase_map)
            self._add_array_stats(phase_group, phase_map, mask=None)
            source = 'thresholding'
            phase_group._v_attrs.source = source
            phase_group._v_attrs.elements_and_thresholds = elements_and_thresholds

        self._phases[name] = (source, elements_and_thresholds)

    def create_phase_map_from_cluster(self, name, phase_map, k, original_values):
        # Create and store a phase map (boolean array) derived from k-means
        # clustering.  k and original_values can be used to recreate the phase
        # map: k is the number of clusters, original_values is a list of values
        # from the original clustering that this phase comprises.
        if self._state < State.FILTERED:
            raise RuntimeError('Cannot create phase map, no filtered data present')
        if name in self._phases:
            raise RuntimeError('Phase name {} already used'.format(name))
        if len(original_values) < 1:
            raise RuntimeError('No original values specified')

        # Check phase map shape and dtype.
        if phase_map.dtype != np.bool:
            raise RuntimeError('Incorrect dtype for phase {}'.format(name))
        raw_total = self.get_raw_total(masked=False)
        if phase_map.shape != raw_total.shape:
            raise RuntimeError('Incorrect shape for phase {}'.format(name))

        # Store phase map.
        with self._h5file() as h5file:
            if '/phase' in h5file:
                all_phases = h5file.get_node('/phase')
            else:
                all_phases = h5file.create_group('/', 'phase', 'Phase maps')

            phase_group = h5file.create_group(all_phases, name)
            phase_data = h5file.create_carray(phase_group, 'data', obj=phase_map)
            self._add_array_stats(phase_group, phase_map, mask=None)
            source = 'cluster'
            phase_group._v_attrs.source = source
            phase_group._v_attrs.k = k
            phase_group._v_attrs.original_values = original_values

        self._phases[name] = (source, k, original_values)

    def create_ratio_map(self, name, preset=None, elements=None,
                         correction_model=None):
        # Create and store a ratio map of the same shape as the element maps.
        # Either preset should be specified, or elements; the former gives a
        # preset ratio, the latter a custom ratio.
        # For a custom ratio map, elements is a list of element names of
        # len > 1, the ratio map is
        #     elements[0] / sum(elements)
        # whereas elements is a list of a single element, the ratio map is
        #     elements[0]
        # If a preset then it is looked up in the valid presets to determine
        # the corresponding element list.
        # Correction model may be either the name of a correction model, or
        # None if no correction is to be used.
        # Note: Uses unmasked numpy arrays, using np.nan to denote masked out
        # pixels.
        if self._state <= State.NORMALISED:
            raise RuntimeError('Cannot create ratio map, no h factor present')
        if correction_model is not None and \
           correction_model not in correction_models:
            raise RuntimeError('No such correction model: {}'.format(correction_model))
        if name in self._ratios.keys():
            raise RuntimeError("Ratio name '{}' already used".format(name))
        if preset is not None and elements is not None:
            raise RuntimeError('Only specify one of preset and elements when creating a ratio map')

        # Get preset ratio.
        if preset is not None:
            if preset not in self.get_valid_preset_ratios():
                raise RuntimeError('No such preset ratio: {}'.format(preset))
            elements = preset_ratios[preset]

        if len(elements) < 2:
            raise RuntimeError('Not implemented')

        # Check elements are available.
        missing_elements = [e for e in elements if e not in self.elements]
        if len(missing_elements) > 0:
            raise RuntimeError('Missing elements: ' +
                               ', '.join(missing_elements))

        # Get correction model from name.
        if correction_model is not None:
            model = correction_models[correction_model]

            # Check elements are in correction model.
            missing_elements = [e for e in elements if e not in model]
            if len(missing_elements) > 0:
                raise RuntimeError('Elements not in correction model: ' +
                                   ', '.join(missing_elements))

        if correction_model is None:
            # If no correction model, do not need to multiply by h-factor.
            numerator = self.get_filtered(elements[0], masked=False)
            denominator = numerator.copy()
            for element in elements[1:]:
                denominator += self.get_filtered(element, masked=False)
        else:
            # Using a correction model.  If not a preset, apply correction to
            # each (h-factor multiplied) filtered element map before combining
            # to create ratio.  If is a preset, combine (h-factor multiplied)
            # filtered element maps before applying correction.
            h_factor = self.get_h_factor(masked=False)

            numerator = self.get_filtered(elements[0], masked=False)*h_factor
            if preset is None:
                numerator = utils.apply_correction_model(model, elements[0],
                                                         numerator)

            denominator = numerator.copy()
            for element in elements[1:]:
                term = self.get_filtered(element, masked=False)*h_factor
                if preset is None:
                    term = utils.apply_correction_model(model, element, term)
                denominator += term

        # Avoid zero/zero by masking such pixels beforehand.
        denominator[denominator == 0.0] = np.nan
        ratio = numerator / denominator

        if preset is not None and correction_model is not None:
            # Apply correction.
            ratio = utils.apply_correction_model(model, preset, ratio)

        formula = self.get_formula_from_elements(elements)

        # Restrict values to between 0 and 1.
        # Need to deal with runtime warnings about nans here.
        #print('==> before min, max', ratio.min(), ratio.max())
        #ratio[ratio < 0.0] = np.nan
        #ratio[ratio > 1.0] = np.nan
        #print('==> after min, max', ratio.min(), ratio.max())

        mask = np.isnan(ratio)

        with self._h5file() as h5file:
            if '/ratio' in h5file:
                all_ratios = h5file.get_node('/ratio')
            else:
                all_ratios = h5file.create_group('/', 'ratio', 'Ratio maps')

            ratio_group = h5file.create_group(all_ratios, name)
            ratio_data = h5file.create_carray(ratio_group, 'data', obj=ratio)
            ratio_mask = h5file.create_carray(ratio_group, 'mask', obj=mask,
                                              chunkshape=ratio_data.chunkshape)
            self._add_array_stats(ratio_group, ratio, mask=mask)
            ratio_group._v_attrs.formula = formula
            ratio_group._v_attrs.correction_model = correction_model
            ratio_group._v_attrs.preset = preset

        self._ratios[name] = (formula, correction_model, preset)

    def create_region(self, name, shape_string, region):
        # region is a boolean array.
        if self._state < State.FILTERED:
            raise RuntimeError('Cannot create region, no filtered data present')
        if name in self._regions:
            raise RuntimeError('Region name {} already used'.format(name))
        if shape_string not in ('ellipse', 'polygon', 'rectangle'):
            raise RuntimeError('Unrecognised region shape string {}'.format(shape_string))
        if region is None:
            raise RuntimeError('No region boolean array specified')

        # Check region shape and dtype.
        if region.dtype != np.bool:
            raise RuntimeError('Incorrect dtype for region {}'.format(name))
        raw_total = self.get_raw_total(masked=False)
        if region.shape != raw_total.shape:
            raise RuntimeError('Incorrect shape for region {}'.format(name))

        # Store region.
        with self._h5file() as h5file:
            if '/region' in h5file:
                all_regions = h5file.get_node('/region')
            else:
                all_regions = h5file.create_group('/', 'region', 'Region maps')

            region_group = h5file.create_group(all_regions, name)
            region_data = h5file.create_carray(region_group, 'data', obj=region)
            self._add_array_stats(region_group, region, mask=None)
            region_group._v_attrs.shape = shape_string

        self._regions[name] = shape_string

    def delete_all_clusters(self):
        with self._h5file() as h5file:
            if '/cluster' in h5file:
                node = h5file.get_node('/cluster')
                node._f_remove(recursive=True)

    def delete_phase_map(self, name):
        if name not in self.phases:
            raise RuntimeError('No such phase map {}'.format(name))
        self._phases.pop(name)
        with self._h5file() as h5file:
            node = h5file.get_node('/phase', name)
            node._f_remove(recursive=True)

    def delete_ratio_map(self, name):
        if name not in self.ratios:
            raise RuntimeError('No such ratio map {}'.format(name))
        ratio = self._ratios.pop(name)
        with self._h5file() as h5file:
            node = h5file.get_node('/ratio', name)
            node._f_remove(recursive=True)

    def delete_region(self, name):
        if name not in self.regions:
            raise RuntimeError('No such region {}'.format(name))
        self._regions.pop(name)
        with self._h5file() as h5file:
            node = h5file.get_node('/region', name)
            node._f_remove(recursive=True)

    @property
    def display_options(self):
        if self._display_options is None:
            self._display_options = DisplayOptions(self)
            self.load_display_options()
        return self._display_options

    @property
    def elements(self):
        # Read-only property.
        return self._elements

    @property
    def filename(self):
        # Read-only property.
        return self._filename

    def filter(self, pixel_totals, median, progress_callback=None):
        # pixel_totals and median are booleans.
        if self._state != State.RAW:
            raise RuntimeError('Project does not contain raw data')

        if pixel_totals:
            raw_total, stats = self.get_raw_total(masked=False, want_stats=True)
            raw_total_median = stats['median']
            raw_total_std = stats['std']
            # Mask of pixels to remove.
            median_mask = \
                np.logical_or(raw_total < raw_total_median - 2*raw_total_std,
                              raw_total > raw_total_median + raw_total_std)

        with self._h5file() as h5file:
            # Keep arrays unmasked here, using np.nan as masked value.
            filtered_group = h5file.create_group('/', 'filtered',
                                                 'Filtered element maps')
            filtered_group._v_attrs.pixel_totals_filter = pixel_totals
            filtered_group._v_attrs.median_filter = median

            total = None
            raw_mask = None
            filtered_mask = None
            n = len(self.elements)
            for index, element in enumerate(self.elements):
                if progress_callback:
                    text = 'Filtering element {} ({} of {})'.format( \
                        element, index+1, n)
                    progress_callback(index*1.0/n, text)

                raw = self.get_raw(element, h5file=h5file, masked=False)
                if raw_mask is None:
                    # All raw masks are identical, so calculate only once.
                    raw_mask = raw == -1

                # Convert raw array to floats.
                filtered = np.asarray(raw, dtype=np.float64)
                filtered[raw_mask] = np.nan

                if pixel_totals:
                    # Same pixel mask applied to each element map.
                    filtered[median_mask] = np.nan

                if median:
                    # Median filter applied separately to each element map.
                    filtered = utils.median_filter_with_nans(filtered)

                if filtered_mask is None:
                    # All filtered masks are identical, so calculate only once.
                    filtered_mask = np.isnan(filtered)

                element_group = h5file.create_group(filtered_group, element)
                h5file.create_carray(element_group, 'data', obj=filtered)
                h5file.create_soft_link(element_group, 'mask',
                                        '/filtered/total/mask')
                self._add_array_stats(element_group, filtered,
                                      mask=filtered_mask)

                if total is None:
                    total = filtered.copy()
                else:
                    total += filtered

            total_group = h5file.create_group(filtered_group, 'total')
            total_data = h5file.create_carray(total_group, 'data', obj=total)
            total_mask = h5file.create_carray(total_group, 'mask',
                obj=filtered_mask, chunkshape=total_data.chunkshape)
            self._add_array_stats(total_group, total, mask=filtered_mask)

            self._state = State.FILTERED

            if progress_callback:
                progress_callback(1.0, 'Finished')

    def filter_normalise_and_h_factor(self, pixel_totals, median,
                                      progress_callback=None):
        if progress_callback:
            n = len(self.elements)
            time_ratios = np.asarray([2.0*n, n, 1.0])
            time_ratios /= time_ratios.sum()
            cum = np.hstack(([0.0], time_ratios.cumsum()))
            def local_callback(fraction, text):
                fraction = cum[stage] + fraction*(cum[stage+1] - cum[stage])
                progress_callback(fraction, text)
        else:
            local_callback = None

        stage = 0
        self.filter(pixel_totals, median, progress_callback=local_callback)

        stage = 1
        self.normalise(progress_callback=local_callback)

        stage = 2
        self.create_h_factor(progress_callback=local_callback)

    def get_cluster_elements(self):
        with self._h5file_ro() as h5file:
            if '/cluster' in h5file:
                group = h5file.get_node('/cluster')
                return group._v_attrs.elements
            else:
                return None

    def get_cluster_indices(self, k, masked=True, want_stats=False):
        # Return array indicating which cluster each pixel is in, from 0 to k-1.
        # If masked==True, invalid pixels are masked out otherwise they are -1.
        if not self.has_cluster():
            raise RuntimeError('No k-means cluster data present')

        return self._get_array('/cluster/k{}/indices'.format(k), masked,
                               want_stats)

    def get_cluster_k(self):
        with self._h5file_ro() as h5file:
            if '/cluster' in h5file:
                group = h5file.get_node('/cluster')
                return (group._v_attrs.k_min, group._v_attrs.k_max)
            else:
                return None

    def get_correction_model_elements(self, correction_model):
        return correction_models[correction_model].keys()

    def get_correction_model_names(self):
        return sorted(correction_models.keys())

    def get_element_from_csv_filename(self, csv_filename):
        match = self.is_valid_csv_filename(csv_filename)
        if not match:
            raise RuntimeError('Invalid CSV file name: {}'.format(csv_file))
        return match.group(1)

    def get_filter_options(self):
        # Return tuple of filter option booleans: (pixel_totals, median).
        if self._state <= State.RAW:
            raise RuntimeError('No filtered data present')

        with self._h5file_ro() as h5file:
            node = h5file.get_node('/filtered')
            return (node._v_attrs.pixel_totals_filter,
                    node._v_attrs.median_filter)

    def get_filtered(self, element, masked=True, want_stats=False, h5file=None):
        # Return filtered element map.  If masked==True, invalid pixels are
        # masked out otherwise they are np.nan.
        if self._state <= State.RAW:
            raise RuntimeError('No filtered data present')
        if element not in self._elements:
            raise RuntimeError('No such element: {}'.format(element))

        return self._get_array('/filtered/' + element, masked, want_stats,
                               h5file=h5file)

    def get_filtered_within_limits(self, element, lower, upper):
        # Return boolean array of the pixels in a filtered element map that are
        # within the specified lower, upper limits.
        if element not in self.elements:
            raise RuntimeError('Unrecognised element {}'.format(element))
        if upper < lower:
            raise RuntimeError('Lower, upper limits for element {} are decreasing'.format(element))

        # Note that filtered has nans instead of being a masked array.
        filtered = self.get_filtered(element, masked=False)

        with np.errstate(invalid='ignore'):
            return np.logical_and(filtered >= lower, filtered <= upper)

    def get_filtered_total(self, masked=True, want_stats=False, h5file=None):
        # Return total of all filtered element maps.  If masked==True, invalid
        # pixels are masked out otherwise they are np.nan.
        if self._state <= State.RAW:
            raise RuntimeError('No filtered data present')

        return self._get_array('/filtered/total', masked, want_stats,
                               h5file=h5file)

    def get_formula_from_elements(self, elements):
        return '{} / ({})'.format(elements[0], '+'.join(elements))

    def get_h_factor(self, masked=True, want_stats=False):
        # Return h factor array.  If masked==True, invalid pixels are masked
        # out otherwise they are np.nan.
        if self._state <= State.NORMALISED:
            raise RuntimeError('No h factor present')

        return self._get_array('/h_factor', masked, want_stats)

    def get_normalised(self, element, masked=True, want_stats=False,
                       h5file=None):
        # Return normalised element ma.  If masked==True, invalid pixels are
        # masked out otherwise they are np.nan.
        if self._state <= State.FILTERED:
            raise RuntimeError('No normalised data present')
        if element not in self._elements:
            raise RuntimeError('No such element: {}'.format(element))

        return self._get_array('/normalised/' + element, masked, want_stats,
                               h5file)

    def get_phase(self, name, masked=True, want_stats=False, h5file=None):
        # Return phase map which is an unmasked boolean array.
        if name not in self._phases:
            raise RuntimeError('No such phase map: {}'.format(name))

        return self._get_array('/phase/' + name, masked=masked,
                               want_stats=want_stats, h5file=h5file)

    def get_preset_elements(self, preset_name):
        return preset_ratios[preset_name]

    def get_preset_formula(self, preset_name):
        return self.get_formula_from_elements(self.get_preset_elements(preset_name))

    def get_ratio(self, name, masked=True, want_stats=False):
        # Return ratio map.  If masked==True, invalid pixels are masked out
        # otherwise they are np.nan.
        if self._state <= State.NORMALISED:
            raise RuntimeError('No normalised data present')
        if name not in self._ratios:
            raise RuntimeError('No such ratio: {}'.format(name))

        return self._get_array('/ratio/' + name, masked, want_stats)

    def get_raw(self, element, masked=True, want_stats=False, h5file=None):
        # Return raw element map.  If masked==True, invalid pixels are masked
        # out otherwise they are -1.
        if self._state <= State.EMPTY:
            raise RuntimeError('No raw data present')
        if element not in self._elements:
            raise RuntimeError('No such element: {}'.format(element))

        return self._get_array('/raw/' + element, masked, want_stats, h5file)

    def get_raw_total(self, masked=True, want_stats=False):
        # Return total of all raw element maps.  If masked==True, invalid
        # pixels are masked out otherwise they are -1.
        if self._state <= State.EMPTY:
            raise RuntimeError('No raw data present')

        return self._get_array('/raw/total', masked, want_stats)

    def get_region(self, name, masked=True, want_stats=False, h5file=None):
        # Return region which is an unmasked boolean array.
        if name not in self._regions:
            raise RuntimeError('No such region: {}'.format(name))

        return self._get_array('/region/' + name, masked=masked,
                               want_stats=want_stats, h5file=h5file)

    def get_valid_preset_ratios(self):
        if self._state <= State.EMPTY:
            raise RuntimeError('No raw data present')

        if self._valid_preset_ratios is None:
            def is_valid(elements):
                for element in elements:
                    if element not in self._elements:
                        return False
                return True

            self._valid_preset_ratios = [ \
                k for k, v in preset_ratios.items() if is_valid(v)]

        return self._valid_preset_ratios

    def has_cluster(self):
        with self._h5file_ro() as h5file:
            return '/cluster' in h5file

    def import_raw_csv_files(self, directory, csv_filenames=None,
                             progress_callback=None):
        # If no csv_filenames are specified, loads all appropriate files from
        # the directory.
        if self._state != State.EMPTY:
            raise RuntimeError('Project already contains raw data')

        if csv_filenames:
            # Check csv_filenames are correct.
            for csv_filename in csv_filenames:
                if os.path.dirname(csv_filename) != '':
                    raise RuntimeError('Unexpected directory in {}'.format(csv_filename))
                if not self.is_valid_csv_filename(csv_filename):
                    raise RuntimeError('Invalid CSV file name: {}'.format(csv_filename))
        else:
            csv_filenames = list(filter(self._csv_file_re.match,
                                        os.listdir(directory)))

        csv_filenames.sort()

        with self._h5file() as h5file:
            h5file.create_group('/', 'raw', 'Raw element maps')

            # Load files one at a time and save in project file.
            shape = None
            total = None
            elements = []
            n = len(csv_filenames)
            for index, csv_filename in enumerate(csv_filenames):
                element = self.get_element_from_csv_filename(csv_filename)

                text = 'Loading element {} from CSV file ({} of {} files)'.format( \
                    element, index+1, n)
                if progress_callback:
                    progress_callback(index*1.0/(n+1), text)

                elements.append(element)
                full_filename = os.path.join(directory, csv_filename)
                raw = utils.read_csv(full_filename, self._raw_dtype, shape)
                if index == 0:
                    shape = raw.shape

                # Add raw array to project file.
                # Correcting for mask and adding stats later.
                element_group = h5file.create_group('/raw', element)
                h5file.create_carray(element_group, 'data', obj=raw)
                h5file.create_soft_link(element_group, 'mask',
                                        '/raw/total/mask')

                if total is None:
                    total = raw.copy()
                else:
                    total += raw

            # Set cached list of elements.
            h5file.create_array('/', 'elements', obj=elements, title='Elements')
            self._elements = elements

            if progress_callback:
                progress_callback(n/(n+1.0), 'Calculating and writing pixel totals')

            # Mask out pixels for which total is zero.
            mask = total == 0
            has_mask = np.any(mask)
            if has_mask:
                total[mask] = -1

            # Write raw total to project file.
            total_group = h5file.create_group('/raw', 'total')
            total_data = h5file.create_carray(total_group, 'data', obj=total)
            if has_mask:
                h5file.create_carray(total_group, 'mask', obj=mask,
                                     chunkshape=total_data.chunkshape)
            else:
                h5file.create_array(total_group, 'mask', obj=np.ma.nomask)
            self._add_array_stats(total_group, total, mask=mask)

            if has_mask:
                # Update all raw element maps with mask.
                for element in self.elements:
                    data_node = h5file.get_node('/raw/' + element + '/data')
                    raw = data_node.read()
                    raw[mask] = -1
                    data_node[:] = raw

            if progress_callback:
                progress_callback((n+0.5)/(n+1.0), 'Calculating and writing statistics')

            # Set element stats.
            for element in self.elements:
                data_node = h5file.get_node('/raw/' + element + '/data')
                raw = data_node.read()
                self._add_array_stats(data_node._v_parent, raw, mask=mask)

            self._state = State.RAW

            if progress_callback:
                progress_callback(1.0, 'Finished')

    def is_valid_csv_filename(self, csv_filename):
        return self._csv_file_re.match(csv_filename)

    def k_means_clustering(self, k_min, k_max, want_all_elements, reorder=True,
                           progress_callback=None):
        # k_min and k_max are min and max number of clusters.
        # If reorder is True, will reorder labels so that they are consistent
        # across different k values rather than being randomly ordered.
        if self.has_cluster():
            raise RuntimeError('k-means clustering already performed')
        if self._state != State.H_FACTOR:
            raise RuntimeError('No h-factor map present')
        if k_max <= k_min:
            raise RuntimeError('k (number of clusters) must be increasing')

        # Obtain array of all filtered element maps.  k-means clustering cannot
        # deal with masked arrays (or np.nan or np.inf) so need to remove
        # masked out pixels beforehand.
        if progress_callback:
            progress_callback(0.0, 'Preparing array of all filtered element maps')

        elements = self._elements
        if not want_all_elements:
            elements = sorted(set(self.common_elements).intersection(elements))

        all_elements = None
        for i, element in enumerate(elements):
            filtered = self.get_filtered(element)  # Masked.

            if i == 0:
                ny, nx = filtered.shape

                # mask_valid is 1D array of pixels to keep.  It is the same for
                # all filtered element maps.
                filtered_mask = filtered.mask
                mask_valid = ~filtered_mask.ravel()
                if np.all(mask_valid):
                    mask_valid = None
                    npixels = nx*ny
                else:
                    npixels = np.sum(mask_valid)

                all_elements = np.empty((npixels, len(elements)))

            all_elements[:, i] = filtered.compressed()

        with self._h5file() as h5file:
            cluster_group = h5file.create_group('/', 'cluster',
                                                'k-means clustering')
            cluster_group._v_attrs.k_min = k_min
            cluster_group._v_attrs.k_max = k_max
            cluster_group._v_attrs.elements = \
                'all' if want_all_elements else ', '.join(elements)

            for k in range(k_min, k_max+1):
                if progress_callback:
                    text = 'Calculating clusters for k={}'.format(k)
                    progress_callback((k-k_min+1) / (k_max-k_min+2), text)

                kmeans = MiniBatchKMeans(n_clusters=k, random_state=1234,
                                         n_init=10)

                # Indices are cluster of each pixel in range 0 to k-1.
                # Use -1 to indicate masked out pixels.
                indices = kmeans.fit_predict(all_elements).astype(
                    self._indices_dtype)
                if mask_valid is not None:
                    masked_labels = indices
                    indices = np.full((nx*ny), -1, dtype=self._indices_dtype)
                    indices[mask_valid] = masked_labels
                    masked_labels = None

                indices.shape = (ny, nx)
                centroids = kmeans.cluster_centers_

                if reorder:
                    element_stds = np.std(all_elements, axis=0)
                    sort_element_index = np.argmax(element_stds)
                    sort_indices = np.argsort(centroids[:, sort_element_index])

                    # Reorder centroids.
                    centroids = centroids[sort_indices]

                    # Reorder indices.
                    unsorted = indices.copy()
                    for to_index in range(k):
                        from_index = sort_indices[to_index]
                        indices[unsorted == from_index] = to_index
                    unsorted = None

                # Write to h5 file.  Separate mask for each as they may be
                # edited.
                k_group = h5file.create_group(cluster_group, 'k{}'.format(k))
                indices_group = h5file.create_group(k_group, 'indices')
                indices_data = h5file.create_carray(indices_group, 'data',
                                                    obj=indices)
                indices_mask = h5file.create_carray(indices_group, 'mask',
                    obj=filtered_mask, chunkshape=indices_data.chunkshape)
                self._add_array_stats(indices_group, indices,
                                      mask=filtered_mask)
                h5file.create_carray(k_group, 'centroids', obj=centroids)

            if progress_callback:
                progress_callback(1.0, 'Finished')

    def load_display_options(self):
        options = self.display_options
        with self._h5file_ro() as h5file:
            if '/display_options' not in h5file:
                return

            group_node = h5file.get_node('/display_options')

            def read_and_set_option(name):
                if name in group_node._v_attrs:
                    attr_name = '_' + name
                    if not hasattr(options, attr_name):
                        raise RuntimeError('No such attribute: '+attr_name)
                    setattr(options, attr_name, group_node._v_attrs[name])

            for name in ['colourmap_name', 'show_ticks_and_labels',
                         'overall_title', 'show_project_filename', 'show_date',
                         'use_scale', 'pixel_size', 'units', 'show_scale_bar',
                         'scale_bar_location', 'scale_bar_colour',
                         'use_histogram_bin_count', 'histogram_bin_count',
                         'histogram_bin_width', 'histogram_max_bin_count',
                         'show_mean_median_std_lines', 'auto_zoom_region']:
                read_and_set_option(name)

    def load_file(self, filename):
        if self._state != State.INVALID:
            raise RuntimeError('Cannot load into existing project')

        self._filename = filename
        with self._h5file_ro(ignore_state=True) as h5file:
            # Check file version number.
            version = h5file.root._v_attrs.file_version
            if version != 1:
                raise RuntimeError('Unrecognised file version: ' + version)

            # Read state.
            self._state = State[h5file.root._v_attrs.state]

            shape = None
            indices_stats = ['min', 'max', 'invalid', 'valid']
            all_stats = indices_stats + ['mean', 'median', 'std']
            ratio_stats = all_stats + ['formula', 'correction_model', 'preset']
            phase_stats = ['valid', 'invalid', 'source']
            region_stats = ['valid', 'invalid', 'shape']

            if self._state < State.RAW:
                if '/raw' in h5file:
                    raise RuntimeError('Unexpected node /raw')
            else:
                # Get list of all elements.
                elements = sorted(h5file.get_node('/raw')._v_children.keys())
                if len(elements) == 0 or elements[-1] != 'total':
                    raise RuntimeError('No raw total')
                elements = elements[:-1]
                self._elements = elements

                elements_and_total = self._elements + ['total']

                # Check raw.
                raw_chunkshape = None
                for element in elements_and_total:
                    node = h5file.get_node('/raw/{}'.format(element))
                    attrs = node._v_attrs._v_attrnames
                    if not all([name in attrs for name in all_stats]):
                        raise RuntimeError('Missing stats in raw {}'.format(element))

                    for type_, dtype in zip(['data', 'mask'], [self._raw_dtype, np.bool]):
                        node = h5file.get_node('/raw/{}/{}'.format(element, type_))
                        if isinstance(node, tables.link.SoftLink):
                            node = node.dereference()

                        if node.dtype != dtype:
                            raise RuntimeError('Incorrect dtype for raw {} {}'.format(element, type_))

                        if type_ == 'mask' and node.shape == ():
                            if node.read() != False:
                                raise RuntimeError('Incorrect empty mask for raw {}'.format(element))
                        elif shape is None:
                            shape = node.shape
                            raw_chunkshape = node.chunkshape
                        else:
                            if node.shape != shape:
                                raise RuntimeError('Incorrect raw shape for {} {}'.format(element, type_))
                            if node.chunkshape != raw_chunkshape:
                                raise RuntimeError('Incorrect raw chunkshape for {} {}'.format(element, type_))

            if self._state < State.FILTERED:
                if '/filtered' in h5file:
                    raise RuntimeError('Unexpected node /filtered')
            else:
                # Check filtered.
                filtered_chunkshape = None
                for element in elements_and_total:
                    node = h5file.get_node('/filtered/{}'.format(element))
                    attrs = node._v_attrs._v_attrnames
                    if not all([name in attrs for name in all_stats]):
                        raise RuntimeError('Missing stats in filtered {}'.format(element))

                    for type_, dtype in zip(['data', 'mask'], [np.float64, np.bool]):
                        node = h5file.get_node('/filtered/{}/{}'.format(element, type_))
                        if isinstance(node, tables.link.SoftLink):
                            node = node.dereference()

                        if node.dtype != dtype:
                            raise RuntimeError('Incorrect dtype for filtered {} {}'.format(element, type_))

                        if type_ == 'mask' and node.shape == ():
                            if node.read() != False:
                                raise RuntimeError('Incorrect empty mask for filtered {}'.format(element))
                        else:
                            if node.shape != shape:
                                raise RuntimeError('Incorrect filtered shape for {} {}'.format(element, type_))
                            if filtered_chunkshape is None:
                                filtered_chunkshape = node.chunkshape
                            else:
                                if node.chunkshape != filtered_chunkshape:
                                    raise RuntimeError('Incorrect filtered chunkshape for {} {}'.format(element, type_))

            if self._state < State.NORMALISED:
                if '/normalised' in h5file:
                    raise RuntimeError('Unexpected node /normalised')
            else:
                # Check normalised.
                normalised_chunkshape = None
                for element in elements:   # Not including 'total'!
                    node = h5file.get_node('/normalised/{}'.format(element))
                    attrs = node._v_attrs._v_attrnames
                    if not all([name in attrs for name in all_stats]):
                        raise RuntimeError('Missing stats in normalised {}'.format(element))

                    for type_, dtype in zip(['data', 'mask'], [np.float64, np.bool]):
                        node = h5file.get_node('/normalised/{}/{}'.format(element, type_))
                        if isinstance(node, tables.link.SoftLink):
                            node = node.dereference()

                        if node.dtype != dtype:
                            raise RuntimeError('Incorrect dtype for normalised {} {}'.format(element, type_))

                        if type_ == 'mask' and node.shape == ():
                            if node.read() != False:
                                raise RuntimeError('Incorrect empty mask for normalised {}'.format(element))
                        else:
                            if node.shape != shape:
                                raise RuntimeError('Incorrect normalised shape for {} {}'.format(element, type_))
                            if normalised_chunkshape is None:
                                normalised_chunkshape = node.chunkshape
                            else:
                                if node.chunkshape != normalised_chunkshape:
                                    raise RuntimeError('Incorrect normalised chunkshape for {} {}'.format(element, type_))

            if self._state < State.H_FACTOR:
                if '/h_factor' in h5file:
                    raise RuntimeError('Unexpected node /h_factor')
            else:
                # Check h-factor.
                h_factor_chunkshape = None
                node = h5file.get_node('/h_factor')
                attrs = node._v_attrs._v_attrnames
                if not all([name in attrs for name in all_stats]):
                    raise RuntimeError('Missing stats in h_factor')

                for type_, dtype in zip(['data', 'mask'], [np.float64, np.bool]):
                    node = h5file.get_node('/h_factor/{}'.format(type_))
                    if isinstance(node, tables.link.SoftLink):
                        node = node.dereference()

                    if node.dtype != dtype:
                        raise RuntimeError('Incorrect dtype for h-factor {}'.format(type_))

                    if type_ == 'mask' and node.shape == ():
                        if node.read() != False:
                            raise RuntimeError('Incorrect empty mask for h_factor')
                    else:
                        if node.shape != shape:
                            raise RuntimeError('Incorrect h_factor shape for {}'.format(type_))
                        if h_factor_chunkshape is None:
                            h_factor_chunkshape = node.chunkshape
                        else:
                            if node.chunkshape != h_factor_chunkshape:
                                raise RuntimeError('Incorrect normalised chunkshape for {}'.format(type_))

            if '/ratio' in h5file:
                if self._state < State.H_FACTOR:
                    raise RuntimeError('Unexpected node /ratio')

                # Load and check ratios.
                ratio_chunkshape = None
                group_node = h5file.get_node('/ratio')
                for ratio_node in group_node._f_list_nodes():
                    name = ratio_node._v_name

                    attrs = ratio_node._v_attrs._v_attrnames
                    if not all([name in attrs for name in ratio_stats]):
                        raise RuntimeError('Missing stats in ratio {}'.format(name))

                    # Non-stat attributes of the ratio node.
                    formula = ratio_node._v_attrs.formula
                    correction_model = ratio_node._v_attrs.correction_model
                    preset = ratio_node._v_attrs.preset
                    is_preset = preset is not None

                    if name in self._ratios:
                        raise RuntimeError('Ratio name {} used more than once'.format(name))
                    if correction_model is not None and \
                        correction_model not in correction_models:
                        raise RuntimeError('Ratio {} has invalid correction model {}'.format(name, correction_model))
                    if is_preset and preset not in self.get_valid_preset_ratios():
                        raise RuntimeError('Invalid preset ratio {}'.format(preset))

                    self._ratios[name] = (formula, correction_model, preset)

                    for type_, dtype in zip(['data', 'mask'], [np.float64, np.bool]):
                        node = h5file.get_node('/ratio/{}/{}'.format(name, type_))
                        if isinstance(node, tables.link.SoftLink):
                            node = node.dereference()

                        if node.dtype != dtype:
                            raise RuntimeError('Incorrect dtype for ratio {} {}'.format(name, type_))

                        if type_ == 'mask' and node.shape == ():
                            if node.read() != False:
                                raise RuntimeError('Incorrect empty mask for ratio {}'.format(name))
                        else:
                            if node.shape != shape:
                                raise RuntimeError('Incorrect shape for ratio {} {}'.format(name, type_))
                            if ratio_chunkshape is None:
                                ratio_chunkshape = node.chunkshape
                            else:
                                if node.chunkshape != ratio_chunkshape:
                                    raise RuntimeError('Incorrect chunkshape for ratio {}'.format(name, type_))

            if '/cluster' in h5file:
                if self._state < State.H_FACTOR:
                    raise RuntimeError('Unexpected node /cluster')

                group_node = h5file.get_node('/cluster')
                k_min = group_node._v_attrs.k_min
                k_max = group_node._v_attrs.k_max
                cluster_elements = group_node._v_attrs.elements
                if k_min > k_max:
                    raise RuntimeError('Cluster k_min is greater than k_max')

                n_cluster_elements = len(self.elements) \
                    if cluster_elements == 'all' else len(cluster_elements)

                cluster_chunkshape = None
                for k in range(k_min, k_max+1):
                    k_node = h5file.get_node('/cluster/k{}'.format(k))

                    # Cluster k indices is masked array.
                    indices = h5file.get_node(k_node, 'indices')
                    attrs = indices._v_attrs._v_attrnames
                    if not all([name in attrs for name in indices_stats]):
                        raise RuntimeError('Missing stats in cluster indices {}'.format(k))

                    for type_, dtype in zip(['data', 'mask'], [self._indices_dtype, np.bool]):
                        node = h5file.get_node(indices, type_)
                        if isinstance(node, tables.link.SoftLink):
                            node = node.dereference()

                        if node.dtype != dtype:
                            raise RuntimeError('Incorrect dtype for cluster indices {} {}'.format(k, type_))

                        if type_ == 'mask' and node.shape == ():
                            if node.read() != False:
                                raise RuntimeError('Incorrect empty mask for cluster indices {}'.format(k))
                        else:
                            if node.shape != shape:
                                raise RuntimeError('Incorrect shape for cluster indices {} {}'.format(k, type_))
                            if cluster_chunkshape is None:
                                cluster_chunkshape = node.chunkshape
                            else:
                                if node.chunkshape != cluster_chunkshape:
                                    raise RuntimeError('Incorrect chunkshape for cluster indices {} {}'.format(k, type_))

                    # Cluster k centroids.
                    centroids = h5file.get_node(k_node, 'centroids')
                    if centroids.shape != (k, n_cluster_elements):
                        raise RuntimeError('Incorrect shape for cluster centroids {}'.format(k))
                    if centroids.dtype != np.float64:
                        raise RuntimeError('Incorrect dtype for cluster centroids {}'.format(k))

            if '/phase' in h5file:
                if self._state < State.FILTERED:
                    raise RuntimeError('Unexpected node /phase')

                group_node = h5file.get_node('/phase')
                for phase_node in group_node._f_list_nodes():
                    name = phase_node._v_name

                    # Check attributes.
                    attrs = phase_node._v_attrs._v_attrnames
                    if not all([name in attrs for name in phase_stats]):
                        raise RuntimeError('Missing stats in phase {}'.format(name))

                    source = phase_node._v_attrs.source
                    if source not in ['thresholding', 'cluster']:
                        raise RuntimeError('Incorrect source {} for phase {}'.format(source, name))

                    is_thresholding = source == 'thresholding'
                    if is_thresholding:
                        if 'elements_and_thresholds' not in attrs:
                            raise RuntimeError('No elements_and_thresholds for phase {}'.format(name))
                    else:
                        if 'k' not in attrs:
                            raise RuntimeError('No k for phase {}'.format(name))
                        if 'original_values' not in attrs:
                            raise RuntimeError('No original_values for phase {}'.format(name))

                    # Check array.
                    node = h5file.get_node(phase_node, 'data')
                    if node.dtype != np.bool:
                        raise RuntimeError('Incorrect dtype for phase {}'.format(name))
                    if node.shape != shape:
                        raise RuntimeError('Incorrect shape for phase {}'.format(name))

                    # Store cached data.
                    if is_thresholding:
                        tuple_ = (source,
                                  phase_node._v_attrs.elements_and_thresholds)
                    else:
                        tuple_ = (source, phase_node._v_attrs.k,
                                  phase_node._v_attrs.original_values)
                    self._phases[name] = tuple_

            if '/region' in h5file:
                if self._state < State.FILTERED:
                    raise RuntimeError('Unexpected node /region')

                group_node = h5file.get_node('/region')
                for region_node in group_node._f_list_nodes():
                    name = region_node._v_name

                    # Check attributes.
                    attrs = region_node._v_attrs._v_attrnames
                    if not all([name in attrs for name in region_stats]):
                        raise RuntimeError('Missing stats in region {}'.format(name))

                    shape_string = region_node._v_attrs.shape
                    if shape_string not in ['ellipse', 'polygon', 'rectangle']:
                        raise RuntimeError('Incorrect shape {} for region {}'.format(shape_string, name))

                    # Check array.
                    node = h5file.get_node(region_node, 'data')
                    if node.dtype != np.bool:
                        raise RuntimeError('Incorrect dtype for region {}'.format(name))
                    if node.shape != shape:
                        raise RuntimeError('Incorrect shape for region {}'.format(name))

                    self._regions[name] = shape_string

            self.load_display_options()

    def normalise(self, progress_callback=None):
        if self._state != State.FILTERED:
            raise RuntimeError('Project does not contain filtered data')

        with self._h5file() as h5file:
            filtered_total = self.get_filtered_total(h5file=h5file)
            mask = filtered_total.mask

            normalised_group = h5file.create_group('/', 'normalised',
                                                   'Normalised element maps')

            n = len(self.elements)
            for index, element in enumerate(self.elements):
                if progress_callback:
                    text = 'Normalising element {} ({} of {})'.format( \
                        element, index+1, n)
                    progress_callback(index*1.0/n, text)

                normalised = self.get_filtered(element, masked=False,
                                               h5file=h5file)
                normalised /= filtered_total.data  # nan / nan -> nan.

                element_group = h5file.create_group(normalised_group, element)
                h5file.create_carray(element_group, 'data', obj=normalised)
                h5file.create_soft_link(element_group, 'mask',
                                        '/filtered/total/mask')
                self._add_array_stats(element_group, normalised, mask=mask)

            self._state = State.NORMALISED

        if progress_callback:
            progress_callback(1.0, 'Finished')

    @property
    def phases(self):
        # Read-only property.
        return self._phases

    @property
    def ratios(self):
        # Read-only property.
        return self._ratios

    @property
    def regions(self):
        # Read-only property.
        return self._regions

    def rename_phase(self, old_name, name):
        if name in self.phases:
            raise RuntimeError('There is already a phase with name {}'.format(name))

        print('before', self._phases)
        old_tuple = self._phases.pop(old_name)
        self._phases[name] = old_tuple
        print('after', self._phases)

        with self._h5file() as h5file:
            h5file.rename_node('/phase', name, old_name)

    def rename_ratio(self, old_name, name):
        if name in self.ratios:
            raise RuntimeError('There is already a ratio with name {}'.format(name))

        old_tuple = self._ratios.pop(old_name)
        self._ratios[name] = old_tuple

        with self._h5file() as h5file:
            h5file.rename_node('/ratio', name, old_name)

    def rename_region(self, old_name, name):
        if name in self.regions:
            raise RuntimeError('There is already a region with name {}'.format(name))

        old_tuple = self._regions.pop(old_name)
        self._regions[name] = old_tuple

        with self._h5file() as h5file:
            h5file.rename_node('/region', name, old_name)

    def save_display_options(self):
        options = self.display_options
        with self._h5file() as h5file:
            if '/display_options' in h5file:
                group_node = h5file.get_node('/display_options')
            else:
                group_node = h5file.create_group('/', 'display_options')

            for name in ['colourmap_name', 'show_ticks_and_labels',
                         'overall_title', 'show_project_filename', 'show_date',
                         'use_scale', 'pixel_size', 'units', 'show_scale_bar',
                         'scale_bar_location', 'use_histogram_bin_count',
                         'histogram_bin_count', 'histogram_bin_width',
                         'histogram_max_bin_count',
                         'show_mean_median_std_lines', 'auto_zoom_region']:
                group_node._v_attrs[name] = getattr(options, '_' + name)

    def set_filename(self, filename):
        if self._state != State.INVALID:
            raise RuntimeError('Project filename already set')

        self._filename = filename
        with self._h5file() as f:
            # Creates project file.
            self._state = State.EMPTY

    @property
    def shape(self):
        # Read-only property.  Could cache it instead.
        if self._state >= State.FILTERED:
            return self.get_filtered_total(masked=False).shape
        elif self._state == State.RAW:
            return self.get_raw_total(masked=False).shape
        else:
            return None

    @property
    def state(self):
        # Read-only property.
        return self._state

    def write_debug(self):
        with self._h5file_ro() as h5file:
            print('##########')
            print(h5file)
            print('##########')



