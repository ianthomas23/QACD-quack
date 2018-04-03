from contextlib import contextmanager
from enum import IntEnum, unique
import numpy as np
import os
import re
from sklearn.cluster import MiniBatchKMeans
import tables

from .correction_models import correction_models
from .elements import element_properties
from .preset_ratios import preset_ratios
from .utils import median_filter_with_nans, read_csv


@unique
class State(IntEnum):
    INVALID = -1    # Filename not set.
    EMPTY = 1       # Filename set.
    RAW = 2         # Added raw element maps, including total.
    FILTERED = 3    # Filtered element maps, including total.
    NORMALISED = 4  # Normalised element maps.
    H_FACTOR = 5    # Calculation of h factor for each normalised pixel.
    CLUSTERING = 6  # k-means clustering to help identify phases.


class QACDProject:
    def __init__(self):
        self._state = State.INVALID
        self._filename = None

        # Cached data to avoid recalculating/re-reading from file.
        self._elements = None
        self._valid_preset_ratios = None
        self._ratios = {}

        # Regular expression to match input CSV filenames.
        self._csv_file_re = re.compile('^([A-Z][a-z]?) K series.csv$')

        # Compression filters for pytables chunked arrays.
        self._compression_filters = tables.Filters(complevel=5, complib='blosc')

        # numpy array dtypes.
        self._raw_dtype = np.int32
        self._indices_dtype = np.int8

    def _add_array_stats(self, h5node, array, mask=None):
        # Add statistics of the specified array to the specified h5 file node.
        # If a mask is specified, it is applied to the array before calculating
        # the stats.
        if mask is not None:
            array = np.ma.masked_array(array, mask=mask)

        h5node._v_attrs.min = array.min()
        h5node._v_attrs.max = array.max()

        if array.dtype != self._indices_dtype:
            h5node._v_attrs.mean = array.mean()
            h5node._v_attrs.median = np.ma.median(array)
            h5node._v_attrs.std = array.std()

        number_invalid = np.ma.count_masked(array)
        h5node._v_attrs.invalid = number_invalid
        h5node._v_attrs.valid = array.size - number_invalid

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
            mask = h5file.get_node(group_node, 'mask').read()
            array = np.ma.masked_array(array, mask=mask)

        if array.dtype in [self._raw_dtype, self._indices_dtype]:
            np.ma.set_fill_value(array, -1)
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

    def calculate_h_factor(self, progress_callback=None):
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

    def create_ratio_map(self, name, elements=None, correction_model=None):
        # Create and store a ratio map of the same shape as the element maps.
        # If elements is a list of element names of len > 1, the ratio map is
        #     elements[0] / sum(elements)
        # where each item in elements is an element name, e.g. 'Mg'.
        # If elements is a list of a single element, the ration map is
        #     elements[0]
        # If elements is None then look up the name in preset_ratios to obtain
        # the elements.
        # Return the node name.
        # Note: Uses unmasked numpy arrays, using np.nan to denote masked out
        # pixels.
        if self._state <= State.NORMALISED:
            raise RuntimeError('Cannot create ratio map, no h factor present')
        if correction_model is not None and \
           correction_model not in correction_models:
            raise RuntimeError('No such correction model: {}'.format(correction_model))
        if name in self._ratios.keys():
            raise RuntimeError("Ratio name '{}' already used".format(name))

        # Get preset ratio.
        if elements is None:
            raise RuntimeError('Cannot deal with ratios of presets yet')
            if name not in self.get_valid_preset_ratios():
                raise RuntimeError('No such preset ratio: {}'.format(name))
            elements = preset_ratios[name]

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
            # If no correction model, do not need to multiply by h factor.
            numerator = self.get_filtered(elements[0], masked=False)
            denominator = numerator.copy()
            for element in elements[1:]:
                denominator += self.get_filtered(element, masked=False)
        else:
            h_factor = self.get_h_factor(masked=False)

            correction = model[elements[0]]
            if correction[0] != 'poly':
                raise RuntimeError('Unrecognised correction type: {}'.format(correction[0]))
            poly = list(reversed(correction[1]))  # Decreasing power order.
            poly = np.poly1d(poly)
            numerator = poly(self.get_filtered( \
                elements[0], masked=False)*h_factor)

            denominator = numerator.copy()
            for element in elements[1:]:
                correction = model[element]
                if correction[0] != 'poly':
                    raise RuntimeError('Unrecognised correction type: {}'.format(correction[0]))
                poly = list(reversed(correction[1]))  # Decreasing power order.
                poly = np.poly1d(poly)
                denominator += poly(self.get_filtered( \
                    element, masked=False)*h_factor)

        # Avoid zero/zero by masking such pixels beforehand.
        denominator[denominator == 0.0] = np.nan
        ratio = numerator / denominator

        formula = '{}/({})'.format(elements[0], '+'.join(elements))

        mask = np.isnan(ratio)

        with self._h5file() as h5file:
            if '/ratio' in h5file:
                all_ratios = h5file.get_node('/ratio')
            else:
                all_ratios = h5file.create_group('/', 'ratio', 'Ratio maps')

            node_name = 'ratio_{}'.format(all_ratios._v_nchildren)
            ratio_group = h5file.create_group(all_ratios, node_name)
            ratio_data = h5file.create_carray(ratio_group, 'data', obj=ratio)
            ratio_mask = h5file.create_carray(ratio_group, 'mask', obj=mask,
                                              chunkshape=ratio_data.chunkshape)
            self._add_array_stats(ratio_group, ratio, mask=mask)
            ratio_group._v_attrs.name = name
            ratio_group._v_attrs.formula = formula
            ratio_group._v_attrs.correction_model = correction_model

        self._ratios[name] = (formula, node_name)
        return node_name

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
                    filtered = median_filter_with_nans(filtered)

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
        self.calculate_h_factor(progress_callback=local_callback)

    def get_cluster_indices(self, k, masked=True, want_stats=False):
        # Return array indicating which cluster each pixel is in, from 0 to k-1.
        # If masked==True, invalid pixels are masked out otherwise they are -1.
        if self._state != State.CLUSTERING:
            raise RuntimeError('No k-means cluster data present')

        return self._get_array('/cluster/k{}/indices'.format(k), masked,
                               want_stats)

    def get_element_from_csv_filename(self, csv_filename):
        match = self.is_valid_csv_filename(csv_filename)
        if not match:
            raise RuntimeError('Invalid CSV file name: {}'.format(csv_file))
        return match.group(1)

    def get_filtered(self, element, masked=True, want_stats=False, h5file=None):
        # Return filtered element map.  If masked==True, invalid pixels are
        # masked out otherwise they are np.nan.
        if self._state <= State.RAW:
            raise RuntimeError('No filtered data present')
        if element not in self._elements:
            raise RuntimeError('No such element: {}'.format(element))

        return self._get_array('/filtered/' + element, masked, want_stats,
                               h5file=h5file)

    def get_filtered_total(self, masked=True, want_stats=False, h5file=None):
        # Return total of all filtered element maps.  If masked==True, invalid
        # pixels are masked out otherwise they are np.nan.
        if self._state <= State.RAW:
            raise RuntimeError('No filtered data present')

        return self._get_array('/filtered/total', masked, want_stats,
                               h5file=h5file)

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

    def get_ratio_by_name(self, ratio, masked=True, want_stats=False):
        # Return ratio map.  If masked==True, invalid pixels are masked out
        # otherwise they are np.nan.
        if self._state <= State.NORMALISED:
            raise RuntimeError('No normalised data present')
        if ratio not in self._ratios:
            raise RuntimeError('No such ratio: {}'.format(ratio))

        node_name = self._ratios[ratio][1]
        return self._get_array('/ratio/' + node_name, masked, want_stats)

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
                raw = read_csv(full_filename, self._raw_dtype, shape)
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

    def k_means_clustering(self, k_min, k_max, reorder=True):
        # k_min and k_max are min and max number of clusters.
        # If reorder is True, will reorder labels so that they are consistent
        # across different k values rather than being randomly ordered.
        if self._state == State.CLUSTERING:
            raise RuntimeError('k-means clustering already performed')
        if self._state != State.H_FACTOR:
            raise RuntimeError('No h-factor map present')
        if k_max <= k_min:
            raise RuntimeError('k (number of clusters) must be increasing')

        # Obtain array of all filtered element maps.  k-means clustering cannot
        # deal with masked arrays (or np.nan or np.inf) so need to remove
        # masked out pixels beforehand.
        all_elements = None
        for i, element in enumerate(self.elements):
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

                all_elements = np.empty((npixels, len(self.elements)))

            all_elements[:, i] = filtered.compressed()

        with self._h5file() as h5file:
            cluster_group = h5file.create_group('/', 'cluster',
                                                'k-means clustering')
            for k in range(k_min, k_max+1):
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

            self._state = State.CLUSTERING

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
    def ratios(self):
        # Read-only property.
        return self._ratios

    def set_filename(self, filename):
        if self._state != State.INVALID:
            raise RuntimeError('Project filename already set')

        self._filename = filename
        with self._h5file() as f:
            # Creates project file.
            self._state = State.EMPTY

    @property
    def state(self):
        # Read-only property.
        return self._state

    def write_debug(self):
        with self._h5file_ro() as h5file:
            print('##########')
            print(h5file)
            print('##########')



