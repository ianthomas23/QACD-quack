# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui_about_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.resize(422, 564)
        self.verticalLayout = QtWidgets.QVBoxLayout(AboutDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.icon = QtWidgets.QLabel(AboutDialog)
        self.icon.setText("")
        self.icon.setPixmap(QtGui.QPixmap("resources/application_icon.png"))
        self.icon.setAlignment(QtCore.Qt.AlignCenter)
        self.icon.setObjectName("icon")
        self.verticalLayout.addWidget(self.icon)
        self.label_3 = QtWidgets.QLabel(AboutDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label = QtWidgets.QLabel(AboutDialog)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(AboutDialog)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.logo = QtWidgets.QLabel(AboutDialog)
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap("resources/logo256.png"))
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        self.logo.setObjectName("logo")
        self.verticalLayout.addWidget(self.logo)
        self.label_4 = QtWidgets.QLabel(AboutDialog)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(AboutDialog)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.buttonBox = QtWidgets.QDialogButtonBox(AboutDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AboutDialog)
        self.buttonBox.accepted.connect(AboutDialog.accept)
        self.buttonBox.rejected.connect(AboutDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        _translate = QtCore.QCoreApplication.translate
        AboutDialog.setWindowTitle(_translate("AboutDialog", "About QACD-quack"))
        self.label_3.setText(_translate("AboutDialog", "Quantitative Assessment of Compositional Distribution"))
        self.label.setText(_translate("AboutDialog", "This software is used for the processing of X-ray spectrum images or element maps collected by EDS (Energy Dispersive X-ray Spectroscopy) on scanning electron microscopes and electron microprobes."))
        self.label_2.setText(_translate("AboutDialog", "Original idea by Matthew Loocke"))
        self.label_4.setText(_translate("AboutDialog", "School of Earth and Ocean Sciences,\n"
"Cardiff University."))
        self.label_5.setText(_translate("AboutDialog", "<html><head/><body><p><a href=\"http://www.cardiff.ac.uk/earth-ocean-sciences\"><span style=\" text-decoration: underline; color:#0000ff;\">http://www.cardiff.ac.uk/earth-ocean-sciences</span></a></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AboutDialog = QtWidgets.QDialog()
    ui = Ui_AboutDialog()
    ui.setupUi(AboutDialog)
    AboutDialog.show()
    sys.exit(app.exec_())

