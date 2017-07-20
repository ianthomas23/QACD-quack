import dataInit2 as di
import datetime as dt
import os
from PyQt4.QtGui import QMainWindow, QDialog, QFileDialog
from PyQt4.QtCore import pyqtSignature
import qacd_corr as qcr
import tables as tb

from Import_Dialog_gen import Ui_QACD_Import

class myDialog(QDialog, Ui_QACD_Import):
    def __init__(self, parent=None):
        QDialog.__init__(self,parent)
        self.setupUi(self)
        self.setFixedSize(self.size())

        self.chooseFilesButton.clicked.connect(self.on_choose_files)
        self.checkBox_opt.clicked.connect(self.on_enable_pixel_step_size)
        self.groupUnits.buttonClicked.connect(self.on_change_units)
        self.engageButton.clicked.connect(self.on_engage)

        self.Parameters = {}
        self.units = 'metres'

        self.set_project_file()
        self.on_enable_pixel_step_size()

    def init_start(self):
        ells = self.Parameters['Ells']
        names = self.Parameters['Files']
        pixVar = self.Parameters['Pix']
        medVar = self.Parameters['Med']
        Length = self.Parameters['Length']
        pxsz = self.Parameters['pxszopt']
        f = tb.open_file(self.varProj, mode = 'a')
        f.create_group(f.root, 'Filtered', 'Filtered')
        f.create_group(f.root, 'Phase', 'Phase')
        Param = f.create_group(f.root, 'parameters', 'parameters')
        f.create_array(Param, 'ElementList', ells)
        f.close()
        #print "cython forward"
        f = tb.open_file("temp.h5", mode='a')
        f.create_array(f.root, 'names', names)
        f.create_array(f.root, 'Length', Length)
        f.create_array(f.root, 'pxszopt', pxsz)
        f.close()
        Dict = {'varProj': self.varProj,
                'Length': Length,
                'Names': names,
                'pxszopt': pxsz}
        if pixVar and medVar:
            print('Filtering data by pixel totals and a 3-by-3 nearest neighbor median filter...')
            di.Data_Load1(Dict, Length)
        elif pixVar and not medVar:
            print('Filtering data by pixel totals...')
            di.Data_Load2(Dict, Length)
        elif not pixVar and medVar:
            print('Filtering data with a 3-by-3 nearest neighbor median filter...')
            di.Data_Load3(Dict, Length)
        print('Data Loaded')
        st1 = qcr.elratio(self.varProj)
        print('elratio', st1)
        st2 = qcr.h_factor(self.varProj)
        print('h factor', st2)
        print('Your Data have been processed')

    def on_choose_files(self):
        filenames = QFileDialog.getOpenFileNames(self, 'Pick your files', '',
                                                 'CSV Files (*.csv)')
        self.filenames = [str(filename) for filename in filenames]
        print(self.filenames)

        global ells, Length
        Length = len(self.filenames)
        ells = []
        names = []
        for filename in self.filenames:
            pname, fname = os.path.split(filename) # split strings into path and file
            var, tag = fname.split("K series.csv") # remove the file ext and tag
            var = var.replace(' ', '')
            ells.append(var)
            names.append(filename)
            self.listWidget_Files.addItem(var)
        print('elements', ells)
        self.Parameters['Proj'] = self.varProj
        self.Parameters['Ells'] = ells
        self.Parameters['Files'] = names
        self.Parameters['Length'] = Length

    def on_change_units(self, button):
        if button == self.buttonUnits_mm:
            self.units = 'mm'
        elif button == self.buttonUnits_um:
            self.units = 'um'
        elif button == self.buttonUnits_nm:
            self.units = 'nm'
        else:
            raise RuntimeError('Erroneous units radio button')

    def on_enable_pixel_step_size(self):
        enabled = self.checkBox_opt.isChecked()
        #if enabled:
        #    print('Pixel Options Checked!')
        #else:
        #    print('No pixel options!')
        self.spinPixelStepSize.setEnabled(enabled)
        self.label.setEnabled(enabled)
        self.buttonUnits_mm.setEnabled(enabled)
        self.buttonUnits_um.setEnabled(enabled)
        self.buttonUnits_nm.setEnabled(enabled)

    def on_engage(self):
        self.engageButton.setText('This can take a minute...')
        self.set_log()
        self.init_start()
        print('Data Imported and Processed')
        self.close()

    def set_log(self):
        pixel_step_size = self.spinPixelStepSize.value()
        f = tb.open_file(self.varProj, mode='a')
        log = f.get_node(f.root, 'Log').read()
        tp = self.Parameters['Ells']
        files = len(tp)
        string = str(files) + " files on " + str(dt.datetime.now().strftime('%I:%M%p, %d %B %Y'))
        print(string)
        log[2] = string

        pixVar = self.checkBox_pix.isChecked()
        medVar = self.checkBox_med.isChecked()
        if pixVar:
            if medVar:
                log[3] = 'Median & Pixel'
            else:
                log[3] = 'Pixel Only'
        else:
            if medVar:
                log[3] = 'Median Only'
            else:
                pass  # Neither set.
        log[4] = '{} {}'.format(pixel_step_size, self.units)
        print('log', log)
        f.remove_node(f.root, "Log")
        f.create_array(f.root, 'Log', log)
        if self.checkBox_opt.isChecked():
            print('Pixel Options Checked!')
            self.Parameters['pxszopt'] = 'Yes'
            self.Parameters['pixsize'] = pixel_step_size
            self.Parameters['pixunit'] = self.units
            f.create_array(f.root, 'PixSize', [pixel_step_size, self.units])
        elif self.checkBox_opt.isChecked() == False:
            print('No pixel options!')
            self.Parameters['pxszopt'] = 'No'
            self.Parameters['pixsize'] = 1.0
            self.Parameters['pixunit'] = ''
            f.create_array(f.root, 'PixSize', [1.0, ''])
        f.flush()
        f.close()
        self.Parameters['Pix'] = pixVar
        self.Parameters['Med'] = medVar

    def set_project_file(self):
        f = tb.open_file('temp.h5', mode='a')
        tm = f.get_node(f.root, 'varProj')
        self.varProj = tm.read()
        f.close()
