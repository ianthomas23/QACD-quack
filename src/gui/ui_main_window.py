# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui_main_window.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.tabWidget = QtWidgets.QTabWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabWidget.setObjectName("tabWidget")
        self.rawTab = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rawTab.sizePolicy().hasHeightForWidth())
        self.rawTab.setSizePolicy(sizePolicy)
        self.rawTab.setObjectName("rawTab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.rawTab)
        self.verticalLayout.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.rawTab)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.rawElementList = QtWidgets.QListWidget(self.rawTab)
        self.rawElementList.setObjectName("rawElementList")
        self.verticalLayout.addWidget(self.rawElementList)
        self.tabWidget.addTab(self.rawTab, "")
        self.filteredTab = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filteredTab.sizePolicy().hasHeightForWidth())
        self.filteredTab.setSizePolicy(sizePolicy)
        self.filteredTab.setObjectName("filteredTab")
        self.verticalLayout1 = QtWidgets.QVBoxLayout(self.filteredTab)
        self.verticalLayout1.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout1.setObjectName("verticalLayout1")
        self.label1 = QtWidgets.QLabel(self.filteredTab)
        self.label1.setObjectName("label1")
        self.verticalLayout1.addWidget(self.label1)
        self.filteredElementList = QtWidgets.QListWidget(self.filteredTab)
        self.filteredElementList.setObjectName("filteredElementList")
        self.verticalLayout1.addWidget(self.filteredElementList)
        self.tabWidget.addTab(self.filteredTab, "")
        self.normalisedTab = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.normalisedTab.sizePolicy().hasHeightForWidth())
        self.normalisedTab.setSizePolicy(sizePolicy)
        self.normalisedTab.setObjectName("normalisedTab")
        self.verticalLayout2 = QtWidgets.QVBoxLayout(self.normalisedTab)
        self.verticalLayout2.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout2.setObjectName("verticalLayout2")
        self.label2 = QtWidgets.QLabel(self.normalisedTab)
        self.label2.setObjectName("label2")
        self.verticalLayout2.addWidget(self.label2)
        self.normalisedElementList = QtWidgets.QListWidget(self.normalisedTab)
        self.normalisedElementList.setObjectName("normalisedElementList")
        self.verticalLayout2.addWidget(self.normalisedElementList)
        self.tabWidget.addTab(self.normalisedTab, "")
        self.ratioTab = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ratioTab.sizePolicy().hasHeightForWidth())
        self.ratioTab.setSizePolicy(sizePolicy)
        self.ratioTab.setObjectName("ratioTab")
        self.verticalLayout3 = QtWidgets.QVBoxLayout(self.ratioTab)
        self.verticalLayout3.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout3.setObjectName("verticalLayout3")
        self.ratioTable = QtWidgets.QTableWidget(self.ratioTab)
        self.ratioTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.ratioTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.ratioTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.ratioTable.setShowGrid(False)
        self.ratioTable.setGridStyle(QtCore.Qt.SolidLine)
        self.ratioTable.setColumnCount(3)
        self.ratioTable.setObjectName("ratioTable")
        self.ratioTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.ratioTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.ratioTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.ratioTable.setHorizontalHeaderItem(2, item)
        self.ratioTable.horizontalHeader().setHighlightSections(False)
        self.ratioTable.horizontalHeader().setSortIndicatorShown(True)
        self.ratioTable.horizontalHeader().setStretchLastSection(True)
        self.ratioTable.verticalHeader().setVisible(False)
        self.verticalLayout3.addWidget(self.ratioTable)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.newRatioButton = QtWidgets.QPushButton(self.ratioTab)
        self.newRatioButton.setObjectName("newRatioButton")
        self.horizontalLayout.addWidget(self.newRatioButton)
        self.deleteRatioButton = QtWidgets.QPushButton(self.ratioTab)
        self.deleteRatioButton.setObjectName("deleteRatioButton")
        self.horizontalLayout.addWidget(self.deleteRatioButton)
        self.dummyLabel2 = QtWidgets.QLabel(self.ratioTab)
        self.dummyLabel2.setText("")
        self.dummyLabel2.setObjectName("dummyLabel2")
        self.horizontalLayout.addWidget(self.dummyLabel2)
        self.verticalLayout3.addLayout(self.horizontalLayout)
        self.tabWidget.addTab(self.ratioTab, "")
        self.clusterTab = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clusterTab.sizePolicy().hasHeightForWidth())
        self.clusterTab.setSizePolicy(sizePolicy)
        self.clusterTab.setObjectName("clusterTab")
        self.verticalLayout4 = QtWidgets.QVBoxLayout(self.clusterTab)
        self.verticalLayout4.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout4.setObjectName("verticalLayout4")
        self.clusterTable = QtWidgets.QTableWidget(self.clusterTab)
        self.clusterTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.clusterTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.clusterTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.clusterTable.setShowGrid(False)
        self.clusterTable.setGridStyle(QtCore.Qt.SolidLine)
        self.clusterTable.setColumnCount(1)
        self.clusterTable.setObjectName("clusterTable")
        self.clusterTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.clusterTable.setHorizontalHeaderItem(0, item)
        self.clusterTable.horizontalHeader().setHighlightSections(False)
        self.clusterTable.horizontalHeader().setSortIndicatorShown(True)
        self.clusterTable.horizontalHeader().setStretchLastSection(True)
        self.clusterTable.verticalHeader().setVisible(False)
        self.verticalLayout4.addWidget(self.clusterTable)
        self.includedElementsLabel = QtWidgets.QLabel(self.clusterTab)
        self.includedElementsLabel.setWordWrap(True)
        self.includedElementsLabel.setObjectName("includedElementsLabel")
        self.verticalLayout4.addWidget(self.includedElementsLabel)
        self.tabWidget.addTab(self.clusterTab, "")
        self.phaseTab = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.phaseTab.sizePolicy().hasHeightForWidth())
        self.phaseTab.setSizePolicy(sizePolicy)
        self.phaseTab.setObjectName("phaseTab")
        self.verticalLayout5 = QtWidgets.QVBoxLayout(self.phaseTab)
        self.verticalLayout5.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout5.setObjectName("verticalLayout5")
        self.phaseTable = QtWidgets.QTableWidget(self.phaseTab)
        self.phaseTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.phaseTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.phaseTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.phaseTable.setShowGrid(False)
        self.phaseTable.setGridStyle(QtCore.Qt.SolidLine)
        self.phaseTable.setColumnCount(1)
        self.phaseTable.setObjectName("phaseTable")
        self.phaseTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.phaseTable.setHorizontalHeaderItem(0, item)
        self.phaseTable.horizontalHeader().setHighlightSections(False)
        self.phaseTable.horizontalHeader().setSortIndicatorShown(True)
        self.phaseTable.horizontalHeader().setStretchLastSection(True)
        self.phaseTable.verticalHeader().setVisible(False)
        self.verticalLayout5.addWidget(self.phaseTable)
        self.horizontalLayout1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout1.setObjectName("horizontalLayout1")
        self.newPhaseFilteredButton = QtWidgets.QPushButton(self.phaseTab)
        self.newPhaseFilteredButton.setObjectName("newPhaseFilteredButton")
        self.horizontalLayout1.addWidget(self.newPhaseFilteredButton)
        self.deletePhaseButton = QtWidgets.QPushButton(self.phaseTab)
        self.deletePhaseButton.setObjectName("deletePhaseButton")
        self.horizontalLayout1.addWidget(self.deletePhaseButton)
        self.dummyLabel3 = QtWidgets.QLabel(self.phaseTab)
        self.dummyLabel3.setText("")
        self.dummyLabel3.setObjectName("dummyLabel3")
        self.horizontalLayout1.addWidget(self.dummyLabel3)
        self.verticalLayout5.addLayout(self.horizontalLayout1)
        self.tabWidget.addTab(self.phaseTab, "")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.rightVerticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.rightVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.rightVerticalLayout.setObjectName("rightVerticalLayout")
        self.topRightHorizontalLayout = QtWidgets.QHBoxLayout()
        self.topRightHorizontalLayout.setObjectName("topRightHorizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.plotTypeLabel = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotTypeLabel.sizePolicy().hasHeightForWidth())
        self.plotTypeLabel.setSizePolicy(sizePolicy)
        self.plotTypeLabel.setObjectName("plotTypeLabel")
        self.gridLayout.addWidget(self.plotTypeLabel, 0, 0, 1, 1)
        self.phaseLabel = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.phaseLabel.sizePolicy().hasHeightForWidth())
        self.phaseLabel.setSizePolicy(sizePolicy)
        self.phaseLabel.setObjectName("phaseLabel")
        self.gridLayout.addWidget(self.phaseLabel, 0, 1, 1, 1)
        self.regionLabel = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.regionLabel.sizePolicy().hasHeightForWidth())
        self.regionLabel.setSizePolicy(sizePolicy)
        self.regionLabel.setObjectName("regionLabel")
        self.gridLayout.addWidget(self.regionLabel, 0, 2, 1, 1)
        self.zoomLabel = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zoomLabel.sizePolicy().hasHeightForWidth())
        self.zoomLabel.setSizePolicy(sizePolicy)
        self.zoomLabel.setObjectName("zoomLabel")
        self.gridLayout.addWidget(self.zoomLabel, 0, 3, 1, 1)
        self.plotTypeComboBox = QtWidgets.QComboBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotTypeComboBox.sizePolicy().hasHeightForWidth())
        self.plotTypeComboBox.setSizePolicy(sizePolicy)
        self.plotTypeComboBox.setObjectName("plotTypeComboBox")
        self.plotTypeComboBox.addItem("")
        self.plotTypeComboBox.addItem("")
        self.plotTypeComboBox.addItem("")
        self.gridLayout.addWidget(self.plotTypeComboBox, 1, 0, 1, 1)
        self.phaseComboBox = QtWidgets.QComboBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.phaseComboBox.sizePolicy().hasHeightForWidth())
        self.phaseComboBox.setSizePolicy(sizePolicy)
        self.phaseComboBox.setObjectName("phaseComboBox")
        self.gridLayout.addWidget(self.phaseComboBox, 1, 1, 1, 1)
        self.regionComboBox = QtWidgets.QComboBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.regionComboBox.sizePolicy().hasHeightForWidth())
        self.regionComboBox.setSizePolicy(sizePolicy)
        self.regionComboBox.setObjectName("regionComboBox")
        self.gridLayout.addWidget(self.regionComboBox, 1, 2, 1, 1)
        self.undoButton = QtWidgets.QToolButton(self.layoutWidget)
        self.undoButton.setObjectName("undoButton")
        self.gridLayout.addWidget(self.undoButton, 1, 3, 1, 1)
        self.redoButton = QtWidgets.QToolButton(self.layoutWidget)
        self.redoButton.setObjectName("redoButton")
        self.gridLayout.addWidget(self.redoButton, 1, 4, 1, 1)
        self.topRightHorizontalLayout.addLayout(self.gridLayout)
        self.dummyLabel = QtWidgets.QLabel(self.layoutWidget)
        self.dummyLabel.setText("")
        self.dummyLabel.setObjectName("dummyLabel")
        self.topRightHorizontalLayout.addWidget(self.dummyLabel)
        self.rightVerticalLayout.addLayout(self.topRightHorizontalLayout)
        self.matplotlibWidget = MatplotlibWidget(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.matplotlibWidget.sizePolicy().hasHeightForWidth())
        self.matplotlibWidget.setSizePolicy(sizePolicy)
        self.matplotlibWidget.setObjectName("matplotlibWidget")
        self.rightVerticalLayout.addWidget(self.matplotlibWidget)
        self.verticalLayout_2.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuProject = QtWidgets.QMenu(self.menubar)
        self.menuProject.setObjectName("menuProject")
        self.menuAction = QtWidgets.QMenu(self.menubar)
        self.menuAction.setObjectName("menuAction")
        self.menuOptions = QtWidgets.QMenu(self.menubar)
        self.menuOptions.setObjectName("menuOptions")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionProjectNew = QtWidgets.QAction(MainWindow)
        self.actionProjectNew.setObjectName("actionProjectNew")
        self.actionProjectOpen = QtWidgets.QAction(MainWindow)
        self.actionProjectOpen.setObjectName("actionProjectOpen")
        self.actionProjectClose = QtWidgets.QAction(MainWindow)
        self.actionProjectClose.setObjectName("actionProjectClose")
        self.actionFilter = QtWidgets.QAction(MainWindow)
        self.actionFilter.setObjectName("actionFilter")
        self.actionDisplayOptions = QtWidgets.QAction(MainWindow)
        self.actionDisplayOptions.setObjectName("actionDisplayOptions")
        self.actionClustering = QtWidgets.QAction(MainWindow)
        self.actionClustering.setObjectName("actionClustering")
        self.menuProject.addAction(self.actionProjectNew)
        self.menuProject.addAction(self.actionProjectOpen)
        self.menuProject.addAction(self.actionProjectClose)
        self.menuAction.addAction(self.actionFilter)
        self.menuAction.addAction(self.actionClustering)
        self.menuOptions.addAction(self.actionDisplayOptions)
        self.menubar.addAction(self.menuProject.menuAction())
        self.menubar.addAction(self.menuAction.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(5)
        self.plotTypeComboBox.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "QACD quack"))
        self.label.setText(_translate("MainWindow", "Elements"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.rawTab), _translate("MainWindow", "Raw"))
        self.label1.setText(_translate("MainWindow", "Elements"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.filteredTab), _translate("MainWindow", "Filtered"))
        self.label2.setText(_translate("MainWindow", "Elements"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.normalisedTab), _translate("MainWindow", "Normalised"))
        self.ratioTable.setSortingEnabled(True)
        item = self.ratioTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Name"))
        item = self.ratioTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Formula"))
        item = self.ratioTable.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Correction model"))
        self.newRatioButton.setText(_translate("MainWindow", "New Ratio"))
        self.deleteRatioButton.setText(_translate("MainWindow", "Delete Ratio"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ratioTab), _translate("MainWindow", "Ratios"))
        self.clusterTable.setSortingEnabled(True)
        item = self.clusterTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "k (number of phases)"))
        self.includedElementsLabel.setText(_translate("MainWindow", "Included elements:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.clusterTab), _translate("MainWindow", "Clusters"))
        self.phaseTable.setSortingEnabled(True)
        item = self.phaseTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Name"))
        self.newPhaseFilteredButton.setToolTip(_translate("MainWindow", "Create new phase map by thresholding filtered element maps"))
        self.newPhaseFilteredButton.setText(_translate("MainWindow", "New phase"))
        self.deletePhaseButton.setText(_translate("MainWindow", "Delete phase"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.phaseTab), _translate("MainWindow", "Phases"))
        self.plotTypeLabel.setText(_translate("MainWindow", "Plot type"))
        self.phaseLabel.setText(_translate("MainWindow", "Phase"))
        self.regionLabel.setText(_translate("MainWindow", "Region"))
        self.zoomLabel.setText(_translate("MainWindow", "Zoom"))
        self.plotTypeComboBox.setItemText(0, _translate("MainWindow", "Map"))
        self.plotTypeComboBox.setItemText(1, _translate("MainWindow", "Histogram"))
        self.plotTypeComboBox.setItemText(2, _translate("MainWindow", "Map and histogram"))
        self.undoButton.setText(_translate("MainWindow", "Undo"))
        self.redoButton.setText(_translate("MainWindow", "Redo"))
        self.menuProject.setTitle(_translate("MainWindow", "Project"))
        self.menuAction.setTitle(_translate("MainWindow", "Action"))
        self.menuOptions.setTitle(_translate("MainWindow", "Options"))
        self.actionProjectNew.setText(_translate("MainWindow", "New..."))
        self.actionProjectOpen.setText(_translate("MainWindow", "Open"))
        self.actionProjectClose.setText(_translate("MainWindow", "Close"))
        self.actionFilter.setText(_translate("MainWindow", "Filter and Normalise ..."))
        self.actionDisplayOptions.setText(_translate("MainWindow", "Display..."))
        self.actionClustering.setText(_translate("MainWindow", "k-means Clustering"))

from .matplotlib_widget import MatplotlibWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

