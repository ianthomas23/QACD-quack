# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Phase_Dialog.ui'
#
# Created: Wed Jan 20 14:16:25 2016
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from matplotlib.figure import Figure
from tempfile import mkdtemp
import os.path as path
import matplotlib.cm as cm
import tables as tb
import numpy as np
import gc
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas,NavigationToolbar2QT as NavigationToolbar)
import matplotlib.style as mps
#mps.use('qacd_xmap')

class MyMplCanvas(FigureCanvas):
    def __init__(self,parent=None,width=10,height=6,dpi=100):
        #mps.use('qacd_xmap')
        fig = Figure(figsize=(width,height),dpi=dpi)
        self.axes = fig.add_subplot(111)
        #we want the axes cleared every time plot() is called
        self.axes.hold(False)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.compute_initial_figure()
    def compute_initial_figure(self):
        pass
class MplCanvas_hist(MyMplCanvas):
    def compute_initial_figure(self):
        self.imagelims = {}
        self.data = DataHolder()
        self.mapnames = self.data.get_maplist()
        self.curmap = 'Some'
        self.my_cmap = cm.gnuplot
        self.my_cmap.set_under('k', alpha=0)
        self.my_cmap.set_over('k', alpha=0)
        name = self.mapnames[0]
        self.curmap = name
        ds = self.data.get_series_data(name)
        mini = np.nanmin(ds)
        maxi = np.nanmax(ds)
        tmp = [mini, maxi]
        self.imagelims[name]=tmp
        self.im = self.axes.imshow(ds, cmap=self.my_cmap, interpolation='nearest')
        self.im.set_label(name)
        self.im.set_clim(tmp)
        self.im._remove_method = lambda a:self.axes.images.remove(a)
        print str(name)
        global cb
        divider = make_axes_locatable(self.axes)
        fig = self.axes.get_figure()
        cax = divider.append_axes('right',size='5%', pad=0.04)
        cb = self.figure.colorbar(self.im, cax=cax)
        cb.ax.tick_params(labelsize=10)
        fig.tight_layout()
        fig.canvas.draw()
        return
    def get_image_labels(self):
        return self.mapnames
    def get_statlist(self):
        stats = self.data.get_statlist
        return stats
    def get_current_image_lims(self, name):
        imlims = self.imagelims[name]
        return imlims
    def get_imagelims(self):
        return self.imagelims
    def change_map(self, name):
        ds = self.data.get_series_data(name)
        mini = np.nanmin(ds)
        maxi = np.nanmax(ds)
        tmp = [mini, maxi]
        self.imagelims[name]=tmp
        global im
        self.im.set_data(ds)
        self.im.set_label(name)
        self.im.set_clim(tmp)
        print str(name)
        fig = self.axes.get_figure()
        cb.update_bruteforce(self.im)
        fig.tight_layout()
        fig.canvas.draw()
        print "Map changed"
        self.curmap = name
        return tmp
    def update_lims(self, name, lims):
        self.im.set_clim(lims)
        self.imagelims.pop(name)
        self.imagelims[name]=lims
        fig = self.axes.get_figure()
        cb.update_bruteforce(self.im)
        fig.canvas.draw()
        return
    def del_data(self):
        self.data.del_data()
        self.im.remove()
        self.axes.clear()
        del self.data, self.imagelims, self.mapnames, self.curmap, self.my_cmap,  self.im
        del self.axes
        gc.collect()
        self.close()
        return
class Ui_Phase_Dialog(object):
    valueChanged = QtCore.pyqtSignal(int)
    sliderReleased = QtCore.pyqtSignal(int)
    def setupUi(self, Dialog):
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.fig_lims = {}
        self.varmax = ''
        self.varmin2 = ''
        self.varmax2 = ''
        self.varmin = ''
        self.ells = []
        self.mapvar = ''
        self.varProj = ''
        self.statdic = {}

        self.threshDic = {}
        self.threshCount = 0
        self.counter = 0
        self.Thcheck = {}

        Dialog.setObjectName("Dialog")
        Dialog.resize(1528, 827)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        Dialog.setWindowTitle("QACD- 3.Phase Thresholding")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/main_icon/16x16.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)

        self.mplwindow = QtGui.QWidget(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mplwindow.sizePolicy().hasHeightForWidth())
        self.mplwindow.setSizePolicy(sizePolicy)
        self.mplvl = QtGui.QVBoxLayout(self.mplwindow)
        self.mplvl.setMargin(0)
        self.sc = MplCanvas_hist(self.mplwindow, width=11.5,height=6.5,dpi=100)
        self.toolbar = NavigationToolbar(self.sc,self.mplwindow, coordinates=True)
        self.mplvl.addWidget(self.toolbar)
        self.mplvl.addWidget(self.sc)
        self.gridLayout.addWidget(self.mplwindow, 0, 0, 7, 4)

        self.label_Maps = QtGui.QLabel("Element Maps:",Dialog)
        self.gridLayout.addWidget(self.label_Maps, 0, 4, 1, 1)

        self.first_plot()

        self.mplfigs = QtGui.QListWidget(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mplfigs.sizePolicy().hasHeightForWidth())
        self.mplfigs.setSizePolicy(sizePolicy)
        self.mplfigs.setMaximumSize(QtCore.QSize(256, 192))
        self.gridLayout.addWidget(self.mplfigs, 1, 4, 1, 2)

        self.mplfigs.itemClicked.connect(self.changemap)

        self.list_pop()

        self.label_SelMapDet = QtGui.QLabel("Selected Map Details:",Dialog)
        self.gridLayout.addWidget(self.label_SelMapDet, 2, 4, 1, 2)

        self.textBrowser_Details = QtGui.QPlainTextEdit(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser_Details.sizePolicy().hasHeightForWidth())
        self.textBrowser_Details.setSizePolicy(sizePolicy)
        self.textBrowser_Details.setMaximumSize(QtCore.QSize(256, 192))
        self.textBrowser_Details.setReadOnly(True)
        self.gridLayout.addWidget(self.textBrowser_Details, 3, 4, 1, 2)

        self.label_ThreshTb = QtGui.QLabel("Thresholded Map Values:",Dialog)
        self.gridLayout.addWidget(self.label_ThreshTb, 4, 4, 1, 2)

        self.First_Figure()
        Length = len(self.ells)

        self.tableWidget_Thresh = QtGui.QTableWidget(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget_Thresh.sizePolicy().hasHeightForWidth())
        self.tableWidget_Thresh.setSizePolicy(sizePolicy)
        self.tableWidget_Thresh.setMaximumSize(QtCore.QSize(256, 192))
        self.tableWidget_Thresh.setRowCount(Length)
        self.tableWidget_Thresh.setColumnCount(3)
        item = QtGui.QTableWidgetItem("Map")
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget_Thresh.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem("Lower")
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget_Thresh.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem("Upper")
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget_Thresh.setHorizontalHeaderItem(2, item)
        self.tableWidget_Thresh.horizontalHeader().setDefaultSectionSize(80)
        self.tableWidget_Thresh.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.tableWidget_Thresh, 5, 4, 1, 2)

        self.pushButton_UpdateTb = QtGui.QPushButton("Update Current Threshold Values",Dialog)
        self.gridLayout.addWidget(self.pushButton_UpdateTb, 6, 4, 1, 2)
        self.pushButton_UpdateTb.clicked.connect(self.get_thresh)

        self.label_2 = QtGui.QLabel("Upper:",Dialog)
        self.gridLayout.addWidget(self.label_2, 7, 0, 1, 1)
        self.horizontalSlider = QtGui.QSlider(Dialog)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.horizontalSlider.setRange(self.varmin, self.varmax)
        self.horizontalSlider.setValue(self.varmax)
        self.horizontalSlider.setSingleStep(1)
        self.gridLayout.addWidget(self.horizontalSlider, 7, 1, 1, 1)
        self.lineEdit_upper = QtGui.QLineEdit(Dialog)
        self.lineEdit_upper.setText(str(self.varmax))
        self.lineEdit_upper.setReadOnly(True)
        self.gridLayout.addWidget(self.lineEdit_upper, 7, 2, 1, 1)

        self.label_3 = QtGui.QLabel("Lower:",Dialog)
        self.gridLayout.addWidget(self.label_3, 8, 0, 1, 1)
        self.horizontalSlider_2 = QtGui.QSlider(Dialog)
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.horizontalSlider_2.setRange(self.varmin, self.varmax)
        self.horizontalSlider_2.setValue(self.varmin)
        self.horizontalSlider_2.setSingleStep(1)
        self.gridLayout.addWidget(self.horizontalSlider_2, 8, 1, 1, 1)
        self.lineEdit_lower = QtGui.QLineEdit(Dialog)
        self.lineEdit_lower.setText(str(self.varmin))
        self.lineEdit_lower.setReadOnly(True)
        self.gridLayout.addWidget(self.lineEdit_lower, 8, 2, 1, 1)

        self.horizontalSlider.sliderReleased.connect(self.maxSlider)
        self.lineEdit_upper.connect(self.horizontalSlider,QtCore.SIGNAL('valueChanged(int)'), self.Upper_Label)
        self.horizontalSlider_2.sliderReleased.connect(self.minSlider)
        self.lineEdit_lower.connect(self.horizontalSlider_2,QtCore.SIGNAL('valueChanged(int)'), self.Lower_Label)

        spacerItem = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 7, 3, 1, 1)

        self.label_6 = QtGui.QLabel("Name your phase:",Dialog)
        self.gridLayout.addWidget(self.label_6, 7, 4, 1, 1)

        self.lineEdit = QtGui.QLineEdit(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMaximumSize(QtCore.QSize(144, 16777215))
        self.gridLayout.addWidget(self.lineEdit, 7, 5, 1, 1)

        self.pushButton_CreatePhase = QtGui.QPushButton("Exit and Create New Phase Mask",Dialog)
        self.gridLayout.addWidget(self.pushButton_CreatePhase, 8, 4, 1, 2)
        self.gridLayout.setColumnStretch(1, 1)
        self.pushButton_CreatePhase.clicked.connect(self.calculate_ph)

        QtCore.QMetaObject.connectSlotsByName(Dialog)

        f = tb.open_file("temp.h5",mode='a')
        self.varProj = f.get_node(f.root,"varProj").read()
        f.close()
        f = tb.open_file(self.varProj, mode='a')
        Filt = f.root.Filtered
        self.statdic = {}
        for item in self.ells:
            tp = f.get_node(Filt, item)
            st = tp.attrs.stats
            self.statdic[item]=st
        print self.statdic
        f.close()
        self.Map_Stat()
    def list_pop(self):
        for i in xrange(0, len(self.ells)):
            var = self.ells[i]
            self.Thcheck[var] = 0
            self.mplfigs.addItem(var)
        return
    def first_plot(self):
        self.ells = self.sc.get_image_labels()
        return
    def Map_Stat(self):
        Stats = self.statdic[self.mapvar]
        self.textBrowser_Details.setPlainText(Stats)
        print 'tried it'
        return
    def calculate_ph(self):
        phase = str(self.lineEdit.text())
        f = tb.open_file("temp.h5",mode='a')
        self.varProj = f.get_node(f.root,"varProj").read()
        f.close()
        import qacd_thresholding as qdt
        strn = qdt.worker2(self.threshDic, self.varProj, phase)
        print strn
        f = tb.open_file(self.varProj, mode='a')
        log = f.get_node(f.root, "Log").read()
        import datetime
        string = datetime.datetime.now().strftime("%I:%M%p, %d %B %Y")
        log[9] = string
        var = log[10]
        if var == 'N/A':
            log[10] = str(1)
            log[12] = str(1)
        else:
            var2 = int(var) + 1
            log[10] = str(var2)
            log[12] = str(var2)
        print log
        f.remove_node(f.root, "Log")
        f.create_array(f.root, "Log", log)
        f.close()
        self.sc.del_data()
        del self.sc
        gc.collect()
        self.close()
    def get_thresh(self):
        low = self.lineEdit_lower.text()
        low = float(low)
        up = self.lineEdit_upper.text()
        up = float(up)
        var = self.mapvar
        lim = [low, up]
        self.fig_lims.pop(var)
        self.fig_lims[var]=lim
        tck = self.Thcheck[var]
        if tck == 0:
            self.Thcheck.pop(var)
            self.Thcheck[var]=self.threshCount
            tmp = {'max':up, 'min':low}
            self.threshDic[var]=tmp
            print self.threshDic
            self.tableWidget_Thresh.setItem(self.threshCount,0, QtGui.QTableWidgetItem(var))
            self.tableWidget_Thresh.setItem(self.threshCount,1, QtGui.QTableWidgetItem(self.lineEdit_lower.text()))
            self.tableWidget_Thresh.setItem(self.threshCount,2, QtGui.QTableWidgetItem(self.lineEdit_upper.text()))
            self.threshCount = self.threshCount + 1
        else:
            self.Thcheck.pop(var)
            self.Thcheck[var]=tck
            tmp = {'max':up, 'min':low}
            self.threshDic[var]=tmp
            print self.threshDic
            self.tableWidget_Thresh.setItem(tck,0, QtGui.QTableWidgetItem(var))
            self.tableWidget_Thresh.setItem(tck,1, QtGui.QTableWidgetItem(self.lineEdit_lower.text()))
            self.tableWidget_Thresh.setItem(tck,2, QtGui.QTableWidgetItem(self.lineEdit_upper.text()))
        return
    def maxSlider(self):
        self.varmax = self.horizontalSlider.value() / float(1)
        if self.counter is not 0:
            self.update_plt()
        else:
            print 'No update'
        return
    def minSlider(self):
        self.varmin = self.horizontalSlider_2.value() / float(1)
        if self.counter is not 0:
            self.update_plt()
        else:
            print 'No update'
        return
    def Lower_Label(self, int):
        vp=str(int)
        self.lineEdit_lower.setText(vp)
        return
    def Upper_Label(self, int):
        vp=str(int)
        self.lineEdit_upper.setText(vp)
        return
    def update_plt(self):
        lims = [self.varmin, self.varmax]
        name = self.mapvar
        self.sc.update_lims(name, lims)
    def First_Figure(self):
        self.mapvar = self.ells[0]
        lims = self.sc.get_current_image_lims(self.mapvar)
        self.fig_lims[self.mapvar]=lims
        self.varmin = lims[0]
        self.varmax = lims[1]
        self.counter = self.counter + 1
        return
    def changemap(self,item):
        #self.sc.new_map()
        var = str(item.text())
        self.mapvar = var
        print self.mapvar
        lims = self.sc.change_map(self.mapvar)
        self.varmin = lims[0]
        self.varmax = lims[1]
        self.fig_lims[var] = lims
        self.horizontalSlider.setRange(self.varmin, self.varmax)
        self.horizontalSlider.setValue(self.varmax)
        self.horizontalSlider_2.setRange(self.varmin, self.varmax)
        self.horizontalSlider_2.setValue(self.varmin)
        self.counter = 0
        self.counter = self.counter + 1
        self.Map_Stat()
        return
class DataHolder(object):
    def __init__(self):
        self.varProj = ''
        self.names = []
        self.stats = {}
        self.load_data()
    def load_data(self):
        f = tb.open_file("temp.h5",mode='a')
        self.varProj = f.get_node(f.root,"varProj").read()
        f.close()
        f = tb.open_file(self.varProj,mode='a')
        Filt = f.root.Filtered
        Para = f.root.parameters
        self.names = f.get_node(Para, "ElementList").read()

        for i in xrange(0, len(self.names)):
            item = self.names[i]
            d = f.get_node(Filt,item)
            self.stats[item]=str(d.attrs.stats)
        item = str(self.names[0])
        fname = path.join(mkdtemp(),'map.dat')
        d = f.get_node(Filt,item)
        ds = d.read()
        #print("==> CHECK", ds)
        #ds[np.isinf(ds)]=np.nan
        y, x = ds.shape[0], ds.shape[1]
        dty = ds.dtype
        dsx = np.memmap(fname,dtype=dty,mode='w+',shape=(y,x))
        dsx[:] = ds[:]
        del ds
        f.close()
        return dsx
    def get_maplist(self):
        return self.names
    def get_statlist(self):
        return self.stats
    def get_series_data(self,name):
        f = tb.open_file(self.varProj,mode='a')
        Filt = f.root.Filtered
        fname = path.join(mkdtemp(),'map.dat')
        d = f.get_node(Filt,name)
        ds = d.read()
        #ds[np.isinf(ds)]=np.nan
        self.stats=str(d.attrs.stats)
        y, x = ds.shape[0], ds.shape[1]
        dty = ds.dtype
        dsx = np.memmap(fname,dtype=dty,mode='w+',shape=(y,x))
        dsx[:] = ds[:]
        del ds
        f.close()
        return dsx
    def del_data(self):
        del self.varProj, self.names, self.stats
        return

import ProjectManager_rc

if __name__=='_main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    myDialog = QtGui.QDialog()
    ui = Ui_Phase_Dialog()
    ui.setupUi(myDialog)
    myDialog.show()
    sys.exit(app.exec_())

