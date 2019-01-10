from PyQt5 import QtCore, QtGui, QtWidgets

from .enums import ModeType
from .ui_new_region_dialog import Ui_NewRegionDialog


class NewRegionDialog(QtWidgets.QDialog, Ui_NewRegionDialog):
    def __init__(self, project, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.project = project

        self.okButton = self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)

        self._button_to_mode = \
            {self.ellipseRadioButton: ModeType.REGION_ELLIPSE,
             self.polygonRadioButton: ModeType.REGION_POLYGON,
             self.rectangleRadioButton: ModeType.REGION_RECTANGLE}

        for button in self._button_to_mode.keys():
            button.clicked.connect(self.change_type)

        self.nameLineEdit.textChanged.connect(self.update_ok_button)

        self.ellipseRadioButton.click()

    def accept(self):
        try:
            # Validation.
            name = self.get_name()
            if len(name) < 1:
                raise RuntimeError('No region name specified')

            if name in self.project.regions:
                raise RuntimeError("The region name '{}' has already been used".format(name))

            # Create new region.
            mode_handler = self.get_mode_handler()
            region = mode_handler.get_region()
            if region is None:
                raise RuntimeError('No region boolean array')
            self.project.create_region(name, mode_handler.get_shape_string(),
                                       region)

            # Close dialog.
            self.get_matplotlib_widget().set_default_mode_type()
            super().accept()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Error', str(e))

    def change_type(self):
        mode_type = self._button_to_mode[self.sender()]
        self.get_matplotlib_widget().set_mode_type(mode_type, listener=self)
        self.update_ok_button()

    def get_matplotlib_widget(self):
        return self.parent().matplotlibWidget

    def get_mode_handler(self):
        return self.get_matplotlib_widget()._mode_handler

    def get_name(self):
        return self.nameLineEdit.text().strip()

    def reject(self):
        self.get_matplotlib_widget().set_mode_type(ModeType.ZOOM)
        super().reject()

    def update_ok_button(self):
        has_region = self.get_mode_handler().has_region()
        self.okButton.setEnabled(has_region and
                                 len(self.nameLineEdit.text()) > 0)

    def update_from_mode_handler(self):
        self.update_ok_button()
