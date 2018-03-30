import numpy as np
import os
from PyQt5 import QtCore, QtWidgets, QtGui
import string
import time

from src.model.elements import element_properties
from src.model.qacd_project import QACDProject, State
from .filter_dialog import FilterDialog
from .matplotlib_widget import MatplotlibWidget, PlotType
from .progress_dialog import ProgressDialog
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
        self.rawElementList.itemSelectionChanged.connect(self.change_tab_list_item)
        self.filteredElementList.itemSelectionChanged.connect(self.change_tab_list_item)
        self.normalisedElementList.itemSelectionChanged.connect(self.change_tab_list_item)

        # Set initial width of tabWidget.  Needs improvement.
        self.splitter.setSizes([50, 100])

        # Hide all but the first tab.
        for i in range(self.tabWidget.count()-1, 0, -1):
            self.tabWidget.removeTab(i)

        self._tabs_and_lists = (
            ('raw', self.rawTab, self.rawElementList),
            ('filtered', self.filteredTab, self.filteredElementList),
            ('normalised', self.normalisedTab, self.normalisedElementList),
        )

        self._project = None

        # Current data to display.
        self._array = None
        self._array_stats = None
        self._type = None
        self._element = None

        self._ignore_selection_change = False

        self.update_menu()
        self.update_title()

    def change_plot_type(self):
        self.update_matplotlib_widget()

    def change_tab_list_item(self):
        if self._ignore_selection_change:
            return

        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.BusyCursor)

        if self._project is not None:
            # Determine which list widget and which element selected.
            tab_index = self.tabWidget.currentIndex()
            self._type, _, list_widget = self._tabs_and_lists[tab_index]
            self._element = list_widget.currentItem().text().split()[0]

            # Clear other list widgets.
            self._ignore_selection_change = True
            for index, tuple_ in enumerate(self._tabs_and_lists):
                if index != tab_index:
                    tuple_[2].clearSelection()
            self._ignore_selection_change = False

            # Retrieve array and array stats from project.
            if self._type == 'raw':
                if self._element == 'Total':
                    ret = self._project.get_raw_total(want_stats=True)
                else:
                    ret = self._project.get_raw(self._element, want_stats=True)
            elif self._type == 'filtered':
                if self._element == 'Total':
                    ret = self._project.get_filtered_total(want_stats=True)
                else:
                    ret = self._project.get_filtered(self._element, want_stats=True)
            elif self._type == 'normalised':
                if self._element in ('h', 'h-factor'):
                    ret = self._project.get_h_factor(want_stats=True)
                else:
                    ret = self._project.get_normalised(self._element, want_stats=True)
            else:
                raise RuntimeError('Not implemented ' + type_)

            self._array, self._array_stats = ret

        self.update_status_bar()
        self.update_matplotlib_widget()
        QtWidgets.QApplication.restoreOverrideCursor()

    def close_project(self):
        if self._project is not None:
            self._project = None
            self._array = None
            self._array_stats = None
            self._type = None
            self._element = None

            # Clear list widgets.
            for _, _, list_widget in self._tabs_and_lists:
                list_widget.clear()

            # Hide all but the first tab.
            for i in range(self.tabWidget.count()-1, 0, -1):
                self.tabWidget.removeTab(i)

            self.update_matplotlib_widget()
            self.update_menu()
            self.update_title()

    def fill_list_widget(self, index):
        type_string, tab_widget, list_widget = self._tabs_and_lists[index]
        want_total = list_widget in (self.rawElementList, self.filteredElementList)
        want_h_factor = list_widget == self.normalisedElementList

        list_widget.clear()

        for i, element in enumerate(self._project.elements):
            name = element_properties[element][0]
            list_widget.addItem('{} - {}'.format(element, name))
        if want_total:
            list_widget.addItem('Total')
            list_widget.item(i+1).setToolTip( \
                'Sum of all {} element maps'.format(type_string))
        if want_h_factor:
            list_widget.addItem('h-factor')

        # Show tab.
        if self.tabWidget.widget(index) != tab_widget:
            title = type_string[0].upper() + type_string[1:]
            self.tabWidget.insertTab(index, tab_widget, title)

    def filter(self):
        dialog = FilterDialog(parent=self)
        if dialog.exec_():
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.BusyCursor)

            pixel_totals = dialog.pixelTotalsCheckBox.isChecked()
            median_filter = dialog.medianFilterCheckBox.isChecked()

            def thread_func(project, pixel_totals, median_filter, progress_callback):
                self.short_wait()
                project.filter_normalise_and_h_factor( \
                    pixel_totals, median_filter, progress_callback=progress_callback)

            ProgressDialog.worker_thread( \
                self, 'Filter and Normalise', thread_func,
                args=[self._project, pixel_totals, median_filter])

            self.fill_list_widget(1)
            self.fill_list_widget(2)

            self.tabWidget.setCurrentIndex(1)  # Bring tab to front.

            self.update_menu()
            QtWidgets.QApplication.restoreOverrideCursor()

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

        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.BusyCursor)

        self.close_project()
        try:
            self._project = QACDProject()
            self._project.set_filename(filename)

            csv_directory = os.path.dirname(csv_files[0])
            csv_files = [os.path.basename(f) for f in csv_files]
        except:
            print('Need to display message box')

        def thread_func(project, csv_directory, csv_files, progress_callback):
            self.short_wait()
            project.import_raw_csv_files(csv_directory, csv_files,
                                         progress_callback=progress_callback)

        ProgressDialog.worker_thread( \
            self, 'New project ' + os.path.basename(filename), thread_func,
            args=[self._project, csv_directory, csv_files])

        self.fill_list_widget(0)
        self.tabWidget.setCurrentIndex(0)  # Bring tab to front.

        self.update_menu()
        self.update_status_bar()
        self.update_title()
        QtWidgets.QApplication.restoreOverrideCursor()

    def open_project(self):
        # Need to wrap project functions (except read-only ones) in try..except
        # block.

        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.BusyCursor)

        project = QACDProject()  # Check can create project.
        project.set_filename('example.quack')

        def thread_func(project, directory, progress_callback):
            self.short_wait()
            project.import_raw_csv_files(directory,
                                         progress_callback=progress_callback)

        ProgressDialog.worker_thread(self, 'Opening project', thread_func,
                                     args=[project, 'test_data'])
 #                                    args=[project, '../1309D-41R2'])
        print(project.elements)

        self.close_project()
        self._project = project

        self.fill_list_widget(0)
        self.tabWidget.setCurrentIndex(0)  # Bring tab to front.

        self.update_menu()
        self.update_title()
        QtWidgets.QApplication.restoreOverrideCursor()

    def short_wait(self):
        time.sleep(0.1)

    def status_bar_change(self):
        if (self.statusbar.currentMessage() == '' and \
            self._array is not None):
            self.update_status_bar()

    def update_matplotlib_widget(self):
        if self._type is None:
            self.matplotlibWidget.clear()
        else:
            plot_type = PlotType(self.plotTypeComboBox.currentIndex())
            if self._element in ('h', 'h-factor'):
                title = 'h-factor'
            else:
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
