# Script to start QACD-quack graphical user interface.

from PyQt5 import QtWidgets
import sys

from src.ui.main_window import MainWindow


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()
