from PyQt5 import QtCore, QtGui, QtWidgets

from src.model.elements import element_properties
from .matplotlib_widget import PlotType
from .ui_new_phase_filtered_dialog import Ui_NewPhaseFilteredDialog


class NewPhaseFilteredDialog(QtWidgets.QDialog, Ui_NewPhaseFilteredDialog):
    def __init__(self, project, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.project = project
        self.matplotlibWidget.initialise(owning_window=self,
                                         zoom_enabled=False)

        self.fill_element_table()
        self.elementTable.itemSelectionChanged.connect(self.change_element)
        self.lowerSlider.sliderReleased.connect(self.update_element_map)
        self.upperSlider.sliderReleased.connect(self.update_element_map)
        self.lowerSlider.actionTriggered.connect(self.change_lower_slider)
        self.upperSlider.actionTriggered.connect(self.change_upper_slider)
        self.updateThresholdsButton.clicked.connect(self.update_thresholds)
        self.clearThresholdsButton.clicked.connect(self.clear_thresholds)

        # Currently selected element map.
        self.element = None
        self.array = None
        self.array_stats = None

        self.select_element(self.project.elements[0])

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
        self.set_thresholds(None, None)

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

    def select_element(self, element, lower=None, upper=None):
        self.element = element
        if self.element is not None:

            self.array, self.array_stats = self.project.get_filtered( \
                self.element, want_stats=True)
            title = 'Filtered {} element'.format(self.element)

            self.matplotlibWidget.update( \
                PlotType.MAP, self.array, self.array_stats, title,
                show_colorbar=True)

            for control in (self.lowerSlider, self.upperSlider,
                            self.lowerLineEdit, self.upperLineEdit,
                            self.updateThresholdsButton):
                control.setEnabled(True)

            for slider in (self.lowerSlider, self.upperSlider):
                slider.setMinimum(self.array_stats['min'])
                slider.setMaximum(self.array_stats['max'])

            lower = int(lower) if lower is not None else self.array_stats['min']
            upper = int(upper) if upper is not None else self.array_stats['max']

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
        if lower is not None:
            lower = str(lower)

        if upper is not None:
            upper = str(upper)

        table_widget = self.elementTable
        match = table_widget.findItems(self.element, QtCore.Qt.MatchExactly)
        row = match[0].row()

        # Disable sorting whilst changing content.
        sorting = table_widget.isSortingEnabled()
        table_widget.setSortingEnabled(False)

        self.set_table_widget_cell(table_widget, row, 2, lower)
        self.set_table_widget_cell(table_widget, row, 3, upper)

        # Re-enable sorting.
        table_widget.setSortingEnabled(sorting)

    def set_table_widget_cell(self, table_widget, row, column, text):
        if not text:
#            table_widget.removeCellWidget(row, column)
            table_widget.setItem(row, column, None)
        else:
            item = QtWidgets.QTableWidgetItem(text)
            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
            table_widget.setItem(row, column, item)

    def update_element_map(self):
        lower = self.lowerSlider.value()
        upper = self.upperSlider.value()
        self.matplotlibWidget.set_colormap_limits(lower, upper)

    def update_thresholds(self):
        self.set_thresholds(self.lowerSlider.value(), self.upperSlider.value())
