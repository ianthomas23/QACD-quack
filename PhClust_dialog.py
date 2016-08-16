# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PhClust_dialog.ui'
#
# Created: Thu Jan 28 17:37:18 2016
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from matplotlib.figure import Figure
import matplotlib.cm as cm
import tables as tb
import numpy as np
import os.path as path
from tempfile import mkdtemp
import gc
import sys
from mpl_toolkits.axes_grid1 import make_axes_locatable
from PIL import Image
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.style as mps
import matplotlib.colors as mpc
from matplotlib.ticker import AutoMinorLocator

class MyMplCanvas(FigureCanvas):
    def __init__(self,parent=None,width=12.51,height=7.78,dpi=100):
        mps.use('qacd_xmap')
        fig = Figure(figsize=(width,height),dpi=dpi)
        self.axes = fig.add_subplot(111)
        #we want the axes cleared every time plot() is called
        self.axes.hold(True)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.compute_initial_figure()
    def compute_initial_figure(self):
        pass
class MplCanvas(MyMplCanvas):
    def compute_initial_figure(self):
        self.datahold = DataHolder()
        self.names = self.datahold.get_names()
        imag = self.datahold.get_series_data()
        self.data = self.datahold.get_datdic()
        self.factor = self.datahold.get_factor()
        Length = len(self.names)
        title = "Phasemap (K = " +str(Length-1) + ")"
        mini = np.min(imag)
        maxi = np.max(imag)
        #uni = np.unique(imag)
        N = Length#+1
        #valls = [(self.data[item])/255.0 for item in self.names]
        self.my_cmap = self.discrete_cmap(N, 'nipy_spectral')#, valls)
        self.my_cmap.set_under('k', alpha=0)
        self.my_cmap.set_over('k', alpha=0)
        self.im = self.axes.imshow(imag,cmap=self.my_cmap, 
                                   interpolation='nearest',
                                   vmin = mini-.5, vmax = maxi+.5)
        self.im.set_clim(mini, maxi)
        self.im.set_label('image1')
        self.axes.set_title(title)
        fig = self.axes.get_figure()
        divider = make_axes_locatable(self.axes)
        self.cax = divider.append_axes("right", size="3%", pad=0.1)
        step = 255/(Length - 1)
        #ini = int(step/2)
        #eni = 255 - int(ini)
        self.cb = fig.colorbar(self.im,cax=self.cax, ticks = np.arange(0, 255, step))
        self.cb.ax.tick_params(labelsize=10)
        minorticks = AutoMinorLocator()
        self.cb.ax.yaxis.set_minor_locator(minorticks)
        fig.tight_layout()
        fig.canvas.draw()
        return
    def discrete_cmap(self, N, cmap):
        if type(cmap) == str:
            cmap = cm.get_cmap(cmap)
        colors_i = np.concatenate((np.linspace(0, 1., N), (0., 0., 0., 0.)))#(np.linspace(0, 1., N), (0., 0., 0., 0.)))
        colors_rgba = cmap(colors_i)
        indices = np.linspace(0, 1., N+1)
        cdict = {}
        for ki, key in enumerate(('red', 'green', 'blue')):
            cdict[key] = [(indices[i], colors_rgba[i-1, ki], colors_rgba[i, ki]) for i in xrange(N+1)]
        #return colormap object
        return mpc.LinearSegmentedColormap(cmap.name + "_%d"%N, cdict, 1024)
    def refresh(self):
        self.names = []
        self.names = self.datahold.get_names()
        self.data = {}
        self.data = self.datahold.get_datdic()
        self.stats = {}
        self.stats = self.datahold.get_statdic()
        self.phasemap = []
        self.phasemap = self.datahold.get_pmap()
        return        
    def get_names(self):
        self.names = []
        self.names = self.datahold.get_names()
        return self.names
    def get_data(self):
        self.data = {}
        self.data = self.datahold.get_datdic()
        return self.data
    def get_stats(self):
        self.stats = {}
        self.stats = self.datahold.get_statdic()
        return self.stats
    def get_pmap(self):
        self.phasemap = self.datahold.get_pmap()
        return self.phasemap
    def rename_phase(self,mapvar,mskVar):
        self.datahold.rename_phase(mapvar,mskVar)
        string = "Phase " + str(mapvar) + " has been renamed to " + str(mskVar)
        self.refresh()
        return string
    def delete_phase(self,mapvar):
        self.datahold.delete_phase(mapvar)
        string = "Phase " + str(mapvar) + " has been deleted"
        self.refresh()
        self.update_fig()
        return string
    def merge_phase(self,phA,phB):
        self.datahold.merge_phase(phA,phB)
        string = "Phase " + str(phA) + " has been merged into " + str(phB)
        self.refresh()
        self.update_fig()
        return string
    def update_fig(self):
        fig = self.axes.get_figure()
        image = self.datahold.get_series_data()
        mini = np.min(image)
        maxi = np.max(image)
        print 'mini,maxi', mini, maxi
        print image
        self.im.set_data(image)
        fig.canvas.draw()
        fig.tight_layout()
        fig.canvas.draw()
        return
    def closeFigure(self):
        del self.datahold
        del self.names, self.data, self.factor, self.stats, self.phasemap
        gc.collect()
        self.axes.clear()
        return
        
class Ui_PhClust_Dialog(object):
    def setupUi(self, PhClust_Dialog):
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.mapvar = ''
        self.mskVar = ''
        self.idx = 10
        self.names = []
        self.data = {}
        self.phasemap = []
        self.stats = {}
        
        PhClust_Dialog.setObjectName("PhClust_Dialog")
        PhClust_Dialog.resize(1551, 824)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PhClust_Dialog.sizePolicy().hasHeightForWidth())
        PhClust_Dialog.setSizePolicy(sizePolicy)
        PhClust_Dialog.setMaximumSize(QtCore.QSize(1551, 824))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/main_icon/16x16.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        PhClust_Dialog.setWindowIcon(icon)
        PhClust_Dialog.setWindowTitle("QACD-3b.Phase Cluster Edit") 

        
        self.widget_mpl = QtGui.QWidget(PhClust_Dialog)
        self.widget_mpl.setGeometry(QtCore.QRect(290, 10, 1251, 801))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_mpl.sizePolicy().hasHeightForWidth())
        self.widget_mpl.setSizePolicy(sizePolicy)
        self.mvl = QtGui.QVBoxLayout(self.widget_mpl)
        self.mvl.setMargin(0)
        self.sc = MplCanvas(self.widget_mpl, width=12.51,height=7.78,dpi=100)
        self.toolbar = NavigationToolbar(self.sc,self.widget_mpl, coordinates=True)
        self.mvl.addWidget(self.toolbar)
        self.mvl.addWidget(self.sc)
        self.widget_mpl.setFocus()

        self.widget = QtGui.QWidget(PhClust_Dialog)
        self.widget.setGeometry(QtCore.QRect(10, 11, 271, 643))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.gridLayout.setMargin(0)

        self.label_curph = QtGui.QLabel("Current Phase Value:",self.widget)
        self.gridLayout.addWidget(self.label_curph, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        
        self.spinBox_CurPh = QtGui.QSpinBox(self.widget)
        self.spinBox_CurPh.setReadOnly(True)
        self.spinBox_CurPh.setRange(0, 255)
        self.gridLayout.addWidget(self.spinBox_CurPh, 0, 2, 1, 1)
        
        self.listView_Phases = QtGui.QListWidget(self.widget)
        self.listView_Phases.itemClicked.connect(self.phase_select)
        self.gridLayout.addWidget(self.listView_Phases, 1, 0, 1, 3)
        
        self.lineEdit_Phname = QtGui.QLineEdit(self.widget)
        self.gridLayout.addWidget(self.lineEdit_Phname, 2, 0, 1, 2)                
        
        self.label_pha = QtGui.QLabel("Phase A:",self.widget)
        self.label_pha.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.gridLayout.addWidget(self.label_pha, 4, 0, 1, 1)        
        self.comboBox_pha = QtGui.QComboBox(self.widget)
        self.gridLayout.addWidget(self.comboBox_pha, 4, 1, 1, 2)
        
        self.label_phb = QtGui.QLabel("Phase B:",self.widget)
        self.label_phb.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.gridLayout.addWidget(self.label_phb, 5, 0, 1, 1)        
        self.comboBox_phb = QtGui.QComboBox(self.widget)
        self.gridLayout.addWidget(self.comboBox_phb, 5, 1, 1, 2)
        
        self.label_info = QtGui.QLabel("Phase Map Info:",self.widget)
        self.gridLayout.addWidget(self.label_info, 7, 0, 1, 3)
        
        self.tableWidget_info = QtGui.QTableWidget(self.widget)
        self.tableWidget_info.setColumnCount(0)
        self.tableWidget_info.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget_info, 8, 0, 1, 3)

        self.pushButton_Rename = QtGui.QPushButton("Rename",self.widget)
        self.pushButton_Rename.clicked.connect(self.ph_rename)
        self.gridLayout.addWidget(self.pushButton_Rename, 2, 2, 1, 1)
        
        self.pushButton_Create_Exit = QtGui.QPushButton("Create Phase Masks and Exit",self.widget)
        self.pushButton_Create_Exit.clicked.connect(self.phase_create)
        self.gridLayout.addWidget(self.pushButton_Create_Exit, 9, 0, 1, 3)
        
        self.pushButton_phmerge = QtGui.QPushButton("Merge Phase A into Phase B",self.widget)
        self.pushButton_phmerge.clicked.connect(self.ph_merge)
        self.gridLayout.addWidget(self.pushButton_phmerge, 6, 0, 1, 3)
        
        self.pushButton_Delete = QtGui.QPushButton("Delete the Selected Phase",self.widget)
        self.pushButton_Delete.clicked.connect(self.ph_delete)
        self.gridLayout.addWidget(self.pushButton_Delete, 3, 0, 1, 3)

        self.combo_populate()

        QtCore.QMetaObject.connectSlotsByName(PhClust_Dialog)
    def combo_populate(self):
        self.names = []
        self.data = {}
        self.pmap = []
        self.stats = {}
        self.names = self.sc.get_names()
        self.data = self.sc.get_data()
        self.stats = self.sc.get_stats()
        self.phasemap = self.sc.get_pmap()
        self.comboBox_pha.clear()
        self.comboBox_phb.clear()
        self.listView_Phases.clear()
        for item in self.names:
            self.comboBox_pha.addItem(item)
            self.comboBox_phb.addItem(item)
            self.listView_Phases.addItem(item)
        self.table_populate()
        return
    def table_populate(self):
        Length = len(self.names)
        self.tableWidget_info.setRowCount(Length+1)
        self.tableWidget_info.setColumnCount(3)
        self.tableWidget_info.horizontalHeader().setVisible(False)
        self.tableWidget_info.verticalHeader().setVisible(False)
        self.tableWidget_info.setItem(0,0,QtGui.QTableWidgetItem('PhaseMap'))
        ls = []
        for i in xrange(0,Length):
            j = i + 1
            var = self.names[i]
            pix = self.stats[var]
            self.tableWidget_info.setItem(j,0,QtGui.QTableWidgetItem(var))
            self.tableWidget_info.setItem(j,1,QtGui.QTableWidgetItem(str(pix)))
            self.tableWidget_info.setItem(j,2,QtGui.QTableWidgetItem('pixels'))
            ls.append(pix)
            print pix
        total = 0
        for item in ls:
            total = total + item
        print total
        self.stats['PhaseMap']=total
        self.tableWidget_info.setItem(0,1,QtGui.QTableWidgetItem(str(total)))
        self.tableWidget_info.setItem(0,2,QtGui.QTableWidgetItem('pixels'))
        self.tableWidget_info.resizeColumnToContents(0)
        self.tableWidget_info.resizeColumnToContents(1)
        print self.stats
        return        
    def phase_select(self, item):
        var = unicode(item.text(),'utf-8')
        print var
        self.mapvar = var
        self.lineEdit_Phname.setText(var)
        val = self.data[var]
        self.spinBox_CurPh.setValue(val)
        return        
    def ph_rename(self):
        self.mskVar = str(self.lineEdit_Phname.text())
        string = self.sc.rename_phase(self.mapvar,self.mskVar)
        print string
        self.combo_populate()
        print self.names
        print self.data
        return
    def ph_delete(self):
        print (str(self.mapvar) + " is to be deleted")
        string = self.sc.delete_phase(self.mapvar)
        print string
        self.combo_populate()
        print self.names
        print self.data
        return      
    def ph_merge(self):
        phA = unicode(self.comboBox_pha.currentText(),'utf-8')
        phB = unicode(self.comboBox_phb.currentText(),'utf-8')
        self.mapvar = phA
        string = self.sc.merge_phase(phA,phB)
        print string
        self.combo_populate()
        print self.names
        print self.data
        return
    def phase_create(self):
        f = tb.open_file("temp.h5",mode='a')
        varProj = f.get_node(f.root,"varProj").read()
        clust = f.get_node(f.root,"clust").read()
        tmp = f.root
        lis = tmp._v_children
        if 'nums' in lis.keys():
            nums = f.get_node(f.root,"nums").read()
            ftime = 'Yes'
        else: 
            ftime = 'No'
        f.close()
        f = tb.open_file(varProj,mode='a')
        Clust = f.root._f_get_child(clust)
        Pmp = Clust.PhaseMap
        pmap = self.sc.get_pmap()
        self.names = self.sc.get_names()
        self.data = self.sc.get_data()
        tp = Pmp._v_children
        if 'masks' in tp.keys():
            tmp = f.get_node(Pmp, 'masks')
            tmp._f_remove(recursive=True)
        else:
            print 'New node'
        Pmsk = f.create_group(Pmp,"masks")
        self.stats = {}
        ls = []
        filters = tb.Filters(complevel=5, complib='blosc')
        if 'Removed' in tp.keys():
            tmp = f.get_node(Pmp, 'Removed')
            tmp._f_remove(recursive=True)
        else:
            print 'New node'
        for item in self.names:
            if item == 'Removed':
                print 'Removed'
                val = self.data['Removed']
                f.create_array(Pmp,item,val)
            else:
                val = self.data[item]
                ds = pmap==val
                atom2 = tb.Atom.from_dtype(ds.dtype)
                dset = f.createCArray(Pmsk,item,atom2,ds.shape,filters=filters)
                dset[:] = ds
                num = np.sum(ds)
                ls.append(num)
                self.stats[item] = num
                dset.attrs.pixels = num
        total = 0
        for item in ls:
            total = total + item
        self.stats['PhaseMap']=total
        atom2 = tb.Atom.from_dtype(pmap.dtype)
        mp = f.createCArray(Pmsk,"PhaseMap",atom2,pmap.shape,filters=filters)
        mp[:] = pmap
        phasnum = len(self.names)
        mp.attrs.phasenum = phasnum
        mp.attrs.pixels = total
        log = f.get_node(f.root, "Log").read()
        import datetime
        string = datetime.datetime.now().strftime("%I:%M%p, %d %B %Y")
        log[9] = string
        if ftime == 'Yes':
            log[11] = nums
        else:
            print 'Not the first time...'
        f.remove_node(f.root, "Log")
        f.create_array(f.root, "Log", log)
        f.close()
        del self.stats, self.data, self.names, ls, log, total, pmap
        self.sc.closeFigure()
        del self.sc
        self.close()
        return

class DataHolder(object):
    def __init__(self):
        self.varProj = ''
        self.data = {}
        self.stats = {}
        self.names = []
        self.factor = 1.0
        self.load_data()
        self.clust = ''
        self.fname = ''
        self.dty = ''
        self.shapes = ()
        self.imag = 'something'
    def load_data(self):
        f = tb.open_file("temp.h5",mode='a')
        self.varProj = f.get_node(f.root,"varProj").read()
        self.clust = f.get_node(f.root,"clust").read()
        f.close()
        f = tb.open_file(self.varProj,mode='a')
        Clust = f.root._f_get_child(self.clust)
        Ph = Clust.PhaseMap
        self.fname = path.join(mkdtemp(),'pmap.dat')
        pm = f.get_node(Ph,'pmap').read()
        pm = pm + 1
        y, x = pm.shape[0], pm.shape[1]
        self.dty = pm.dtype
        vals = np.unique(pm)
        self.factor = 255/float(len(vals))
        self.shapes = (y, x)
        self.phasemap = np.memmap(self.fname,dtype=self.dty,mode='w+',shape=(y,x))
        self.phasemap[:] = pm[:]
        del pm
        gc.collect()
        del gc.garbage[:]
        for i in xrange(0,(len(vals)+1)):
            if i == 0:
                phname = "Removed"
                self.names.append(phname)
            else:
                phname = "Phase " + str(i)            
                self.names.append(phname)
        Length = len(self.names)
        for i in xrange(0,Length):
            if i == 0:
                name = self.names[i]
                self.data[name] = 0
                self.stats[name] = 0
            else:
                name = self.names[i]
                val = i*self.factor
                ds = self.phasemap==i
                pix = np.sum(ds)
                self.stats[name]=pix
                self.data[name]=val
        f.close()
        self.phasemap = self.phasemap*self.factor
    def get_series_data(self):
        del self.imag
        tmp = self.phasemap.astype(int)
        self.imag = self.imresize(tmp)
        return self.imag
    def imresize(self, im):
        im2 = Image.fromarray(np.uint8(cm.nipy_spectral(im, bytes=True)))
        x,y = im2.size[0],im2.size[1]
        sz = (1250,int((1250.0/x)*y))
        stm = im2.resize(sz)
        return stm
    def get_factor(self):
        return self.factor
    def get_names(self):
        return self.names
    def get_pmap(self):
        return self.phasemap
    def get_datdic(self):
        return self.data
    def get_statdic(self):
        return self.stats
    def merge_phase(self,phA,phB):
        valA = self.data[phA]
        valB = self.data[phB]
        self.phasemap[self.phasemap ==valA] = valB
        self.phasemap.flush()
        self.data.pop(phA)
        s=self.stats[phA]
        t=self.stats[phB]
        tmp = s+t
        self.stats.pop(phA)
        self.stats.pop(phB)
        self.stats[phB]=tmp
        tpN = self.names
        self.names = []
        for i in xrange(0,len(tpN)):
            var = tpN[i]
            if var == phA:
                print 'Phase Merged'
            else:
                self.names.append(var)
            print var
        return
    def rename_phase(self,mapvar,mskVar):
        for i in xrange(0,len(self.names)):
            var = self.names[i]
            if var == mapvar:
                self.names[i] = mskVar
            else:
                print var
        print self.names
        tmp = self.data[mapvar]
        self.data.pop(mapvar)
        self.data[mskVar] = tmp
        tmp = self.stats[mapvar]
        self.stats.pop(mapvar)
        self.stats[mskVar] = tmp
        return
    def delete_phase(self,mapvar):
        v = self.data[mapvar]
        self.phasemap[self.phasemap == v] = 0.0
        self.phasemap.flush()   
        self.data.pop(mapvar)
        self.stats.pop(mapvar)
        tpN = self.names
        self.names = []
        for i in xrange(0,len(tpN)):
            var = tpN[i]
            if var == mapvar:
                print 'Phase Removed'
            else:
                self.names.append(var)
            print var
        ds = self.phasemap==0
        pix = np.sum(ds)
        print  pix
        self.stats.pop('Removed')
        self.stats['Removed']=pix
        print np.sum(self.phasemap[self.phasemap==v])
        return
        
import ProjectManager_rc

if __name__=='_main__':
    app = QtGui.QApplication(sys.argv)
    myDialog = QtGui.QDialog()
    ui = Ui_PhClust_Dialog()
    ui.setupUi(myDialog)
    myDialog.show()
    sys.exit(app.exec_())
