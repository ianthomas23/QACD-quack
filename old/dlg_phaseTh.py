__author__ = 'Matthew Loocke'
__version__= '0.0.1'

"""
Module implementing Init Dialog
"""

from PyQt4.QtGui import QMainWindow, QDialog
from PyQt4.QtCore import pyqtSignature
from PyQt4.QtCore import Qt

from Ph_Dialog_v2 import Ui_Phase_Dialog

class myDialog(QDialog,Ui_Phase_Dialog):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setupUi(self)
