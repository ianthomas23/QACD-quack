# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui_progress_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ProgressDialog(object):
    def setupUi(self, ProgressDialog):
        ProgressDialog.setObjectName("ProgressDialog")
        ProgressDialog.setWindowModality(QtCore.Qt.NonModal)
        ProgressDialog.resize(498, 52)
        self.verticalLayout = QtWidgets.QVBoxLayout(ProgressDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(ProgressDialog)
        self.label.setText("")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.progress = QtWidgets.QProgressBar(ProgressDialog)
        self.progress.setProperty("value", 0)
        self.progress.setObjectName("progress")
        self.verticalLayout.addWidget(self.progress)

        self.retranslateUi(ProgressDialog)
        QtCore.QMetaObject.connectSlotsByName(ProgressDialog)

    def retranslateUi(self, ProgressDialog):
        _translate = QtCore.QCoreApplication.translate
        ProgressDialog.setWindowTitle(_translate("ProgressDialog", "ProgressDialog"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ProgressDialog = QtWidgets.QDialog()
    ui = Ui_ProgressDialog()
    ui.setupUi(ProgressDialog)
    ProgressDialog.show()
    sys.exit(app.exec_())

