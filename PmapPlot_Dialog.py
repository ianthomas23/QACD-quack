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
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import utils

class MyMplCanvas(FigureCanvas):
    def __init__(self,parent=None,width=10,height=6,dpi=100):
        utils.set_style()
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
        self.dataset = f.get_node(f.root,'dataset').read()
        #self.phases = f.get_node(f.root, 'phases').read()
        f.close()
        self.annot = []
        self.title = 'Some'
        self.PixSize, self.pixun = self.pix_ret()
        self.data = self.data_ret2()
        print self.data

        mini = np.nanmin(self.data)
        maxi = np.nanmax(self.data)
        print mini, maxi
        print maxi-mini+1

        self.my_cmap = cm.get_cmap('gnuplot',maxi-mini+1)
        self.my_cmap.set_under('k', alpha=0)
        self.my_cmap.set_over('k', alpha=0)

        im = self.axes.imshow(self.data,cmap=self.my_cmap,interpolation='nearest',
                              vmin = mini-.5, vmax = maxi+.5)
        self.axes.set_title(self.title)
        fig = self.axes.get_figure()
        cb = fig.colorbar(im,ticks=np.arange(mini,maxi+1), fraction=0.046, pad = 0.04)
        cb.ax.set_yticklabels(self.annot)
        cb.ax.tick_params(labelsize=10)
        fig.subplots_adjust(left=0.0,right=0.75, top=0.95, bottom=0.05)
        fig.tight_layout()

        xmin,xmax = self.axes.get_xlim()
        xticks = self.axes.get_xticks()
        self.axes.yaxis.set_ticks_position('left')
        self.axes.xaxis.set_ticks_position('bottom')
        Length = len(xticks)
        xlabels = ['Some']*len(xticks)
        xlabels[0] = ''
        xlabels[Length-1]=''
        for i in xrange(1,Length-1):
            val = xticks[i]
            if self.pixun == 'um':
                val = int((val*self.PixSize)/1000)
            elif self.pixun == 'nm':
                val = int((val*self.PixSize)/1000000000)
            elif self.pixun == 'mm':
                val = int(val*self.PixSize)
            print val
            string = str(val) + "mm"
            xlabels[i]=string
        print xlabels
        fig.canvas.draw()
        self.axes.set_xticklabels(xlabels)
        self.axes.set_yticklabels([])

    def pix_ret(self):
        f = tb.open_file(self.varProj,mode='a')
        pxsz = f.get_node(f.root,'PixSize').read()
        PixSize = float(pxsz[0])
        pxun = pxsz[1]
        f.close()
        print PixSize, pxun
        return PixSize, pxun
    def data_ret2(self):
        f = tb.open_file(self.varProj,mode='a')
        tm = f.root._f_get_child(self.dataset)
        Grp = tm._f_get_child('PhaseMap')
        masks = Grp._f_get_child('masks')
        pxsz = f.get_node(f.root,'PixSize').read()
        self.PixSize = float(pxsz[0])
        self.pxun = pxsz[1]
        tmp = masks._v_children
        self.names = []
        mskls = []
        self.phpix = []
        i = 1
        for item in tmp.keys():
            if item == 'PhaseMap':
                print 'Not a phase'
            else:
                self.names.append(item)
                ds = f.get_node(masks,item).read()
                ds1 = ds * 1.0
                num = np.sum(ds)
                string = str(item) + ", "+str(num)+" pixels"
                self.phpix.append(num)
                self.annot.append(string)
                ds1[ds1==1.0]=i
                mskls.append(ds1)
                i = i + 1
                print i
        print
        phasemap = mskls[0]
        for i in xrange(1,len(mskls)):
            ds = mskls[i]
            phasemap = phasemap + ds
        print phasemap
        print np.nanmax(phasemap), np.nanmin(phasemap)
        Total = np.sum(self.phpix)
        print Total
        phasemap[phasemap==0]=np.nan
        self.title = ('PhaseMap (N = ' + str(Total)+' pixels)')
        f.close()
        gc.collect()
        return phasemap

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        f = tb.open_file('figtemp.h5',mode='a')
        self.varProj = f.get_node(f.root,'varProj').read()
        self.mapvar = f.get_node(f.root,'mapvar').read()
        self.dataset = f.get_node(f.root,'dataset').read()
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
        sc = MplCanvas_hist(self.mplwidget, width=10,height=6,dpi=100)
        self.toolbar = NavigationToolbar(sc,self.mplwidget,coordinates=True)
        self.mvl.addWidget(self.toolbar)
        self.mvl.addWidget(sc)
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
        self.checkBox_Stats = QtGui.QCheckBox("Stats File",self.widget)
        self.gridLayout.addWidget(self.checkBox_Stats, 2, 0, 1, 2)
        self.checkBox_Stats.toggled.connect(self.StatCheck)
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
        self.pushButton_Export = QtGui.QPushButton("Export Figure and Phase Stats Text File",self.widget)
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
        filetitle = str(self.lineEdit_fname.text())
        filefmt = str(self.comboBox_format.currentText())
        height = float(self.doubleSpinBox_Het.value())
        width = float(self.doubleSpinBox_wid.value())
        dpi = int(self.spinBox_DPI.value())
        Settings = dict(figtitle=figtitle,filetitle=filetitle,
                        filefmt=filefmt,height=height,width=width,options=self.statck,
                        dpi=dpi,varProj=self.varProj,mapvar=str(self.mapvar),
                        dataset=str(self.dataset))
        import qacd_plot as qp
        string = qp.savefig_pmap(Settings)
        print string
        gc.collect()
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

