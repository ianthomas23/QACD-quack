# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui_display_options_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DisplayOptionsDialog(object):
    def setupUi(self, DisplayOptionsDialog):
        DisplayOptionsDialog.setObjectName("DisplayOptionsDialog")
        DisplayOptionsDialog.resize(390, 477)
        self.verticalLayout = QtWidgets.QVBoxLayout(DisplayOptionsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(DisplayOptionsDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.listWidget = QtWidgets.QListWidget(DisplayOptionsDialog)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.reverseCheckBox = QtWidgets.QCheckBox(DisplayOptionsDialog)
        self.reverseCheckBox.setObjectName("reverseCheckBox")
        self.verticalLayout.addWidget(self.reverseCheckBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(DisplayOptionsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DisplayOptionsDialog)
        self.buttonBox.accepted.connect(DisplayOptionsDialog.accept)
        self.buttonBox.rejected.connect(DisplayOptionsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(DisplayOptionsDialog)

    def retranslateUi(self, DisplayOptionsDialog):
        _translate = QtCore.QCoreApplication.translate
        DisplayOptionsDialog.setWindowTitle(_translate("DisplayOptionsDialog", "Display Options"))
        self.label.setText(_translate("DisplayOptionsDialog", "Colormap"))
        self.reverseCheckBox.setText(_translate("DisplayOptionsDialog", "Reverse"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DisplayOptionsDialog = QtWidgets.QDialog()
    ui = Ui_DisplayOptionsDialog()
    ui.setupUi(DisplayOptionsDialog)
    DisplayOptionsDialog.show()
    sys.exit(app.exec_())

