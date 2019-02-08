import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

from src.model.elements import element_properties
from .enums import ArrayType, PlotType
from .ui_new_phase_filtered_dialog import Ui_NewPhaseFilteredDialog
from .zoom_history import ZoomHistory


class NewPhaseFilteredDialog(QtWidgets.QDialog, Ui_NewPhaseFilteredDialog):
    def __init__(self, project, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window)

        self.project = project
        self.elementMatplotlibWidget.initialise( \
            owning_window=self, display_options=self.project.display_options,
            zoom_enabled=True, status_callback=self.status_callback)
        self.phaseMatplotlibWidget.initialise( \
            owning_window=self, display_options=self.project.display_options,
            zoom_enabled=True, status_callback=self.status_callback)

        # Initial vertical sizes above and below splitter.
        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 1)

        self.fill_element_table()
        self.elementTable.itemSelectionChanged.connect(self.change_element)
        self.lowerSlider.sliderReleased.connect(self.update_element_map_colourmap_limits)
        self.upperSlider.sliderReleased.connect(self.update_element_map_colourmap_limits)
        self.lowerSlider.actionTriggered.connect(self.change_lower_slider)
        self.upperSlider.actionTriggered.connect(self.change_upper_slider)
        self.updateThresholdsButton.clicked.connect(self.update_thresholds)
        self.clearThresholdsButton.clicked.connect(self.clear_thresholds)

        self.okButton = self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)
        self.nameEdit.textChanged.connect(self.update_ok_button)
        self.undoButton.clicked.connect(self.zoom_undo)
        self.redoButton.clicked.connect(self.zoom_redo)

        # Currently selected element map.
        self.element = None
        self.array = None
        self.array_stats = None
        self.zoom = None    # None or float array of shape (2,2).

        # Cache of per-element filtered within limits arrays.
        self.cache = {}

        # Currently displayed phase map (masked array).
        self.phase_map = None

        self.status_callback_data = None
        self.zoom_history = ZoomHistory()

        # Select first row in element table.
        self.elementTable.setCurrentCell(0, 0)

    def accept(self):
        try:
            # Validation.
            name = self.nameEdit.text().strip()
            if len(name) < 1:
                raise RuntimeError('No phase map name specified')

            if name in self.project.phases:
                raise RuntimeError("The phase map name '{}' has already been used".format(name))

            # Create new phase map.
            table_widget = self.elementTable
            elements_and_thresholds = []
            for element in sorted(self.cache.keys()):
                match = table_widget.findItems(element, QtCore.Qt.MatchExactly)
                row = match[0].row()
                lower = int(table_widget.item(row, 2).text())
                upper = int(table_widget.item(row, 3).text())
                elements_and_thresholds.append((element, lower, upper))
            self.project.create_phase_map_by_thresholding( \
                name, elements_and_thresholds, phase_map=self.phase_map)

            # Close dialog.
            super().accept()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Error', str(e))

    def change_element(self):
        # Change of selected item in element table.
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.BusyCursor)

        row = self.elementTable.currentRow()
        element = self.elementTable.item(row, 0).text()
        lower = self.elementTable.item(row, 2)
        if lower is not None:
            lower = lower.text()
        upper = self.elementTable.item(row, 3)
        if upper is not None:
            upper = upper.text()

        self.select_element(element, lower, upper)

        QtWidgets.QApplication.restoreOverrideCursor()
        self.update_buttons()

    def change_lower_slider(self, action):
        position = self.lowerSlider.sliderPosition()
        if position >= self.upperSlider.value():
            position = self.upperSlider.value()-1
            self.lowerSlider.setSliderPosition(position)
        self.lowerLineEdit.setText(str(position))

        if action != QtWidgets.QAbstractSlider.SliderMove:
            self.update_element_map_colourmap_limits()

    def change_upper_slider(self, action):
        position = self.upperSlider.sliderPosition()
        if position <= self.lowerSlider.value():
            position = self.lowerSlider.value()+1
            self.upperSlider.setSliderPosition(position)
        self.upperLineEdit.setText(str(position))

        if action != QtWidgets.QAbstractSlider.SliderMove:
            self.update_element_map_colourmap_limits()

    def change_zoom(self, zoom):
        self.zoom = zoom
        for widget in (self.elementMatplotlibWidget,
                       self.phaseMatplotlibWidget):
            if widget._array is not None:
                widget.update(PlotType.MAP, widget._array_type, widget._array,
                              widget._array_stats, widget._title, widget._name,
                              map_zoom=self.zoom)

    def clear_thresholds(self):
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.BusyCursor)

        self.set_thresholds(None, None)
        self.update_phase_map()

        QtWidgets.QApplication.restoreOverrideCursor()
        self.update_buttons()

    def fill_element_table(self):
        table_widget = self.elementTable

        # Disable sorting whilst changing content.
        sorting = table_widget.isSortingEnabled()
        table_widget.setSortingEnabled(False)

        elements = self.project.elements
        self.elementTable.setRowCount(len(elements))

        # Fill table widget.
        for row, element in enumerate(elements):
            self.set_table_widget_cell(table_widget, row, 0, element)
            name = element_properties[element][0]
            self.set_table_widget_cell(table_widget, row, 1, name)

        # Correct table widget properties.
        horiz = table_widget.horizontalHeader()

        horiz.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        column_width = horiz.sectionSize(1)
        horiz.setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        horiz.resizeSection(1, column_width)

        horiz.setDefaultAlignment(QtCore.Qt.AlignLeft)
        vert = table_widget.verticalHeader()
        vert.setDefaultSectionSize(vert.minimumSectionSize())

        # Re-enable sorting.
        table_widget.setSortingEnabled(sorting)

    def get_name(self):
        return self.nameEdit.text().strip()

    def select_element(self, element, lower=None, upper=None):
        self.element = element
        if self.element is not None:

            self.array, self.array_stats = self.project.get_filtered( \
                self.element, want_stats=True)
            title = 'Filtered {} element'.format(self.element)

            self.elementMatplotlibWidget.update(PlotType.MAP,
                ArrayType.FILTERED, self.array, self.array_stats, title,
                self.element, map_zoom=self.zoom)

            for control in (self.lowerSlider, self.upperSlider,
                            self.lowerLineEdit, self.upperLineEdit,
                            self.updateThresholdsButton):
                control.setEnabled(True)

            min_ = int(self.array_stats['min'])
            max_ = int(self.array_stats['max'])

            for slider in (self.lowerSlider, self.upperSlider):
                slider.setMinimum(min_)
                slider.setMaximum(max_)

            lower = int(lower) if lower is not None else min_
            upper = int(upper) if upper is not None else max_

            self.lowerSlider.setSliderPosition(lower)
            self.upperSlider.setSliderPosition(upper)

            self.lowerLineEdit.setText(str(lower))
            self.upperLineEdit.setText(str(upper))

            if lower is not None and upper is not None:
                self.update_element_map_colourmap_limits()
        else:
            for control in (self.lowerSlider, self.upperSlider,
                            self.lowerLineEdit, self.upperLineEdit,
                            self.updateThresholdsButton):
                control.setEnabled(False)

    def set_table_widget_cell(self, table_widget, row, column, text):
        if not text:
            table_widget.setItem(row, column, None)
        else:
            item = QtWidgets.QTableWidgetItem(text)
            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
            table_widget.setItem(row, column, item)

    # Set thresholds for current element.  May be None.
    def set_thresholds(self, lower, upper):
        table_widget = self.elementTable
        match = table_widget.findItems(self.element, QtCore.Qt.MatchExactly)
        row = match[0].row()

        # Disable sorting whilst changing content.
        sorting = table_widget.isSortingEnabled()
        table_widget.setSortingEnabled(False)

        self.set_table_widget_cell(table_widget, row, 2, \
            str(lower) if lower is not None else None)
        self.set_table_widget_cell(table_widget, row, 3, \
            str(upper) if upper is not None else None)

        # Re-enable sorting.
        table_widget.setSortingEnabled(sorting)

        # Update cache.
        if lower is None or upper is None:
            self.cache.pop(self.element, None)
        else:
            self.cache[self.element] = self.project.get_filtered_within_limits(\
                self.element, lower, upper)

    def status_callback(self, matplotlib_widget, data):
        if not (data is None and self.status_callback_data is None):
            self.status_callback_data = data
            self.update_status_bar()

    def update_buttons(self):
        row = self.elementTable.currentRow()
        lower_item = self.elementTable.item(row, 2)
        upper_item = self.elementTable.item(row, 3)
        changed_threshold = lower_item is None or upper_item is None or \
            int(lower_item.text()) != self.lowerSlider.sliderPosition() or \
            int(upper_item.text()) != self.upperSlider.sliderPosition()

        self.updateThresholdsButton.setEnabled(changed_threshold)
        self.clearThresholdsButton.setEnabled(self.element in self.cache)
        self.update_ok_button()

        self.undoButton.setEnabled(self.zoom_history.has_undo())
        self.redoButton.setEnabled(self.zoom_history.has_redo())

    def update_element_map_colourmap_limits(self):
        lower = self.lowerSlider.value()
        upper = self.upperSlider.value()
        self.elementMatplotlibWidget.set_colourmap_limits(lower, upper)
        self.update_buttons()

    def update_ok_button(self):
        self.okButton.setEnabled(bool(self.cache) and \
                                 len(self.nameEdit.text()) > 0)

    def update_phase_map(self):
        previously_empty = not self.phaseMatplotlibWidget.has_map_axes()

        self.phase_map = None
        for element, array in self.cache.items():
            if self.phase_map is None:
                self.phase_map = array
            else:
                self.phase_map = np.logical_and(self.phase_map, array)

        if self.phase_map is None:
            self.phaseMatplotlibWidget.clear()
        else:
            self.phase_map = np.ma.masked_equal(self.phase_map, 0)
            self.phaseMatplotlibWidget.update(PlotType.MAP, ArrayType.PHASE,
                self.phase_map, None, None, None, map_zoom=self.zoom)
            if previously_empty and self.zoom_history.has_any():
                zoom = self.zoom_history.current()
                self.change_zoom(zoom[1])

    def update_status_bar(self):
        if self.status_callback_data is None:
            msg = None
        else:
            x, y, value = self.status_callback_data[1:]
            if value is None:
                msg = 'x={} y={} value=none'.format(x, y)
            else:
                msg = 'x={} y={} value={:g}'.format(x, y, value)

        self.statusbar.setText(msg)

    def update_thresholds(self):
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.BusyCursor)

        self.set_thresholds(self.lowerSlider.value(), self.upperSlider.value())
        self.update_phase_map()

        QtWidgets.QApplication.restoreOverrideCursor()
        self.update_buttons()

    def zoom_append(self, matplotlib_widget, from_, to):
        self.zoom_history.append(from_, to)
        self.change_zoom(to)
        self.update_buttons()

    def zoom_redo(self):
        zoom = self.zoom_history.redo()
        self.change_zoom(zoom[1])
        self.update_buttons()

    def zoom_undo(self):
        zoom = self.zoom_history.undo()
        self.change_zoom(zoom[0])
        self.update_buttons()
