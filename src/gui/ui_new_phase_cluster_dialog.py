# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui_new_phase_cluster_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NewPhaseClusterDialog(object):
    def setupUi(self, NewPhaseClusterDialog):
        NewPhaseClusterDialog.setObjectName("NewPhaseClusterDialog")
        NewPhaseClusterDialog.resize(703, 815)
        self.buttonBox = QtWidgets.QDialogButtonBox(NewPhaseClusterDialog)
        self.buttonBox.setGeometry(QtCore.QRect(220, 780, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.matplotlibWidget = MatplotlibWidget(NewPhaseClusterDialog)
        self.matplotlibWidget.setGeometry(QtCore.QRect(59, 29, 591, 451))
        self.matplotlibWidget.setObjectName("matplotlibWidget")
        self.tableWidget = QtWidgets.QTableWidget(NewPhaseClusterDialog)
        self.tableWidget.setGeometry(QtCore.QRect(50, 490, 511, 211))
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.tableWidget.horizontalHeader().setHighlightSections(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.clearButton = QtWidgets.QPushButton(NewPhaseClusterDialog)
        self.clearButton.setGeometry(QtCore.QRect(40, 730, 121, 25))
        self.clearButton.setObjectName("clearButton")
        self.deleteButton = QtWidgets.QPushButton(NewPhaseClusterDialog)
        self.deleteButton.setGeometry(QtCore.QRect(210, 730, 191, 25))
        self.deleteButton.setObjectName("deleteButton")
        self.mergeButton = QtWidgets.QPushButton(NewPhaseClusterDialog)
        self.mergeButton.setGeometry(QtCore.QRect(450, 730, 191, 25))
        self.mergeButton.setObjectName("mergeButton")

        self.retranslateUi(NewPhaseClusterDialog)
        self.buttonBox.accepted.connect(NewPhaseClusterDialog.accept)
        self.buttonBox.rejected.connect(NewPhaseClusterDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewPhaseClusterDialog)

    def retranslateUi(self, NewPhaseClusterDialog):
        _translate = QtCore.QCoreApplication.translate
        NewPhaseClusterDialog.setWindowTitle(_translate("NewPhaseClusterDialog", "New phase maps from cluster map"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("NewPhaseClusterDialog", "Phase name"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("NewPhaseClusterDialog", "Value"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("NewPhaseClusterDialog", "Colour"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("NewPhaseClusterDialog", "Pixels"))
        self.clearButton.setText(_translate("NewPhaseClusterDialog", "Clear selections"))
        self.deleteButton.setText(_translate("NewPhaseClusterDialog", "Delete selected phases"))
        self.mergeButton.setText(_translate("NewPhaseClusterDialog", "Merge selected phases"))

from .matplotlib_widget import MatplotlibWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    NewPhaseClusterDialog = QtWidgets.QDialog()
    ui = Ui_NewPhaseClusterDialog()
    ui.setupUi(NewPhaseClusterDialog)
    NewPhaseClusterDialog.show()
    sys.exit(app.exec_())

