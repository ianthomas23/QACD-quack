# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Import_Dialog.ui'
#
# Created: Wed Jan 20 10:40:30 2016
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import os
import sys
import tables as tb
import gc

gc.set_threshold(100, 5, 5)

class Ui_QACD_Import(object):
    pixVar = "False"
    medVar = "False"
    units = "metres"
    pixsz = 1.0
    pixun = ""
    Parameters = {}
    def setupUi(self, QACD_Import):
        QACD_Import.setObjectName("QACD_Import")
        QACD_Import.resize(331, 563)
        QACD_Import.setWindowTitle("QACD- 2.Data Import")
        QACD_Import.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(QACD_Import.sizePolicy().hasHeightForWidth())
        QACD_Import.setSizePolicy(sizePolicy)
        QACD_Import.setFixedSize(331, 563)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/main_icon/16x16.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        QACD_Import.setWindowIcon(icon)

        self.widget = QtGui.QWidget(QACD_Import)
        self.widget.setGeometry(QtCore.QRect(10, 10, 311, 431))

        self.label_2 = QtGui.QLabel("<html><head/><body><p>Step 1. Choose your map files.</p><p>Step 2. Choose your Map Filtration options.</p><p>Step 3. It is optional to provide the step/pixel size.</p><p>Step 4. Import and filter selected maps.</p></body></html>",QACD_Import)
        self.label_2.setGeometry(QtCore.QRect(10, 450, 311, 101))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setScaledContents(True)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setWordWrap(True)


        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)

        self.label_Files = QtGui.QLabel("Map Files (.CSV):",self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Files.sizePolicy().hasHeightForWidth())
        self.label_Files.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.label_Files, 0, 0, 1, 1)
        self.Button_Files = QtGui.QPushButton("1. Choose Files",self.widget)
        self.gridLayout.addWidget(self.Button_Files, 0, 1, 1, 3)
        self.Button_Files.clicked.connect(self.File_Set)
        self.Button_Files.setToolTip("<html><head/><body><p>Step 1. Choose your map files.</p></body></html>")

        self.listWidget_Files = QtGui.QListWidget(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget_Files.sizePolicy().hasHeightForWidth())
        self.listWidget_Files.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.listWidget_Files, 1, 0, 1, 4)



        self.label_Filt = QtGui.QLabel("2. Map Filtration:",self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Filt.sizePolicy().hasHeightForWidth())
        self.label_Filt.setSizePolicy(sizePolicy)
        self.label_Filt.setToolTip("<html><head/><body><p>Step 2. Choose your Map Filtration options.</p></body></html>")
        self.gridLayout.addWidget(self.label_Filt, 2, 0, 1, 4)

        self.checkBox_pix = QtGui.QCheckBox("Pixel Totals (Salt-N-Pepper Noise)",self.widget)
        self.checkBox_pix.stateChanged.connect(self.pix_check)
        self.gridLayout.addWidget(self.checkBox_pix, 3, 0, 1, 4)
        self.checkBox_pix.setToolTip("<html><head/><body><p>Pixel Totals: Recommended on larger maps.</p></body></html>")
        self.checkBox_med = QtGui.QCheckBox("3-by-3 Median Filter",self.widget)
        self.checkBox_med.stateChanged.connect(self.med_check)
        self.gridLayout.addWidget(self.checkBox_med, 4, 0, 1, 4)

        self.Button_Engage = QtGui.QPushButton("4. Import and Filter Selected Maps",self.widget)
        self.Button_Engage.setToolTip("The data import and filtration process can be tedious and long. The dialog may become unresponsive for a moment after clicking this button.")
        self.Button_Engage.clicked.connect(self.Engage)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.Button_Engage.setFont(font)
        self.gridLayout.addWidget(self.Button_Engage, 9, 0, 1, 4)

        self.label_opt = QtGui.QLabel("3. Optional Information for Map Import:",self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_opt.sizePolicy().hasHeightForWidth())
        self.label_opt.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.label_opt, 6, 0, 1, 4)

        self.checkBox_opt = QtGui.QCheckBox("Include Pixel Step Size:",self.widget)
        self.checkBox_opt.clicked.connect(self.optional_chck)
        self.checkBox_opt.setChecked(True)
        self.gridLayout.addWidget(self.checkBox_opt, 7, 0, 1, 2)
        self.doubleSpinBox = QtGui.QDoubleSpinBox(self.widget)
        self.doubleSpinBox.setDecimals(2)
        self.doubleSpinBox.setMaximum(10000.0)
        self.doubleSpinBox.setProperty("value", 10.0)
        self.gridLayout.addWidget(self.doubleSpinBox, 7, 2, 1, 2)

        self.label = QtGui.QLabel("Pixel Step Size Units:",self.widget)
        self.gridLayout.addWidget(self.label, 8, 0, 1, 1)
        self.radio_group=QtGui.QButtonGroup(self.widget)
        self.radio_group.setExclusive(True)
        self.radbut_1 = QtGui.QRadioButton("mm",self.widget)
        self.gridLayout.addWidget(self.radbut_1, 8, 1, 1, 1)
        self.radbut_2 = QtGui.QRadioButton("um",self.widget)
        self.gridLayout.addWidget(self.radbut_2, 8, 2, 1, 1)
        self.radbut_3 = QtGui.QRadioButton("nm",self.widget)
        self.gridLayout.addWidget(self.radbut_3, 8, 3, 1, 1)
        self.radbut_1.setChecked(True)
        self.radio_group.addButton(self.radbut_1, 1)
        self.radio_group.addButton(self.radbut_2, 2)
        self.radio_group.addButton(self.radbut_3, 3)

        self.radbut_1.clicked.connect(self.btnstate)
        self.radbut_2.clicked.connect(self.btnstate)
        self.radbut_3.clicked.connect(self.btnstate)

        QtCore.QMetaObject.connectSlotsByName(QACD_Import)

        self.set_project_file()
    def optional_chck(self):
        if self.checkBox_opt.isChecked() == True:
            print'Pixel Options Checked!'
            self.doubleSpinBox.setEnabled(True)
            self.label.setEnabled(True)
            self.radbut_1.setEnabled(True)
            self.radbut_2.setEnabled(True)
            self.radbut_3.setEnabled(True)
        elif self.checkBox_opt.isChecked() == False:
            print'No pixel options!'
            self.doubleSpinBox.setEnabled(False)
            self.label.setEnabled(False)
            self.radbut_1.setEnabled(False)
            self.radbut_2.setEnabled(False)
            self.radbut_3.setEnabled(False)
        return
    def btnstate(self, b):
        var = self.radio_group.checkedId()
        if var == 1:
            self.units = "mm"
        elif var == 2:
            self.units = "um"
        elif var == 3:
            self.units = "nm"
        print self.units
        return
    def set_project_file(self):
        import tables as tb
        f = tb.open_file('temp.h5', mode='a')
        tm = f.get_node(f.root, 'varProj')
        self.varProj = tm.read()
        f.close()
        return
    def File_Set(self):
        fnms = QtGui.QFileDialog.getOpenFileNames(self,"Pick your files",'',"CSV Files (*.csv)")
        self.filenames = []
        for fnm in fnms:
            self.filenames.append(str(fnm))
        print self.filenames
        global ells, Length
        Length = len(self.filenames)
        ells = range(Length)
        names = range(Length)
        for i in xrange(0,Length):
            name = ''.join(self.filenames[i]) #format name as string
            pname, fname = os.path.split(name) #split strings into path and file
            var, tag = fname.split("K series.csv") # remove the file ext and tag
            var2 = str(var)
            var2 = var2.replace(" ","")
            ells[i] = var2
            names[i] = name
            self.listWidget_Files.addItem(var2)
        print ells
        self.Parameters['Proj'] = self.varProj
        self.Parameters['Ells'] = ells
        self.Parameters['Files'] = names
        self.Parameters['Length'] = Length
        return
    def pix_check(self,state):
        if state ++ QtCore.Qt.Checked:
            self.pixVar = 'True'
        else:
            self.pixVar = 'False'
    def med_check(self,state):
        if state ++ QtCore.Qt.Checked:
            self.medVar = 'True'
        else:
            self.medVar = 'False'
    def setLog(self):
        self.pixsz = float(self.doubleSpinBox.value())
        f = tb.open_file(self.varProj, mode='a')
        log = f.get_node(f.root, "Log").read()
        tp = self.Parameters['Ells']
        files = len(tp)
        import datetime
        #string = datetime.datetime.now().strftime("%I:%M%p, %d %B %Y")
        string = str(files) + " files on " + str(datetime.datetime.now().strftime("%I:%M%p, %d %B %Y"))
        print string
        log[2] = string
        both = 1
        if self.pixVar == 'True':
            both = both + 2
        if self.medVar == 'True':
            both = both + 4
        if both == 3:
            log[3] = 'Pixel Only'
            print log
        elif both == 5:
            log[3] = 'Median Only'
            print log
        elif both == 7:
            log[3] = 'Median & Pixel'
            print log
        del both, string
        tmp = str(self.pixsz) + self.units
        print tmp
        log[4] = tmp
        del tmp
        f.remove_node(f.root, "Log")
        f.create_array(f.root, 'Log', log)
        del log
        if self.checkBox_opt.isChecked() == True:
            print'Pixel Options Checked!'
            self.Parameters['pxszopt']='Yes'
            self.Parameters['pixsize'] = self.pixsz
            self.Parameters['pixunit'] = self.units
            lis = [self.pixsz, self.units]
            f.create_array(f.root, 'PixSize', lis)
        elif self.checkBox_opt.isChecked() == False:
            print'No pixel options!'
            self.Parameters['pxszopt']='No'
            self.Parameters['pixsize'] = 1.0
            self.Parameters['pixunit'] = ""
            lis = [1.0, ""]
            f.create_array(f.root, 'PixSize', lis)
        f.flush()
        f.close()
        self.Parameters['Pix']=self.pixVar
        self.Parameters['Med']=self.medVar
        return
    def Engage(self):
        self.Button_Engage.setText('This can take a minute...')
        self.setLog()
        self.init_Start()
        print "Data Imported and Processed"
        self.close()
    def init_Start(self):
        ells = self.Parameters['Ells']
        names = self.Parameters['Files']
        pixVar = self.Parameters['Pix']
        medVar = self.Parameters['Med']
        Length = self.Parameters['Length']
        pxsz = self.Parameters['pxszopt']
        f = tb.open_file(self.varProj, mode = 'a')
        f.create_group(f.root,'Filtered','Filtered')
        f.create_group(f.root,'Phase','Phase')
        Param = f.create_group(f.root,'parameters','parameters')
        f.create_array(Param,'ElementList',ells)
        f.close()
        print "cython forward"
        f = tb.open_file("temp.h5", mode='a')
        f.create_array(f.root, 'names', names)
        f.create_array(f.root, 'Length', Length)
        f.create_array(f.root, 'pxszopt', pxsz)
        f.close()
        gc.collect()
        Dict = {'varProj':self.varProj,'Length':Length,'Names':names,'pxszopt':pxsz}
        if pixVar=='True' and medVar =='True':
            print 'Filtering data by pixel totals and a 3-by-3 nearest neighbor median filter...'
            import dataInit2 as di
            di.Data_Load1(Dict,Length)
        elif pixVar=='True' and medVar =='False':
            print 'Filtering data by pixel totals...'
            import dataInit2 as di
            di.Data_Load2(Dict,Length)
        elif pixVar=='False' and medVar =='True':
            print 'Filtering data with a 3-by-3 nearest neighbor median filter...'
            import dataInit2 as di
            di.Data_Load3(Dict,Length)
        print 'Data Loaded'
        import qacd_corr as qcr
        st1 = qcr.elratio(self.varProj)
        print st1
        st2 = qcr.h_factor(self.varProj)
        print st2
        del ells, names, pixVar, medVar, Length, pxsz, Dict
        gc.collect()
        gc.collect()
        del gc.garbage[:]
        print "Your Data have been processed"
        return
import ProjectManager_rc

if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    myDialog = QtGui.QDialog()
    ui = Ui_QACD_Import()
    ui.setupUi(myDialog)
    myDialog.show()
    sys.exit(app.exec_())
