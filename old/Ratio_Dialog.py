# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ratio_Dialog.ui'
#
# Created: Mon Jan 25 09:55:22 2016
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import tables as tb
import gc

#class Presets(object):
class Ui_Ratio_Dialog(object):
    def setupUi(self, Ratio_Dialog):
        self.mapvar_a = ''
        self.mapvar_b = ''
        self.mapvar_c = ''
        self.ells = []
        self.phls = []
        self.curPh = ''
        self.curpres = {}
        self.presets = {}
        Ratio_Dialog.setObjectName("Ratio_Dialog")
        Ratio_Dialog.resize(299, 414)
        Ratio_Dialog.setWindowTitle("QACD- Map Calculator")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/main_icon/16x16.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Ratio_Dialog.setWindowIcon(icon)
        
        self.widget = QtGui.QWidget(Ratio_Dialog)
        self.widget.setGeometry(QtCore.QRect(11, 11, 273, 391))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)

        self.label_Title = QtGui.QLabel("Element Ratio Map Creation",self.widget)
        self.gridLayout.addWidget(self.label_Title, 0, 0, 1, 6)
        
        self.listWidget_Elem = QtGui.QListWidget(self.widget)
        self.gridLayout.addWidget(self.listWidget_Elem, 1, 0, 1, 6)
        self.label_MapName = QtGui.QLabel("Ratio Map Name:",self.widget)
        self.gridLayout.addWidget(self.label_MapName, 5, 0, 1, 2)
        self.lineEdit_Name = QtGui.QLineEdit(self.widget)
        self.gridLayout.addWidget(self.lineEdit_Name, 5, 2, 1, 4)
        self.label_Presets = QtGui.QLabel("Presets:",self.widget)
        self.gridLayout.addWidget(self.label_Presets, 2, 0, 1, 1)
        self.comboBox_Presets = QtGui.QComboBox(self.widget)
        self.gridLayout.addWidget(self.comboBox_Presets, 2, 1, 1, 5)
        self.comboBox_Presets.activated[str].connect(self.preset_select)
        
        self.label = QtGui.QLabel("A:",self.widget)
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.comboBox = QtGui.QComboBox(self.widget)
        self.gridLayout.addWidget(self.comboBox, 3, 1, 1, 1)
        self.comboBox.activated[str].connect(self.mapvar_A)
        
        self.label_2 = QtGui.QLabel("B:",self.widget)
        self.gridLayout.addWidget(self.label_2, 3, 2, 1, 1)
        self.comboBox_2 = QtGui.QComboBox(self.widget)
        self.gridLayout.addWidget(self.comboBox_2, 3, 3, 1, 1)
        self.comboBox_2.activated[str].connect(self.mapvar_B)
        
        self.label_3 = QtGui.QLabel("C:",self.widget)
        self.gridLayout.addWidget(self.label_3, 3, 4, 1, 1)
        self.comboBox_3 = QtGui.QComboBox(self.widget)
        self.gridLayout.addWidget(self.comboBox_3, 3, 5, 1, 1)
        self.comboBox_3.activated[str].connect(self.mapvar_C)
        
        self.label_RatFunc = QtGui.QLabel("Ratio Func:",self.widget)
        self.gridLayout.addWidget(self.label_RatFunc, 4, 0, 1, 3)
        self.label_Func = QtGui.QLabel("A / A + B",self.widget)
        self.gridLayout.addWidget(self.label_Func, 4, 2, 1, 3)
        self.pushButton_Add = QtGui.QPushButton("Add Map to Project",self.widget)
        self.gridLayout.addWidget(self.pushButton_Add, 6, 0, 1, 6)
        self.pushButton_Add.clicked.connect(self.Create_Map)

        self.Populate_boxes()

    def Populate_boxes(self):
        f = tb.open_file('temp.h5', mode='a')        
        self.varProj = (f.get_node(f.root, 'varProj')).read()
        f.close()
        f = tb.open_file(self.varProj, mode='a')
        tmp = f.root
        lis = tmp._v_children
        if 'MapList' in lis.keys():
            self.ells = f.get_node(f.root,"MapList").read()
        else:
            Para = f.root.parameters
            el = f.get_node(Para, 'ElementList')
            self.ells = el.read()
        for item in self.ells:
            self.listWidget_Elem.addItem(item)
            self.comboBox.addItem(item)
            self.comboBox_2.addItem(item)
            self.comboBox_3.addItem(item)
        print 'items added'
        self.presets['Custom1']={'type':'B','function':'A /(A+B)','A':'Fe','B':'Ti'}
        self.presets['Custom2']={'type':'C','function':'A /(A+B+C)','A':'Mg','B':'Fe','C':'Ca'}
        self.presets['Single']={'type':'A','function':'A','A':'Mg'}
        if 'Cr' in self.ells:
            if 'Al' in self.ells:
                self.presets['Cr#'] = {'type':'B','function':'Cr/(Cr + Al)','A':'Cr','B':'Al'}
            else:
                print 'No Cr map'
        if 'Na' in self.ells:
            if 'Ca' in self.ells:
                self.presets['Anorthite'] = {'type':'B','type':'B','function':'Ca/(Ca + Na)','A':'Ca','B':'Na'}
            else:
                print 'No Ca map'
        if 'K' in self.ells:
            if 'Na' in self.ells:
                self.presets['Orthoclase'] = {'type':'B','type':'B','function':'K/(K + Na)','A':'K','B':'Na'}
            else:
                print 'No Na map'
        if 'Anorthite' in self.presets:
            if 'K' in self.ells:
                self.presets['AnorthiteK'] = {'type':'C','function':'Ca/(Ca+Na+K)','A':'Ca','B':'Na','C':'K'}
                self.presets['OrthoclaseC'] = {'type':'C','function':'K/(Ca+Na+K)','A':'K','B':'Ca','C':'Na'}
            else:
                print 'No K map'
        if 'Mg' in self.ells:
            if 'Fe' in self.ells:
                self.presets['Mg#'] = {'type':'B','function':'Mg /(Mg+Fe)','A':'Mg','B':'Fe'}
            else:
                print 'No Mg map'
        if 'Mn' in self.ells:
            if 'Ca' in self.ells:
                self.presets['Grossular'] = {'type':'D','function':'Ca/(Ca+Mg+Fe+Mn)','A':'Ca','B':'Mg','C':'Fe','D':'Mn'}
                self.presets['Pyrope'] = {'type':'D','function':'Mg/(Ca+Mg+Fe+Mn)','A':'Mg','B':'Ca','C':'Fe','D':'Mn'}
                self.presets['Almandine'] = {'type':'D','function':'Fe/(Ca+Mg+Fe+Mn)','A':'Fe','B':'Mg','C':'Ca','D':'Mn'}
                self.presets['Spessartine'] = {'type':'D','function':'Mn/(Ca+Mg+Fe+Mn)','A':'Mn','B':'Mg','C':'Fe','D':'Ca'}
            else:
                print 'No Mn map'
        self.comboBox_Presets.addItems(self.presets.keys())
        id = self.comboBox_Presets.findText('Custom1')
        self.comboBox_Presets.setCurrentIndex(id)
        id1 = self.comboBox.findText('Mg')
        id2 = self.comboBox_2.findText('Fe')
        id3 = self.comboBox_3.findText('Ca')
        self.comboBox.setCurrentIndex(id1)
        self.comboBox_2.setCurrentIndex(id2)
        self.comboBox_3.setCurrentIndex(id3)
        self.lineEdit_Name.setText('Custom1')
        self.curpres = 'Custom1'
        f.close()
        gc.collect()
        return
    def preset_select(self, item):
        var = str(item)
        self.curpres = var
        pres = self.presets[var]
        func = pres['function']
        self.label_Func.setText(func)
        typ = pres['type']
        if typ == 'A':
            va = pres['A']
            id1 = self.comboBox.findText(va)
            self.comboBox.clear()
            self.comboBox_2.clear()
            self.comboBox_3.clear()
            for item in self.ells:
                self.comboBox.addItem(item)
            self.comboBox.setCurrentIndex(id1)
        elif typ == 'B':
            va = pres['A']
            vb = pres['B']
            self.comboBox.clear()
            self.comboBox_2.clear()
            self.comboBox_3.clear()
            for item in self.ells:
                self.comboBox.addItem(item)
                self.comboBox_2.addItem(item)
            id1 = self.comboBox.findText(va)
            id2 = self.comboBox_2.findText(vb)
            self.comboBox.setCurrentIndex(id1)
            self.comboBox_2.setCurrentIndex(id2)
        elif typ == 'C':
            va = pres['A']
            vb = pres['B']
            vc = pres['C']
            self.mapvar_a = va
            self.mapvar_b = vb
            self.mapvar_c = vc
            self.comboBox.clear()
            self.comboBox_2.clear()
            self.comboBox_3.clear()
            for item in self.ells:
                self.comboBox.addItem(item)
                self.comboBox_2.addItem(item)
                self.comboBox_3.addItem(item)
            id1 = self.comboBox.findText(va)
            id2 = self.comboBox_2.findText(vb)
            id3 = self.comboBox_3.findText(vc)
            self.comboBox.setCurrentIndex(id1)
            self.comboBox_2.setCurrentIndex(id2)
            self.comboBox_3.setCurrentIndex(id3)
        elif typ == 'D':
            va = pres['A']
            vb = pres['B']
            vc = pres['C']
            self.mapvar_a = va
            self.mapvar_b = vb
            self.mapvar_c = vc
            self.comboBox.clear()
            self.comboBox_2.clear()
            self.comboBox_3.clear()
            for item in self.ells:
                self.comboBox.addItem(item)
            id1 = self.comboBox.findText(va)
            self.comboBox.setCurrentIndex(id1)
        self.lineEdit_Name.setText(self.curpres)
        return
    def mapvar_A(self, item):
        self.mapvar_a = str(item)
        return
    def mapvar_B(self, item):
        self.mapvar_b = str(item)
        return
    def mapvar_C(self, item):
        self.mapvar_c = str(item)
        return
    def Create_Map(self):
        self.mapvar_a = str(self.comboBox.currentText())
        self.mapvar_b = str(self.comboBox_2.currentText())
        self.mapvar_c= str(self.comboBox_3.currentText())
        mapname = str(self.lineEdit_Name.text())
        mindic = {'Anorthite': 1,'Orthoclase':1,'Mg#':1,'Cr#':1,
                  'Custom1':2,
                  'Single':3,
                  'Custom2':5,
                  'AnorthiteK':4,'OrthoclaseC':4, 
                  'Grossular':6, 'Pyrope':6, 'Almandine':6, 'Spessartine':6}
        val = mindic[self.curpres]
        val2 = val
        items = ("None","General", "Feldspar", "Pyroxene", "Olivine", "Oxide", "Garnet")
        if self.curpres == 'Mg#':
            val2 = 'MgN'
        elif self.curpres == 'Cr#':
            val2 = 'CrN'
        elif self.curpres == 'Grossular':
            val2 = 'Gro'
        elif self.curpres == 'Pyrope':
            val2 = 'Py'
        elif self.curpres == 'Spessartine':
            val2 = 'Sp'
        elif self.curpres == 'Almandine':
            val2 = 'Alm'
        if val == 6:
            phase = 'Garnet'
            if self.curpres == 'Grossular':
                val2 = 'Gro'
            elif self.curpres == 'Pyrope':
                val2 = 'Py'
            elif self.curpres == 'Spessartine':
                val2 = 'Sp'
            elif self.curpres == 'Almandine':
                val2 = 'Alm'
        elif self.curpres == 'Anorthite':
            phase = 'Feldspar'
            val2 = 'An'
        elif self.curpres == 'AnorthiteK':
            phase = 'Feldspar'
            val2 = 'AnK'
        elif self.curpres == 'Orthoclase':
            phase = 'Feldspar'
            val2 = 'Or'
        elif self.curpres == 'OrthoclaseC':
            phase = 'Feldspar'
            val2 = 'Or'
        else:
            item, ok = QtGui.QInputDialog.getItem(self,"Select Correction Type","List of Correction Models", items, 0, False)
            phase = str(item)
        print phase
        mapDic = {'A':self.mapvar_a,'B':self.mapvar_b,'C':self.mapvar_c,'function':val, 'correction':phase, 'val2': val2}
        import qacd_ratio as qr
        if val == 1:
            stringer = qr.map_calc1(self.varProj,mapname,mapDic)
        elif val == 2:
            stringer = qr.map_calc2(self.varProj,mapname,mapDic)
        elif val == 3:
            stringer = qr.map_calc3(self.varProj,mapname,mapDic)
        elif val == 4:
            stringer = qr.map_calc4(self.varProj,mapname,mapDic)
        elif val == 5:
            stringer = qr.map_calc5(self.varProj,mapname,mapDic)
        elif val == 6:
            stringer = qr.map_calc6(self.varProj,mapname,mapDic)
        print stringer
        f = tb.open_file(self.varProj, mode='a')
        tmp = f.root
        lis = tmp._v_children
        if phase == 'None':
            if 'MapList' in lis.keys():
                lst = f.get_node(f.root,"MapList").read()
                lst.append(mapname)
                f.remove_node(tmp, "MapList")
                f.create_array(tmp, "MapList", lst)
            else:
                lst = self.ells
                lst.append(mapname)
                f.create_array(tmp, "MapList", lst)
        else:
            if 'CorrList' in lis.keys():
                lst = f.get_node(f.root,"CorrList").read()
                lst.append(mapname)
                f.remove_node(tmp, "CorrList")
                f.create_array(tmp, "CorrList", lst)
            else:
                lst = []
                lst.append(mapname)
                f.create_array(tmp, "CorrList", lst)
            print
        log = f.get_node(f.root, "Log").read()
        import datetime
        string = datetime.datetime.now().strftime("%I:%M%p, %d %B %Y")
        log[14] = string
        var = log[13]
        if var == 'N/A':
            log[13] = str(1)
        else:
            var2 = int(var) + 1
            log[13] = str(var2)
        f.remove_node(f.root, "Log")
        f.create_array(f.root, "Log", log)
        f.close()
        self.close()
        return
        
import ProjectManager_rc

if __name__=='_main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    myDialog = QtGui.QDialog()
    ui = Ui_Ratio_Dialog()
    ui.setupUi(myDialog)
    myDialog.show()
    sys.exit(app.exec_())

