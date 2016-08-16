# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Edit_Dialog.ui'
#
# Created: Thu Feb 04 10:55:04 2016
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import tables as tb

class Ui_ClustPop_Dialog(object):
    def setupUi(self, ClustPop_Dialog):
        ClustPop_Dialog.setObjectName("ClustPop_Dialog")
        ClustPop_Dialog.resize(332, 158)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ClustPop_Dialog.sizePolicy().hasHeightForWidth())
        ClustPop_Dialog.setSizePolicy(sizePolicy)
        ClustPop_Dialog.setMaximumSize(QtCore.QSize(332, 158))
        ClustPop_Dialog.setWindowTitle("Cluster Editing")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/main_icon/16x16.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ClustPop_Dialog.setWindowIcon(icon)
        
        self.widget = QtGui.QWidget(ClustPop_Dialog)
        self.widget.setGeometry(QtCore.QRect(10, 10, 311, 137))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)
        self.label = QtGui.QLabel("Previously clustered datasets:",self.widget)
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.comboBox = QtGui.QComboBox(self.widget)
        self.gridLayout.addWidget(self.comboBox, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel("You can continue editing phases from older sessions.",self.widget)
        self.label_2.setWordWrap(True)
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 2)
        self.label_3 = QtGui.QLabel("Would you like to continue editing these Phases and Phasemaps?",self.widget)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setWordWrap(True)
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(self.widget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Yes)
        self.buttonBox.accepted.connect(self.edit_cont)
        self.buttonBox.rejected.connect(self.edit_canc)
        self.buttonBox.setCenterButtons(True)
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)
        QtCore.QMetaObject.connectSlotsByName(ClustPop_Dialog)
        self.populate_combo()
        
    def edit_cont(self):
        var = str(self.comboBox.currentText())
        f = tb.open_file("temp.h5",mode='a')
        tmp = f.root._v_children
        for item in tmp.keys():
            if item == "clust":
                f.remove_node(f.root,"clust")
            else:
                print 'clust removed'
        tp = f.create_array(f.root,"clust",var)
        tp.attrs.reason = 42
        f.close()
        self.close()
    def edit_canc(self):
        self.close()
    def populate_combo(self):
        f = tb.open_file("temp.h5",mode='a')
        varProj = f.get_node(f.root,"varProj").read()
        f.close()
        f = tb.open_file(varProj,mode='a')
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
                self.comboBox.addItem(item)
                print item
        print 'Populated'
        f.close()
        return            
   
import ProjectManager_rc

if __name__=='_main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    myDialog = QtGui.QDialog()
    ui = Ui_ClustPop_Dialog()
    ui.setupUi(myDialog)
    myDialog.show()
    sys.exit(app.exec_())
