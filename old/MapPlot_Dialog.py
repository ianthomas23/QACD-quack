# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Plot_Dialog.ui'
#
# Created: Tue Jan 26 17:02:56 2016
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!


from PyQt4 import QtCore, QtGui
from matplotlib.figure import Figure
import matplotlib.cm as cm
from mpl_toolkits.axes_grid1 import make_axes_locatable
import tables as tb
import numpy as np
import sys
import gc
from tempfile import mkdtemp
import os.path as path
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import utils

utils.set_style()

class MyMplCanvas(FigureCanvas):
    def __init__(self,parent=None,width=10,height=6,dpi=100):
        fig = Figure(figsize=(width,height),dpi=dpi)
        self.axes = fig.add_subplot(111)
        #we want the axes cleared every time plot() is called
        self.axes.hold(False)
        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
    def compute_initial_figure(self):
        pass

class MplCanvas_hist(MyMplCanvas):
    def compute_initial_figure(self):
        f = tb.open_file('figtemp.h5',mode='a')
        self.varProj = f.get_node(f.root,'varProj').read()
        self.mapvar = f.get_node(f.root,'mapvar').read()
        tr = f.get_node(f.root,'phase').read()
        self.phase = str(tr)
        self.autoth = f.get_node(f.root, 'threshold').read()
        self.string = f.get_node(f.root, 'string').read()
        self.dataset = f.get_node(f.root,'dataset').read()
        self.datagroup = f.get_node(f.root,'datagrp').read()
        f.close()
        f = tb.open_file(self.varProj,mode='a')
        ells = f.get_node(f.root.parameters,'ElementList').read()
        self.annot = "Some"
        self.title = 'Some'
        if self.dataset == 'Phase':
            data = self.data_ret()
        else:
            data = self.data_ret2()
        print data
        self.PixSize, self.pixun = self.pix_ret()

        self.my_cmap = cm.get_cmap('gnuplot')
        self.my_cmap.set_under('k', alpha=0)
        self.my_cmap.set_over('k', alpha=0)

        if self.mapvar in ells:
            im1 = self.axes.imshow(data,cmap=self.my_cmap,interpolation='nearest', aspect='equal')
            self.axes.set_title(self.title)
            fig = self.axes.get_figure()
            divider = make_axes_locatable(self.axes)
            cax = divider.append_axes("right", size="3%", pad=0.1)
            fig.colorbar(im1,cax=cax)
            fig.tight_layout()
        elif self.autoth == 0:
            im1 = self.axes.imshow(data,cmap=self.my_cmap,vmin=0, vmax=1.0, interpolation='nearest',aspect='equal')
            self.axes.set_title(self.title)
            fig = self.axes.get_figure()
            divider = make_axes_locatable(self.axes)
            cax = divider.append_axes("right", size="3%", pad=0.1)
            cb = fig.colorbar(im1,cax=cax)
            cb.set_clim(0.0, 1.0)
            cb.ax.tick_params(labelsize=10)
            fig.tight_layout()
        elif self.autoth == 1:
            mx, mn = np.nanmax(data), np.nanmin(data)
            im1 = self.axes.imshow(data,cmap=self.my_cmap,vmin=mn, vmax=mx, interpolation='nearest',aspect='equal')
            self.axes.set_title(self.title)
            fig = self.axes.get_figure()
            divider = make_axes_locatable(self.axes)
            cax = divider.append_axes("right", size="3%", pad=0.1)
            fig.colorbar(im1,cax=cax)
            fig.tight_layout()

        xmin,xmax = self.axes.get_xlim()
        ymin,ymax = self.axes.get_ylim()
        xstep = ((xmax+0.5) / 5.0)
        ystep = ((ymin+0.5) / 4.0)
        xticks = np.arange(xmin,(xmax + xstep), xstep)
        yticks = np.arange(ymin,(ymax - ystep), -ystep)
        self.axes.yaxis.set_ticks_position('left')
        self.axes.xaxis.set_ticks_position('bottom')
        self.axes.xaxis.set_ticks(xticks)
        self.axes.yaxis.set_ticks(yticks)
        Length = len(xticks)
        Length2 = len(yticks)
        xlabels = ['Some']*Length
        ylabels = ['Some']*Length2
        xlabels[0] = '0' + str(self.pixun)
        for i in xrange(1,Length):
            val = xticks[i]
            val = int(val*self.PixSize)
            print val
            string = str(val) + str(self.pixun)
            xlabels[i]=string
        print xlabels
        for i in xrange(0,Length2):
            if i == (Length2-1):
                ylabels[i] = '0' + str(self.pixun)
            else:
                val = yticks[i]
                val = int(val*self.PixSize)
                print val
                string = str(val) + str(self.pixun)
                ylabels[i]=string
        print ylabels
        fig.canvas.draw()
        self.axes.set_xticklabels(xlabels)
        self.axes.set_yticklabels(ylabels)
        self.axes.tick_params(labelsize=12)
    def closeFigure(self):
        del self.varProj, self.mapvar, self.phase, self.dataset, self.annot, self.title
        self.axes.clear()
        gc.collect()
        self.close()
        return
    def pix_ret(self):
        f = tb.open_file(self.varProj,mode='a')
        pxsz = f.get_node(f.root,'PixSize').read()
        PixSize = float(pxsz[0])
        pxun = pxsz[1]
        f.close()
        print PixSize, pxun
        return PixSize, pxun
    def data_ret(self):
        if self.phase == 'No Phase':
            f = tb.open_file(self.varProj,mode='a')
            Filt = f.root._f_get_child(self.datagroup)
            tp = f.get_node(Filt,self.mapvar)
            fname = path.join(mkdtemp(),'pmap.dat')
            dsm = tp.read()
            dsm[np.isnan(dsm)]=0
            dsm[np.isnan(dsm)]=0
            dsm[np.isinf(dsm)]=0
            y, x = dsm.shape[0], dsm.shape[1]
            dty = dsm.dtype
            dsx = np.memmap(fname,dtype=dty,mode='w+',shape=(y,x))
            dsx[:] = dsm[:]
            del dsm
            self.title = ('Map of ' + str(self.mapvar))
            f.close()
            return dsx
        else:
            f = tb.open_file(self.varProj,mode='a')
            Filt = f.root._f_get_child(self.datagroup)
            tp = f.get_node(Filt,self.mapvar)
            fname = path.join(mkdtemp(),'pmap.dat')
            ds = tp.read()
            ds[np.isnan(ds)]=0
            if self.string == 'phase':
                ds.fill(1)
                self.title = ('Map of ' + str(self.phase))
            else:
                self.title = ('Map of ' + str(self.mapvar) + ' in ' + str(self.phase))
            print self.title
            tm = f.get_node(f.root.Phase,self.phase)
            mask = tm.read()
            dsm = ds/mask
            del ds
            dsm[np.isnan(dsm)]=np.nan
            dsm[np.isinf(dsm)]=np.nan
            y, x = dsm.shape[0], dsm.shape[1]
            dty = dsm.dtype
            dsx = np.memmap(fname,dtype=dty,mode='w+',shape=(y,x))
            dsx[:] = dsm[:]
            del dsm
            f.close()
            return dsx
        print dsx
        return dsx
    def data_ret2(self):
        if self.phase == 'No Phase':
            f = tb.open_file(self.varProj,mode='a')
            Filt = f.root._f_get_child(self.datagroup)
            tp = f.get_node(Filt,self.mapvar)
            fname = path.join(mkdtemp(),'pmap.dat')
            dsm = tp.read()
            dsm[np.isnan(dsm)]=0
            dsm[np.isnan(dsm)]=0
            dsm[np.isinf(dsm)]=0
            y, x = dsm.shape[0], dsm.shape[1]
            dty = dsm.dtype
            dsx = np.memmap(fname,dtype=dty,mode='w+',shape=(y,x))
            dsx[:] = dsm[:]
            del dsm
            self.title = ('Map of ' + str(self.mapvar))
            f.close()
            return dsx
        else:
            f = tb.open_file(self.varProj,mode='a')
            Filt = f.root._f_get_child(self.datagroup)
            tp = f.get_node(Filt,self.mapvar)
            fname = path.join(mkdtemp(),'pmap.dat')
            ds = tp.read()
            ds[np.isnan(ds)]=0
            if self.string == 'phase':
                ds.fill(1)
                self.title = ('Map of ' + str(self.phase))
            else:
                self.title = ('Map of ' + str(self.mapvar) + ' in ' + str(self.phase))
            print self.title
            grp = f.root._f_get_child(self.dataset)
            grp2 = grp._f_get_child('PhaseMap')
            Phase = grp2._f_get_child('masks')
            tm = f.get_node(Phase,self.phase)
            mask = tm.read()
            dsm = ds/mask
            del ds
            dsm[np.isnan(dsm)]=np.nan
            dsm[np.isinf(dsm)]=np.nan
            y, x = dsm.shape[0], dsm.shape[1]
            dty = dsm.dtype
            dsx = np.memmap(fname,dtype=dty,mode='w+',shape=(y,x))
            dsx[:] = dsm[:]
            del dsm
            f.close()
            return dsx
        print dsx
        return dsx

class MplWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        canvas = MplCanvas_hist()
        self.vbl = QtGui.QVBoxLayout()
        self.vbl.addWidget(canvas)
        self.setLayout(self.vbl)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        f = tb.open_file('figtemp.h5',mode='a')
        self.varProj = f.get_node(f.root,'varProj').read()
        self.mapvar = f.get_node(f.root,'mapvar').read()
        self.string = f.get_node(f.root,'string').read()
        self.phase = f.get_node(f.root,'phase').read()
        self.autoth2 = f.get_node(f.root, 'threshold').read()
        self.phase = str(self.phase)
        self.dataset = f.get_node(f.root,'dataset').read()
        self.datagroup = f.get_node(f.root,'datagrp').read()
        self.formats = ['png','pdf','ps','svg']
        f.close()
        self.statck = 0
        self.titleck = 1
        self.fmtvar = ''

        Dialog.setObjectName("Dialog")
        Dialog.resize(1022, 742)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/main_icon/16x16.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setWindowTitle("QACD- Figure 1")

        self.mplwidget = QtGui.QWidget(self)
        self.mplwidget.setGeometry(QtCore.QRect(10, 0, 1000, 600))
        self.mvl = QtGui.QVBoxLayout(self.mplwidget)
        self.sc = MplCanvas_hist(self.mplwidget, width=10,height=6,dpi=100)
        self.mvl.addWidget(self.sc)
        self.mplwidget.setFocus()


        self.widget = QtGui.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(15, 600, 991, 131))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)

        font2 = QtGui.QFont()
        font2.setUnderline(True)
        #Options Labels
        self.label_ExpSet = QtGui.QLabel("Export Settings",self.widget)
        font1 = QtGui.QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setUnderline(True)
        font1.setWeight(50)
        self.label_ExpSet.setFont(font1)
        self.gridLayout.addWidget(self.label_ExpSet, 0, 0, 1, 3)

        #Width objects
        self.label_Wid = QtGui.QLabel("Width (in):",self.widget)
        self.label_Wid.setFont(font2)
        self.gridLayout.addWidget(self.label_Wid, 1, 0, 1, 1)
        self.doubleSpinBox_wid = QtGui.QDoubleSpinBox(self.widget)
        self.doubleSpinBox_wid.setDecimals(1)
        self.doubleSpinBox_wid.setSingleStep(0.1)
        self.doubleSpinBox_wid.setValue(10.0)
        self.gridLayout.addWidget(self.doubleSpinBox_wid, 1, 1, 1, 1)
        #Height objects
        self.label_Het = QtGui.QLabel("Height (in):",self.widget)
        self.label_Het.setFont(font2)
        self.gridLayout.addWidget(self.label_Het, 1, 2, 1, 1)
        self.doubleSpinBox_Het = QtGui.QDoubleSpinBox(self.widget)
        self.doubleSpinBox_Het.setDecimals(1)
        self.doubleSpinBox_Het.setSingleStep(0.1)
        self.doubleSpinBox_Het.setValue(6.0)
        self.gridLayout.addWidget(self.doubleSpinBox_Het, 1, 3, 1, 1)
        #DPI objects
        self.label_DPI = QtGui.QLabel("Figure Resolution (DPI):",self.widget)
        self.label_DPI.setFont(font2)
        self.gridLayout.addWidget(self.label_DPI, 1, 4, 1, 2)
        self.spinBox_DPI = QtGui.QSpinBox(self.widget)
        self.spinBox_DPI.setRange(0,900)
        self.spinBox_DPI.setValue(300)
        self.gridLayout.addWidget(self.spinBox_DPI, 1, 6, 1, 1)
        #Filename objects
        self.label_fname = QtGui.QLabel("File name:",self.widget)
        self.label_fname.setFont(font2)
        self.label_fname.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_fname = QtGui.QLineEdit(self.widget)
        self.gridLayout.addWidget(self.lineEdit_fname, 1, 12, 1, 1)
        #File format objects
        self.label_Format = QtGui.QLabel("Format:",self.widget)
        self.label_Format.setFont(font2)
        self.label_Format.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_Format.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_Format, 1, 7, 1, 1)
        self.comboBox_format = QtGui.QComboBox(self.widget)
        self.comboBox_format.activated[str].connect(self.formatBox)
        self.gridLayout.addWidget(self.comboBox_format, 1, 8, 1, 2)
        #Stats Boxes
        self.checkBox_Stats = QtGui.QCheckBox("Stats Annotation",self.widget)
        self.gridLayout.addWidget(self.checkBox_Stats, 2, 0, 1, 2)
        self.checkBox_Stats.toggled.connect(self.StatCheck)
        self.checkBox_Stats.setDisabled(True)
        self.label_StatOptions = QtGui.QLabel("Options:",self.widget)
        self.label_StatOptions.setFont(font2)
        self.gridLayout.addWidget(self.label_StatOptions, 2, 2, 1, 1)
        self.checkBox_Pix = QtGui.QCheckBox("Pixels (N)",self.widget)
        self.checkBox_Pix.setDisabled(True)
        self.gridLayout.addWidget(self.checkBox_Pix, 2, 3, 1, 2)
        self.checkBox_Mean = QtGui.QCheckBox("Mean",self.widget)
        self.checkBox_Mean.setDisabled(True)
        self.gridLayout.addWidget(self.checkBox_Mean, 2, 5, 1, 1)
        self.checkBox_Median = QtGui.QCheckBox("Median",self.widget)
        self.checkBox_Median.setDisabled(True)
        self.gridLayout.addWidget(self.checkBox_Median, 2, 7, 1, 1)
        self.checkBox_Std = QtGui.QCheckBox("Standard Deviation",self.widget)
        self.checkBox_Std.setDisabled(True)
        self.gridLayout.addWidget(self.checkBox_Std, 2, 9, 1, 4)
        #Title Objects
        self.lineEdit_Title = QtGui.QLineEdit(self.widget)
        self.lineEdit_Title.setEnabled(True)
        self.gridLayout.addWidget(self.lineEdit_Title, 3, 3, 1, 6)
        self.checkBox_Title = QtGui.QCheckBox("Include Figure Title",self.widget)
        self.checkBox_Title.toggled.connect(self.TitleCheck)
        self.checkBox_Title.setChecked(True)
        self.gridLayout.addWidget(self.checkBox_Title, 3, 0, 1, 2)
        self.label_Title = QtGui.QLabel("Figure Title:",self.widget)
        self.label_Title.setFont(font2)
        self.gridLayout.addWidget(self.label_Title, 3, 2, 1, 1)
        #Export Buttons
        self.pushButton_Export = QtGui.QPushButton("Export Figure with the Above Settings",self.widget)
        self.pushButton_Export.clicked.connect(self.FigureExport)
        self.gridLayout.addWidget(self.pushButton_Export, 3, 10, 1, 3)

        self.gridLayout.addWidget(self.label_fname, 1, 10, 1, 2)
        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setRowStretch(2, 1)
        self.gridLayout.setRowStretch(3, 1)
        #Spacers
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 9, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 10, 1, 1)

        for item in self.formats:
            self.comboBox_format.addItem(item)
        index = self.comboBox_format.findText('pdf')
        self.comboBox_format.setCurrentIndex(index)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def FigureExport(self):
        figtitle = str(self.lineEdit_Title.text())
        filetitle = str(self.lineEdit_fname.text())+"_map"
        filefmt = str(self.comboBox_format.currentText())
        height = float(self.doubleSpinBox_Het.value())
        width = float(self.doubleSpinBox_wid.value())
        dpi = int(self.spinBox_DPI.value())
        self.fmtvar = str(self.comboBox_format.currentText())
        Settings = dict(figtitle=figtitle,filetitle=filetitle, threshold=self.autoth2,
                        filefmt=filefmt,height=height,width=width,options=self.statck,
                        dpi=dpi,varProj=self.varProj,phase=str(self.phase),
                        mapvar=str(self.mapvar), dataset=self.dataset,datagroup=self.datagroup)
        import qacd_plot as qp
        qp.savefig_map(Settings)
        self.sc.closeFigure()
        del self.sc
        gc.collect()
        gc.collect()
        del gc.garbage[:]
        self.close()
        return
    def formatBox(self,item):
        self.fmtvar = str(item)
        return
    def StatCheck(self):
        if self.checkBox_Stats.isChecked() == True:
            self.statck = 1
            self.checkBox_Pix.setChecked(True)
            self.checkBox_Mean.setChecked(True)
            self.checkBox_Median.setChecked(True)
            self.checkBox_Std.setChecked(True)
        else:
            self.statck = 0
        return
    def TitleCheck(self):
        if self.checkBox_Title.isChecked() == True:
            self.titleck = 1
            self.lineEdit_Title.setEnabled(True)
        else:
            self.titleck = 0
            self.lineEdit_Title.setDisabled(True)
        return

import ProjectManager_rc

if __name__=='_main__':
    app = QtGui.QApplication(sys.argv)
    myDialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(myDialog)
    myDialog.show()
    sys.exit(app.exec_())

