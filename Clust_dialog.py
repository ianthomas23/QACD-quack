# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Clust_dialog.ui'
#
# Created: Thu Jan 28 17:37:00 2016
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from matplotlib.figure import Figure
import matplotlib.cm as cm
import tables as tb
import numpy as np
import gc
import sys
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.style as mps

class MyMplCanvas(FigureCanvas):
    def __init__(self,parent=None,width=10,height=6,dpi=100):
        #mps.use('qacd_xmap')
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

class MplCanvas_hist(MyMplCanvas):
    def compute_initial_figure(self):
        self.data = DataHolder()
        self.mapnames = self.data.get_maplist()
        self.annot = "Some"
        self.title = 'Some'
        self.my_cmap = cm.gnuplot
        name = self.mapnames[0]
        self.curmap = name
        ds = self.data.get_series_data(name)
        im = self.axes.imshow(ds)
        print str(name)
        fig = self.axes.get_figure()
        global cb
        cb = fig.colorbar(im)
        fig.canvas.draw()
        return
    def get_current(self):
        return self.curmap
    def get_image_labels(self):
        return self.mapnames
    def update_fig(self,name):
        del self.axes.images[0]
        ds = self.data.get_series_data(name)
        self.curmap = name
        fig = self.axes.get_figure()
        im = self.axes.imshow(ds)
        print str(name)
        cb.update_bruteforce(im)
        fig.canvas.draw()
        return
    def closeFigure(self):
        del self.data
        self.axes.clear()
        gc.collect()
        self.close()
        return

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        self.imageref = []

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        Dialog.setObjectName("Dialog")
        Dialog.resize(1451, 868)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMaximumSize(QtCore.QSize(1451, 868))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/main_icon/16x16.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setWindowTitle("QACD-3b.Pick the best Phase Map")

        self.mplwindow = QtGui.QWidget(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mplwindow.sizePolicy().hasHeightForWidth())
        self.mplwindow.setSizePolicy(sizePolicy)
        self.mvl = QtGui.QVBoxLayout(self.mplwindow)
        self.mvl.setMargin(0)
        self.sc = MplCanvas_hist(self.mplwindow, width=11.5,height=6.5,dpi=100)
        self.toolbar = NavigationToolbar(self.sc,self.mplwindow, coordinates=True)
        self.mvl.addWidget(self.toolbar)
        self.mvl.addWidget(self.sc)
        self.mplwindow.setFocus()

        self.first_plot()
        maxi = len(self.imageref)
        self.curzord = maxi

        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.addWidget(self.mplwindow, 0, 0, 2, 5)

        self.label_2 = QtGui.QLabel("Phase Maps:",Dialog)
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.horizontalSlider = QtGui.QSlider(Dialog)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setRange(0,(maxi-1))
        self.horizontalSlider.sliderReleased.connect(self.update_plot)
        self.horizontalSlider.setValue(0)
        self.gridLayout.addWidget(self.horizontalSlider, 2, 1, 1, 1)

        self.label_6 = QtGui.QLabel("Current:",Dialog)
        self.gridLayout.addWidget(self.label_6, 2, 3, 1, 1)
        self.lineEdit = QtGui.QLineEdit(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setText(str(self.imageref[0]))
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMaximumSize(QtCore.QSize(144, 16777215))
        self.gridLayout.addWidget(self.lineEdit, 2, 4, 1, 1)
        self.pushButton_CreatePhase = QtGui.QPushButton("Edit/Use Selected Phase Mask",Dialog)
        self.pushButton_CreatePhase.clicked.connect(self.cont_ph)
        self.gridLayout.addWidget(self.pushButton_CreatePhase, 3, 3, 1, 2)

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def first_plot(self):
        self.imageref = self.sc.get_image_labels()
        return
    def update_plot(self):
        idx = int(self.horizontalSlider.value())
        var = self.imageref[idx]
        self.lineEdit.setText(str(var))
        temp = self.sc.update_fig(var)
        gc.collect()
        print 'Updated'
        return
    def cont_ph(self):
        node = str(self.lineEdit.text())
        f = tb.open_file("temp.h5",mode='a')
        varProj = f.get_node(f.root,"varProj").read()
        clust = f.get_node(f.root,"clust").read()
        f.close()
        f = tb.open_file(varProj,mode='a')
        Clust = f.root._f_get_child(clust)
        ls = Clust._v_children
        self.names = ls.keys()
        #f.rename_node(Clust, "PhaseMap", name=node)
        for item in self.names:
            if item == 'Stack':
                print 'Stack'
            elif item == node:
                f.rename_node(Clust, "PhaseMap", name=node)
            else:
                f.remove_node(Clust, name=item, recursive=True)
        print Clust
        log = f.get_node(f.root, "Log").read()
        import datetime
        string = datetime.datetime.now().strftime("%I:%M%p, %d %B %Y")
        log[9] = string
        print log
        f.remove_node(f.root, "Log")
        f.create_array(f.root, "Log", log)
        f.close()
        self.close()
        return
    def closeEvent(self, e):
        self.sc.closeFigure()
        return

class DataHolder(object):
    def __init__(self):
        self.varProj = ''
        self.names = []
        self.clust = ""
        self.load_data()
    def load_data(self):
        f = tb.open_file("temp.h5",mode='a')
        self.varProj = f.get_node(f.root,"varProj").read()
        self.clust = f.get_node(f.root,"clust").read()
        f.close()
        f = tb.open_file(self.varProj,mode='a')
        Clust = f.root._f_get_child(self.clust)
        ls = Clust._v_children
        tp = ls.keys()
        self.names = []
        for item in tp:
            if item == 'Stack':
                print 'Stack'
            else:
                self.names.append(item)
        f.close()
        print 'Loaded'
    def get_maplist(self):
        return self.names
    def get_series_data(self,name):
        f = tb.open_file(self.varProj,mode='a')
        Clust = f.root._f_get_child(self.clust)
        grp = Clust._f_get_child(name)
        ds = f.get_node(grp,'pmap').read()
        f.close()
        val = 255/np.max(ds)
        ds = ds*val
        im = self.imresize(ds)
        return im
    def imresize(self, im):
        from PIL import Image
        im2 = Image.fromarray(np.uint8(cm.gnuplot(im, bytes=True)))
        x,y = im2.size[0],im2.size[1]
        sz = (1150,int((1150.0/x)*y))
        return im2.resize(sz)


import ProjectManager_rc

if __name__=='_main__':
    app = QtGui.QApplication(sys.argv)
    myDialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(myDialog)
    myDialog.show()
    sys.exit(app.exec_())
