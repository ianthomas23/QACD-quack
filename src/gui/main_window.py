import numpy as np
import os
from PyQt5 import QtCore, QtWidgets, QtGui
import string
import time

from src.model.elements import element_properties
from src.model.qacd_project import QACDProject, State
from .display_options_dialog import DisplayOptionsDialog
from .filter_dialog import FilterDialog
from .matplotlib_widget import MatplotlibWidget, PlotType
from .new_ratio_dialog import NewRatioDialog
from .progress_dialog import ProgressDialog
from .ui_main_window import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setupUi(self)

        self.actionProjectNew.triggered.connect(self.new_project)
        self.actionProjectOpen.triggered.connect(self.choose_open_project)
        self.actionProjectClose.triggered.connect(self.close_project)
        self.actionFilter.triggered.connect(self.filter)
        self.actionDisplayOptions.triggered.connect(self.display_options)

        self.statusbar.messageChanged.connect(self.status_bar_change)

        self.plotTypeComboBox.currentIndexChanged.connect(self.change_plot_type)
        self.rawElementList.itemSelectionChanged.connect(self.change_tab_list_item)
        self.filteredElementList.itemSelectionChanged.connect(self.change_tab_list_item)
        self.normalisedElementList.itemSelectionChanged.connect(self.change_tab_list_item)
        self.ratioTable.itemSelectionChanged.connect(self.change_tab_list_item)

        self.newRatioButton.clicked.connect(self.new_ratio)
        self.deleteRatioButton.clicked.connect(self.delete_ratio)

        # Set initial width of tabWidget.  Needs improvement.
        #self.splitter.setSizes([50, 100])

        # Hide all but the first tab.
        for i in range(self.tabWidget.count()-1, 0, -1):
            self.tabWidget.removeTab(i)

        self._tabs_and_lists = (
            ('raw', self.rawTab, self.rawElementList),
            ('filtered', self.filteredTab, self.filteredElementList),
            ('normalised', self.normalisedTab, self.normalisedElementList),
            ('ratio', self.ratioTab, self.ratioTable),
        )

        # Correct table widget properties.
        horiz = self.ratioTable.horizontalHeader()
        horiz.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        horiz.setDefaultAlignment(QtCore.Qt.AlignLeft)

        vert = self.ratioTable.verticalHeader()
        vert.setDefaultSectionSize(vert.minimumSectionSize())

        # Member variables.
        self._project = None

        # Current data to display.
        self._array = None
        self._array_stats = None
        self._type = None
        self._element = None  # Should be 'name' really, or 'identifier'

        self._ignore_selection_change = False
        self._display_options_shown = False

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
            if tab_index == 3:
                row = list_widget.currentRow()
                item = list_widget.item(row, 0)
                self._element = item.text()
            else:
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
            elif self._type == 'ratio':
                ret = self._project.get_ratio_by_name(self._element, want_stats=True)
            else:
                raise RuntimeError('Not implemented ' + type_)

            self._array, self._array_stats = ret

        self.update_menu()
        self.update_status_bar()
        self.update_matplotlib_widget()
        QtWidgets.QApplication.restoreOverrideCursor()

    def choose_open_project(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filename, _ = QtWidgets.QFileDialog.getOpenFileName( \
            self, 'Select project file to open', '',
            'Quack project files (*.quack)', options=options)
        if filename:
            self.open_project(filename)

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

    def delete_ratio(self):
        table_widget = self.ratioTable

        row = table_widget.currentRow()
        name = table_widget.item(row, 0).text()
        button = QtWidgets.QMessageBox.question(self, 'Delete ratio map',
            "Are you sure you want to delete ratio map '{}'?".format(name))
        if button == QtWidgets.QMessageBox.Yes:
            table_widget.clearSelection()
            table_widget.removeRow(row)
            self.update_menu()
            self._project.delete_ratio_map(name)

    def display_options(self):
        def finished():
            self._display_options_shown = False
            self.update_menu()

        colormap_name = self.matplotlibWidget.get_colormap_name()
        valid_colormap_names = self.matplotlibWidget.get_valid_colormap_names()

        dialog = DisplayOptionsDialog(colormap_name, valid_colormap_names,
                                      parent=self)
        dialog.finished.connect(finished)
        dialog.show()

        self._display_options_shown = True
        self.update_menu()

    def fill_list_widget(self, index):
        type_string, tab_widget, list_widget = self._tabs_and_lists[index]
        want_total = list_widget in (self.rawElementList, self.filteredElementList)
        want_h_factor = (list_widget == self.normalisedElementList and
                         self._project.state >= State.H_FACTOR)
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

    def fill_table_widget(self, index):
        table_widget = self.ratioTable

        # Disable sorting whilst changing content.
        sorting = table_widget.isSortingEnabled()
        table_widget.setSortingEnabled(False)

        tab_widget = self.ratioTab
        if self.tabWidget.widget(index) != tab_widget:
            self.tabWidget.insertTab(index, tab_widget, 'Ratios')

        table_widget.setRowCount(len(self._project.ratios))

        row = 0
        for name, v in self._project.ratios.items():
            text = (name, v[0], v[1])
            for i in range(3):
                item = QtWidgets.QTableWidgetItem(text[i])
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                table_widget.setItem(row, i, item)
            row += 1
        table_widget.setSortingEnabled(sorting)

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
            self.fill_table_widget(3)
            self.tabWidget.setCurrentIndex(2)  # Bring tab to front.

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
        self.update_matplotlib_widget()
        QtWidgets.QApplication.restoreOverrideCursor()

    def new_ratio(self):
        dialog = NewRatioDialog(self._project, parent=self)
        if dialog.exec_():
            name = dialog.nameEdit.text()
            elements = dialog.ratio_elements
            correction_model = dialog.correctionModelCombo.currentText() or None
            self._project.create_ratio_map(name, elements, correction_model)

            self.fill_table_widget(3)  # Update user interface.

            # Find row matching name and select it.
            table_widget = self.ratioTable
            nrows = table_widget.rowCount()
            names = [table_widget.item(row, 0).text() for row in range(nrows)]
            row = names.index(name)
            table_widget.selectRow(row)

            self.update_menu()

    def open_project(self, filename):
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.BusyCursor)

        project = None
        try:
            project = QACDProject()
            project.load_file(filename)
        except:
            print('Need to display message box')

        # Opened project is OK, so can close previous project.
        self.close_project()
        self._project = project

        if self._project.state >= State.RAW:
            self.fill_list_widget(0)
            self.tabWidget.setCurrentIndex(0)  # Bring tab to front.

        if self._project.state >= State.FILTERED:
            self.fill_list_widget(1)
            self.tabWidget.setCurrentIndex(1)  # Bring tab to front.

        if self._project.state >= State.NORMALISED:
            self.fill_list_widget(2)
            self.tabWidget.setCurrentIndex(2)  # Bring tab to front.

        if self._project.state >= State.H_FACTOR:
            self.fill_table_widget(3)
            self.tabWidget.setCurrentIndex(3)  # Bring tab to front.

        self.update_menu()
        self.update_status_bar()
        self.update_title()
        self.update_matplotlib_widget()
        QtWidgets.QApplication.restoreOverrideCursor()

    def set_colormap(self, colormap):
        if self.matplotlibWidget is not None:
            self.matplotlibWidget.set_colormap(colormap)

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
            elif self._type == 'ratio':
                title = self._element + ' ratio'
            else:
                if self._element == 'Total':
                    name = 'total'
                else:
                    name = element_properties[self._element][0]
                title = '{} {} element'.format(string.capwords(self._type), name)
            self.matplotlibWidget.update(plot_type, self._array,
                                         self._array_stats, title)

    def update_menu(self):
        valid_project = self._project is not None
        self.actionProjectClose.setEnabled(valid_project)
        self.actionFilter.setEnabled(valid_project and
                                     self._project.state == State.RAW)
        self.actionDisplayOptions.setEnabled(not self._display_options_shown)
        self.deleteRatioButton.setEnabled(self.ratioTable.currentItem() is not None)

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
