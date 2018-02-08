from contextlib import contextmanager
from enum import Enum, unique
import numpy as np
import os
import re
import tables

import utils


@unique
class State(Enum):
    INVALID = -1   # Filename not set.
    EMPTY = 1      # Filename set.
    RAW = 2        # Added raw data.
    FILTERED = 3   # Filtered data.


class QACDProject:
    def __init__(self):
        self._state = State.INVALID
        self._filename = None
        self._elements = None  # Cacheing this to avoid reading from file.

        # Regular expression to match input CSV filenames.
        self._csv_file_re = re.compile('^([A-Z][a-z]?) K series.csv$')

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

    @contextmanager
    def _h5file(self):
        # All writing to h5 file is done in a 'with self._h5file() as f' block.
        # State should also be changed within such a block to ensure it is
        # correctly written to file.
        if self._state == State.INVALID:
            h5file = tables.open_file(self._filename, mode='w', title='QACD-quack file')
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
            filtered_group = h5file.create_group('/', 'filtered', 'Filtered element maps')
            filtered_group._v_attrs.pixel_totals_filter = pixel_totals
            filtered_group._v_attrs.median_filter = median
            filters = tables.Filters(complevel=5, complib='blosc')

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

                node = h5file.create_carray(filtered_group, element, obj=filtered,
                                            filters=filters)
                self._add_array_stats(filtered, node)

                if total is None:
                    total = filtered.copy()
                else:
                    total += filtered

            filtered_total_node = h5file.create_carray(filtered_group, \
                'total', obj=total, filters=filters)
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

        with self._h5file_ro() as h5file:
            node = h5file.get_node('/filtered', element)
            filtered = node.read()
            if want_stats:
                stats = {key:node.attrs[key] for key in node.attrs._f_list('user')}
                return filtered, stats
            else:
                return filtered

    def get_filtered_total(self, want_stats=False):
        if self._state in [State.INVALID, State.EMPTY, State.RAW]:
            raise RuntimeError('No filtered data present')

        with self._h5file_ro() as h5file:
            node = h5file.get_node('/filtered/total')
            filtered_total = node.read()
            if want_stats:
                stats = {key:node.attrs[key] for key in node.attrs._f_list('user')}
                return filtered_total, stats
            else:
                return filtered_total

    def get_raw(self, element, want_stats=False):
        if self._state in [State.INVALID, State.EMPTY]:
            raise RuntimeError('No raw data present')
        if element not in self._elements:
            raise RuntimeError('No such element: {}'.format(element))

        with self._h5file_ro() as h5file:
            node = h5file.get_node('/raw', element)
            raw = node.read()
            if want_stats:
                stats = {key:node.attrs[key] for key in node.attrs._f_list('user')}
                return raw, stats
            else:
                return raw

    def get_raw_total(self, want_stats=False):
        if self._state in [State.INVALID, State.EMPTY]:
            raise RuntimeError('No raw data present')

        with self._h5file_ro() as h5file:
            node = h5file.get_node('/raw/total')
            raw_total = node.read()
            if want_stats:
                stats = {key:node.attrs[key] for key in node.attrs._f_list('user')}
                return raw_total, stats
            else:
                return raw_total

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
            filters = tables.Filters(complevel=5, complib='blosc')

            # Load files one at a time and save in project file.
            shape = None
            total = None
            elements = []
            for index, csv_filename in enumerate(csv_filenames):
                element = self.get_element_from_csv_filename(csv_filename)
                elements.append(element)
                full_filename = os.path.join(directory, csv_filename)
                raw = np.genfromtxt(full_filename, delimiter=',', dtype=np.int32,
                                    filling_values=-1)
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
                                            filters=filters)
                self._add_array_stats(raw, node)

                if total is None:
                    total = raw.astype(np.float64)
                else:
                    total += raw

            raw_total_node = h5file.create_carray(raw_group, 'total', obj=total,
                                                  filters=filters)
            self._add_array_stats(total, raw_total_node)

            h5file.create_array('/', 'elements', obj=elements, title='Elements')
            self._elements = elements

            self._state = State.RAW

    def is_valid_csv_filename(self, csv_filename):
        return self._csv_file_re.match(csv_filename)

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
