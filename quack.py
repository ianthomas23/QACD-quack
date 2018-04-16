# Script to start QACD-quack graphical user interface.

from PyQt5 import QtWidgets
import sys

from src.gui.main_window import MainWindow


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    if len(sys.argv) > 1:
        main_window.open_project(sys.argv[1])
    app.exec_()
