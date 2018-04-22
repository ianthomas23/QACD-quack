# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui_clustering_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ClusteringDialog(object):
    def setupUi(self, ClusteringDialog):
        ClusteringDialog.setObjectName("ClusteringDialog")
        ClusteringDialog.resize(370, 274)
        self.verticalLayout = QtWidgets.QVBoxLayout(ClusteringDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(ClusteringDialog)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(ClusteringDialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.kMinimumSpin = QtWidgets.QSpinBox(ClusteringDialog)
        self.kMinimumSpin.setMinimum(1)
        self.kMinimumSpin.setProperty("value", 5)
        self.kMinimumSpin.setObjectName("kMinimumSpin")
        self.horizontalLayout.addWidget(self.kMinimumSpin)
        self.label_3 = QtWidgets.QLabel(ClusteringDialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.kMaximumSpin = QtWidgets.QSpinBox(ClusteringDialog)
        self.kMaximumSpin.setMinimum(1)
        self.kMaximumSpin.setProperty("value", 10)
        self.kMaximumSpin.setObjectName("kMaximumSpin")
        self.horizontalLayout.addWidget(self.kMaximumSpin)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.groupBox = QtWidgets.QGroupBox(ClusteringDialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.allElementsRadioButton = QtWidgets.QRadioButton(self.groupBox)
        self.allElementsRadioButton.setChecked(True)
        self.allElementsRadioButton.setObjectName("allElementsRadioButton")
        self.verticalLayout_3.addWidget(self.allElementsRadioButton)
        self.commonElementsRadioButton = QtWidgets.QRadioButton(self.groupBox)
        self.commonElementsRadioButton.setObjectName("commonElementsRadioButton")
        self.verticalLayout_3.addWidget(self.commonElementsRadioButton)
        self.verticalLayout.addWidget(self.groupBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(ClusteringDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ClusteringDialog)
        self.buttonBox.accepted.connect(ClusteringDialog.accept)
        self.buttonBox.rejected.connect(ClusteringDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ClusteringDialog)

    def retranslateUi(self, ClusteringDialog):
        _translate = QtCore.QCoreApplication.translate
        ClusteringDialog.setWindowTitle(_translate("ClusteringDialog", "k-means Clustering"))
        self.label.setText(_translate("ClusteringDialog", "<html><head/><body><p>Enter a minimum and maximum number of phases (k) in the sample. Remember that the glass slide of a thin section needs to be accounted for along with any potential major alteration phases.</p></body></html>"))
        self.label_2.setText(_translate("ClusteringDialog", "Minimum k:"))
        self.label_3.setText(_translate("ClusteringDialog", "Maximum k:"))
        self.groupBox.setTitle(_translate("ClusteringDialog", "Elements to include"))
        self.allElementsRadioButton.setText(_translate("ClusteringDialog", "All elements"))
        self.commonElementsRadioButton.setText(_translate("ClusteringDialog", "Common elements only (Al, Ca, Fe, Mg, Si)"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ClusteringDialog = QtWidgets.QDialog()
    ui = Ui_ClusteringDialog()
    ui.setupUi(ClusteringDialog)
    ClusteringDialog.show()
    sys.exit(app.exec_())

