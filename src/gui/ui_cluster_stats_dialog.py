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
        self.tabWidget = QtWidgets.QTabWidget(ClusterStatsDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tableTab = QtWidgets.QWidget()
        self.tableTab.setObjectName("tableTab")
        self.tableLayout = QtWidgets.QVBoxLayout(self.tableTab)
        self.tableLayout.setContentsMargins(9, 9, 9, 9)
        self.tableLayout.setObjectName("tableLayout")
        self.label = QtWidgets.QLabel(self.tableTab)
        self.label.setObjectName("label")
        self.tableLayout.addWidget(self.label)
        self.table = QtWidgets.QTableWidget(self.tableTab)
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
        self.tabWidget.addTab(self.tableTab, "")
        self.plotTab = QtWidgets.QWidget()
        self.plotTab.setObjectName("plotTab")
        self.plotLayout = QtWidgets.QVBoxLayout(self.plotTab)
        self.plotLayout.setContentsMargins(9, 9, 9, 9)
        self.plotLayout.setObjectName("plotLayout")
        self.clusterStatsWidget = ClusterStatsWidget(self.plotTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.clusterStatsWidget.sizePolicy().hasHeightForWidth())
        self.clusterStatsWidget.setSizePolicy(sizePolicy)
        self.clusterStatsWidget.setObjectName("clusterStatsWidget")
        self.plotLayout.addWidget(self.clusterStatsWidget)
        self.tabWidget.addTab(self.plotTab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(ClusterStatsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ClusterStatsDialog)
        self.tabWidget.setCurrentIndex(1)
        self.buttonBox.accepted.connect(ClusterStatsDialog.accept)
        self.buttonBox.rejected.connect(ClusterStatsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ClusterStatsDialog)

    def retranslateUi(self, ClusterStatsDialog):
        _translate = QtCore.QCoreApplication.translate
        ClusterStatsDialog.setWindowTitle(_translate("ClusterStatsDialog", "Cluster Stats Dialog"))
        self.label.setText(_translate("ClusterStatsDialog", "Click on a column heading to sort on that column"))
        self.table.setSortingEnabled(True)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tableTab), _translate("ClusterStatsDialog", "Table"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.plotTab), _translate("ClusterStatsDialog", "Plot"))

from .cluster_stats_widget import ClusterStatsWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ClusterStatsDialog = QtWidgets.QDialog()
    ui = Ui_ClusterStatsDialog()
    ui.setupUi(ClusterStatsDialog)
    ClusterStatsDialog.show()
    sys.exit(app.exec_())

