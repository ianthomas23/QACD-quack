# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui_display_options_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DisplayOptionsDialog(object):
    def setupUi(self, DisplayOptionsDialog):
        DisplayOptionsDialog.setObjectName("DisplayOptionsDialog")
        DisplayOptionsDialog.resize(425, 477)
        self.verticalLayout = QtWidgets.QVBoxLayout(DisplayOptionsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(DisplayOptionsDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.colourmapTab = QtWidgets.QWidget()
        self.colourmapTab.setObjectName("colourmapTab")
        self.verticalLayout1 = QtWidgets.QVBoxLayout(self.colourmapTab)
        self.verticalLayout1.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout1.setObjectName("verticalLayout1")
        self.colourmapListWidget = QtWidgets.QListWidget(self.colourmapTab)
        self.colourmapListWidget.setObjectName("colourmapListWidget")
        self.verticalLayout1.addWidget(self.colourmapListWidget)
        self.reverseCheckBox = QtWidgets.QCheckBox(self.colourmapTab)
        self.reverseCheckBox.setObjectName("reverseCheckBox")
        self.verticalLayout1.addWidget(self.reverseCheckBox)
        self.tabWidget.addTab(self.colourmapTab, "")
        self.scaleTab = QtWidgets.QWidget()
        self.scaleTab.setObjectName("scaleTab")
        self.useScaleCheckBox = QtWidgets.QCheckBox(self.scaleTab)
        self.useScaleCheckBox.setGeometry(QtCore.QRect(40, 50, 211, 23))
        self.useScaleCheckBox.setObjectName("useScaleCheckBox")
        self.pixelSizeLabel = QtWidgets.QLabel(self.scaleTab)
        self.pixelSizeLabel.setGeometry(QtCore.QRect(40, 110, 64, 17))
        self.pixelSizeLabel.setObjectName("pixelSizeLabel")
        self.unitsComboBox = QtWidgets.QComboBox(self.scaleTab)
        self.unitsComboBox.setGeometry(QtCore.QRect(250, 100, 86, 25))
        self.unitsComboBox.setObjectName("unitsComboBox")
        self.showScaleBarCheckBox = QtWidgets.QCheckBox(self.scaleTab)
        self.showScaleBarCheckBox.setGeometry(QtCore.QRect(30, 180, 181, 23))
        self.showScaleBarCheckBox.setObjectName("showScaleBarCheckBox")
        self.pixelSizeLineEdit = QtWidgets.QLineEdit(self.scaleTab)
        self.pixelSizeLineEdit.setGeometry(QtCore.QRect(120, 100, 113, 25))
        self.pixelSizeLineEdit.setObjectName("pixelSizeLineEdit")
        self.tabWidget.addTab(self.scaleTab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(DisplayOptionsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DisplayOptionsDialog)
        self.tabWidget.setCurrentIndex(1)
        self.buttonBox.accepted.connect(DisplayOptionsDialog.accept)
        self.buttonBox.rejected.connect(DisplayOptionsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(DisplayOptionsDialog)

    def retranslateUi(self, DisplayOptionsDialog):
        _translate = QtCore.QCoreApplication.translate
        DisplayOptionsDialog.setWindowTitle(_translate("DisplayOptionsDialog", "Display Options"))
        self.reverseCheckBox.setText(_translate("DisplayOptionsDialog", "Reverse"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.colourmapTab), _translate("DisplayOptionsDialog", "Colourmap"))
        self.useScaleCheckBox.setText(_translate("DisplayOptionsDialog", "Use physical scale"))
        self.pixelSizeLabel.setText(_translate("DisplayOptionsDialog", "Pixel size"))
        self.showScaleBarCheckBox.setText(_translate("DisplayOptionsDialog", "Show scale bar"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.scaleTab), _translate("DisplayOptionsDialog", "Scale"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DisplayOptionsDialog = QtWidgets.QDialog()
    ui = Ui_DisplayOptionsDialog()
    ui.setupUi(DisplayOptionsDialog)
    DisplayOptionsDialog.show()
    sys.exit(app.exec_())

