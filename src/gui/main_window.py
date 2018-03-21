import numpy as np
import os
from PyQt5 import QtCore, QtWidgets, QtGui
import string

from src.model.elements import element_properties
from src.model.qacd_project import QACDProject, State
from .filter_dialog import FilterDialog
from .matplotlib_widget import MatplotlibWidget, PlotType
from .ui_main_window import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setupUi(self)

        self.actionProjectNew.triggered.connect(self.new_project)
        self.actionProjectOpen.triggered.connect(self.open_project)
        self.actionProjectClose.triggered.connect(self.close_project)
        self.actionFilter.triggered.connect(self.filter)

        self.statusbar.messageChanged.connect(self.status_bar_change)

        self.plotTypeComboBox.currentIndexChanged.connect(self.change_plot_type)
        self.rawElementList.itemSelectionChanged.connect(
            lambda: self.change_list_item('raw'))
        self.filteredElementList.itemSelectionChanged.connect(
            lambda: self.change_list_item('filtered'))

        # Set initial width of tabWidget.  Needs improvement.
        self.splitter.setSizes([50, 100])

        self._project = None

        # Current data to display.
        self._array = None
        self._array_stats = None
        self._type = None
        self._element = None

        self._ignore_selection_change = False

        self.tabWidget.setCurrentIndex(0)  # Bring tab to front.
        self.update_menu()
        self.update_title()

    def change_list_item(self, type_):
        if self._ignore_selection_change:
            return

        if self._project is not None:
            self._ignore_selection_change = True
            self._type = type_
            if self._type == 'raw':
                self.filteredElementList.clearSelection()
                self._element = self.rawElementList.currentItem().text().split()[0]
                if self._element == 'Total':
                    self._array, self._array_stats = \
                        self._project.get_raw_total(want_stats=True)
                else:
                    self._array, self._array_stats = \
                        self._project.get_raw(self._element, want_stats=True)
            elif self._type == 'filtered':
                self.rawElementList.clearSelection()
                self._element = self.filteredElementList.currentItem().text().split()[0]
                if self._element == 'Total':
                    self._array, self._array_stats = \
                        self._project.get_filtered_total(want_stats=True)
                else:
                    self._array, self._array_stats = \
                        self._project.get_filtered(self._element, want_stats=True)
            else:
                raise RuntimeError('Not implemented ' + type_)
            self._ignore_selection_change = False

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
            self.filteredElementList.clear()

            self.update_matplotlib_widget()
            self.update_menu()
            self.update_title()

    def fill_list_widget(self, list_widget, type_string, want_total):
        list_widget.clear()

        for i, element in enumerate(self._project.elements):
            name = element_properties[element][0]
            list_widget.addItem('{} - {}'.format(element, name))
        if want_total:
            list_widget.addItem('Total')
            list_widget.item(i+1).setToolTip( \
                'Sum of all {} element maps'.format(type_string))

    def filter(self):
        dialog = FilterDialog(parent=self)
        if dialog.exec_():
            pixel_totals = dialog.pixelTotalsCheckBox.isChecked()
            median_filter = dialog.medianFilterCheckBox.isChecked()
            self._project.filter(pixel_totals, median_filter)

            self.fill_list_widget(self.filteredElementList, 'filtered', True)
            self.tabWidget.setCurrentIndex(1)  # Bring tab to front.

            self.update_menu()

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

        self.fill_list_widget(self.rawElementList, 'raw', True)
        self.tabWidget.setCurrentIndex(0)  # Bring tab to front.

        self.update_menu()
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

        self.fill_list_widget(self.rawElementList, 'raw', True)
        self.tabWidget.setCurrentIndex(0)  # Bring tab to front.

        self.update_menu()
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
            title = '{} {}'.format(string.capwords(self._type), name)
            self.matplotlibWidget.update(plot_type, self._array,
                                         self._array_stats, title)

    def update_menu(self):
        valid_project = self._project is not None
        self.actionProjectClose.setEnabled(valid_project)
        self.actionFilter.setEnabled(valid_project and
                                     self._project.state == State.RAW)

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
