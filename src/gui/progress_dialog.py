from PyQt5 import QtCore, QtGui, QtWidgets
import threading

from .ui_progress_dialog import Ui_ProgressDialog


class ProgressDialog(QtWidgets.QDialog, Ui_ProgressDialog):
    callback_signal = QtCore.pyqtSignal(int, str)

    def __init__(self, title, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle(title)
        self.callback_signal.connect(self.callback)
        self.callback(0, '')

    def callback(self, percent, text):
        #print(percent, text)
        self.label.setText(text)
        self.progress.setValue(percent)
        self.update()  # Schedule repaint.

        if percent >= 100:
            QtCore.QTimer.singleShot(500, self.close)

    # Display progress of worker thread.
    # Note args excludes the callback; it is appended herein.
    @staticmethod
    def worker_thread(parent, title, thread_func, args):
        def local_callback(fraction, text=''):
            progress.callback_signal.emit(int(100*fraction), text)

        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.BusyCursor)

        progress = ProgressDialog(title, parent=parent)
        thread = threading.Thread(target=thread_func,
                                  args=args + [local_callback])
        progress.show()  # Display dialog before starting worker thread.
        thread.start()
        progress.exec_()
        thread.join()  # Wait for thread (in case dialog closed early).

        QtWidgets.QApplication.restoreOverrideCursor()
