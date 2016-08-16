# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'About_Dialog.ui'
#
# Created: Wed Feb 03 13:57:14 2016
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_About_Dialog(object):
    def setupUi(self, About_Dialog):
        About_Dialog.setObjectName("About_Dialog")
        About_Dialog.resize(404, 393)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/main_icon/16x16.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        About_Dialog.setWindowIcon(icon)
        About_Dialog.setWindowTitle("QACD-About")
        self.widget = QtGui.QWidget(About_Dialog)
        self.widget.setGeometry(QtCore.QRect(11, 11, 381, 371))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)
        self.pushButton = QtGui.QPushButton("Cancel",self.widget)
        self.pushButton.clicked.connect(self.close)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setDefault(False)
        self.pushButton.setFlat(False)
        self.gridLayout.addWidget(self.pushButton, 7, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_2 = QtGui.QLabel("About the QACD Software",self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.label = QtGui.QLabel(self.widget)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/main_icon/128x128.png"))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(self.label, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 7, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 7, 0, 1, 1)
        self.label_7 = QtGui.QLabel("Website coming soon...",self.widget)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_7, 6, 0, 1, 3)
        self.label_5 = QtGui.QLabel("This software is designed to be used for the processing of X-ray spectrum images or element maps collected by EDS on scaning electron microscopes and electron microprobes. For more details on the functionality see the manual or the step-by-step getting started guide in the help menu.",self.widget)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setWordWrap(True)
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 3)
        self.label_6 = QtGui.QLabel("For further questions email the author: LoockeMP@cardiff.ac.uk",self.widget)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 3)
        self.label_4 = QtGui.QLabel("Created by: Matthew Loocke",self.widget)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 3)
        self.label_3 = QtGui.QLabel("QACD version 1.0.0 (3 January 2016)",self.widget)
        self.label_3.setTextFormat(QtCore.Qt.RichText)
        self.label_3.setScaledContents(False)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 3)
        self.gridLayout.setRowStretch(1, 1)

        QtCore.QMetaObject.connectSlotsByName(About_Dialog)

    def close(self):
        self.close()
        return
    
import ProjectManager_rc

if __name__=='_main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    myDialog = QtGui.QDialog()
    ui = Ui_About_Dialog()
    ui.setupUi(myDialog)
    myDialog.show()
    sys.exit(app.exec_())
