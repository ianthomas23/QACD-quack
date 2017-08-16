# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'K_dialog.ui'
#
# Created: Wed Aug 16 15:28:01 2017
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

class Ui_K_Dialog(object):
    def setupUi(self, K_Dialog):
        K_Dialog.setObjectName(_fromUtf8("K_Dialog"))
        K_Dialog.resize(451, 160)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/main_icon/16x16.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        K_Dialog.setWindowIcon(icon)
        self.widget = QtGui.QWidget(K_Dialog)
        self.widget.setGeometry(QtCore.QRect(10, 0, 431, 151))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_3 = QtGui.QLabel(self.widget)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.spinBox = QtGui.QSpinBox(self.widget)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(20)
        self.spinBox.setProperty("value", 5)
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.gridLayout.addWidget(self.spinBox, 1, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.widget)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 1, 2, 1, 1)
        self.spinBox_2 = QtGui.QSpinBox(self.widget)
        self.spinBox_2.setMinimum(1)
        self.spinBox_2.setMaximum(20)
        self.spinBox_2.setProperty("value", 10)
        self.spinBox_2.setObjectName(_fromUtf8("spinBox_2"))
        self.gridLayout.addWidget(self.spinBox_2, 1, 3, 1, 2)
        self.label = QtGui.QLabel(self.widget)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 0, 1, 5)
        self.label_2 = QtGui.QLabel(self.widget)
        font = QtGui.QFont()
        font.setBold(False)
        font.setUnderline(True)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 5)
        self.pushButton = QtGui.QPushButton(self.widget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 3, 3, 1, 2)
        self.label_5 = QtGui.QLabel(self.widget)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 3)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setColumnStretch(3, 1)

        self.retranslateUi(K_Dialog)
        QtCore.QMetaObject.connectSlotsByName(K_Dialog)

    def retranslateUi(self, K_Dialog):
        K_Dialog.setWindowTitle(_translate("K_Dialog", "QACD-3b.Pick your K", None))
        self.label_3.setText(_translate("K_Dialog", "Minimum (K):", None))
        self.label_4.setText(_translate("K_Dialog", "Maximum (K):", None))
        self.label.setText(_translate("K_Dialog", "<html><head/><body><p>Enter a range for the estimated number of phases (K) in the sample. Remember that the glass slide of a thin section needs to be accounted for along with any potential major alteration phases.</p></body></html>", None))
        self.label_2.setText(_translate("K_Dialog", "Step 3b. Phase Clustering:", None))
        self.pushButton.setText(_translate("K_Dialog", "Continue", None))
        self.label_5.setText(_translate("K_Dialog", "Warning: This can take a few minutes.", None))

import ProjectManager_rc
