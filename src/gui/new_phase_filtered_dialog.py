import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

from src.model.elements import element_properties
from .matplotlib_widget import PlotType
from .ui_new_phase_filtered_dialog import Ui_NewPhaseFilteredDialog


class NewPhaseFilteredDialog(QtWidgets.QDialog, Ui_NewPhaseFilteredDialog):
    def __init__(self, project, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.project = project
        self.elementMatplotlibWidget.initialise(owning_window=self,
                                                zoom_enabled=False)
        self.phaseMatplotlibWidget.initialise(owning_window=self,
                                              zoom_enabled=False)

        self.fill_element_table()
        self.elementTable.itemSelectionChanged.connect(self.change_element)
        self.lowerSlider.sliderReleased.connect(self.update_element_map)
        self.upperSlider.sliderReleased.connect(self.update_element_map)
        self.lowerSlider.actionTriggered.connect(self.change_lower_slider)
        self.upperSlider.actionTriggered.connect(self.change_upper_slider)
        self.updateThresholdsButton.clicked.connect(self.update_thresholds)
        self.clearThresholdsButton.clicked.connect(self.clear_thresholds)

        self.okButton = self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)
        self.nameEdit.textChanged.connect(self.update_ok_button)

        # Currently selected element map.
        self.element = None
        self.array = None
        self.array_stats = None

        # Cache of per-element filtered within limits arrays.
        self.cache = {}

        # Currently displayed phase map (masked array).
        self.phase_map = None

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
            self.project.create_phase_map_from_filtered( \
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
            self.update_element_map()

    def change_upper_slider(self, action):
        position = self.upperSlider.sliderPosition()
        if position <= self.lowerSlider.value():
            position = self.lowerSlider.value()+1
            self.upperSlider.setSliderPosition(position)
        self.upperLineEdit.setText(str(position))

        if action != QtWidgets.QAbstractSlider.SliderMove:
            self.update_element_map()

    def clear_thresholds(self):
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.BusyCursor)

        self.set_thresholds(None, None)
        self.update_phase_map()

        QtWidgets.QApplication.restoreOverrideCursor()
        self.update_buttons()

    def fill_element_table(self):
        # Correct table widget properties.
        table_widget = self.elementTable
        horiz = table_widget.horizontalHeader()
        horiz.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        horiz.setDefaultAlignment(QtCore.Qt.AlignLeft)
        vert = table_widget.verticalHeader()
        vert.setDefaultSectionSize(vert.minimumSectionSize())

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

            self.elementMatplotlibWidget.update( \
                PlotType.MAP, self.array, self.array_stats, title,
                show_colorbar=True)

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
                self.update_element_map()
        else:
            for control in (self.lowerSlider, self.upperSlider,
                            self.lowerLineEdit, self.upperLineEdit,
                            self.updateThresholdsButton):
                control.setEnabled(False)

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

    def set_table_widget_cell(self, table_widget, row, column, text):
        if not text:
            table_widget.setItem(row, column, None)
        else:
            item = QtWidgets.QTableWidgetItem(text)
            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
            table_widget.setItem(row, column, item)

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

    def update_element_map(self):
        lower = self.lowerSlider.value()
        upper = self.upperSlider.value()
        self.elementMatplotlibWidget.set_colormap_limits(lower, upper)
        self.update_buttons()

    def update_ok_button(self):
        self.okButton.setEnabled(bool(self.cache) and \
                                 len(self.nameEdit.text()) > 0)

    def update_phase_map(self):
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
            self.phaseMatplotlibWidget.update( \
                PlotType.MAP, self.phase_map, None, None, show_colorbar=False,
                cmap_int_max=2)

    def update_thresholds(self):
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.BusyCursor)

        self.set_thresholds(self.lowerSlider.value(), self.upperSlider.value())
        self.update_phase_map()

        QtWidgets.QApplication.restoreOverrideCursor()
        self.update_buttons()
