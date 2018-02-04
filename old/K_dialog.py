# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'K_dialog.ui'
#
# Created: Thu Jan 28 17:36:45 2016
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui


class Ui_K_Dialog(object):
    def setupUi(self, K_Dialog):
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        K_Dialog.setObjectName("K_Dialog")
        K_Dialog.resize(451, 160)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/main_icon/16x16.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        K_Dialog.setWindowIcon(icon)
        K_Dialog.setWindowTitle("QACD-3b.Pick your K")
        
        self.widget = QtGui.QWidget(K_Dialog)
        self.widget.setGeometry(QtCore.QRect(10, 0, 431, 151))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)
        
        self.label_3 = QtGui.QLabel("Minimum (K):",self.widget)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.spinBox = QtGui.QSpinBox(self.widget)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(20)
        self.spinBox.setProperty("value", 5)
        self.gridLayout.addWidget(self.spinBox, 1, 1, 1, 1)
        
        self.label_4 = QtGui.QLabel("Maximum (K):",self.widget)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_4, 1, 2, 1, 1)
        self.spinBox_2 = QtGui.QSpinBox(self.widget)
        self.spinBox_2.setMinimum(1)
        self.spinBox_2.setMaximum(20)
        self.spinBox_2.setProperty("value", 10)
        self.gridLayout.addWidget(self.spinBox_2, 1, 3, 1, 2)
        
        self.label = QtGui.QLabel("""<html><head/><body><p>Enter a range for the estimated number 
                                     of phases (K) in the sample. Remember that the glass slide of 
                                     a thin section needs to be accounted for along with any potential 
                                     major alteration phases.</p></body></html>""",self.widget)
        self.label.setWordWrap(True)
        self.gridLayout.addWidget(self.label, 2, 0, 1, 5)
        
        self.label_2 = QtGui.QLabel("Step 3b. Phase Clustering:",self.widget)
        font = QtGui.QFont()
        font.setBold(False)
        font.setUnderline(True)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 5)
        
        self.pushButton = QtGui.QPushButton("Continue",self.widget)
        self.gridLayout.addWidget(self.pushButton, 3, 3, 1, 2)
        self.pushButton.clicked.connect(self.cont_Ph)
        
        self.label_5 = QtGui.QLabel("Warning: This can take a few minutes.",self.widget)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setWordWrap(True)
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 3)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setColumnStretch(3, 1)

        QtCore.QMetaObject.connectSlotsByName(K_Dialog)
    def cont_Ph(self):
        self.pushButton.setText("Calculating...")
        mini = int(self.spinBox.value())
        maxi = int(self.spinBox_2.value())
        K = range(mini,maxi+1)
        import qacd_kmeans2 as qk
        qk.monte_carlo(K)
        self.close()
        return

import ProjectManager_rc
if __name__=='_main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    myDialog = QtGui.QDialog()
    ui = Ui_K_Dialog()
    ui.setupUi(myDialog)
    myDialog.show()
    sys.exit(app.exec_())
