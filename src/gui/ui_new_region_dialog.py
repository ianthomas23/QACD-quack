# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui_new_region_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NewRegionDialog(object):
    def setupUi(self, NewRegionDialog):
        NewRegionDialog.setObjectName("NewRegionDialog")
        NewRegionDialog.resize(392, 221)
        self.formLayout = QtWidgets.QFormLayout(NewRegionDialog)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(NewRegionDialog)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.label_2)
        self.groupBox = QtWidgets.QGroupBox(NewRegionDialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.ellipseRadioButton = QtWidgets.QRadioButton(self.groupBox)
        self.ellipseRadioButton.setChecked(True)
        self.ellipseRadioButton.setObjectName("ellipseRadioButton")
        self.verticalLayout_3.addWidget(self.ellipseRadioButton)
        self.polygonRadioButton = QtWidgets.QRadioButton(self.groupBox)
        self.polygonRadioButton.setObjectName("polygonRadioButton")
        self.verticalLayout_3.addWidget(self.polygonRadioButton)
        self.rectangleRadioButton = QtWidgets.QRadioButton(self.groupBox)
        self.rectangleRadioButton.setObjectName("rectangleRadioButton")
        self.verticalLayout_3.addWidget(self.rectangleRadioButton)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.groupBox)
        self.label = QtWidgets.QLabel(NewRegionDialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label)
        self.nameLineEdit = QtWidgets.QLineEdit(NewRegionDialog)
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.nameLineEdit)
        self.buttonBox = QtWidgets.QDialogButtonBox(NewRegionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.buttonBox)

        self.retranslateUi(NewRegionDialog)
        self.buttonBox.accepted.connect(NewRegionDialog.accept)
        self.buttonBox.rejected.connect(NewRegionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewRegionDialog)

    def retranslateUi(self, NewRegionDialog):
        _translate = QtCore.QCoreApplication.translate
        NewRegionDialog.setWindowTitle(_translate("NewRegionDialog", "Create new region"))
        self.label_2.setText(_translate("NewRegionDialog", "To create a new region, select the area of interest using the mouse, enter a name, and click the OK button."))
        self.groupBox.setTitle(_translate("NewRegionDialog", "Shape of region to create"))
        self.ellipseRadioButton.setText(_translate("NewRegionDialog", "Ellipse"))
        self.polygonRadioButton.setText(_translate("NewRegionDialog", "Polygon"))
        self.rectangleRadioButton.setText(_translate("NewRegionDialog", "Rectangle"))
        self.label.setText(_translate("NewRegionDialog", "Region name"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    NewRegionDialog = QtWidgets.QDialog()
    ui = Ui_NewRegionDialog()
    ui.setupUi(NewRegionDialog)
    NewRegionDialog.show()
    sys.exit(app.exec_())

