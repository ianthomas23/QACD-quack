# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Figure_Dialog.ui'
#
# Created: Tue Jan 26 11:00:51 2016
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import tables as tb
import gc


class Ui_Figure_Dialog(object):
    def setupUi(self, Figure_Dialog):
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.varProj = ''
        self.dset = ''
        self.mapvar = ''
        self.phase = ''
        self.phls = []
        self.ells = []
        self.curdat = {}
        self.curdat2 = {}
        self.curdat3 = {}
        self.curdat0 = {}
        self.phgrps = []
        self.autoth = 0
        Figure_Dialog.setObjectName("Figure_Dialog")
        Figure_Dialog.resize(279, 562)
        Figure_Dialog.setWindowTitle("QACD- Figure Creator")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/main_icon/16x16.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Figure_Dialog.setWindowIcon(icon)
        Figure_Dialog.setModal(False)
        
        self.widget = QtGui.QWidget(Figure_Dialog)
        self.widget.setGeometry(QtCore.QRect(10, 10, 258, 544))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)

        self.label_Dataset = QtGui.QLabel("Phase Set:",self.widget)
        self.gridLayout.addWidget(self.label_Dataset, 0, 0, 1, 1)
        self.comboBox_Data = QtGui.QComboBox(self.widget)
        self.gridLayout.addWidget(self.comboBox_Data, 0, 1, 1, 3)
        self.comboBox_Data.activated[str].connect(self.dataset_select)
        
        self.label_Dataset2 = QtGui.QLabel("Dataset:",self.widget)
        self.gridLayout.addWidget(self.label_Dataset2, 1, 0, 1, 1)
        self.comboBox_Data2 = QtGui.QComboBox(self.widget)
        self.gridLayout.addWidget(self.comboBox_Data2, 1, 1, 1, 3)
        self.comboBox_Data2.activated[str].connect(self.dataset_select2)
        
        self.listWidget_Data = QtGui.QListWidget(self.widget)
        self.gridLayout.addWidget(self.listWidget_Data, 2, 0, 1, 4)
        self.listWidget_Data.itemClicked.connect(self.list_select)
        
        self.label_PhMask = QtGui.QLabel("Phase Mask:",self.widget)
        self.gridLayout.addWidget(self.label_PhMask, 3, 0, 1, 2)
        self.comboBox_Mask = QtGui.QComboBox(self.widget)
        self.gridLayout.addWidget(self.comboBox_Mask, 3, 2, 1, 2)
        self.comboBox_Mask.addItem('No Phase')
        self.comboBox_Mask.activated[str].connect(self.phase_select)
        
        #self.label_MapInfo = QtGui.QLabel("Map Info:",self.widget)
        #self.gridLayout.addWidget(self.label_MapInfo, 4, 0, 1, 4)
        self.checkBox_Auto = QtGui.QCheckBox("Auto Threshold",self.widget)
        self.gridLayout.addWidget(self.checkBox_Auto, 4, 0, 1, 4)
        self.checkBox_Auto.toggled.connect(self.Auto_thresh)
        self.textedit_Info = QtGui.QTextEdit(self.widget)
        self.gridLayout.addWidget(self.textedit_Info, 5, 0, 1, 4)
        
        self.pushButton_Exit = QtGui.QPushButton("Exit and Return to Project Manager",self.widget)
        self.gridLayout.addWidget(self.pushButton_Exit, 7, 0, 1, 4)
        self.pushButton_Exit.clicked.connect(self.exit_cls)
        self.pushButton_Map = QtGui.QPushButton("Create Map Plot",self.widget)
        self.gridLayout.addWidget(self.pushButton_Map, 6, 0, 1, 2)
        self.pushButton_Map.setToolTip('Right-click for more options')
        self.pushButton_Map.clicked.connect(self.map_form)
        self.pushButton_Map.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.pushButton_Map.customContextMenuRequested.connect(self.on_context)
        self.pushButton_Hist = QtGui.QPushButton("Create Histogram",self.widget)
        self.gridLayout.addWidget(self.pushButton_Hist, 6, 2, 1, 2)
        self.pushButton_Hist.clicked.connect(self.hist_form)
        
        #set up right click context menu for Cluster Button
        self.popMenu_Clust = QtGui.QMenu(self)
        self.popMenu_Clust.addAction(QtGui.QAction('Create Plot of Selected Phase Mask', self))
        self.popMenu_Clust.setToolTip('This will create a plot of the phase mask instead of masking the selected map.')
        self.popMenu_Clust.triggered.connect(self.clust_popup)

        QtCore.QMetaObject.connectSlotsByName(Figure_Dialog)

        self.populate()
    def on_context(self, point):
        self.popMenu_Clust.exec_(self.pushButton_Map.mapToGlobal(point))
        return
    def clust_popup(self):
        string = 'phase'
        f = tb.open_file('figtemp.h5', mode='w')
        f.create_array(f.root, 'varProj', self.varProj)
        f.create_array(f.root, 'mapvar', str(self.mapvar))
        self.phase = str(self.comboBox_Mask.currentText())
        f.create_array(f.root, 'phase', self.phase)
        print self.phase
        f.create_array(f.root, 'dataset', str(self.dset))
        f.create_array(f.root, 'string', string)
        f.close()
        from dlg_plotM import myDialog
        self.pltDlg = myDialog(self)
        self.pltDlg.exec_()
        self.pltDlg = ""
        gc.collect()
        del gc.garbage[:]
        f = tb.open_file(self.varProj, mode='a')
        log = f.get_node(f.root, "Log").read()
        import datetime
        string = datetime.datetime.now().strftime("%I:%M%p, %d %B %Y")
        log[15] = string
        f.remove_node(f.root, "Log")
        f.create_array(f.root, "Log", log)
        f.close()
        return
    def populate(self):
        f = tb.open_file('temp.h5',mode='a')
        self.varProj = (f.get_node(f.root, 'varProj')).read()
        f.close()
        f = tb.open_file(self.varProj, mode='a')
        tmp = f.root._v_children
        self.phgrps = []
        ls = tmp.keys()
        for item in ls:
            if item == 'PixSize':
                print 'Not a cluster'
            elif item =='Log':
                print 'Not a cluster'
            elif item =='Total':
                print 'Not a cluster'
            elif item =='Filtered':
                print 'Not a cluster'
            elif item =='parameters':
                print 'Not a cluster'
            elif item =='Original':
                print 'Not a cluster'
            elif item =='nums':
                print 'Not a cluster'
            elif item =='Stack1':
                print 'Not a cluster'
            elif item =='Stack2':
                print 'Not a cluster'
            elif item =='Hcorrect':
                print 'Not a cluster'
            elif item =='NormStack':
                print 'Not a cluster'
            elif item =='HFactor':
                print 'Not a cluster'
            elif item =='Concentration':
                print 'Not a cluster'
            elif item =='CorrList':
                print 'Not a cluster'
            elif item =='MapList':
                print 'Not a cluster'
            else:
                self.phgrps.append(item)
                self.comboBox_Data.addItem(item)
                print item
        i1 = "Filtered"
        #i2 = "Hcorrect"
        i3 = "Concentration"
        self.comboBox_Data2.addItem(i1)
        #self.comboBox_Data2.addItem(i2)
        self.comboBox_Data2.addItem(i3)
        index = self.comboBox_Data.findText('Phase')
        self.comboBox_Data.setCurrentIndex(index)
        self.dset = 'Phase'
        index2 = self.comboBox_Data2.findText('Filtered')
        self.comboBox_Data2.setCurrentIndex(index2)
        self.datas = 'Filtered'
        Filt = f.root.Filtered
        #Hcor = f.root.Hcorrect
        if 'Concentration' in ls:
            Conc = f.root.Concentration
            tmp3 = Conc._v_children
            self.ells3 = tmp3.keys()
            for item in self.ells3:
                if item == 'Arrays':
                    print 'Skipped Arrays'
                else:
                    tp = f.get_node(Conc,item)
                    string = tp.attrs.stats
                    self.curdat3[item] = string
        else:
            print 'No Concentration Node'
        Phase = f.root.Phase
        tmp = Filt._v_children
        #tmp2 = Hcor._v_children        
        self.ells = tmp.keys()
        #self.ells2 = tmp2.keys()
        for item in self.ells:
            if item == 'Arrays':
                print 'Skipped Arrays'
            else:
                self.listWidget_Data.addItem(item)
        tmp = Phase._v_children
        self.phls = tmp.keys()
        for item in tmp.keys():
            self.comboBox_Mask.addItem(item)
        for item in self.ells:
            if item == 'Arrays':
                print 'Skipped Arrays'
            else:
                tp = f.get_node(Filt,item)
                string = tp.attrs.stats
                self.curdat[item] = string   
        f.close()
        return
            
    def dataset_select(self,item):
        self.dset = str(item)
        f = tb.open_file(self.varProj, mode='a')
        Phase = f.root._f_get_child(self.dset)
        print Phase
        if self.dset == 'Phase':
            tmp = Phase._v_children
            self.phls = tmp.keys()
            self.comboBox_Mask.clear()
            self.comboBox_Mask.addItem("No Phase")
            for item in self.phls:
                self.comboBox_Mask.addItem(item)
            self.phase = "No Phase"
        else:
            t = Phase._f_get_child('PhaseMap')
            msk = t._f_get_child('masks')
            tmp = msk._v_children
            self.phls = tmp.keys()
            self.comboBox_Mask.clear()
            self.comboBox_Mask.addItem("No Phase")
            for item in self.phls:
                self.comboBox_Mask.addItem(item)
            self.phase = "No Phase"
        f.close()
        return
    def dataset_select2(self,item):
        self.datas = str(item)
        f = tb.open_file(self.varProj, mode='a')
        dats = f.root._f_get_child(self.datas)
        if self.datas == "Filtered":
            tmp = dats._v_children
            self.ells = tmp.keys()
            self.listWidget_Data.clear()
            self.curdat0 = {}
            self.curdat0 = self.curdat
            for item in self.ells:
                if item == 'Arrays':
                    print 'Skipped Arrays'
                else:
                    self.listWidget_Data.addItem(item)
        elif self.datas == "Concentration":
            tmp = dats._v_children
            self.ells = tmp.keys()
            self.listWidget_Data.clear()
            self.curdat0 = {}
            self.curdat0 = self.curdat3
            for item in self.ells:
                self.listWidget_Data.addItem(item)
        f.close()
        return           
    def phase_select(self,item):
        self.phase = str(item)
        return
    def Auto_thresh(self):
        if self.checkBox_Auto.isChecked() == True:
            self.autoth = 1
        else:
            self.autoth = 0
        return
    def list_select(self,item):
        self.mapvar = unicode(item.text(),'utf-8')
        string = self.curdat0[self.mapvar]
        self.textedit_Info.setText(string)
        return
    def exit_cls(self):
        print 'Finished!'
        self.close()
        return
    def map_form(self):
        string = 'map'
        f = tb.open_file('figtemp.h5', mode='w')
        f.create_array(f.root, 'varProj', self.varProj)
        f.create_array(f.root, 'mapvar', str(self.mapvar))
        self.phase = str(self.comboBox_Mask.currentText())
        f.create_array(f.root, 'phase', self.phase)
        print self.phase
        f.create_array(f.root, 'dataset', str(self.dset))
        f.create_array(f.root, 'datagrp', str(self.datas))
        f.create_array(f.root, 'string', string)
        f.create_array(f.root, 'threshold', self.autoth)
        f.close()
        from dlg_plotM import myDialog
        self.pltDlg = myDialog(self)
        self.pltDlg.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.pltDlg.show()
        gc.collect()
        del gc.garbage[:]
        f = tb.open_file(self.varProj, mode='a')
        log = f.get_node(f.root, "Log").read()
        import datetime
        string = datetime.datetime.now().strftime("%I:%M%p, %d %B %Y")
        log[15] = string
        f.remove_node(f.root, "Log")
        f.create_array(f.root, "Log", log)
        f.close()
        return
    def hist_form(self):
        string = 'hist'
        f = tb.open_file('figtemp.h5', mode='w')
        f.create_array(f.root, 'varProj', self.varProj)
        f.create_array(f.root, 'mapvar', str(self.mapvar))
        self.phase = str(self.comboBox_Mask.currentText())
        f.create_array(f.root, 'phase', self.phase)
        print self.phase
        f.create_array(f.root, 'dataset', str(self.dset))
        f.create_array(f.root, 'datagrp', str(self.datas))
        f.create_array(f.root, 'string', string)
        f.create_array(f.root, 'threshold', self.autoth)
        f.close()
        from dlg_plotH import myDialog
        self.pltDlg = myDialog(self)
        self.pltDlg.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.pltDlg.show()
        gc.collect()
        del gc.garbage[:]
        f = tb.open_file(self.varProj, mode='a')
        log = f.get_node(f.root, "Log").read()
        import datetime
        string = datetime.datetime.now().strftime("%I:%M%p, %d %B %Y")
        log[16] = string
        f.remove_node(f.root, "Log")
        f.create_array(f.root, "Log", log)
        f.close()
        gc.collect()
        return

import ProjectManager_rc

if __name__=='_main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    myDialog = QtGui.QDialog()
    ui = Ui_Figure_Dialog()
    ui.setupUi(myDialog)
    myDialog.show()
    sys.exit(app.exec_())

