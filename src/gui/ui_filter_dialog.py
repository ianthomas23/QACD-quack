# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui_filter_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FilterDialog(object):
    def setupUi(self, FilterDialog):
        FilterDialog.setObjectName("FilterDialog")
        FilterDialog.resize(184, 82)
        self.formLayout = QtWidgets.QFormLayout(FilterDialog)
        self.formLayout.setObjectName("formLayout")
        self.pixelTotalsCheckBox = QtWidgets.QCheckBox(FilterDialog)
        self.pixelTotalsCheckBox.setChecked(True)
        self.pixelTotalsCheckBox.setObjectName("pixelTotalsCheckBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.pixelTotalsCheckBox)
        self.medianFilterCheckBox = QtWidgets.QCheckBox(FilterDialog)
        self.medianFilterCheckBox.setChecked(True)
        self.medianFilterCheckBox.setObjectName("medianFilterCheckBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.medianFilterCheckBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(FilterDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.buttonBox)

        self.retranslateUi(FilterDialog)
        self.buttonBox.accepted.connect(FilterDialog.accept)
        self.buttonBox.rejected.connect(FilterDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(FilterDialog)

    def retranslateUi(self, FilterDialog):
        _translate = QtCore.QCoreApplication.translate
        FilterDialog.setWindowTitle(_translate("FilterDialog", "Filter Options"))
        self.pixelTotalsCheckBox.setText(_translate("FilterDialog", "Clip pixel totals"))
        self.medianFilterCheckBox.setText(_translate("FilterDialog", "3-by-3 median filter"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FilterDialog = QtWidgets.QDialog()
    ui = Ui_FilterDialog()
    ui.setupUi(FilterDialog)
    FilterDialog.show()
    sys.exit(app.exec_())

