# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui_cluster_stats_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ClusterStatsDialog(object):
    def setupUi(self, ClusterStatsDialog):
        ClusterStatsDialog.setObjectName("ClusterStatsDialog")
        ClusterStatsDialog.resize(977, 693)
        self.verticalLayout = QtWidgets.QVBoxLayout(ClusterStatsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableTab = QtWidgets.QTabWidget(ClusterStatsDialog)
        self.tableTab.setObjectName("tableTab")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tableLayout = QtWidgets.QVBoxLayout(self.tab)
        self.tableLayout.setContentsMargins(9, 9, 9, 9)
        self.tableLayout.setObjectName("tableLayout")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setObjectName("label")
        self.tableLayout.addWidget(self.label)
        self.table = QtWidgets.QTableWidget(self.tab)
        self.table.setStyleSheet("")
        self.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.verticalHeader().setVisible(False)
        self.tableLayout.addWidget(self.table)
        self.tableTab.addTab(self.tab, "")
        self.otherTab = QtWidgets.QWidget()
        self.otherTab.setObjectName("otherTab")
        self.tableTab.addTab(self.otherTab, "")
        self.verticalLayout.addWidget(self.tableTab)
        self.buttonBox = QtWidgets.QDialogButtonBox(ClusterStatsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ClusterStatsDialog)
        self.buttonBox.accepted.connect(ClusterStatsDialog.accept)
        self.buttonBox.rejected.connect(ClusterStatsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ClusterStatsDialog)

    def retranslateUi(self, ClusterStatsDialog):
        _translate = QtCore.QCoreApplication.translate
        ClusterStatsDialog.setWindowTitle(_translate("ClusterStatsDialog", "Cluster Stats Dialog"))
        self.label.setText(_translate("ClusterStatsDialog", "Click on a column heading to sort on that column"))
        self.table.setSortingEnabled(True)
        self.tableTab.setTabText(self.tableTab.indexOf(self.tab), _translate("ClusterStatsDialog", "Table"))
        self.tableTab.setTabText(self.tableTab.indexOf(self.otherTab), _translate("ClusterStatsDialog", "Other"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ClusterStatsDialog = QtWidgets.QDialog()
    ui = Ui_ClusterStatsDialog()
    ui.setupUi(ClusterStatsDialog)
    ClusterStatsDialog.show()
    sys.exit(app.exec_())

