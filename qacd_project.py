from contextlib import contextmanager
from enum import Enum, unique
import numpy as np
import os
import re
import tables

from correction_models import correction_models
from elements import element_properties
from preset_ratios import preset_ratios
import utils


@unique
class State(Enum):
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

        # Cached data to avoid recalculating/re-reading from file.
        self._elements = None
        self._valid_preset_ratios = None
        self._ratios = {}

        # Regular expression to match input CSV filenames.
        self._csv_file_re = re.compile('^([A-Z][a-z]?) K series.csv$')

        # Compression filters for pytables chunked arrays.
        self._compression_filters = tables.Filters(complevel=5, complib='blosc')

    def _add_array_stats(self, array, h5node):
        # Add statistics of the specified array to the specified h5 file node.
        number_invalid = np.isnan(array).sum()

        h5node.attrs.min = np.nanmin(array)
        h5node.attrs.max = np.nanmax(array)
        h5node.attrs.mean = np.nanmean(array)
        h5node.attrs.median = np.nanmedian(array)
        h5node.attrs.std = np.nanstd(array)
        h5node.attrs.invalid = number_invalid
        h5node.attrs.valid = array.size - number_invalid

    def _get_array(self, full_node_name, want_stats=False):
        with self._h5file_ro() as h5file:
            node = h5file.get_node(full_node_name)
            array = node.read()
            if want_stats:
                stats = {key:node.attrs[key] for key
                         in node.attrs._f_list('user')}
                return array, stats
            else:
                return array

    @contextmanager
    def _h5file(self):
        # All writing to h5 file is done in a 'with self._h5file() as f' block.
        # State should also be changed within such a block to ensure it is
        # correctly written to file.
        if self._state == State.INVALID:
            h5file = tables.open_file(self._filename, mode='w',
                                      title='QACD-quack file')
            h5file.root._v_attrs.file_version = 1
        else:
            h5file = tables.open_file(self._filename, mode='r+')
            assert(State[h5file.root._v_attrs.state] == self._state)
        yield h5file
        h5file.root._v_attrs.state = self._state.name
        h5file.close()

    @contextmanager
    def _h5file_ro(self):
        # Read only access to h5 file.
        h5file = tables.open_file(self._filename, mode='r')
        assert(State[h5file.root._v_attrs.state] == self._state)
        yield h5file
        h5file.close()

    def calculate_h_factor(self):
        if self._state != State.NORMALISED:
            raise RuntimeError('Project does not contain normalised data')

        with self._h5file() as h5file:
            Z_mean = None
            A_mean = None
            for element in self.elements:
                normalised = h5file.get_node('/normalised', element).read()
                Z, A = element_properties[element][1:3]

                if Z_mean is None:
                    Z_mean = normalised*Z
                    A_mean = normalised*A
                else:
                    Z_mean += normalised*Z
                    A_mean += normalised*A

            h_factor = 1.2*A_mean / (Z_mean**2)

            node = h5file.create_carray('/', 'h_factor', obj=h_factor,
                title='H factor (Philibert 1963)',
                filters=self._compression_filters)
            self._add_array_stats(h_factor, node)

            self._state = State.H_FACTOR

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
        if self._state in [State.INVALID, State.EMPTY, State.RAW,
                           State.FILTERED, State.NORMALISED]:
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
            numerator = self.get_filtered(elements[0])
            denominator = numerator.copy()
            for element in elements[1:]:
                denominator += self.get_filtered(element)
        else:
            h_factor = self.get_h_factor()

            correction = model[elements[0]]
            if correction[0] != 'poly':
                raise RuntimeError('Unrecognised correction type: {}'.format(correction[0]))
            poly = list(reversed(correction[1]))  # Decreasing power order.
            poly = np.poly1d(poly)
            numerator = poly(self.get_filtered(elements[0])*h_factor)

            denominator = numerator.copy()
            for element in elements[1:]:
                correction = model[element]
                if correction[0] != 'poly':
                    raise RuntimeError('Unrecognised correction type: {}'.format(correction[0]))
                poly = list(reversed(correction[1]))  # Decreasing power order.
                poly = np.poly1d(poly)
                denominator += poly(self.get_filtered(element)*h_factor)

        # Avoid zero/zero by setting such pixels to nan beforehand.
        denominator[denominator == 0.0] = np.nan
        ratio = numerator / denominator

        formula = '{}/({})'.format(elements[0], '+'.join(elements))

        with self._h5file() as h5file:
            if '/ratio' in h5file:
                ratio_group = h5file.get_node('/ratio')
            else:
                ratio_group = h5file.create_group('/', 'ratio', 'Ratio maps')

            node_name = 'ratio_{}'.format(ratio_group._v_nchildren)
            node = h5file.create_carray(ratio_group, node_name, obj=ratio,
                filters=self._compression_filters)
            self._add_array_stats(ratio, node)
            node.attrs.name = name
            node.attrs.formula = formula
            node.attrs.correction_model = correction_model

        self._ratios[name] = (formula, node_name)
        return node_name

    @property
    def elements(self):
        # Read-only property.
        return self._elements

    def filter(self, pixel_totals, median):
        # pixel_totals and median are booleans.
        if self._state != State.RAW:
            raise RuntimeError('Project does not contain raw data')

        if pixel_totals:
            raw_total, stats = self.get_raw_total(want_stats=True)
            raw_total_median = stats['median']
            raw_total_std = stats['std']
            # Mask of pixels to remove.
            mask = np.logical_or(raw_total < raw_total_median - 2*raw_total_std,
                                 raw_total > raw_total_median + raw_total_std)

        with self._h5file() as h5file:
            filtered_group = h5file.create_group('/', 'filtered',
                                                 'Filtered element maps')
            filtered_group._v_attrs.pixel_totals_filter = pixel_totals
            filtered_group._v_attrs.median_filter = median

            total = None
            for element in self.elements:
                raw = h5file.get_node('/raw', element).read()

                # Convert raw array to floats.
                filtered = np.asarray(raw, dtype=np.float64)

                if pixel_totals:
                    # Same pixel mask applied to each element map.
                    filtered[mask] = np.nan

                if median:
                    # Median filter applied separately to each element map.
                    filtered = utils.median_filter_with_nans(filtered)

                node = h5file.create_carray(filtered_group, \
                    element, obj=filtered, filters=self._compression_filters)
                self._add_array_stats(filtered, node)

                if total is None:
                    total = filtered.copy()
                else:
                    total += filtered

            filtered_total_node = h5file.create_carray(filtered_group, \
                'total', obj=total, filters=self._compression_filters)
            self._add_array_stats(total, filtered_total_node)

            self._state = State.FILTERED

    def get_element_from_csv_filename(self, csv_filename):
        match = self.is_valid_csv_filename(csv_filename)
        if not match:
            raise RuntimeError('Invalid CSV file name: {}'.format(csv_file))
        return match.group(1)

    def get_filtered(self, element, want_stats=False):
        if self._state in [State.INVALID, State.EMPTY, State.RAW]:
            raise RuntimeError('No filtered data present')
        if element not in self._elements:
            raise RuntimeError('No such element: {}'.format(element))

        return self._get_array('/filtered/' + element, want_stats)

    def get_filtered_total(self, want_stats=False):
        if self._state in [State.INVALID, State.EMPTY, State.RAW]:
            raise RuntimeError('No filtered data present')

        return self._get_array('/filtered/total', want_stats)

    def get_h_factor(self, want_stats=False):
        if self._state in [State.INVALID, State.EMPTY, State.RAW,
                           State.FILTERED, State.NORMALISED]:
            raise RuntimeError('No h factor present')

        return self._get_array('/h_factor', want_stats)

    def get_normalised(self, element, want_stats=False):
        if self._state in [State.INVALID, State.EMPTY, State.RAW,
                           State.FILTERED]:
            raise RuntimeError('No normalised data present')
        if element not in self._elements:
            raise RuntimeError('No such element: {}'.format(element))

        return self._get_array('/normalised/' + element, want_stats)

    def get_raw(self, element, want_stats=False):
        if self._state in [State.INVALID, State.EMPTY]:
            raise RuntimeError('No raw data present')
        if element not in self._elements:
            raise RuntimeError('No such element: {}'.format(element))

        return self._get_array('/raw/' + element, want_stats)

    def get_raw_total(self, want_stats=False):
        if self._state in [State.INVALID, State.EMPTY]:
            raise RuntimeError('No raw data present')

        return self._get_array('/raw/total', want_stats)

    def get_valid_preset_ratios(self):
        if self._state in [State.INVALID, State.EMPTY]:
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

    def import_raw_csv_files(self, directory, csv_filenames=None):
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
            raw_group = h5file.create_group('/', 'raw', 'Raw element maps')

            # Load files one at a time and save in project file.
            shape = None
            total = None
            elements = []
            for index, csv_filename in enumerate(csv_filenames):
                element = self.get_element_from_csv_filename(csv_filename)
                elements.append(element)
                full_filename = os.path.join(directory, csv_filename)
                raw = np.genfromtxt(full_filename, delimiter=',',
                                    dtype=np.int32, filling_values=-1)
                # If csv file lines contain trailing comma, ignore last column.
                if np.all(raw[:, -1] == -1):
                    raw = raw[:, :-1]

                # Check shape is OK.
                if index == 0:
                    shape = raw.shape
                    if len(shape) != 2:
                        raise RuntimeError('Expected 2D array from CSV file: {}'.format( \
                                           csv_file))
                elif raw.shape != shape:
                    raise RuntimeError('Different sized csv files: {} and {}'.format( \
                                       shape, raw.shape))

                # Add raw array to project file.
                node = h5file.create_carray(raw_group, element, obj=raw,
                                            filters=self._compression_filters)
                self._add_array_stats(raw, node)

                if total is None:
                    total = raw.astype(np.float64)
                else:
                    total += raw

            raw_total_node = h5file.create_carray(raw_group, \
                'total', obj=total, filters=self._compression_filters)
            self._add_array_stats(total, raw_total_node)

            h5file.create_array('/', 'elements', obj=elements, title='Elements')
            self._elements = elements

            self._state = State.RAW

    def is_valid_csv_filename(self, csv_filename):
        return self._csv_file_re.match(csv_filename)

    def normalise(self):
        if self._state != State.FILTERED:
            raise RuntimeError('Project does not contain filtered data')

        with self._h5file() as h5file:
            filtered_total = h5file.get_node('/filtered/total').read()

            normalised_group = h5file.create_group('/', 'normalised',
                                                   'Normalised element maps')

            for element in self.elements:
                normalised = h5file.get_node('/filtered', element).read()
                normalised /= filtered_total

                node = h5file.create_carray(normalised_group, \
                    element, obj=normalised, filters=self._compression_filters)
                self._add_array_stats(normalised, node)

            self._state = State.NORMALISED

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


