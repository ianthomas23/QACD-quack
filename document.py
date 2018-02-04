import numpy as np
import os
import re
import tables


class Document:
    def __init__(self):
        self._csv_file_re = re.compile('^([A-Z][a-z]?) K series.csv$')
        self._elements = []

    @property
    def elements(self):
        # Read-only property.
        return self._elements

    def get_element_from_csv_file(self, csv_file):
        match = self.is_valid_csv_file(csv_file)
        if not match:
            raise RuntimeError('Invalid CSV file name: {}'.format(csv_file))
        return match.group(1)

    def is_valid_csv_file(self, csv_file):
        return self._csv_file_re.match(csv_file)

    def load_csv_files(self, directory, csv_files):
        csv_files.sort()

        # Check csv_files are correct.
        for csv_file in csv_files:
            if os.path.dirname(csv_file) != '':
                raise RuntimeError('Unexpected directory in {}'.format(csv_file))
            if not self.is_valid_csv_file(csv_file):
                raise RuntimeError('Invalid CSV file name: {}'.format(csv_file))



        h5file = tables.open_file('out.h5', mode='w', title='QACD-quack file')
        root_group = h5file.root

        raw_group = h5file.create_group(root_group, 'raw', 'Raw element data')
        filtered_group = h5file.create_group(root_group, 'filtered', 'Filtered element data')

        filters = tables.Filters(complevel=5, complib='blosc')



        # Load files one at a time.
        for csv_file in csv_files:
            element = self.get_element_from_csv_file(csv_file)
            filename = os.path.join(directory, csv_file)
            raw = np.genfromtxt(filename, delimiter=',', dtype=np.int32,
                                filling_values=-1)
            # If csv file lines contain trailing comma, ignore last column.
            if np.all(raw[:, -1] == -1):
                raw = raw[:, :-1]

            print(element, raw.shape, np.mean(raw), np.min(raw), np.max(raw))

            # Not setting using chunks yet.
            #h5file.create_array(raw_group, element, raw)
            h5file.create_carray(raw_group, element, obj=raw, filters=filters)


        print(h5file)
        h5file.close()
