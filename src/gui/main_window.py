import numpy as np
import os
from PyQt5 import QtCore, QtWidgets, QtGui
import string
import time

from src.model.elements import element_properties
from src.model.qacd_project import QACDProject, State
from .about_dialog import AboutDialog
from .clustering_dialog import ClusteringDialog
from .enums import ArrayType, ModeType, PlotType
from .display_options_dialog import DisplayOptionsDialog
from .filter_dialog import FilterDialog
from .matplotlib_widget import ArrayType, PlotType
from .new_phase_cluster_dialog import NewPhaseClusterDialog
from .new_phase_filtered_dialog import NewPhaseFilteredDialog
from .new_ratio_dialog import NewRatioDialog
from .new_region_dialog import NewRegionDialog
from .progress_dialog import ProgressDialog
from .ui_main_window import Ui_MainWindow
from .zoom_history import ZoomHistory


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    # Inner class for current data displayed.
    class Current:
        def __init__(self):
            self.clear()

        def clear(self):
            # Selected array read from project.
            self.selected_array = None
            self.selected_array_stats = None

            # Displayed array is selected array masked by phase and/or region.
            # May be same objects as selected above.
            self.displayed_array = None
            self.displayed_array_stats = None

            self.array_type = ArrayType.INVALID
            self.name = None    # e.g. element name, or 'total', etc.
            self.phase = None   # None or phase boolean array.
            self.region = None  # None or region boolean array.
            self.colourmap_limits = None  # None or tuple of (lower, upper).
            self.mask = None    # None or combined phase & region boolean array.

        def create_mask(self):
            # Mask excludes colourmap limits as these have a different effect
            # on each element map.
            have_phase = self.phase is not None
            have_region = self.region is not None

            if have_phase and have_region:
                self.mask = np.logical_or(self.phase, self.region)
            elif have_phase:
                self.mask = self.phase
            elif have_region:
                self.mask = self.region
            else:
                self.mask = None

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setupUi(self)

        self.matplotlibWidget.initialise(owning_window=self,
                                         display_options=None,
                                         status_callback=self.status_callback)

        self.statusbar.messageChanged.connect(self.status_bar_change)

        # Menu items.
        self.actionProjectNew.triggered.connect(self.new_project)
        self.actionProjectOpen.triggered.connect(self.choose_open_project)
        self.actionProjectClose.triggered.connect(self.close_project)
        self.actionFilter.triggered.connect(self.filter)
        self.actionClustering.triggered.connect(self.clustering)
        self.actionNewRegion.triggered.connect(self.new_region)
        self.actionExportImage.triggered.connect(self.export_image)
        self.actionDisplayOptions.triggered.connect(self.display_options)
        self.actionAbout.triggered.connect(self.about)

        # Tab widget controls.
        self.newRatioButton.clicked.connect(self.new_ratio)
        self.deleteRatioButton.clicked.connect(self.delete_ratio)
        self.newPhaseClusterButton.clicked.connect(self.new_phase_cluster)
        self.newPhaseFilteredButton.clicked.connect(self.new_phase_filtered)
        self.deletePhaseButton.clicked.connect(self.delete_phase)
        self.deleteRegionButton.clicked.connect(self.delete_region)

        # Matplotlib toolbar controls.
        self.plotTypeComboBox.currentIndexChanged.connect(self.change_plot_type)
        self.phaseComboBox.currentIndexChanged.connect(self.change_phase)
        self.regionComboBox.currentIndexChanged.connect(self.change_region)
        self.undoButton.clicked.connect(self.zoom_undo)
        self.redoButton.clicked.connect(self.zoom_redo)
        self.undoColourmapButton.clicked.connect(self.zoom_colourmap_undo)
        self.redoColourmapButton.clicked.connect(self.zoom_colourmap_redo)

        # Hide all but the first tab.
        for i in range(self.tabWidget.count()-1, 0, -1):
            self.tabWidget.removeTab(i)

        self._tabs_and_tables = (  # Final column is editable name boolean.
            (ArrayType.RAW,        self.rawTab,        self.rawTable,        'Raw',        False),
            (ArrayType.FILTERED,   self.filteredTab,   self.filteredTable,   'Filtered',   False),
            (ArrayType.NORMALISED, self.normalisedTab, self.normalisedTable, 'Normalised', False),
            (ArrayType.RATIO,      self.ratioTab,      self.ratioTable,      'Ratios',     True),
            (ArrayType.CLUSTER,    self.clusterTab,    self.clusterTable,    'Clusters',   False),
            (ArrayType.PHASE,      self.phaseTab,      self.phaseTable,      'Phases',     True),
            (ArrayType.REGION,     self.regionTab,     self.regionTable,     'Regions',    True),
        )

        # Correct table widget properties and connect signals and slots.
        for (_, _, table, _, editable_name) in self._tabs_and_tables:
            horiz = table.horizontalHeader()
            horiz.setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
            horiz.setDefaultAlignment(QtCore.Qt.AlignLeft)

            vert = table.verticalHeader()
            vert.setDefaultSectionSize(vert.minimumSectionSize())

            table.itemSelectionChanged.connect(self.change_table_item)
            if editable_name:
                table.itemChanged.connect(self.change_name)

        # Read-only checkboxes.
        for checkbox in (self.pixelTotalsCheckBox, self.medianFilterCheckBox):
            checkbox.setFocusPolicy(QtCore.Qt.NoFocus)
            checkbox.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)

        # Member variables.
        self._project = None

        self._current = self.Current()  # Current data displayed.

        self._ignore_change_name = False
        self._ignore_change_selection = False
        self._display_options_shown = False   # Modeless dialog.
        self._new_region_shown = False        # Modeless dialog.

        self._zoom_history = ZoomHistory()
        self._zoom_colourmap_history = ZoomHistory()

        self._status_callback_data = None

        self.update_controls()
        self.update_title()

    def about(self):
        dialog = AboutDialog(parent=self)
        dialog.exec_()

    def change_name(self, item):
        if self._ignore_change_name or item is None:
            return

        name = item.text()
        old_name = item.data(QtCore.Qt.UserRole)
        if name == old_name:
            # No change, do nothing.
            return

        table_widget = item.tableWidget()
        if table_widget == self.ratioTable:
            all_items = self._project.ratios
        elif table_widget == self.phaseTable:
            all_items = self._project.phases
        elif table_widget == self.regionTable:
            all_items = self._project.regions

        if name in all_items:
            QtWidgets.QMessageBox.warning(self, 'Warning',
                "Name '{}' is already in use, reverting change.".format(name))
            self.ignore_change_name = True
            item.setText(old_name)
            self.ignore_change_name = False
        else:
            self._current.name = name
            item.setData(QtCore.Qt.UserRole, name)
            if table_widget == self.ratioTable:
                self._project.rename_ratio(old_name, name)
            elif table_widget == self.phaseTable:
                self._project.rename_phase(old_name, name)
                self.update_phase_combo_box()
            elif table_widget == self.regionTable:
                self._project.rename_region(old_name, name)
                self.update_region_combo_box()

            self.update_matplotlib_widget()

    def change_phase(self):
        text = self.phaseComboBox.currentText()
        if text == '':
            self._current.phase = None
        else:
            self._current.phase = ~self._project.get_phase(text, masked=False)
        self._current.create_mask()

        if self._project is not None:
            self.update_matplotlib_widget()
            self.update_status_bar()

    def change_plot_type(self):
        self.update_matplotlib_widget()
        self.update_controls()

    def change_region(self):
        text = self.regionComboBox.currentText()
        if text == '':
            self._current.region = None
        else:
            self._current.region = ~self._project.get_region(text, masked=False)
        self._current.create_mask()

        if self._project is not None:
            self.update_matplotlib_widget()
            self.update_status_bar()

    def change_table_item(self):
        if self._ignore_change_selection:
            return

        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.BusyCursor)

        if self._project is not None:
            current = self._current

            # Determine which table widget and which element selected.
            tab_index = self.tabWidget.currentIndex()
            current.array_type, _, table_widget, _, _ = self._tabs_and_tables[tab_index]
            row = table_widget.currentRow()
            item = table_widget.item(row, 0)
            if item is not None:
                current.name = item.text()
            else:
                current.name = None

            # Clear other table widgets.
            self._ignore_change_selection = True
            for index, (_, _, widget, _, _) in enumerate(self._tabs_and_tables):
                if index != tab_index:
                    widget.clearSelection()
                    widget.setCurrentItem(None)
            self._ignore_change_selection = False

            # Retrieve array and array stats from project.
            if current.name is None:
                current.array_type = ArrayType.INVALID
                ret = (None, None)
            elif current.array_type == ArrayType.RAW:
                if current.name == 'Total':
                    ret = self._project.get_raw_total(want_stats=True)
                else:
                    ret = self._project.get_raw(current.name, want_stats=True)
            elif current.array_type == ArrayType.FILTERED:
                if current.name == 'Total':
                    ret = self._project.get_filtered_total(want_stats=True)
                else:
                    ret = self._project.get_filtered(current.name, want_stats=True)
            elif current.array_type == ArrayType.NORMALISED:
                if current.name in ('h', 'h-factor'):
                    ret = self._project.get_h_factor(want_stats=True)
                else:
                    ret = self._project.get_normalised(current.name, want_stats=True)
            elif current.array_type == ArrayType.RATIO:
                ret = self._project.get_ratio(current.name, want_stats=True)
            elif current.array_type == ArrayType.CLUSTER:
                current.name = int(current.name)
                ret = self._project.get_cluster_indices(current.name, want_stats=True)
            elif current.array_type == ArrayType.PHASE:
                ret = self._project.get_phase(current.name, want_stats=True)
            elif current.array_type == ArrayType.REGION:
                ret = self._project.get_region(current.name, want_stats=True)
            else:
                raise RuntimeError('Not implemented ' + type_)

            current.selected_array, current.selected_array_stats = ret

        self.update_controls()
        self.update_matplotlib_widget()
        self.update_status_bar()
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
            self._current.clear()

            # Clear table widgets.
            for i, (_, _, widget, _, _) in enumerate(self._tabs_and_tables):
                widget.setRowCount(0)

            # Hide all but the first tab.
            for i in range(self.tabWidget.count()-1, 0, -1):
                self.tabWidget.removeTab(i)

            self.matplotlibWidget.set_display_options(None)

            self.update_matplotlib_widget()
            self.matplotlibWidget.clear_all()
            self.update_controls()
            self.update_phase_combo_box()
            self.update_region_combo_box()
            self.update_status_bar()
            self.update_title()

    def clustering(self):
        dialog = ClusteringDialog(self._project, parent=self)
        if dialog.exec_():
            if self._project.has_cluster():
                button = QtWidgets.QMessageBox.question(self,
                    'k-means cluster maps already exist',
                    'Proceeding will delete the previous k-means cluster maps.<br>Do you want to continue?')
                if button == QtWidgets.QMessageBox.Yes:
                    self._project.delete_all_clusters()
                    self.fill_table_widget(4)
                else:
                    return

            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.BusyCursor)

            k_min, k_max, want_all_elements = dialog.get_values()

            def thread_func(project, k_min, k_max, progress_callback):
                self.short_wait()
                project.k_means_clustering(k_min, k_max, want_all_elements,
                    progress_callback=progress_callback)

            ProgressDialog.worker_thread( \
                self, 'k-means Clustering', thread_func,
                args=[self._project, k_min, k_max])

            self.fill_table_widget(4)
            self.tabWidget.setCurrentIndex(4)  # Bring tab to front.

            self.update_controls()
            QtWidgets.QApplication.restoreOverrideCursor()

    def delete_phase(self):
        table_widget = self.phaseTable

        row = table_widget.currentRow()
        name = table_widget.item(row, 0).text()
        button = QtWidgets.QMessageBox.question(self, 'Delete phase map',
            "Are you sure you want to delete phase map '{}'?".format(name))
        if button == QtWidgets.QMessageBox.Yes:
            table_widget.clearSelection()
            table_widget.setCurrentItem(None)
            table_widget.removeRow(row)

            self._project.delete_phase_map(name)

            self.update_phase_combo_box()
            self.update_controls()
            self._current.clear()
            self.update_matplotlib_widget()

    def delete_ratio(self):
        table_widget = self.ratioTable

        row = table_widget.currentRow()
        name = table_widget.item(row, 0).text()
        button = QtWidgets.QMessageBox.question(self, 'Delete ratio map',
            "Are you sure you want to delete ratio map '{}'?".format(name))
        if button == QtWidgets.QMessageBox.Yes:
            table_widget.clearSelection()
            table_widget.setCurrentItem(None)
            table_widget.removeRow(row)

            self._project.delete_ratio_map(name)

            self.update_controls()
            self._current.clear()
            self.update_matplotlib_widget()

    def delete_region(self):
        table_widget = self.regionTable

        row = table_widget.currentRow()
        name = table_widget.item(row, 0).text()
        button = QtWidgets.QMessageBox.question(self, 'Delete region',
            "Are you sure you want to delete region '{}'?".format(name))
        if button == QtWidgets.QMessageBox.Yes:
            table_widget.clearSelection()
            table_widget.setCurrentItem(None)
            table_widget.removeRow(row)

            self._project.delete_region(name)

            self.update_region_combo_box()
            self.update_controls()
            self._current.clear()
            self.update_matplotlib_widget()

    def display_options(self):
        def finished():
            self._display_options_shown = False
            self.update_controls()

        dialog = DisplayOptionsDialog(self._project.display_options,
                                      parent=self)
        dialog.finished.connect(finished)
        dialog.show()

        self._display_options_shown = True
        self.update_controls()

    def export_image(self):
        file_types = ['Joint Photographic ExpertsGroup (*.jpg)',
                      'Portable Document Format (*.pdf)',
                      'Portable Network Graphics (*.png)',
                      'Scalable Vector Graphics (*.svg)']

        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filename, file_type = QtWidgets.QFileDialog.getSaveFileName( \
            self, 'Select filename to export to', '',
            ';;'.join(file_types),  # Filter.
            file_types[2],          # Initial selected filter.
            options=options)
        if filename:
            correct_extension = file_type[-5:-1]
            file_extension = os.path.splitext(filename)[1]
            if not file_extension:
                filename = filename + correct_extension
            elif file_extension != correct_extension:
                QtWidgets.QMessageBox.critical(self, 'Error',
                    'Incorrect file extension {}\nShould be {} or leave it empty.'.format(file_extension, correct_extension))
                return

            self.matplotlibWidget.export_to_file(filename)

    def fill_table_widget(self, index):
        array_type, tab_widget, table_widget, tab_title, editable_name = \
            self._tabs_and_tables[index]

        # Disable sorting whilst changing content.
        sorting = table_widget.isSortingEnabled()
        table_widget.setSortingEnabled(False)

        if self.tabWidget.widget(index) != tab_widget:
            self.tabWidget.insertTab(index, tab_widget, tab_title)

        rows = []
        if array_type in (ArrayType.RAW, ArrayType.FILTERED, ArrayType.NORMALISED):
            for i, element in enumerate(self._project.elements):
                name = element_properties[element][0]
                rows.append((element, name))
            if array_type in (ArrayType.RAW, ArrayType.FILTERED):
                rows.append(('Total', ''))
            if array_type == ArrayType.NORMALISED and self._project.state >= State.H_FACTOR:
                rows.append(('h-factor', ''))
        elif array_type == ArrayType.RATIO:
            for name, tuple_ in self._project.ratios.items():
                rows.append((name, tuple_[0], tuple_[1]))
        elif array_type == ArrayType.CLUSTER:
            cluster_k = self._project.get_cluster_k()
            if cluster_k is not None:
                k_min, k_max = cluster_k
                for k in range(k_min, k_max+1):
                    rows.append((str(k),))
        elif array_type == ArrayType.PHASE:
            phases = self._project.phases
            for name in sorted(phases.keys()):
                tuple_ = phases[name]
                source = tuple_[0]
                if source == 'thresholding':
                    strings = ['{} \u2264 {} \u2264 {}'.format(x[1], x[0], x[2]) for x in tuple_[1]]
                    details = ', '.join(strings)
                else:
                    details = 'k={}, original values={}'.format( \
                        tuple_[1], ', '.join(map(str, tuple_[2])))
                rows.append((name, source, details))
        elif array_type == ArrayType.REGION:
            regions = self._project.regions
            for name in sorted(regions.keys()):
                rows.append((name, regions[name]))

        self._ignore_change_name = True
        nrows = len(rows)
        table_widget.setRowCount(nrows)
        for i, row in enumerate(rows):
            for j, text in enumerate(row):
                item = QtWidgets.QTableWidgetItem(text)
                if j == 0 and editable_name:
                    # Store hidden data for when user edits first column.
                    item.setData(QtCore.Qt.UserRole, text)
                else:
                    # Non-editable cell.
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                table_widget.setItem(i, j, item)
        self._ignore_change_name = False
        table_widget.setSortingEnabled(sorting)

        # Reset column widths
        for column in range(table_widget.columnCount()):
            table_widget.resizeColumnToContents(column)

        if index == 1:
            filter_options = self._project.get_filter_options()
            self.pixelTotalsCheckBox.setChecked(filter_options[0])
            self.medianFilterCheckBox.setChecked(filter_options[1])
        elif index == 4:
            cluster_elements = self._project.get_cluster_elements()
            self.includedElementsLabel.setText( \
                'Included elements: {}'.format(cluster_elements))

    def filter(self):
        dialog = FilterDialog(parent=self)
        if dialog.exec_():
            pixel_totals = dialog.pixelTotalsCheckBox.isChecked()
            median_filter = dialog.medianFilterCheckBox.isChecked()

            def thread_func(project, pixel_totals, median_filter, progress_callback):
                self.short_wait()
                project.filter_normalise_and_h_factor( \
                    pixel_totals, median_filter, progress_callback=progress_callback)

            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.BusyCursor)

            ProgressDialog.worker_thread( \
                self, 'Filter and Normalise', thread_func,
                args=[self._project, pixel_totals, median_filter])

            for index in range(1, 7):
                self.fill_table_widget(index)
            self.tabWidget.setCurrentIndex(2)  # Bring tab to front.

            self.update_controls()
            QtWidgets.QApplication.restoreOverrideCursor()

    def get_status_string(self, array, stats):
        def stat_to_string(name, label=None):
            label = label or name
            value = stats.get(name)
            if value is None:
                ret = ''
            elif isinstance(value, np.float):
                if int(value) == value:
                    value = int(value)
                else:
                    value = float('{:.5g}'.format(value))
                ret = ', {}={}'.format(label, value)
            else:
                ret = ', {}={}'.format(label, value)
            if name in ('valid', 'invalid'):
                ret += ' ({}%)'.format(int(round(100*value/array.size)))
            return ret

        if array is not None:
            ny, nx = array.shape
            msg = 'pixels={}x{}'.format(nx, ny)
            msg += stat_to_string('valid')
            msg += stat_to_string('invalid')
            msg += stat_to_string('min')
            msg += stat_to_string('max')
            msg += stat_to_string('mean')
            msg += stat_to_string('median')
            msg += stat_to_string('std')
            return msg
        else:
            return None

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

            def thread_func(project, csv_directory, csv_files, progress_callback):
                self.short_wait()
                project.import_raw_csv_files(csv_directory, csv_files,
                                             progress_callback=progress_callback)

            ProgressDialog.worker_thread( \
                self, 'New project ' + os.path.basename(filename), thread_func,
                args=[self._project, csv_directory, csv_files])

            self.matplotlibWidget.set_display_options( \
                self._project.display_options)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Error', str(e))

        self.fill_table_widget(0)
        self.tabWidget.setCurrentIndex(0)  # Bring tab to front.

        self.update_controls()
        self.update_matplotlib_widget()
        self.update_status_bar()
        self.update_title()
        QtWidgets.QApplication.restoreOverrideCursor()

    def new_phase_cluster(self):
        # Create new phase maps from selected cluster map.
        cluster_map = self._current.selected_array
        stats = self._current.selected_array_stats
        dialog = NewPhaseClusterDialog(self._project, cluster_map, stats,
                                       parent=self)
        if dialog.exec_():
            self.fill_table_widget(5)

            # Bring phase tab to front.
            self.tabWidget.setCurrentIndex(5)  # Bring tab to front.

            self.update_phase_combo_box()
            self.update_controls()

    def new_phase_filtered(self):
        # Create new phase map from filtered element maps.
        dialog = NewPhaseFilteredDialog(self._project, parent=self)
        if dialog.exec_():
            name = dialog.get_name()

            self.fill_table_widget(5)

            # Find row matching name and select it.
            table_widget = self.phaseTable
            match = table_widget.findItems(name, QtCore.Qt.MatchExactly)
            row = match[0].row()
            table_widget.clearSelection()
            table_widget.selectRow(row)

            self.update_phase_combo_box()
            self.update_controls()

    def new_ratio(self):
        dialog = NewRatioDialog(self._project, parent=self)
        if dialog.exec_():
            name = dialog.get_name()

            self.fill_table_widget(3)  # Update user interface.

            # Find row matching name and select it.
            table_widget = self.ratioTable
            match = table_widget.findItems(name, QtCore.Qt.MatchExactly)
            row = match[0].row()
            table_widget.clearSelection()
            table_widget.selectRow(row)

            self.update_controls()

    def new_region(self):
        def finished():
            self._new_region_shown = False
            self.fill_table_widget(6)

            if self.tabWidget.currentWidget() == self.regionTab:
                # Find row matching name and select it.
                table_widget = self.regionTable
                name = dialog.get_name()
                match = table_widget.findItems(name, QtCore.Qt.MatchExactly)
                if match is not None and len(match) > 0:
                    row = match[0].row()
                    table_widget.clearSelection()
                    table_widget.selectRow(row)

            self.update_region_combo_box()
            self.update_controls()

        dialog = NewRegionDialog(self._project, parent=self)
        dialog.finished.connect(finished)
        dialog.show()

        self._new_region_shown = True
        self.update_controls()

    def open_project(self, filename):
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.BusyCursor)

        project = None
        try:
            project = QACDProject()
            project.load_file(filename)

            # Opened project is OK, so can close previous project.
            self.close_project()
            self._project = project

            if self._project.state >= State.RAW:
                self.fill_table_widget(0)  # Raw.
                self.tabWidget.setCurrentIndex(0)  # Bring tab to front.

            if self._project.state >= State.FILTERED:
                self.fill_table_widget(1)  # Filtered.
                self.tabWidget.setCurrentIndex(1)  # Bring tab to front.

            if self._project.state >= State.NORMALISED:
                self.fill_table_widget(2)  # Normalised (and h-factor if present).
                self.tabWidget.setCurrentIndex(2)  # Bring tab to front.

            if self._project.state >= State.H_FACTOR:
                self.fill_table_widget(3)  # Ratios.
                self.fill_table_widget(4)  # Clustering.
                self.fill_table_widget(5)  # Phases.
                self.fill_table_widget(6)  # Regions.

            self.matplotlibWidget.set_display_options(project.display_options)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Error', str(e))

        self.update_controls()
        self.update_matplotlib_widget()
        self.update_phase_combo_box()
        self.update_region_combo_box()
        self.update_status_bar()
        self.update_title()
        QtWidgets.QApplication.restoreOverrideCursor()

    def short_wait(self):
        time.sleep(0.1)

    def status_bar_change(self):
        if (self.statusbar.currentMessage() == '' and \
            self._current.selected_array is not None):
            self.update_status_bar()

    def status_callback(self, matplotlib_widget, data):
        if data != self._status_callback_data:
            self._status_callback_data = data
            self.update_status_bar()

    def update_controls(self):
        valid_project = self._project is not None
        showing_phase_or_region = self._current.array_type in \
            (ArrayType.PHASE, ArrayType.REGION)

        # Menu items.
        self.actionProjectClose.setEnabled(valid_project)
        self.actionFilter.setEnabled(valid_project and
                                     self._project.state == State.RAW)
        self.actionClustering.setEnabled(valid_project and
                                         self._project.state == State.H_FACTOR)
        self.actionDisplayOptions.setEnabled(valid_project and
                                             not self._display_options_shown)
        # actionExportImage is also updated in update_matplotlib_widget.
        self.actionExportImage.setEnabled(self.matplotlibWidget.has_content())
        self.actionNewRegion.setEnabled(valid_project and
                                        not self._new_region_shown)

        # Tab widget controls.
        self.deleteRatioButton.setEnabled(self.ratioTable.currentItem() is not None)
        self.deletePhaseButton.setEnabled(self.phaseTable.currentItem() is not None)
        self.deleteRegionButton.setEnabled(self.regionTable.currentItem() is not None)
        self.newPhaseClusterButton.setEnabled(self.clusterTable.currentItem() is not None)

        # Matplotlib toolbar controls.
        self.plotTypeComboBox.setEnabled(not showing_phase_or_region)
        self.plotTypeLabel.setEnabled(not showing_phase_or_region)
        self.phaseComboBox.setEnabled(not showing_phase_or_region)
        self.phaseLabel.setEnabled(not showing_phase_or_region)
        self.regionComboBox.setEnabled(not showing_phase_or_region)
        self.regionLabel.setEnabled(not showing_phase_or_region)
        self.undoButton.setEnabled(self._zoom_history.has_undo() and
                                   self.matplotlibWidget.has_map_axes())
        self.redoButton.setEnabled(self._zoom_history.has_redo() and
                                   self.matplotlibWidget.has_map_axes())
        self.undoColourmapButton.setEnabled(self._zoom_colourmap_history.has_undo())
        self.redoColourmapButton.setEnabled(self._zoom_colourmap_history.has_redo())

    def update_matplotlib_widget(self):
        current = self._current

        if current.array_type is ArrayType.INVALID:
            self.matplotlibWidget.clear()
            changed = True
        else:
            plot_type = PlotType(self.plotTypeComboBox.currentIndex())
            if current.name in ('h', 'h-factor'):
                title = 'h-factor'
            elif current.array_type == ArrayType.RATIO:
                title = current.name + ' ratio'
            elif current.array_type == ArrayType.CLUSTER:
                title = 'k={} cluster'.format(current.name)
            elif current.array_type == ArrayType.PHASE:
                title = current.name + ' phase'
                plot_type = PlotType.MAP  # Don't want histogram.
            elif current.array_type == ArrayType.REGION:
                title = current.name + ' region'
                plot_type = PlotType.MAP  # Don't want histogram.
            else:
                if current.name == 'Total':
                    name = 'total'
                else:
                    name = element_properties[current.name][0]
                type_string = string.capwords(current.array_type.name.lower())
                title = '{} {} element'.format(type_string, name)

            changed = (self.matplotlibWidget._name != current.name or
                       self.matplotlibWidget._array_type != current.array_type)
            if changed:
                current.colourmap_limits = None

            if (current.array_type in (ArrayType.PHASE, ArrayType.REGION) or
                (current.mask is None and current.colourmap_limits is None)):
                current.displayed_array = current.selected_array
                current.displayed_array_stats = current.selected_array_stats
            else:
                clim_mask = None
                if current.colourmap_limits is not None:
                    clim_mask = np.logical_or( \
                        np.ma.less(current.selected_array, current.colourmap_limits[0]),
                        np.ma.greater(current.selected_array, current.colourmap_limits[1]))
                if clim_mask is not None and current.mask is not None:
                    mask = np.logical_or(clim_mask, current.mask)
                elif clim_mask is not None:
                    mask = clim_mask
                else:  # current.mask is not None:
                    mask = current.mask

                # May want to cache this instead of recalculating it each time.
                array = np.ma.masked_where(mask, current.selected_array)
                array_stats = {}
                if 'valid' in current.selected_array_stats:
                    number_invalid = np.ma.count_masked(array)
                    array_stats['invalid'] = number_invalid
                    array_stats['valid'] = array.size - number_invalid
                if 'min' in current.selected_array_stats:
                    array_stats['max'] = array.max()
                    array_stats['min'] = array.min()
                if 'mean' in current.selected_array_stats and current.colourmap_limits is None:
                    array_stats['mean'] = array.mean()
                if 'median' in current.selected_array_stats and current.colourmap_limits is None:
                    array_stats['median'] = np.ma.median(array)
                if 'std' in current.selected_array_stats and current.colourmap_limits is None:
                    array_stats['std'] = array.std()
                current.displayed_array = array
                current.displayed_array_stats = array_stats
                # Assuming update_status_bar will follow anyway.

            self.matplotlibWidget.update( \
                plot_type, current.array_type, current.displayed_array,
                current.displayed_array_stats, title, current.name,
                current.colourmap_limits)

        # Update controls that depend on mpl widget displaying valid data.
        self.actionExportImage.setEnabled(self.matplotlibWidget.has_content())

        if changed and self._zoom_colourmap_history.has_any():
            self._zoom_colourmap_history.clear()
            self.update_controls()

    def update_phase_combo_box(self):
        combo_box = self.phaseComboBox
        combo_box.clear()
        combo_box.addItem('')
        if self._project is not None:
            for name in sorted(self._project.phases.keys()):
                combo_box.addItem(name)

    def update_region_combo_box(self):
        combo_box = self.regionComboBox
        combo_box.clear()
        combo_box.addItem('')
        if self._project is not None:
            for name in sorted(self._project.regions.keys()):
                combo_box.addItem(name)

    def update_status_bar(self):
        data = self._status_callback_data
        if data is None:
            msg = self.get_status_string(self._current.displayed_array,
                                         self._current.displayed_array_stats)
        elif data[0] == 'pixel':
            value = data[3]
            value = 'none' if value is None else '{:g}'.format(value)
            msg = 'x={}, y={}, value={}'.format(data[1], data[2], value)
        elif data[0] == 'histogram':
            bin_width = data[1]
            nbins = data[2]
            msg = 'bin width={:g}, bin count={}'.format(bin_width, nbins)
            if len(data) == 6:
                bin_low = data[3]
                bin_high = data[4]
                count = data[5]
                msg = '{}, bin={:g} to {:g}, pixel count={}'.format( \
                    msg, bin_low, bin_high, count)
        else:  # Should not occur.
            msg = None

        if msg is None:
            self.statusbar.clearMessage()
        else:
            self.statusbar.showMessage(msg)

    def update_title(self):
        title = 'QACD-quack'
        if self._project is not None:
            title += ' - ' + self._project.filename
        self.setWindowTitle(title)

    def zoom_append(self, matplotlib_widget, from_, to):
        if matplotlib_widget == self.matplotlibWidget:
            self._zoom_history.append(from_, to)
            self.matplotlibWidget.set_map_zoom(to[0], to[1])
            self.update_controls()

    def zoom_colourmap_append(self, from_, to):
        self._zoom_colourmap_history.append(from_, to)
        self._current.colourmap_limits = to
        self.update_matplotlib_widget()
        self.update_controls()
        self.update_status_bar()

    def zoom_colourmap_redo(self):
        to = self._zoom_colourmap_history.redo()[1]
        self._current.colourmap_limits = to
        self.update_matplotlib_widget()
        self.update_controls()
        self.update_status_bar()

    def zoom_colourmap_undo(self):
        to = self._zoom_colourmap_history.undo()[0]
        self._current.colourmap_limits = to
        self.update_matplotlib_widget()
        self.update_controls()
        self.update_status_bar()

    def zoom_redo(self):
        zoom = self._zoom_history.redo()
        self.matplotlibWidget.set_map_zoom(zoom[1][0], zoom[1][1])
        self.update_controls()

    def zoom_undo(self):
        zoom = self._zoom_history.undo()
        self.matplotlibWidget.set_map_zoom(zoom[0][0], zoom[0][1])
        self.update_controls()
