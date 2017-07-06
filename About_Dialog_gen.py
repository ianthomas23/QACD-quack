# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'About_Dialog.ui'
#
# Created: Thu Jul  6 15:52:42 2017
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_About_Dialog(object):
    def setupUi(self, About_Dialog):
        About_Dialog.setObjectName(_fromUtf8("About_Dialog"))
        About_Dialog.resize(404, 393)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/main_icon/16x16.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        About_Dialog.setWindowIcon(icon)
        self.layoutWidget = QtGui.QWidget(About_Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(11, 11, 381, 371))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.okButton = QtGui.QPushButton(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.okButton.sizePolicy().hasHeightForWidth())
        self.okButton.setSizePolicy(sizePolicy)
        self.okButton.setDefault(False)
        self.okButton.setFlat(False)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.gridLayout.addWidget(self.okButton, 7, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8(":/main_icon/128x128.png")))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 7, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 7, 0, 1, 1)
        self.label_7 = QtGui.QLabel(self.layoutWidget)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 6, 0, 1, 3)
        self.label_5 = QtGui.QLabel(self.layoutWidget)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 3)
        self.label_6 = QtGui.QLabel(self.layoutWidget)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 3)
        self.label_4 = QtGui.QLabel(self.layoutWidget)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 3)
        self.label_3 = QtGui.QLabel(self.layoutWidget)
        self.label_3.setTextFormat(QtCore.Qt.RichText)
        self.label_3.setScaledContents(False)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 3)
        self.gridLayout.setRowStretch(1, 1)

        self.retranslateUi(About_Dialog)
        QtCore.QMetaObject.connectSlotsByName(About_Dialog)

    def retranslateUi(self, About_Dialog):
        About_Dialog.setWindowTitle(_translate("About_Dialog", "QACD-About", None))
        self.okButton.setText(_translate("About_Dialog", "OK", None))
        self.label_2.setText(_translate("About_Dialog", "About the QACD Software", None))
        self.label_7.setText(_translate("About_Dialog", "Website coming soon...", None))
        self.label_5.setText(_translate("About_Dialog", "This software is designed to be used for the processing of X-ray spectrum images or element maps collected by EDS on scaning electron microscopes and electron microprobes. For more details on the functionality see the manual or the step-by-step getting started guide in the help menu.", None))
        self.label_6.setText(_translate("About_Dialog", "For further questions email the author: LoockeMP@cardiff.ac.uk", None))
        self.label_4.setText(_translate("About_Dialog", "Created by: Matthew Loocke", None))
        self.label_3.setText(_translate("About_Dialog", "QACD version 1.0.0 (3 January 2016)", None))

import ProjectManager_rc
