# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Export_Dialog.ui'
#
# Created: Wed Feb 03 13:34:23 2016
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import HDF5TreeViewModel as htv
import tables as tb
import numpy as np
from pandas import DataFrame

class Ui_Export_Dialog(object):
    def setupUi(self, Export_Dialog):
        self.varProj = ''
        f = tb.open_file('temp.h5',mode='a')
        self.varProj = (f.get_node(f.root, 'varProj')).read()
        f.close()
        Export_Dialog.setObjectName("Export_Dialog")
        Export_Dialog.resize(523, 394)
        Export_Dialog.setWindowTitle("QACD- Export Arrays")
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Export_Dialog.sizePolicy().hasHeightForWidth())
        Export_Dialog.setSizePolicy(sizePolicy)
        Export_Dialog.setMaximumSize(QtCore.QSize(523, 394))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/main_icon/16x16.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Export_Dialog.setWindowIcon(icon)

        self.widget = QtGui.QWidget(Export_Dialog)
        self.widget.setGeometry(QtCore.QRect(10, 10, 502, 366))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)
        self.label_tree = QtGui.QLabel("Project Tree:",self.widget)
        self.gridLayout.addWidget(self.label_tree, 0, 0, 1, 4)
        self.treeView = QtGui.QTreeView(self.widget)
        self.treeView.setStatusTip('Project File/Groups/Data.')
        self.treeView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.gridLayout.addWidget(self.treeView, 1, 0, 9, 4)

        self.label_1_log = QtGui.QLabel("Export Project Log File:",self.widget)
        font = QtGui.QFont()
        font.setUnderline(True)
        self.label_1_log.setFont(font)
        self.gridLayout.addWidget(self.label_1_log, 1, 4, 1, 4)
        self.line_Log = QtGui.QLineEdit(self.widget)
        self.gridLayout.addWidget(self.line_Log, 2, 4, 1, 3)
        self.push_Log = QtGui.QPushButton("Export as CSV",self.widget)
        self.push_Log.clicked.connect(self.export_Log)
        self.gridLayout.addWidget(self.push_Log, 2, 7, 1, 1)

        self.label_2_Clust = QtGui.QLabel("Export Clustered Phase Masks",self.widget)
        font = QtGui.QFont()
        font.setUnderline(True)
        self.label_2_Clust.setFont(font)
        self.gridLayout.addWidget(self.label_2_Clust, 3, 4, 1, 4)
        self.line_Cluster = QtGui.QLineEdit(self.widget)
        self.gridLayout.addWidget(self.line_Cluster, 6, 4, 1, 3)
        self.push_Cluster = QtGui.QPushButton("Export as CSV",self.widget)
        self.push_Cluster.clicked.connect(self.export_Cluster)
        self.gridLayout.addWidget(self.push_Cluster, 6, 7, 1, 1)
        self.label_2a_Groups = QtGui.QLabel("Groups:",self.widget)
        self.gridLayout.addWidget(self.label_2a_Groups, 4, 4, 1, 1)
        self.combo_2a_Groups = QtGui.QComboBox(self.widget)
        self.combo_2a_Groups.activated[str].connect(self.clust_group)
        self.gridLayout.addWidget(self.combo_2a_Groups, 4, 5, 1, 3)
        self.label_2b_Masks = QtGui.QLabel("Phase Masks:",self.widget)
        self.gridLayout.addWidget(self.label_2b_Masks, 5, 4, 1, 1)
        self.combo_2b_Masks = QtGui.QComboBox(self.widget)
        self.gridLayout.addWidget(self.combo_2b_Masks, 5, 5, 1, 3)

        self.label_3_Thresh = QtGui.QLabel("Export Thresholded Phase Masks",self.widget)
        font = QtGui.QFont()
        font.setUnderline(True)
        self.label_3_Thresh.setFont(font)
        self.gridLayout.addWidget(self.label_3_Thresh, 7, 4, 1, 4)
        self.label_3a_Masks = QtGui.QLabel("Phase Masks:",self.widget)
        self.gridLayout.addWidget(self.label_3a_Masks, 8, 4, 1, 1)
        self.line_Thresh = QtGui.QLineEdit(self.widget)
        self.gridLayout.addWidget(self.line_Thresh, 9, 4, 1, 3)
        self.push_thresh = QtGui.QPushButton("Export as CSV",self.widget)
        self.push_thresh.clicked.connect(self.export_Thresh)
        self.gridLayout.addWidget(self.push_thresh, 9, 7, 1, 1)
        self.combo_3a_Masks = QtGui.QComboBox(self.widget)
        self.gridLayout.addWidget(self.combo_3a_Masks, 8, 5, 1, 3)

        self.label_4_Data = QtGui.QLabel("Export Processed Data",self.widget)
        font = QtGui.QFont()
        font.setUnderline(True)
        self.label_4_Data.setFont(font)
        self.gridLayout.addWidget(self.label_4_Data, 10, 4, 1, 4)
        self.label_4a_Maps = QtGui.QLabel("Filtered Maps:",self.widget)
        self.gridLayout.addWidget(self.label_4a_Maps, 11, 4, 1, 1)
        self.combo_4a_Maps = QtGui.QComboBox(self.widget)
        self.gridLayout.addWidget(self.combo_4a_Maps, 11, 5, 1, 3)
        self.line_Data = QtGui.QLineEdit(self.widget)
        self.gridLayout.addWidget(self.line_Data, 12, 4, 1, 3)
        self.push_Data = QtGui.QPushButton("Export as CSV",self.widget)
        self.push_Data.clicked.connect(self.export_Data)
        self.gridLayout.addWidget(self.push_Data, 12, 7, 1, 1)

        self.label_5_corr = QtGui.QLabel("Export Corrected Data",self.widget)
        font = QtGui.QFont()
        font.setUnderline(True)
        self.label_5_corr.setFont(font)
        self.gridLayout.addWidget(self.label_5_corr, 10, 0, 1, 4)
        self.label_5a_maps = QtGui.QLabel("Corrected Maps:",self.widget)
        self.gridLayout.addWidget(self.label_5a_maps, 11, 0, 1, 1)
        self.combo_5a_Maps = QtGui.QComboBox(self.widget)
        self.gridLayout.addWidget(self.combo_5a_Maps, 11, 1, 1, 3)
        self.line_Data2 = QtGui.QLineEdit(self.widget)
        self.gridLayout.addWidget(self.line_Data2, 12, 0, 1, 3)
        self.push_Data2 = QtGui.QPushButton("Export as CSV",self.widget)
        self.push_Data2.clicked.connect(self.export_Data2)
        self.gridLayout.addWidget(self.push_Data2, 12, 3, 1, 1)
        QtCore.QMetaObject.connectSlotsByName(Export_Dialog)

        self.populate()
    def populate(self):
        f = tb.open_file(self.varProj, mode='a')
        tmp = f.root._v_children
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
            elif item =='Phase':
                print 'Not a cluster'
            elif item =='nums':
                print 'Not a cluster'
            elif item =='Stack1':
                print 'Not a cluster'
            elif item =='Stack2':
                print 'Not a cluster'
            else:
                self.combo_2a_Groups.addItem(item)
                print item
        index = self.combo_2a_Groups.findText('Cluster')
        self.combo_2a_Groups.setCurrentIndex(index)
        Clust = f.root._f_get_child('Cluster')
        lis = Clust._v_children
        if 'PhaseMap' in lis.keys():
            pm = Clust._f_get_child('PhaseMap')
            Masks = pm._f_get_child('masks')
            tmp = Masks._v_children
            ls = tmp.keys()
            for item in ls:
                self.combo_2b_Masks.addItem(item)
                print item
        else:
            print
        Phase = f.root.Phase
        tmp = Phase._v_children
        ls = tmp.keys()
        for item in ls:
            self.combo_3a_Masks.addItem(item)
        Filt = f.root.Filtered
        tmp = Filt._v_children
        ells = tmp.keys()
        for item in ells:
            if item == 'Arrays':
                print 'Skipped Arrays'
            else:
                self.combo_4a_Maps.addItem(item)
        Conc = f.root.Concentration
        tmp = Conc._v_children
        clls = tmp.keys()
        for item in clls:
            self.combo_5a_Maps.addItem(item)
        print 'Populated'
        f.close()
        model = htv.HDF5TreeViewModel()
        self.treeView.setModel(model)
        self.treeView.setUniformRowHeights(True)
        self.treeView.setHeaderHidden(True)
        self.treeView.show()
        return
    def clust_group(self,item):
        grp = str(self.combo_2a_Groups.currentText())
        f = tb.open_file(self.varProj,mode='a')
        Clust = f.root._f_get_child(grp)
        pm = Clust._f_get_child('PhaseMap')
        Masks = pm._f_get_child('masks')
        tmp = Masks._v_children
        ls = tmp.keys()
        self.combo_2b_Masks.clear()
        for item in ls:
            self.combo_2b_Masks.addItem(item)
            print item
        f.close()
        return
    def export_Log(self):
        self.logDict = {}
        var = str(self.line_Log.text())
        fname = str(var) + ".csv"
        f = tb.open_file(self.varProj, mode='a')
        log = f.get_node(f.root,"Log").read()
        rowtitles = ['Last Opened','Created','Data Imported','Filtered',
                     'Pixel Size','Map Width','Map Height','Map Area',
                     'Pixels (N)','Phase Masks','Phases Thresh.',
                     'Phases Clust.','Total Phases','Ratio Maps',
                     'Last Ratio Map','Last Map Plot','Last Hist Plot']
        datdic = {'Reason':rowtitles, 'Item':log}
        df = DataFrame(datdic, columns=['Reason', 'Item'])
        df.to_csv(fname)
        f.close()
        print 'Log Exported'
        return
    def export_Cluster(self):
        var = str(self.line_Cluster.text())
        fname = str(var) + ".csv"
        group = str(self.combo_2a_Groups.currentText())
        phase = str(self.combo_2b_Masks.currentText())
        f = tb.open_file(self.varProj, mode='a')
        Clust = f.root._f_get_child(group)
        pm = Clust._f_get_child('PhaseMap')
        Masks = pm._f_get_child('masks')
        ds = f.get_node(Masks,phase).read()
        ds1 = ds.astype(int)
        df = DataFrame(ds1)
        df.to_csv(fname,header=False,index=False,index_label=False)
        f.close()
        print 'Cluster Mask Exported'
        return
    def export_Thresh(self):
        var = str(self.line_Thresh.text())
        fname = str(var) + ".csv"
        phase = str(self.combo_3a_Masks.currentText())
        f = tb.open_file(self.varProj, mode='a')
        Phase = f.root.Phase
        ds = f.get_node(Phase,phase).read()
        df = DataFrame(ds)
        df.to_csv(fname,header=False,index=False,index_label=False)
        f.close()
        print 'Thresholded Phase Exported'
        return
    def export_Data(self):
        var = str(self.line_Data.text())
        fname = str(var) + ".csv"
        print fname
        mapvar = str(self.combo_4a_Maps.currentText())
        f = tb.open_file(self.varProj, mode='a')
        Filt = f.root.Filtered
        ds = f.get_node(Filt,mapvar).read()
        ds[np.isinf(ds)]=np.nan
        df = DataFrame(ds)
        df.to_csv(fname,header=False,index=False,index_label=False)
        f.close()
        print 'Filtered Data Exported'
        return
    def export_Data2(self):
        var = str(self.line_Data2.text())
        fname = str(var) + ".csv"
        print fname
        mapvar = str(self.combo_5a_Maps.currentText())
        f = tb.open_file(self.varProj, mode='a')
        Filt = f.root.Concentration
        ds = f.get_node(Filt,mapvar).read()
        ds[np.isinf(ds)]=np.nan
        df = DataFrame(ds)
        df.to_csv(fname,header=False,index=False,index_label=False)
        f.close()
        print 'Filtered Data Exported'
        return
import ProjectManager_rc

if __name__=='_main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    myDialog = QtGui.QDialog()
    ui = Ui_Export_Dialog()
    ui.setupUi(myDialog)
    myDialog.show()
    sys.exit(app.exec_())
