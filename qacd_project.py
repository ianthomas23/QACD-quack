# attr for min, max, mean, median, etc.
# need to save state too.

from contextlib import contextmanager
from enum import Enum, unique
import numpy as np
import os
import re
import tables
from scipy.ndimage.filters import median_filter


@unique
class State(Enum):
    INVALID = -1   # Filename not set.
    EMPTY = 1      # Filename set.
    RAW = 2        # Added raw data.
    FILTERED = 3   # Filtered data.


class QACDProject:
    def __init__(self):
        self._csv_file_re = re.compile('^([A-Z][a-z]?) K series.csv$')

        self._state = State.INVALID
        self._filename = None
        self._elements = None  # Cacheing this to avoid reading from file.

    @contextmanager
    def _h5file(self):
        if self._state == State.INVALID:
            h5file = tables.open_file(self._filename, mode='w', title='QACD-quack file')
        else:
            h5file = tables.open_file(self._filename, mode='r+')
        yield h5file
        h5file.close()

    @contextmanager
    def _h5file_ro(self):
        h5file = tables.open_file(self._filename, mode='r')
        yield h5file
        h5file.close()

    @property
    def elements(self):
        # Read-only property.
        return self._elements

    def filter(self, median):
        # median is a boolean.
        if self._state != State.RAW:
            raise RuntimeError('Project does not contain raw data')

        with self._h5file() as h5file:
            filtered_group = h5file.create_group('/', 'filtered', 'Filtered element maps')
            filters = tables.Filters(complevel=5, complib='blosc')

            for node in h5file.iter_nodes('/raw'):
                element = node._v_name
                raw = node.read()

                if median:
                    # Median filter applied separately to each raw element map.
                    filtered = median_filter(raw, size=(3, 3), mode='nearest')
                else:
                    filtered = np.asarray(raw, dtype=np.float64)

                node = h5file.create_carray(filtered_group, element, obj=filtered,
                                            filters=filters)
                node.attrs.min = np.nanmin(filtered)
                node.attrs.max = np.nanmax(filtered)
                node.attrs.mean = np.nanmean(filtered)
                node.attrs.median = np.nanmedian(filtered)

        self._state = State.FILTERED

    def get_element_from_csv_filename(self, csv_filename):
        match = self.is_valid_csv_filename(csv_filename)
        if not match:
            raise RuntimeError('Invalid CSV file name: {}'.format(csv_file))
        return match.group(1)

    def get_filtered(self, element, want_stats=False):
        if self._state in [State.INVALID, State.EMPTY, State.RAW]:
            raise RuntimeError('No raw data present')
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

    def is_valid_csv_filename(self, csv_filename):
        return self._csv_file_re.match(csv_filename)

    def load_raw_csv_files(self, directory, csv_filenames):
        if self._state != State.EMPTY:
            raise RuntimeError('Project already contains raw data')

        csv_filenames.sort()

        # Check csv_filenames are correct.
        for csv_filename in csv_filenames:
            if os.path.dirname(csv_filename) != '':
                raise RuntimeError('Unexpected directory in {}'.format(csv_filename))
            if not self.is_valid_csv_filename(csv_filename):
                raise RuntimeError('Invalid CSV file name: {}'.format(csv_filename))

        with self._h5file() as h5file:
            raw_group = h5file.create_group('/', 'raw', 'Raw element maps')
            filters = tables.Filters(complevel=5, complib='blosc')

            # Load files one at a time and save in project file.
            shape = None
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
                node.attrs.min = np.min(raw)
                node.attrs.max = np.max(raw)
                node.attrs.mean = np.mean(raw)
                node.attrs.median = np.median(raw)

            h5file.create_array('/', 'elements', obj=elements, title='Elements')
            self._elements = elements

        self._state = State.RAW

    def set_filename(self, filename):
        if self._state != State.INVALID:
            raise RuntimeError('Project filename already set')

        self._filename = filename
        with self._h5file() as f:
            pass  # Creates project file.
        self._state = State.EMPTY

    @property
    def state(self):
        # Read-only property.
        return self._state
