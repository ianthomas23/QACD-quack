from PyQt5 import QtCore, QtGui, QtWidgets

from .ui_filter_dialog import Ui_FilterDialog


class FilterDialog(QtWidgets.QDialog, Ui_FilterDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
