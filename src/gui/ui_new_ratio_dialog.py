# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui_new_ratio_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NewRatioDialog(object):
    def setupUi(self, NewRatioDialog):
        NewRatioDialog.setObjectName("NewRatioDialog")
        NewRatioDialog.resize(278, 405)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(NewRatioDialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(NewRatioDialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.tabWidget = QtWidgets.QTabWidget(NewRatioDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.presetTab = QtWidgets.QWidget()
        self.presetTab.setObjectName("presetTab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.presetTab)
        self.verticalLayout.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_5 = QtWidgets.QLabel(self.presetTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.presetList = QtWidgets.QListWidget(self.presetTab)
        self.presetList.setObjectName("presetList")
        self.verticalLayout.addWidget(self.presetList)
        self.tabWidget.addTab(self.presetTab, "")
        self.customTab = QtWidgets.QWidget()
        self.customTab.setObjectName("customTab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.customTab)
        self.verticalLayout_2.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.customTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.customTypeCombo = QtWidgets.QComboBox(self.customTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.customTypeCombo.sizePolicy().hasHeightForWidth())
        self.customTypeCombo.setSizePolicy(sizePolicy)
        self.customTypeCombo.setObjectName("customTypeCombo")
        self.customTypeCombo.addItem("")
        self.customTypeCombo.addItem("")
        self.customTypeCombo.addItem("")
        self.verticalLayout_2.addWidget(self.customTypeCombo)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.labelA = QtWidgets.QLabel(self.customTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelA.sizePolicy().hasHeightForWidth())
        self.labelA.setSizePolicy(sizePolicy)
        self.labelA.setObjectName("labelA")
        self.gridLayout.addWidget(self.labelA, 0, 0, 1, 1)
        self.elementACombo = QtWidgets.QComboBox(self.customTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.elementACombo.sizePolicy().hasHeightForWidth())
        self.elementACombo.setSizePolicy(sizePolicy)
        self.elementACombo.setObjectName("elementACombo")
        self.gridLayout.addWidget(self.elementACombo, 0, 1, 1, 1)
        self.labelB = QtWidgets.QLabel(self.customTab)
        self.labelB.setObjectName("labelB")
        self.gridLayout.addWidget(self.labelB, 1, 0, 1, 1)
        self.elementBCombo = QtWidgets.QComboBox(self.customTab)
        self.elementBCombo.setObjectName("elementBCombo")
        self.gridLayout.addWidget(self.elementBCombo, 1, 1, 1, 1)
        self.labelC = QtWidgets.QLabel(self.customTab)
        self.labelC.setObjectName("labelC")
        self.gridLayout.addWidget(self.labelC, 2, 0, 1, 1)
        self.elementCCombo = QtWidgets.QComboBox(self.customTab)
        self.elementCCombo.setObjectName("elementCCombo")
        self.gridLayout.addWidget(self.elementCCombo, 2, 1, 1, 1)
        self.labelD = QtWidgets.QLabel(self.customTab)
        self.labelD.setObjectName("labelD")
        self.gridLayout.addWidget(self.labelD, 3, 0, 1, 1)
        self.elementDCombo = QtWidgets.QComboBox(self.customTab)
        self.elementDCombo.setObjectName("elementDCombo")
        self.gridLayout.addWidget(self.elementDCombo, 3, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.dummy = QtWidgets.QLabel(self.customTab)
        self.dummy.setText("")
        self.dummy.setObjectName("dummy")
        self.verticalLayout_2.addWidget(self.dummy)
        self.tabWidget.addTab(self.customTab, "")
        self.verticalLayout_3.addWidget(self.tabWidget)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(NewRatioDialog)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.formulaLabel = QtWidgets.QLabel(NewRatioDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.formulaLabel.sizePolicy().hasHeightForWidth())
        self.formulaLabel.setSizePolicy(sizePolicy)
        self.formulaLabel.setObjectName("formulaLabel")
        self.gridLayout_2.addWidget(self.formulaLabel, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(NewRatioDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.nameEdit = QtWidgets.QLineEdit(NewRatioDialog)
        self.nameEdit.setObjectName("nameEdit")
        self.gridLayout_2.addWidget(self.nameEdit, 1, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(NewRatioDialog)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 2, 0, 1, 1)
        self.correctionModelCombo = QtWidgets.QComboBox(NewRatioDialog)
        self.correctionModelCombo.setObjectName("correctionModelCombo")
        self.gridLayout_2.addWidget(self.correctionModelCombo, 2, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(NewRatioDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox)

        self.retranslateUi(NewRatioDialog)
        self.tabWidget.setCurrentIndex(1)
        self.buttonBox.accepted.connect(NewRatioDialog.accept)
        self.buttonBox.rejected.connect(NewRatioDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewRatioDialog)

    def retranslateUi(self, NewRatioDialog):
        _translate = QtCore.QCoreApplication.translate
        NewRatioDialog.setWindowTitle(_translate("NewRatioDialog", "New Element Ratio Map"))
        self.label_2.setText(_translate("NewRatioDialog", "Select a Preset or define a Custom ratio"))
        self.label_5.setText(_translate("NewRatioDialog", "Valid presets"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.presetTab), _translate("NewRatioDialog", "Preset"))
        self.label_4.setText(_translate("NewRatioDialog", "Custom type"))
        self.customTypeCombo.setItemText(0, _translate("NewRatioDialog", "Two elements: A / (A+B)"))
        self.customTypeCombo.setItemText(1, _translate("NewRatioDialog", "Three elements: A / (A+B+C)"))
        self.customTypeCombo.setItemText(2, _translate("NewRatioDialog", "Four elements: A / (A+B+C+D)"))
        self.labelA.setText(_translate("NewRatioDialog", "A"))
        self.labelB.setText(_translate("NewRatioDialog", "B"))
        self.labelC.setText(_translate("NewRatioDialog", "C"))
        self.labelD.setText(_translate("NewRatioDialog", "D"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.customTab), _translate("NewRatioDialog", "Custom"))
        self.label.setText(_translate("NewRatioDialog", "Formula"))
        self.formulaLabel.setText(_translate("NewRatioDialog", "TextLabel"))
        self.label_3.setText(_translate("NewRatioDialog", "Name"))
        self.label_6.setText(_translate("NewRatioDialog", "Correction model"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    NewRatioDialog = QtWidgets.QDialog()
    ui = Ui_NewRatioDialog()
    ui.setupUi(NewRatioDialog)
    NewRatioDialog.show()
    sys.exit(app.exec_())

