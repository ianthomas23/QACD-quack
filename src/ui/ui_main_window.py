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
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.tabWidget = QtWidgets.QTabWidget(self.splitter)
        self.tabWidget.setObjectName("tabWidget")
        self.rawTab = QtWidgets.QWidget()
        self.rawTab.setObjectName("rawTab")
        self.tabWidget.addTab(self.rawTab, "")
        self.filteredTab = QtWidgets.QWidget()
        self.filteredTab.setObjectName("filteredTab")
        self.tabWidget.addTab(self.filteredTab, "")
        self.normalisedTab = QtWidgets.QWidget()
        self.normalisedTab.setObjectName("normalisedTab")
        self.tabWidget.addTab(self.normalisedTab, "")
        self.widget = QtWidgets.QWidget(self.splitter)
        self.widget.setObjectName("widget")
        self.horizontalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuProject = QtWidgets.QMenu(self.menubar)
        self.menuProject.setObjectName("menuProject")
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
        self.menuProject.addAction(self.actionProjectNew)
        self.menuProject.addAction(self.actionProjectOpen)
        self.menuProject.addAction(self.actionProjectClose)
        self.menubar.addAction(self.menuProject.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.rawTab), _translate("MainWindow", "Raw"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.filteredTab), _translate("MainWindow", "Filtered"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.normalisedTab), _translate("MainWindow", "Normalised"))
        self.menuProject.setTitle(_translate("MainWindow", "Project"))
        self.actionProjectNew.setText(_translate("MainWindow", "New"))
        self.actionProjectOpen.setText(_translate("MainWindow", "Open"))
        self.actionProjectClose.setText(_translate("MainWindow", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

