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
        NewRegionDialog.resize(478, 823)
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
        self.label2 = QtWidgets.QLabel(NewRegionDialog)
        self.label2.setObjectName("label2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label2)
        self.regionComboBox = QtWidgets.QComboBox(NewRegionDialog)
        self.regionComboBox.setObjectName("regionComboBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.regionComboBox)
        self.label = QtWidgets.QLabel(NewRegionDialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label)
        self.nameLineEdit = QtWidgets.QLineEdit(NewRegionDialog)
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.nameLineEdit)
        self.matplotlibWidget = MatplotlibWidget(NewRegionDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.matplotlibWidget.sizePolicy().hasHeightForWidth())
        self.matplotlibWidget.setSizePolicy(sizePolicy)
        self.matplotlibWidget.setMinimumSize(QtCore.QSize(100, 100))
        self.matplotlibWidget.setObjectName("matplotlibWidget")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.matplotlibWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(NewRegionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.SpanningRole, self.buttonBox)

        self.retranslateUi(NewRegionDialog)
        self.buttonBox.accepted.connect(NewRegionDialog.accept)
        self.buttonBox.rejected.connect(NewRegionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewRegionDialog)

    def retranslateUi(self, NewRegionDialog):
        _translate = QtCore.QCoreApplication.translate
        NewRegionDialog.setWindowTitle(_translate("NewRegionDialog", "Create new region"))
        self.label_2.setText(_translate("NewRegionDialog", "<html><head/><body><p>To create a new region:\n"
"<ol>\n"
"<li>Choose a shape below.</li>\n"
"<li>Select the region using the mouse.</li>\n"
"<li>Enter a name.</li>\n"
"<li>Click the OK button.</li>\n"
"</ol>\n"
"For an ellipse or rectangle region, click and hold the mouse button down, drag to enclose the are of interest, then release the mouse button.</p>\n"
"<p>For a polygon region, click the mouse button to add each point. To close the polygon either double-click the mouse button or place the mouse over the first point (the point will turn yellow) and click the mouse button once.\n"
"</p>\n"
"</body></html>"))
        self.groupBox.setTitle(_translate("NewRegionDialog", "Shape of region to create"))
        self.ellipseRadioButton.setText(_translate("NewRegionDialog", "Ellipse"))
        self.polygonRadioButton.setText(_translate("NewRegionDialog", "Polygon"))
        self.rectangleRadioButton.setText(_translate("NewRegionDialog", "Rectangle"))
        self.label2.setText(_translate("NewRegionDialog", "Region to add to"))
        self.label.setText(_translate("NewRegionDialog", "New region name"))

from .matplotlib_widget import MatplotlibWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    NewRegionDialog = QtWidgets.QDialog()
    ui = Ui_NewRegionDialog()
    ui.setupUi(NewRegionDialog)
    NewRegionDialog.show()
    sys.exit(app.exec_())

