# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui_main_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(951, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources/application_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.topLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.topLayout.setObjectName("topLayout")
        self.splitter = QtWidgets.QSplitter(self.centralWidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.tabWidget = QtWidgets.QTabWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
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
        self.rawTable = QtWidgets.QTableWidget(self.rawTab)
        self.rawTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.rawTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.rawTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.rawTable.setShowGrid(False)
        self.rawTable.setGridStyle(QtCore.Qt.SolidLine)
        self.rawTable.setColumnCount(2)
        self.rawTable.setObjectName("rawTable")
        self.rawTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.rawTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.rawTable.setHorizontalHeaderItem(1, item)
        self.rawTable.horizontalHeader().setDefaultSectionSize(50)
        self.rawTable.horizontalHeader().setHighlightSections(False)
        self.rawTable.horizontalHeader().setSortIndicatorShown(True)
        self.rawTable.horizontalHeader().setStretchLastSection(True)
        self.rawTable.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.rawTable)
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
        self.filteredTable = QtWidgets.QTableWidget(self.filteredTab)
        self.filteredTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.filteredTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.filteredTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.filteredTable.setShowGrid(False)
        self.filteredTable.setGridStyle(QtCore.Qt.SolidLine)
        self.filteredTable.setColumnCount(2)
        self.filteredTable.setObjectName("filteredTable")
        self.filteredTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.filteredTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.filteredTable.setHorizontalHeaderItem(1, item)
        self.filteredTable.horizontalHeader().setDefaultSectionSize(50)
        self.filteredTable.horizontalHeader().setHighlightSections(False)
        self.filteredTable.horizontalHeader().setSortIndicatorShown(True)
        self.filteredTable.horizontalHeader().setStretchLastSection(True)
        self.filteredTable.verticalHeader().setVisible(False)
        self.verticalLayout1.addWidget(self.filteredTable)
        self.pixelTotalsCheckBox = QtWidgets.QCheckBox(self.filteredTab)
        self.pixelTotalsCheckBox.setObjectName("pixelTotalsCheckBox")
        self.verticalLayout1.addWidget(self.pixelTotalsCheckBox)
        self.medianFilterCheckBox = QtWidgets.QCheckBox(self.filteredTab)
        self.medianFilterCheckBox.setObjectName("medianFilterCheckBox")
        self.verticalLayout1.addWidget(self.medianFilterCheckBox)
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
        self.normalisedTable = QtWidgets.QTableWidget(self.normalisedTab)
        self.normalisedTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.normalisedTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.normalisedTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.normalisedTable.setShowGrid(False)
        self.normalisedTable.setGridStyle(QtCore.Qt.SolidLine)
        self.normalisedTable.setColumnCount(2)
        self.normalisedTable.setObjectName("normalisedTable")
        self.normalisedTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.normalisedTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.normalisedTable.setHorizontalHeaderItem(1, item)
        self.normalisedTable.horizontalHeader().setDefaultSectionSize(50)
        self.normalisedTable.horizontalHeader().setHighlightSections(False)
        self.normalisedTable.horizontalHeader().setSortIndicatorShown(True)
        self.normalisedTable.horizontalHeader().setStretchLastSection(True)
        self.normalisedTable.verticalHeader().setVisible(False)
        self.verticalLayout2.addWidget(self.normalisedTable)
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
        self.label = QtWidgets.QLabel(self.ratioTab)
        self.label.setObjectName("label")
        self.verticalLayout3.addWidget(self.label)
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
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.newPhaseClusterButton = QtWidgets.QPushButton(self.clusterTab)
        self.newPhaseClusterButton.setObjectName("newPhaseClusterButton")
        self.horizontalLayout_2.addWidget(self.newPhaseClusterButton)
        self.clusterStatsButton = QtWidgets.QPushButton(self.clusterTab)
        self.clusterStatsButton.setObjectName("clusterStatsButton")
        self.horizontalLayout_2.addWidget(self.clusterStatsButton)
        self.dummyLabel_2 = QtWidgets.QLabel(self.clusterTab)
        self.dummyLabel_2.setText("")
        self.dummyLabel_2.setObjectName("dummyLabel_2")
        self.horizontalLayout_2.addWidget(self.dummyLabel_2)
        self.verticalLayout4.addLayout(self.horizontalLayout_2)
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
        self.phaseTable.setColumnCount(3)
        self.phaseTable.setObjectName("phaseTable")
        self.phaseTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.phaseTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.phaseTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.phaseTable.setHorizontalHeaderItem(2, item)
        self.phaseTable.horizontalHeader().setHighlightSections(False)
        self.phaseTable.horizontalHeader().setSortIndicatorShown(True)
        self.phaseTable.horizontalHeader().setStretchLastSection(True)
        self.phaseTable.verticalHeader().setVisible(False)
        self.verticalLayout5.addWidget(self.phaseTable)
        self.label_2 = QtWidgets.QLabel(self.phaseTab)
        self.label_2.setObjectName("label_2")
        self.verticalLayout5.addWidget(self.label_2)
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
        self.regionTab = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.regionTab.sizePolicy().hasHeightForWidth())
        self.regionTab.setSizePolicy(sizePolicy)
        self.regionTab.setObjectName("regionTab")
        self.verticalLayout6 = QtWidgets.QVBoxLayout(self.regionTab)
        self.verticalLayout6.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout6.setObjectName("verticalLayout6")
        self.regionTable = QtWidgets.QTableWidget(self.regionTab)
        self.regionTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.regionTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.regionTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.regionTable.setShowGrid(False)
        self.regionTable.setGridStyle(QtCore.Qt.SolidLine)
        self.regionTable.setColumnCount(2)
        self.regionTable.setObjectName("regionTable")
        self.regionTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.regionTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.regionTable.setHorizontalHeaderItem(1, item)
        self.regionTable.horizontalHeader().setHighlightSections(False)
        self.regionTable.horizontalHeader().setSortIndicatorShown(True)
        self.regionTable.horizontalHeader().setStretchLastSection(True)
        self.regionTable.verticalHeader().setVisible(False)
        self.verticalLayout6.addWidget(self.regionTable)
        self.label_21 = QtWidgets.QLabel(self.regionTab)
        self.label_21.setObjectName("label_21")
        self.verticalLayout6.addWidget(self.label_21)
        self.horizontalLayout2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout2.setObjectName("horizontalLayout2")
        self.deleteRegionButton = QtWidgets.QPushButton(self.regionTab)
        self.deleteRegionButton.setObjectName("deleteRegionButton")
        self.horizontalLayout2.addWidget(self.deleteRegionButton)
        self.dummyLabel31 = QtWidgets.QLabel(self.regionTab)
        self.dummyLabel31.setText("")
        self.dummyLabel31.setObjectName("dummyLabel31")
        self.horizontalLayout2.addWidget(self.dummyLabel31)
        self.verticalLayout6.addLayout(self.horizontalLayout2)
        self.tabWidget.addTab(self.regionTab, "")
        self.rightVerticalLayoutWidget = QtWidgets.QWidget(self.splitter)
        self.rightVerticalLayoutWidget.setObjectName("rightVerticalLayoutWidget")
        self.rightVerticalLayout = QtWidgets.QVBoxLayout(self.rightVerticalLayoutWidget)
        self.rightVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.rightVerticalLayout.setObjectName("rightVerticalLayout")
        self.topRightHorizontalLayout = QtWidgets.QHBoxLayout()
        self.topRightHorizontalLayout.setObjectName("topRightHorizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.plotTypeLabel = QtWidgets.QLabel(self.rightVerticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotTypeLabel.sizePolicy().hasHeightForWidth())
        self.plotTypeLabel.setSizePolicy(sizePolicy)
        self.plotTypeLabel.setObjectName("plotTypeLabel")
        self.gridLayout.addWidget(self.plotTypeLabel, 0, 0, 1, 1)
        self.phaseLabel = QtWidgets.QLabel(self.rightVerticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.phaseLabel.sizePolicy().hasHeightForWidth())
        self.phaseLabel.setSizePolicy(sizePolicy)
        self.phaseLabel.setObjectName("phaseLabel")
        self.gridLayout.addWidget(self.phaseLabel, 0, 1, 1, 1)
        self.regionLabel = QtWidgets.QLabel(self.rightVerticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.regionLabel.sizePolicy().hasHeightForWidth())
        self.regionLabel.setSizePolicy(sizePolicy)
        self.regionLabel.setObjectName("regionLabel")
        self.gridLayout.addWidget(self.regionLabel, 0, 2, 1, 1)
        self.zoomLabel = QtWidgets.QLabel(self.rightVerticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zoomLabel.sizePolicy().hasHeightForWidth())
        self.zoomLabel.setSizePolicy(sizePolicy)
        self.zoomLabel.setObjectName("zoomLabel")
        self.gridLayout.addWidget(self.zoomLabel, 0, 3, 1, 1)
        self.plotTypeComboBox = QtWidgets.QComboBox(self.rightVerticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotTypeComboBox.sizePolicy().hasHeightForWidth())
        self.plotTypeComboBox.setSizePolicy(sizePolicy)
        self.plotTypeComboBox.setObjectName("plotTypeComboBox")
        self.plotTypeComboBox.addItem("")
        self.plotTypeComboBox.addItem("")
        self.plotTypeComboBox.addItem("")
        self.plotTypeComboBox.addItem("")
        self.gridLayout.addWidget(self.plotTypeComboBox, 1, 0, 1, 1)
        self.phaseComboBox = QtWidgets.QComboBox(self.rightVerticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.phaseComboBox.sizePolicy().hasHeightForWidth())
        self.phaseComboBox.setSizePolicy(sizePolicy)
        self.phaseComboBox.setObjectName("phaseComboBox")
        self.gridLayout.addWidget(self.phaseComboBox, 1, 1, 1, 1)
        self.regionComboBox = QtWidgets.QComboBox(self.rightVerticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.regionComboBox.sizePolicy().hasHeightForWidth())
        self.regionComboBox.setSizePolicy(sizePolicy)
        self.regionComboBox.setObjectName("regionComboBox")
        self.gridLayout.addWidget(self.regionComboBox, 1, 2, 1, 1)
        self.undoButton = QtWidgets.QToolButton(self.rightVerticalLayoutWidget)
        self.undoButton.setObjectName("undoButton")
        self.gridLayout.addWidget(self.undoButton, 1, 3, 1, 1)
        self.redoButton = QtWidgets.QToolButton(self.rightVerticalLayoutWidget)
        self.redoButton.setObjectName("redoButton")
        self.gridLayout.addWidget(self.redoButton, 1, 4, 1, 1)
        self.topRightHorizontalLayout.addLayout(self.gridLayout)
        self.dummyLabel = QtWidgets.QLabel(self.rightVerticalLayoutWidget)
        self.dummyLabel.setText("")
        self.dummyLabel.setObjectName("dummyLabel")
        self.topRightHorizontalLayout.addWidget(self.dummyLabel)
        self.topRightHorizontalLayout.setStretch(1, 1)
        self.rightVerticalLayout.addLayout(self.topRightHorizontalLayout)
        self.matplotlibWidget = MatplotlibWidget(self.rightVerticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.matplotlibWidget.sizePolicy().hasHeightForWidth())
        self.matplotlibWidget.setSizePolicy(sizePolicy)
        self.matplotlibWidget.setObjectName("matplotlibWidget")
        self.rightVerticalLayout.addWidget(self.matplotlibWidget)
        self.topLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 951, 22))
        self.menubar.setNativeMenuBar(False)
        self.menubar.setObjectName("menubar")
        self.menuProject = QtWidgets.QMenu(self.menubar)
        self.menuProject.setObjectName("menuProject")
        self.menuAction = QtWidgets.QMenu(self.menubar)
        self.menuAction.setObjectName("menuAction")
        self.menuExportPixels = QtWidgets.QMenu(self.menuAction)
        self.menuExportPixels.setObjectName("menuExportPixels")
        self.menuOptions = QtWidgets.QMenu(self.menubar)
        self.menuOptions.setObjectName("menuOptions")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
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
        self.actionModeZoom = QtWidgets.QAction(MainWindow)
        self.actionModeZoom.setCheckable(True)
        self.actionModeZoom.setObjectName("actionModeZoom")
        self.actionModeRegionRectangle = QtWidgets.QAction(MainWindow)
        self.actionModeRegionRectangle.setCheckable(True)
        self.actionModeRegionRectangle.setObjectName("actionModeRegionRectangle")
        self.actionModeRegionEllipse = QtWidgets.QAction(MainWindow)
        self.actionModeRegionEllipse.setCheckable(True)
        self.actionModeRegionEllipse.setObjectName("actionModeRegionEllipse")
        self.actionModeRegionPolygon = QtWidgets.QAction(MainWindow)
        self.actionModeRegionPolygon.setCheckable(True)
        self.actionModeRegionPolygon.setObjectName("actionModeRegionPolygon")
        self.actionNewRegion = QtWidgets.QAction(MainWindow)
        self.actionNewRegion.setObjectName("actionNewRegion")
        self.actionExportImage = QtWidgets.QAction(MainWindow)
        self.actionExportImage.setObjectName("actionExportImage")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionExportHistogram = QtWidgets.QAction(MainWindow)
        self.actionExportHistogram.setObjectName("actionExportHistogram")
        self.actionExportTransect = QtWidgets.QAction(MainWindow)
        self.actionExportTransect.setObjectName("actionExportTransect")
        self.actionExportPixelsDisplayedElement = QtWidgets.QAction(MainWindow)
        self.actionExportPixelsDisplayedElement.setObjectName("actionExportPixelsDisplayedElement")
        self.actionExportPixelsAllElements = QtWidgets.QAction(MainWindow)
        self.actionExportPixelsAllElements.setObjectName("actionExportPixelsAllElements")
        self.menuProject.addAction(self.actionProjectNew)
        self.menuProject.addAction(self.actionProjectOpen)
        self.menuProject.addAction(self.actionProjectClose)
        self.menuExportPixels.addAction(self.actionExportPixelsDisplayedElement)
        self.menuExportPixels.addAction(self.actionExportPixelsAllElements)
        self.menuAction.addAction(self.actionFilter)
        self.menuAction.addAction(self.actionClustering)
        self.menuAction.addAction(self.actionNewRegion)
        self.menuAction.addAction(self.actionExportImage)
        self.menuAction.addAction(self.menuExportPixels.menuAction())
        self.menuAction.addAction(self.actionExportHistogram)
        self.menuAction.addAction(self.actionExportTransect)
        self.menuOptions.addAction(self.actionDisplayOptions)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuProject.menuAction())
        self.menubar.addAction(self.menuAction.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(6)
        self.plotTypeComboBox.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "QACD-quack"))
        self.rawTable.setSortingEnabled(True)
        item = self.rawTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Element"))
        item = self.rawTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Name"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.rawTab), _translate("MainWindow", "Raw"))
        self.filteredTable.setSortingEnabled(True)
        item = self.filteredTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Element"))
        item = self.filteredTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Name"))
        self.pixelTotalsCheckBox.setText(_translate("MainWindow", "Clip pixel totals"))
        self.medianFilterCheckBox.setText(_translate("MainWindow", "3-by-3 median filter"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.filteredTab), _translate("MainWindow", "Filtered"))
        self.normalisedTable.setSortingEnabled(True)
        item = self.normalisedTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Element"))
        item = self.normalisedTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Name"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.normalisedTab), _translate("MainWindow", "Normalised"))
        self.ratioTable.setSortingEnabled(True)
        item = self.ratioTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Name"))
        item = self.ratioTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Formula"))
        item = self.ratioTable.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Correction model"))
        self.label.setText(_translate("MainWindow", "Double-click on a name to change it."))
        self.newRatioButton.setToolTip(_translate("MainWindow", "Create a new ratio map"))
        self.newRatioButton.setText(_translate("MainWindow", "New ratio"))
        self.deleteRatioButton.setToolTip(_translate("MainWindow", "Delete the selected ratio map"))
        self.deleteRatioButton.setText(_translate("MainWindow", "Delete ratio"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ratioTab), _translate("MainWindow", "Ratios"))
        self.clusterTable.setSortingEnabled(True)
        item = self.clusterTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "k (number of phases)"))
        self.includedElementsLabel.setText(_translate("MainWindow", "Included elements:"))
        self.newPhaseClusterButton.setToolTip(_translate("MainWindow", "Create new phase map(s) from selected cluster map"))
        self.newPhaseClusterButton.setText(_translate("MainWindow", "New phase(s)"))
        self.clusterStatsButton.setToolTip(_translate("MainWindow", "Show stats of selected k cluster"))
        self.clusterStatsButton.setText(_translate("MainWindow", "Show stats"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.clusterTab), _translate("MainWindow", "Clusters"))
        self.phaseTable.setSortingEnabled(True)
        item = self.phaseTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Name"))
        item = self.phaseTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Source"))
        item = self.phaseTable.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Details"))
        self.label_2.setText(_translate("MainWindow", "Double-click on a name to change it."))
        self.newPhaseFilteredButton.setToolTip(_translate("MainWindow", "Create new phase map by thresholding filtered element maps"))
        self.newPhaseFilteredButton.setText(_translate("MainWindow", "New phase"))
        self.deletePhaseButton.setToolTip(_translate("MainWindow", "Delete the selected phase map"))
        self.deletePhaseButton.setText(_translate("MainWindow", "Delete phase"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.phaseTab), _translate("MainWindow", "Phases"))
        self.regionTable.setSortingEnabled(True)
        item = self.regionTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Name"))
        item = self.regionTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Shape"))
        self.label_21.setText(_translate("MainWindow", "Double-click on a name to change it."))
        self.deleteRegionButton.setToolTip(_translate("MainWindow", "Delete the selected region"))
        self.deleteRegionButton.setText(_translate("MainWindow", "Delete region"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.regionTab), _translate("MainWindow", "Regions"))
        self.plotTypeLabel.setText(_translate("MainWindow", "Plot type"))
        self.phaseLabel.setText(_translate("MainWindow", "Phase"))
        self.regionLabel.setText(_translate("MainWindow", "Region"))
        self.zoomLabel.setText(_translate("MainWindow", "Zoom"))
        self.plotTypeComboBox.setToolTip(_translate("MainWindow", "Type of plot displayed below"))
        self.plotTypeComboBox.setCurrentText(_translate("MainWindow", "Map and histogram"))
        self.plotTypeComboBox.setItemText(0, _translate("MainWindow", "Map"))
        self.plotTypeComboBox.setItemText(1, _translate("MainWindow", "Histogram"))
        self.plotTypeComboBox.setItemText(2, _translate("MainWindow", "Map and histogram"))
        self.plotTypeComboBox.setItemText(3, _translate("MainWindow", "Map and transect"))
        self.phaseComboBox.setToolTip(_translate("MainWindow", "Phase map used in plot below"))
        self.regionComboBox.setToolTip(_translate("MainWindow", "Region used in plot below"))
        self.undoButton.setToolTip(_translate("MainWindow", "Undo previous zoom"))
        self.undoButton.setText(_translate("MainWindow", "Undo"))
        self.redoButton.setToolTip(_translate("MainWindow", "Redo next zoom"))
        self.redoButton.setText(_translate("MainWindow", "Redo"))
        self.menuProject.setTitle(_translate("MainWindow", "Project"))
        self.menuAction.setTitle(_translate("MainWindow", "Action"))
        self.menuExportPixels.setTitle(_translate("MainWindow", "Export Pixels to File"))
        self.menuOptions.setTitle(_translate("MainWindow", "Options"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionProjectNew.setText(_translate("MainWindow", "New..."))
        self.actionProjectNew.setToolTip(_translate("MainWindow", "Create a new project"))
        self.actionProjectOpen.setText(_translate("MainWindow", "Open"))
        self.actionProjectOpen.setToolTip(_translate("MainWindow", "Open an existing project"))
        self.actionProjectClose.setText(_translate("MainWindow", "Close"))
        self.actionProjectClose.setToolTip(_translate("MainWindow", "Close the current project"))
        self.actionFilter.setText(_translate("MainWindow", "Filter and Normalise ..."))
        self.actionFilter.setToolTip(_translate("MainWindow", "Filter and normalise the raw element maps"))
        self.actionDisplayOptions.setText(_translate("MainWindow", "Display..."))
        self.actionDisplayOptions.setToolTip(_translate("MainWindow", "Change display options"))
        self.actionClustering.setText(_translate("MainWindow", "k-means Clustering"))
        self.actionClustering.setToolTip(_translate("MainWindow", "Perform k-means clustering on the filtered element maps"))
        self.actionModeZoom.setText(_translate("MainWindow", "Zoom"))
        self.actionModeRegionRectangle.setText(_translate("MainWindow", "Rectangle Region"))
        self.actionModeRegionEllipse.setText(_translate("MainWindow", "Ellipse Region"))
        self.actionModeRegionPolygon.setText(_translate("MainWindow", "Polygon Region"))
        self.actionNewRegion.setText(_translate("MainWindow", "New Region ..."))
        self.actionNewRegion.setToolTip(_translate("MainWindow", "Create a new region"))
        self.actionExportImage.setText(_translate("MainWindow", "Export Image to File ..."))
        self.actionExportImage.setToolTip(_translate("MainWindow", "Export image to file"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setToolTip(_translate("MainWindow", "About QACD-quack"))
        self.actionExportHistogram.setText(_translate("MainWindow", "Export Histogram to File ..."))
        self.actionExportTransect.setText(_translate("MainWindow", "Export Transect to File ..."))
        self.actionExportPixelsDisplayedElement.setText(_translate("MainWindow", "Displayed Element only ..."))
        self.actionExportPixelsAllElements.setText(_translate("MainWindow", "All Elements ..."))

from .matplotlib_widget import MatplotlibWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

