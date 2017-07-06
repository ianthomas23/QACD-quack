__author__ = 'Matthew Loocke'
__version__= '1.0'

#import 3rd party libraries
from PyQt4.QtGui import QApplication
from unt import MainWindow


if __name__=='__main__':
    import sys
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
