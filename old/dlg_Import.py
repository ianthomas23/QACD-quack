__author__ = 'Matthew Loocke'
__version__= '0.0.1'

"""
Module implementing Init Dialog
"""

from PyQt4.QtGui import QMainWindow, QDialog
from PyQt4.QtCore import pyqtSignature

from Import_Dialog import Ui_QACD_Import

class myDialog(QDialog,Ui_QACD_Import):
    def __init__(self, parent=None):
        QDialog.__init__(self,parent)
        self.setupUi(self)
