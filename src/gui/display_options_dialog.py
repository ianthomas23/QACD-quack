import matplotlib.cm as cm
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

from .ui_display_options_dialog import Ui_DisplayOptionsDialog


class DisplayOptionsDialog(QtWidgets.QDialog, Ui_DisplayOptionsDialog):
    def __init__(self, display_options, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

        self._display_options = display_options

        self._locations_lookup = {'upper left': self.upperLeftRadioButton,
                                  'upper right': self.upperRightRadioButton,
                                  'lower left': self.lowerLeftRadioButton,
                                  'lower right': self.lowerRightRadioButton}

        self._locations_button_group = QtWidgets.QButtonGroup()
        for button in self._locations_lookup.values():
            self._locations_button_group.addButton(button)

        self.applyButton = self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply)
        self.applyButton.clicked.connect(self.apply)

        self.init_colourmap_tab()
        self.init_labels_and_scale_tab()
        self.tabWidget.setCurrentIndex(0)
        self.update_controls()

        self.tabWidget.currentChanged.connect(self.change_tab)

        # Colourmap tab controls.
        self.colourmapListWidget.itemDoubleClicked.connect(self.apply)
        self.colourmapListWidget.itemSelectionChanged.connect(self.update_buttons)
        self.reverseCheckBox.stateChanged.connect(self.update_buttons)

        # Scale tab controls - call update_buttons to enable/disable apply
        # button, and update_controls if need to enable other controls too.
        self.showTicksAndLabelsCheckBox.stateChanged.connect(self.update_buttons)
        self.useScaleCheckBox.stateChanged.connect(self.update_controls)
        self.pixelSizeLineEdit.textChanged.connect(self.update_buttons)
        self.unitsComboBox.currentIndexChanged.connect(self.update_buttons)
        self.showScaleBarCheckBox.stateChanged.connect(self.update_controls)
        self._locations_button_group.buttonClicked.connect(self.update_buttons)

    def accept(self):
        try:
            for index in range(2):
                self.apply_tab(index)
            self.close()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Error', str(e))

    def apply(self):
        try:
            # Apply the current tab.
            self.apply_tab(self.tabWidget.currentIndex())
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Error', str(e))

    def apply_tab(self, tab_index):
        if tab_index == 0:
            # Colourmap tab.
            selected_name = self.get_selected_colourmap_name()
            if selected_name is not None:
                # The following line will update any visible matplotlib_widget
                # objects.
                self._display_options.colourmap_name = selected_name
                self.update_buttons()
        else:
            # Labels and scale tab.
            show_ticks_and_labels = self.showTicksAndLabelsCheckBox.isChecked()

            use_scale = self.useScaleCheckBox.isChecked()
            pixel_size, ok = QtCore.QLocale().toDouble(self.pixelSizeLineEdit.text())
            if not ok or pixel_size == 0.0:
                validator = self.pixelSizeLineEdit.validator()
                raise RuntimeError('Pixel size should be a number between {} and {}'.format( \
                    validator.bottom(), validator.top()))
            units = self.unitsComboBox.currentText()
            show_scale_bar = self.showScaleBarCheckBox.isChecked()
            scale_bar_location = self.get_scale_bar_location()

            self._display_options.set_labels_and_scale( \
                show_ticks_and_labels, use_scale, pixel_size, units,
                show_scale_bar, scale_bar_location)
            self.update_buttons()

    def change_tab(self):
        self.update_buttons()

    def create_pixmap(self, name):
        w, h = self._image_size

        cmap = cm.get_cmap(name)
        c = cmap(np.linspace(0.0, 1.0, w))
        c = (255*c[:, :3]).astype(np.uint32)
        rgb = np.bitwise_or(np.left_shift(c[:, 0], 16),
                            np.bitwise_or(np.left_shift(c[:, 1], 8), c[:, 2]))
        rgb = np.tile(rgb, (h, 1))  # rgb shape is (h, w)

        image = QtGui.QImage(rgb, w, h, QtGui.QImage.Format_RGB32)
        self._images.append(image)

        return QtGui.QPixmap.fromImage(image)

    def get_scale_bar_location(self):
        button = self._locations_button_group.checkedButton()
        matches = [k for k,v in self._locations_lookup.items() if v == button]
        if matches:
            return matches[0]
        else:
            return None

    def get_selected_colourmap_name(self):
        item = self.colourmapListWidget.currentItem()
        if item is not None:
            name = item.text()
            if self.reverseCheckBox.isChecked():
                name += '_r'
        else:
            name = None
        return name

    def init_colourmap_tab(self):
        options = self._display_options

        colourmap_name = options.colourmap_name
        is_reversed = colourmap_name.endswith('_r')
        if is_reversed:
            colourmap_name = colourmap_name[:-2]
        self.reverseCheckBox.setChecked(is_reversed)

        self._image_size = (255, self.colourmapListWidget.font().pointSize()*4 // 3)
        self._images = []  # Need to keep these in scope.

        # Fill list widget with colourmap names.
        selected_item = None
        for index, name in enumerate(options.valid_colourmap_names):
            item = QtWidgets.QListWidgetItem(name, parent=self.colourmapListWidget)
            item.setData(QtCore.Qt.DecorationRole, self.create_pixmap(name))
            if name == colourmap_name:
                selected_item = item

        if selected_item is not None:
            # Selects current colourmap, and scrolls so that it is visible.
            self.colourmapListWidget.setCurrentItem(selected_item)

    def init_labels_and_scale_tab(self):
        options = self._display_options

        # Labels.
        self.showTicksAndLabelsCheckBox.setChecked(options.show_ticks_and_labels)

        # Scale.
        self.useScaleCheckBox.setChecked(options.use_scale)

        validator = QtGui.QDoubleValidator(0.01, 999.99, 2)
        validator.setNotation(QtGui.QDoubleValidator.StandardNotation)
        self.pixelSizeLineEdit.setValidator(validator)
        self.pixelSizeLineEdit.setText(str(options.pixel_size))

        selected_index = None
        for index, units in enumerate(self._display_options.valid_units):
            self.unitsComboBox.addItem(units)
            if units == options.units:
                selected_index = index
        if selected_index is None:
            raise RuntimeError('Cannot find units {}'.format(options.units))
        else:
            self.unitsComboBox.setCurrentIndex(selected_index)

        self.showScaleBarCheckBox.setChecked(options.show_scale_bar)
        self._locations_lookup[options.scale_bar_location].setChecked(True)

    def update_buttons(self):
        options = self._display_options

        tab_index = self.tabWidget.currentIndex()
        if tab_index == 0:
            selected_name = self.get_selected_colourmap_name()
            self.applyButton.setEnabled(selected_name != options.colourmap_name)
        else:
            enabled = \
                self.showTicksAndLabelsCheckBox.isChecked() != options.show_ticks_and_labels or \
                self.useScaleCheckBox.isChecked() != options.use_scale or \
                QtCore.QLocale().toDouble(self.pixelSizeLineEdit.text())[0] != options.pixel_size or \
                self.unitsComboBox.currentText() != options.units or \
                self.showScaleBarCheckBox.isChecked() != options.show_scale_bar or \
                self.get_scale_bar_location() != options.scale_bar_location

            self.applyButton.setEnabled(enabled)

    def update_controls(self):
        self.update_buttons()

        # Scale.
        use_scale = self.useScaleCheckBox.isChecked()
        self.pixelSizeLabel.setEnabled(use_scale)
        self.pixelSizeLineEdit.setEnabled(use_scale)
        self.unitsComboBox.setEnabled(use_scale)
        self.showScaleBarCheckBox.setEnabled(use_scale)
        self.scaleBarLocationGroupBox.setEnabled( \
            use_scale and self.showScaleBarCheckBox.isChecked())
