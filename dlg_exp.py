__author__ = 'Matthew Loocke'
__version__= '0.0.1'

"""
Module implementing Ratio Dialog
"""

from PyQt4.QtGui import QMainWindow, QDialog
from PyQt4.QtCore import pyqtSignature

from Export_Dialog import Ui_Export_Dialog

class myDialog(QDialog,Ui_Export_Dialog):
    def __init__(self, parent=None):
        QDialog.__init__(self,parent)
        self.setupUi(self)
