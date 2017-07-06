from PyQt4.QtGui import QMainWindow, QDialog
from PyQt4.QtCore import pyqtSignature

from About_Dialog_gen import Ui_About_Dialog

class myDialog(QDialog, Ui_About_Dialog):
    def __init__(self, parent=None):
        QDialog.__init__(self,parent)
        self.setupUi(self)

        self.setFixedSize(self.size())
        self.okButton.clicked.connect(self.close)
