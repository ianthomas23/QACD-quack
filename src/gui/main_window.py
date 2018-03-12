import numpy as np
import os
from PyQt5 import QtCore, QtWidgets, QtGui
import string

from src.model.elements import element_properties
from src.model.qacd_project import QACDProject
from .matplotlib_widget import MatplotlibWidget, PlotType
from .ui_main_window import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setupUi(self)

        self.actionProjectNew.triggered.connect(self.new_project)
        self.actionProjectOpen.triggered.connect(self.open_project)
        self.actionProjectClose.triggered.connect(self.close_project)

        self.statusbar.messageChanged.connect(self.status_bar_change)

        self.plotTypeComboBox.currentIndexChanged.connect(self.change_plot_type)
        self.rawElementList.itemSelectionChanged.connect( \
            lambda: self.change_list_item('raw'))

        # Set initial width of tabWidget.  Needs improvement.
        self.splitter.setSizes([50, 100])

        self._project = None

        # Current data to display.
        self._array = None
        self._array_stats = None
        self._type = None
        self._element = None

        self.update_title()

    def change_list_item(self, type_):
        if self._project is not None:
            self._type = type_
            self._element = self.rawElementList.currentItem().text().split()[0]
            if self._type == 'raw':
                if self._element == 'Total':
                    self._array, self._array_stats = \
                        self._project.get_raw_total(want_stats=True)
                else:
                    self._array, self._array_stats = \
                        self._project.get_raw(self._element, want_stats=True)
            else:
                raise RuntimeError('Not implemented ' + type_)

        self.update_status_bar()
        self.update_matplotlib_widget()

    def change_plot_type(self):
        self.update_matplotlib_widget()

    def close_project(self):
        if self._project is not None:
            self._project = None
            self._array = None
            self._array_stats = None
            self._type = None
            self._element = None

            self.rawElementList.clear()

            self.update_matplotlib_widget()
            self.update_title()

    def fill_raw_tab(self):
        # Enable tab if not already present.

        type_ = 'raw'
        element_list = self.rawElementList
        want_total = True

        # Delete contents of list.
        element_list.clear()

        # Fill element list in tab.
        for i, element in enumerate(self._project.elements):
            name = element_properties[element][0]
            element_list.addItem(f'{element} - {name}')
        if want_total:
            element_list.addItem('Total')
            element_list.item(i+1).setToolTip(f'Sum of all {type_} element maps')

        # Bring tab to front.
        self.tabWidget.setCurrentIndex(0)

    def new_project(self):
        # Select file to save new project to.
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filename, _ = QtWidgets.QFileDialog.getSaveFileName( \
            self, 'Save new project as...', '',
            'Quack project files (*.quack)', options=options)
        if not filename:
            return

        if os.path.splitext(filename)[1] != '.quack':
            filename = os.path.splitext(filename)[0] + '.quack'
        # Danger of overwriting without prompting here?

        # Select CSV files to import.
        csv_files, _ = QtWidgets.QFileDialog.getOpenFileNames( \
            self, 'Select CSV files containing raw element maps to import',
            os.path.dirname(filename), 'CSV files (*.csv)', options=options)
        if len(csv_files) < 1:
            return

        self.close_project()
        try:
            self._project = QACDProject()
            self._project.set_filename(filename)

            csv_directory = os.path.dirname(csv_files[0])
            csv_files = [os.path.basename(f) for f in csv_files]
            self._project.import_raw_csv_files(csv_directory, csv_files)
            # Progress bar?
        except:
            print('Need to display message box')

        self.fill_raw_tab()
        self.update_status_bar()
        self.update_title()

    def open_project(self):
        # If OK, close old project.

        # Need to wrap project functions (except read-only ones) in try..except
        # block.

        # Delete previous project first????
        self._project = QACDProject()  # Check can create project.
        #print(self.project)
        self._project.set_filename('example.quack')
        self._project.import_raw_csv_files('test_data')  # Need progress bar...
        print(self._project.elements)

        self.fill_raw_tab()
        self.update_title()

    def status_bar_change(self):
        if (self.statusbar.currentMessage() == '' and \
            self._array is not None):
            self.update_status_bar()

    def update_matplotlib_widget(self):
        if self._type is None:
            self.matplotlibWidget.clear()
        else:
            plot_type = PlotType(self.plotTypeComboBox.currentIndex())
            if self._element == 'Total':
                name = 'total'
            else:
                name = element_properties[self._element][0]
            title = f'{string.capwords(self._type)} {name}'
            self.matplotlibWidget.update(plot_type, self._array,
                                         self._array_stats, title)

    def update_status_bar(self):
        def stat_to_string(name, label=None):
            label = label or name
            value = self._array_stats.get(name)
            if value is None:
                return ''
            elif isinstance(value, np.float):
                if int(value) == value:
                    value = int(value)
                else:
                    value = float('{:.5g}'.format(value))
                return ', {}={}'.format(label, value)
            else:
                return ', {}={}'.format(label, value)

        if self._array is not None:
            ny, nx = self._array.shape
            msg = 'pixels={}x{}'.format(nx, ny)
            msg += stat_to_string('valid')
            msg += stat_to_string('invalid')
            msg += stat_to_string('min')
            msg += stat_to_string('max')
            msg += stat_to_string('mean')
            msg += stat_to_string('median')
            msg += stat_to_string('std')
            self.statusbar.showMessage(msg)
        else:
            self.statusbar.clearMessage()

    def update_title(self):
        title = 'QACD quack'
        if self._project is not None:
            title += ' - ' + self._project.filename
        self.setWindowTitle(title)
