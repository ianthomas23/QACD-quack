# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created: Tue Jan 19 18:03:31 2016
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import HDF5TreeViewModel as htv
import tables as tb
import os
import gc
import sys
import logging
import psutil

gc.set_threshold(10, 5, 5)


class QtHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
    def emit(self, record):
        record = self.format(record)
        if record: XStream.stdout().write('%s\n'%record)
        # originally: XStream.stdout().write("{}\n".format(record))

logger = logging.getLogger(__name__)
handler = QtHandler()
handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

class XStream(QtCore.QObject):
    _stdout = None
    _stderr = None
    messageWritten = QtCore.pyqtSignal(str)
    def flush( self ):
        pass
    def fileno( self ):
        return -1
    def write( self, msg ):
        if ( not self.signalsBlocked() ):
            self.messageWritten.emit(unicode(msg))
    @staticmethod
    def stdout():
        if ( not XStream._stdout ):
            XStream._stdout = XStream()
            sys.stdout = XStream._stdout
        return XStream._stdout
    @staticmethod
    def stderr():
        if ( not XStream._stderr ):
            XStream._stderr = XStream()
            sys.stderr = XStream._stderr
        return XStream._stderr

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.treeSelect = ''
        self.cluster = 1
        self.dirName = ''
        self.log = []
        self.logDict = {}
        self.rowtitles = ['Last Opened','Created','Data Imported','Filtered','Pixel Size',
                          'Map Width','Map Height','Map Area','Pixels (N)','Phase Masks',
                          'Phases Thresh.','Phases Clust.','Total Phases','Ratio Maps',
                          'Last Ratio Map','Last Map Plot','Last Hist Plot']

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(371, 960)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/main_icon/16x16.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.setWindowTitle("QACD-Project Manager")

        self.pushButton_ProStats = QtGui.QPushButton("Phase Maps and Statistics", self.centralwidget)
        self.pushButton_ProStats.setGeometry(QtCore.QRect(10, 655, 349, 31))
        self.pushButton_ProStats.clicked.connect(self.Proj_Stats)
        self.pushButton_ProStats.setStatusTip('Statistics for the project')

        self.Proj_tableWidget = QtGui.QTableWidget(self.centralwidget)
        self.Proj_tableWidget.setGeometry(QtCore.QRect(10, 495, 349, 151))
        self.Proj_tableWidget.setStatusTip('Info regarding the project')
        self.table_initialise()

        self.label_Output = QtGui.QLabel("Program Output and Errors:", self.centralwidget)
        self.label_Output.setGeometry(QtCore.QRect(10, 695, 349, 16))

        self._console = QtGui.QTextBrowser(self.centralwidget)
        self._console.setGeometry(QtCore.QRect(10, 715, 349, 181))
        self._console.setReadOnly(True)
        self._console.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self._console.ensureCursorVisible()
        self._console.textChanged.connect(self.cons_scroll)

        #XStream.stdout().messageWritten.connect( self._console.insertPlainText )
        #XStream.stderr().messageWritten.connect( self._console.insertPlainText )

        self.label3_ProjDesc = QtGui.QLabel("Project Info and Log:", self.centralwidget)
        self.label3_ProjDesc.setGeometry(QtCore.QRect(10, 475, 349, 16))

        self.Dir_treeView = QtGui.QTreeView(self.centralwidget)
        self.Dir_treeView.setGeometry(QtCore.QRect(10, 30, 349, 151))
        self.Dir_treeView.setStatusTip('Contents of the working directory')
        self.Dir_treeView.clicked.connect(self.on_treeView_clicked)
        self.Dir_model = QtGui.QFileSystemModel()

        self.label2_ProjTree = QtGui.QLabel("Project Tree:", self.centralwidget)
        self.label2_ProjTree.setGeometry(QtCore.QRect(10, 330, 349, 16))

        self.label1_WD = QtGui.QLabel("Working Directory:",self.centralwidget)
        self.label1_WD.setGeometry(QtCore.QRect(10, 10, 349, 16))

        self.pushButton_WD = QtGui.QPushButton("Set Working Directory",self.centralwidget)
        self.pushButton_WD.setGeometry(QtCore.QRect(10, 190, 171, 31))
        self.pushButton_WD.clicked.connect(self.Dir_Set)
        self.pushButton_WD.setStatusTip('Set the working directory')

        self.pushButton_1_New = QtGui.QPushButton("1. New Project",self.centralwidget)
        self.pushButton_1_New.setGeometry(QtCore.QRect(10, 230, 171, 28))
        self.pushButton_1_New.clicked.connect(self.New_Proj)
        self.pushButton_1_New.setStatusTip('Step 1: Create a new Project File')

        self.pushButton_2_Import = QtGui.QPushButton("2. Import Data",self.centralwidget)
        self.pushButton_2_Import.setGeometry(QtCore.QRect(189, 230, 171, 28))
        self.pushButton_2_Import.clicked.connect(self.Data_Import)
        self.pushButton_2_Import.setStatusTip('Step 2: Import and Process Data')
        self.pushButton_2_Import.setToolTip('Right-click for option')
        self.pushButton_2_Import.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.pushButton_2_Import.customContextMenuRequested.connect(self.on_context_import)

        self.pushButton_3a_PhThresh = QtGui.QPushButton("3a. Phase Threshold",self.centralwidget)
        self.pushButton_3a_PhThresh.setGeometry(QtCore.QRect(10, 260, 171, 28))
        self.pushButton_3a_PhThresh.clicked.connect(self.Ph_Thresh)
        self.pushButton_3a_PhThresh.setStatusTip('Step 3a: Single phase thresholding')

        self.pushButton_3b_PhClust = QtGui.QPushButton("3b. Phase Cluster",self.centralwidget)
        self.pushButton_3b_PhClust.setGeometry(QtCore.QRect(189, 260, 171, 28))
        self.pushButton_3b_PhClust.setToolTip('Right-click for option')
        self.pushButton_3b_PhClust.clicked.connect(self.Ph_Clust)
        self.pushButton_3b_PhClust.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.pushButton_3b_PhClust.customContextMenuRequested.connect(self.on_context)
        self.pushButton_3b_PhClust.setStatusTip('Step 3b: Kmeans++ phase clustering')
        #self.pushButton_3b_PhClust.setEnabled(False)

        self.pushButton_5_Plot = QtGui.QPushButton("5. Create Plots",self.centralwidget)
        self.pushButton_5_Plot.setGeometry(QtCore.QRect(189, 290, 171, 28))
        self.pushButton_5_Plot.clicked.connect(self.Plot_Pop)
        self.pushButton_5_Plot.setStatusTip('Step 5: Create and export figures and plots')

        self.pushButton_4_Ratio = QtGui.QPushButton("4. Create a Ratio Map",self.centralwidget)
        self.pushButton_4_Ratio.setGeometry(QtCore.QRect(10, 290, 171, 28))
        self.pushButton_4_Ratio.clicked.connect(self.Ratio_Calc)
        self.pushButton_4_Ratio.setStatusTip('Step 4: Create and export figures and plots')

        self.Proj_treeView = QtGui.QTreeView(self.centralwidget)
        self.Proj_treeView.setGeometry(QtCore.QRect(10, 350, 349, 121))
        self.Proj_treeView.setStatusTip('Project File/Groups/Data.')
        self.Proj_treeView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        self.pushButton_Open = QtGui.QPushButton("Open Project",self.centralwidget)
        self.pushButton_Open.setGeometry(QtCore.QRect(189, 190, 171, 31))
        self.pushButton_Open.clicked.connect(self.Open_Proj)
        self.pushButton_Open.setStatusTip('Open an existing project file...')

        #set up right click context menu for Cluster Button
        self.popMenu_Clust = QtGui.QMenu(self)
        self.popMenu_Clust.addAction(QtGui.QAction('Edit Previous Cluster Group', self))
        self.popMenu_Clust.setToolTip('Jump to the final Cluster dialog to continue editing a previous session.')
        self.popMenu_Clust.triggered.connect(self.clust_popup)

        self.popMenu_Import = QtGui.QMenu(self)
        self.popMenu_Import.addAction(QtGui.QAction('Finish creating NormStack and H Factor', self))
        self.popMenu_Import.setToolTip('Perform final data import methods on large projects limited by memory')
        self.popMenu_Import.triggered.connect(self.data_popup)

        #Setup the menubar
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 310, 26))
        #Setup the Project Menu
        self.menuProject = QtGui.QMenu("Project",self.menubar)
        self.actionOpen = QtGui.QAction("Export Maps",MainWindow)
        self.actionOpen.setToolTip('Export maps from the current project file as text files')
        self.actionOpen.triggered.connect(self.Export_Arrays)
        self.actionClose = QtGui.QAction("Close Project",MainWindow)
        self.actionClose.setToolTip('Save and Close Current Project File')
        self.actionClose.triggered.connect(self.Save_and_Close)
        self.actionExit = QtGui.QAction("Exit",MainWindow)
        self.actionExit.setStatusTip('Save and Exit the software')
        self.actionExit.triggered.connect(self.Save_and_Exit)
        self.menuProject.addAction(self.actionOpen)
        self.menuProject.addAction(self.actionClose)
        self.menuProject.addSeparator()
        self.menuProject.addAction(self.actionExit)
        self.menubar.addAction(self.menuProject.menuAction())

        #Setup the Help Menu
        self.menuHelp = QtGui.QMenu("Help",self.menubar)
        self.actionGetting_Started = QtGui.QAction("Getting Started...",MainWindow)
        self.actionGetting_Started.setStatusTip('Using the QACD method')
        self.actionGetting_Started.triggered.connect(self.Start_Docu)
        #self.actionFAQ = QtGui.QAction("FAQ",MainWindow)
        #self.actionFAQ.setStatusTip('Frequently Asked Questions...')
        #self.actionFAQ.triggered.connect(self.Faq_pop)
        self.actionUser_Manual = QtGui.QAction("User Manual",MainWindow)
        self.actionUser_Manual.setStatusTip('A link to the User Manual')
        self.actionUser_Manual.triggered.connect(self.User_Manu)
        self.actionAbout = QtGui.QAction("About",MainWindow)
        self.actionAbout.setStatusTip('About')
        self.actionAbout.triggered.connect(self.About_pop)
        self.menuHelp.addAction(self.actionGetting_Started)
        #self.menuHelp.addAction(self.actionFAQ)
        self.menuHelp.addAction(self.actionUser_Manual)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuHelp.menuAction())
        #Set the Menu and Statusbars for the Project Manager Window
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.MemLabel = QtGui.QLabel("MemUsage",self.centralwidget)
        self.statusbar.addWidget(self.MemLabel)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Time)
        self.timer.start(2500)

        self.dirName = 'direct'
        self.varProj = 'file'


        #Set the central widget
        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        QtCore.QObject

        self.config_up()

    def config_up(self):
        filedir = os.path.dirname(os.path.abspath(__file__))
        filet = "LastFile.txt"
        self.cfgname = os.path.join(filedir, filet)
        old = []
        if os.path.exists(self.cfgname) == True:
            cfg = open(self.cfgname, 'r')
            for line in cfg.readlines():
                old.append(line)
            print old
            cfg.close()
            mess = 'Load last configuration?'
            quest = 'Would you like to load the most recently used directory('+str(old[0])+")?"
            reply = QtGui.QMessageBox.question(self,mess,quest,QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                self.dirName = old[0]
                self.set_dir()
            else:
                self.dirName = 'direct'
                print 'Continuing'
        else:
            print 'No log file'
        return
    def Time(self):
        pid = os.getpid()
        #mem = psutil.Process(pid).memory_info()[0]/float(2**20)
        mem = (psutil.Process(pid).memory_full_info().uss)/1000.00/1024.00
        self.MemLabel.setText("Mem Usage: "+str(mem)+" MB")
    def cons_scroll(self):
        self._console.moveCursor(QtGui.QTextCursor.End)
        self._console.ensureCursorVisible()
        return
    def on_context(self, point):
        self.popMenu_Clust.exec_(self.pushButton_3b_PhClust.mapToGlobal(point))
        return
    def on_context_import(self,  point1):
        self.popMenu_Import.exec_(self.pushButton_2_Import.mapToGlobal(point1))
        return
    def data_popup(self):
        import qacd_corr as qcr
        st1 = qcr.elratio(self.varProj)
        print st1
        st2 = qcr.h_factor(self.varProj)
        print st2
        gc.collect()
        del gc.garbage[:]
        model = htv.HDF5TreeViewModel()
        self.Proj_treeView.setModel(model)
        self.Proj_treeView.setUniformRowHeights(True)
        self.Proj_treeView.setHeaderHidden(True)
        self.Proj_treeView.show()
        self.log_trans()
        print "Your Data have been created"
        return
    def clust_popup(self):
        from dlg_kpop import myDialog
        self.kpopDlg = myDialog(self)
        self.kpopDlg.exec_()
        del self.kpopDlg
        gc.collect()
        gc.collect()
        del gc.garbage[:]
        f = tb.open_file("temp.h5",mode='a')
        tp = f.get_node(f.root, "clust")
        reply = tp.attrs.reason
        f.close()
        if reply == 42:
            from dlg_phclust import myDialog
            self.PhCDlg2 = myDialog(self)
            self.PhCDlg2.exec_()
            self.PhCDlg2 = ""
        else:
            print 'Cancel'
        gc.collect()
        gc.collect()
        del gc.garbage[:]
        model = htv.HDF5TreeViewModel()
        self.Proj_treeView.setModel(model)
        self.Proj_treeView.setUniformRowHeights(True)
        self.Proj_treeView.setHeaderHidden(True)
        self.Proj_treeView.show()
        self.log_trans()
        self.log_trans()
        return
    def table_initialise(self):
        self.Proj_tableWidget.setRowCount(17)
        self.Proj_tableWidget.setColumnCount(2)
        self.Proj_tableWidget.horizontalHeader().setDefaultSectionSize(80)
        self.Proj_tableWidget.horizontalHeader().setVisible(False)
        self.Proj_tableWidget.verticalHeader().setVisible(False)
        for i in xrange(0, len(self.rowtitles)):
            var = self.rowtitles[i]
            self.Proj_tableWidget.setItem(i,0,QtGui.QTableWidgetItem(var))
        self.Proj_tableWidget.resizeColumnToContents(0)
        return
    def log_trans(self):
        f = tb.open_file(self.varProj,mode='a')
        tp = f.get_node(f.root,'Log')
        log = tp.read()
        self.logDict = {}
        self.logDict['Last Opened']=log[0] #datetime of project opening
        self.logDict['Created']=log[1] #datetime of project creation
        self.logDict['Data Imported']=log[2] #datetime of import and # of files
        self.logDict['Filtered']=log[3] #method of filtration
        self.logDict['Pixel Size']=log[4] #size and units
        self.logDict['Map Width']=log[5] #units, points
        self.logDict['Map Height']=log[6] #units, points
        self.logDict['Map Area']=log[7] #units, points
        self.logDict['Pixels (N)']=log[8] #number of pixels
        self.logDict['Phase Masks']=log[9] #Date of last mask
        self.logDict['Phases Thresh.']=log[10] #num thresholded
        self.logDict['Phases Clust.']=log[11] #num clustered
        self.logDict['Total Phases']=log[12] #num of phases total
        self.logDict['Ratio Maps']=log[13] #num of ratio maps created
        self.logDict['Last Ratio Map']=log[14] #date of last
        self.logDict['Last Map Plot']=log[15] #date of last
        self.logDict['Last Hist Plot']=log[16] #date of last
        for i in xrange(0, len(self.rowtitles)):
            var = self.rowtitles[i]
            var2 = str(self.logDict[var])
            self.Proj_tableWidget.setItem(i,1,QtGui.QTableWidgetItem(var2))
        self.Proj_tableWidget.resizeColumnToContents(1)
        return
    def on_treeView_clicked(self, index):
        indexItem = self.Dir_model.index(index.row(), 0, index.parent())
        fileName = self.Dir_model.fileName(indexItem)
        self.treeSelect = fileName
        return
    def Dir_Set(self):
        self.dirName = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
        cfg = open(self.cfgname, 'w')
        value = str(self.dirName)
        cfg.write(value)
        cfg.close()
        self.set_dir()
        return
    def set_dir(self):
        if self.dirName and self.dirName.strip():
            os.chdir(self.dirName)
            stringer = "Working Directory: " + str(self.dirName)
            self.label1_WD.setText(stringer)
            #add in the population of the directory model view with the WD folder contents

            self.Dir_model.setRootPath(self.dirName)
            self.Dir_treeView.setModel(self.Dir_model)
            self.Dir_treeView.setRootIndex(self.Dir_model.index(self.dirName))
            self.Dir_treeView.setUniformRowHeights(True)
            self.Dir_treeView.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)
            self.Dir_treeView.header().setStretchLastSection(False)
            self.Dir_treeView.setHeaderHidden(True)
            self.Dir_treeView.show()
            #self.Dir_treeView.resizeColumnsToContents()
        else:
            print 'Choose a Working Directory'
        gc.collect()
        gc.collect()
        del gc.garbage[:]
        return
    def New_Proj(self):
        fnm = QtGui.QFileDialog.getSaveFileName(self,"Save project as...",'',"HDF5 Files (*.h5)")
        self.projname = str(fnm)
        print("########### hello", self.projname)
        if self.projname and self.projname.strip():
            name = ''.join(self.projname)#format name as strings
            pname,  fname = os.path.split(name)
            self.varProj = str(fname) #declare element name as string
            f = tb.open_file("temp.h5", mode = 'w')
            f.create_array(f.root,'varProj',self.varProj)
            f.close()
            f = tb.open_file(str(self.varProj), mode='w')
            self.log = ['N/A'] * 17
            import datetime
            string = datetime.datetime.now().strftime("%I:%M%p, %d %B %Y")
            self.log[0] = string
            self.log[1] = string
            f.create_group(f.root, "Cluster")
            f.create_array(f.root, "Log", self.log)
            f.close()
            #add in the population of the project tree widget
            model = htv.HDF5TreeViewModel()
            self.Proj_treeView.setModel(model)
            self.Proj_treeView.setUniformRowHeights(True)
            self.Proj_treeView.setHeaderHidden(True)
            self.Proj_treeView.show()
        else:
            print 'Get on with it!'
        gc.collect()
        gc.collect()
        del gc.garbage[:]
        stringer = "Project Tree: " + str(self.varProj)
        self.label2_ProjTree.setText(stringer)
        self.log_trans()
        return
    def Open_Proj(self):
        self.projname = str(self.treeSelect)
        #self.projname = str(QtGui.QFileDialog.getOpenFileName(self,"Name your project",self.dirName,selectedFilter='*.h5'))
        if self.projname and self.projname.strip():
            name = ''.join(self.projname)#format name as strings
            pname,  fname = os.path.split(name)
            self.varProj = str(fname) #declare element name as string
            print self.varProj
            f = tb.open_file("temp.h5", mode = 'w')
            f.create_array(f.root,'varProj',self.varProj)
            f.close()
            f = tb.open_file(self.varProj, mode = 'a')
            l1 = f.get_node(f.root, "Log")
            self.log = l1.read()
            import datetime
            string = datetime.datetime.now().strftime("%I:%M%p, %d %B %Y")
            self.log[0] = string
            f.remove_node(f.root, "Log")
            f.create_array(f.root,"Log",self.log)
            f.close()
            model = htv.HDF5TreeViewModel()
            self.Proj_treeView.setModel(model)
            self.Proj_treeView.setUniformRowHeights(True)
            self.Proj_treeView.setHeaderHidden(True)
            self.Proj_treeView.show()
        else:
            print 'Choose a file!'
        gc.collect()
        gc.collect()
        del gc.garbage[:]
        stringer = "Project Tree: " + str(self.varProj)
        self.label2_ProjTree.setText(stringer)
        self.log_trans()
        return
    def Proj_Stats(self):
        from dlg_figPh import myDialog
        figPh = myDialog(self)
        figPh.exec_()
        del figPh
        gc.collect()
        gc.collect()
        del gc.garbage[:]
        return
    def Data_Import(self):
        from dlg_Import import myDialog
        InitDlg = myDialog(self)
        InitDlg.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        InitDlg.exec_()
        del InitDlg
        gc.collect()
        gc.collect()
        del gc.garbage[:]
        model = htv.HDF5TreeViewModel()
        self.Proj_treeView.setModel(model)
        self.Proj_treeView.setUniformRowHeights(True)
        self.Proj_treeView.setHeaderHidden(True)
        self.Proj_treeView.show()
        self.log_trans()
        Message = 'Close Program-Clear Memory'
        Question = 'For larger maps, we recommend closing the program to clear the memory cache after data import. Do you want to do that now?'
        reply = QtGui.QMessageBox.question(self,Message,Question,QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            self.close()
        else:
            print 'Continuing'
        return
    def Ph_Thresh(self):
        from dlg_phaseTh import myDialog
        PhTDlg = myDialog(self)
        PhTDlg.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        PhTDlg.show()
        gc.collect()
        gc.collect()
        del gc.garbage[:]
        model = htv.HDF5TreeViewModel()
        self.Proj_treeView.setModel(model)
        self.Proj_treeView.setUniformRowHeights(True)
        self.Proj_treeView.setHeaderHidden(True)
        self.Proj_treeView.show()
        self.log_trans()
        return
    def Ph_Clust(self):
        Message = 'First Time'
        Question = 'Have you already carried out phase clustering?'
        reply = QtGui.QMessageBox.question(self,Message,Question,QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        clust = self.cluster
        if reply == QtGui.QMessageBox.Yes:
            f = tb.open_file(self.varProj, mode='a')
            self.cluster = f.get_node(f.root, "nums").read()
            f.close()
            group = "Cluster" + str(self.cluster)
            f = tb.open_file("temp.h5", mode='a')
            tmp = f.root
            lis = tmp._v_children
            if 'clust' in lis.keys():
                f.remove_node(tmp, "clust")
            else:
                print
            f.create_array(tmp, "clust", group)
            if 'nums' in lis.keys():
                f.remove_node(tmp, "nums")
            else:
                print
            f.create_array(tmp, "nums", self.cluster)
            f.close()
            f = tb.open_file(self.varProj, mode='a')
            f.create_group(f.root,group)
            f.close()
        else:
            f = tb.open_file("temp.h5", mode='a')
            f.create_array(f.root, "clust", 'Cluster')
            f.create_array(f.root, "nums", clust)
            f.close()
            f = tb.open_file(self.varProj, mode='a')
            f.create_array(f.root, "nums", self.cluster)
            f.close()
        from dlg_K import myDialog
        print('==> opening dlg_K')
        PhKDlg = myDialog(self)
        PhKDlg.exec_()
        from dlg_clust import myDialog
        print('==> opening dlg_clust')
        PhCDlg = myDialog(self)
        PhCDlg.exec_()
        from dlg_phclust import myDialog
        print('==> opening dlg_phclust')
        PhCDlg2 = myDialog(self)
        PhCDlg2.exec_()
        self.cluster = clust + 1
        model = htv.HDF5TreeViewModel()
        self.Proj_treeView.setModel(model)
        self.Proj_treeView.setUniformRowHeights(True)
        self.Proj_treeView.setHeaderHidden(True)
        self.Proj_treeView.show()
        self.log_trans()
        self.log_trans()
    def Ratio_Calc(self):
        from dlg_ratio import myDialog
        RDlg = myDialog(self)
        RDlg.exec_()
        del RDlg
        gc.collect()
        gc.collect()
        del gc.garbage[:]
        model = htv.HDF5TreeViewModel()
        self.Proj_treeView.setModel(model)
        self.Proj_treeView.setUniformRowHeights(True)
        self.Proj_treeView.setHeaderHidden(True)
        self.Proj_treeView.show()
        self.log_trans()
        return
    def Plot_Pop(self):
        from dlg_figure import myDialog
        FigDlg = myDialog(self)
        FigDlg.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        FigDlg.show()
        gc.collect()
        gc.collect()
        del gc.garbage[:]
        self.log_trans()
        return
    def Save_and_Close(self):
        self.table_initialise()
        self.model = QtGui.QFileSystemModel()
        self.Proj_treeView.setModel(self.model)
        gc.collect()
        del gc.garbage[:]
        return
#    def closeEvent(self, e):
#        cfg = open(self.cfgname, 'w')
#        value = str(self.dirName)
#        cfg.write(value)
#        cfg.close()
#        return
    def Save_and_Exit(self):
        gc.collect()
        del gc.garbage[:]
        self.close()
        return
    def Export_Arrays(self):
        from dlg_exp import myDialog
        self.expDlg = myDialog(self)
        self.expDlg.exec_()
        self.expDlg = ""
        gc.collect()
        del gc.garbage[:]
        return
    def Start_Docu(self):
        return
    def Faq_pop(self):
        return
    def User_Manu(self):
        return
    def About_pop(self):
        from dlg_about import myDialog
        abDlg = myDialog(self)
        abDlg.exec_()


import ProjectManager_rc

if __name__=='__main__':
    app = QtGui.QApplication(sys.argy)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
