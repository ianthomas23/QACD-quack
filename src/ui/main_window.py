from PyQt5 import QtCore, QtWidgets, QtGui

from src.model.qacd_project import QACDProject
from .ui_main_window import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setupUi(self)

        self.actionProjectNew.triggered.connect(self.on_project_new)
        self.actionProjectOpen.triggered.connect(self.on_project_open)
        self.actionProjectClose.triggered.connect(self.on_project_close)

    def on_project_close(self):
        print('Project | Close')

    def on_project_new(self):
        print('Project | New')
        self.project = QACDProject()  # Check can create project.
        print(self.project)

    def on_project_open(self):
        print('Project | Open')
