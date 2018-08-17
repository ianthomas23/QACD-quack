from PyQt5 import QtCore, QtGui, QtWidgets

from .ui_about_dialog import Ui_AboutDialog


class AboutDialog(QtWidgets.QDialog, Ui_AboutDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
