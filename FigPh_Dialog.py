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
        self.varProj = ''
        self.dset = ''
        self.mapvar = ''
        self.phase = ''
        self.phls = []
        self.ells = []
        self.curdat = {}
        self.phgrps = []
        
        Figure_Dialog.setObjectName("Figure_Dialog")
        Figure_Dialog.resize(279, 133)
        Figure_Dialog.setWindowTitle("QACD- Phase Figure")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/main_icon/16x16.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Figure_Dialog.setWindowIcon(icon)
        Figure_Dialog.setModal(False)
        
        self.widget = QtGui.QWidget(Figure_Dialog)
        self.widget.setGeometry(QtCore.QRect(10, 10, 258, 115))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)

        self.label_Dataset = QtGui.QLabel("Phase Set:",self.widget)
        self.gridLayout.addWidget(self.label_Dataset, 0, 0, 1, 1)
        self.comboBox_Data = QtGui.QComboBox(self.widget)
        self.gridLayout.addWidget(self.comboBox_Data, 0, 1, 1, 3)

        self.pushButton_Exit = QtGui.QPushButton("Exit and Return to Project Manager",self.widget)
        self.gridLayout.addWidget(self.pushButton_Exit, 5, 0, 1, 4)
        self.pushButton_Exit.clicked.connect(self.exit_cls)
        self.pushButton_Hist = QtGui.QPushButton("Create Plot of PhaseMap",self.widget)
        self.gridLayout.addWidget(self.pushButton_Hist, 4, 0, 1, 4)
        self.pushButton_Hist.clicked.connect(self.pmap_form)

        QtCore.QMetaObject.connectSlotsByName(Figure_Dialog)

        self.populate()

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
            elif item =='Phase':
                print 'Not a cluster'
            elif item =='nums':
                print 'Not a cluster'
            elif item =='Stack1':
                print 'Not a cluster'
            elif item =='Stack2':
                print 'Not a cluster'
            else:
                self.phgrps.append(item)
                self.comboBox_Data.addItem(item)
                print item
        return      
    def exit_cls(self):
        print 'Finished!'
        self.close()
        return
    def pmap_form(self):
        self.mapvar = 'PhaseMap'
        self.dset = str(self.comboBox_Data.currentText())
        f = tb.open_file('figtemp.h5', mode='w')
        f.create_array(f.root, 'varProj', self.varProj)
        f.create_array(f.root, 'mapvar', str(self.mapvar))
        print self.dset
        f.create_array(f.root, 'dataset', str(self.dset))
        f.close()
        gc.collect()
        from dlg_plotP2 import myDialog
        self.pltDlg = myDialog(self)
        self.pltDlg.exec_()
        self.pltDlg = ""
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
