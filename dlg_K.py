"""
Module implementing Ratio Dialog
"""

from PyQt4.QtGui import QMainWindow, QDialog
from PyQt4.QtCore import pyqtSignature

from K_dialog_gen import Ui_K_Dialog

class myDialog(QDialog, Ui_K_Dialog):
    def __init__(self, parent=None):
        QDialog.__init__(self,parent)
        self.setupUi(self)

        self.pushButton.clicked.connect(self.cont_Ph)

    def cont_Ph(self):
        self.pushButton.setText("Calculating...")
        mini = int(self.spinBox.value())
        maxi = int(self.spinBox_2.value())
        K = range(mini,maxi+1)

        import qacd_kmeans2 as qk
        qk.monte_carlo(K)
        self.close()
