import matplotlib.cm as cm
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

from .ui_display_options_dialog import Ui_DisplayOptionsDialog


class DisplayOptionsDialog(QtWidgets.QDialog, Ui_DisplayOptionsDialog):
    def __init__(self, colormap_name, valid_colormap_names, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.applyButton = self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply)

        self.applyButton.clicked.connect(self.apply)
        self.listWidget.itemSelectionChanged.connect(self.update_buttons)
        self.reverseCheckBox.stateChanged.connect(self.update_buttons)

        self.current_colormap_name = colormap_name

        is_reversed = colormap_name.endswith('_r')
        if is_reversed:
            colormap_name = colormap_name[:-2]
        self.reverseCheckBox.setChecked(is_reversed)

        self._image_size = (255, self.listWidget.font().pointSize()*4 // 3)
        self._images = []  # Need to keep these in scope.

        # Fill list widget with colormap names.
        selected_item = None
        for index, name in enumerate(valid_colormap_names):
            item = QtWidgets.QListWidgetItem(name, parent=self.listWidget)
            item.setData(QtCore.Qt.DecorationRole, self.create_pixmap(name))
            if name == colormap_name:
                selected_item = item

        if selected_item is not None:
            # Selects current colormap, and scrolls so that it is visible.
            self.listWidget.setCurrentItem(selected_item)

        self.update_buttons()

    def accept(self):
        self.apply()
        self.close()

    def apply(self):
        selected_name = self.get_selected_colormap_name()
        if selected_name is not None:
            self.parent().set_colormap_name(selected_name)
            self.current_colormap_name = selected_name
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

    def get_selected_colormap_name(self):
        item = self.listWidget.currentItem()
        if item is not None:
            name = item.text()
            if self.reverseCheckBox.isChecked():
                name += '_r'
        else:
            name = None
        return name

    def update_buttons(self):
        selected_name = self.get_selected_colormap_name()
        self.applyButton.setEnabled(selected_name != self.current_colormap_name)
