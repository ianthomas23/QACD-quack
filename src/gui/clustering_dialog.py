from PyQt5 import QtCore, QtGui, QtWidgets

from .ui_clustering_dialog import Ui_ClusteringDialog


class ClusteringDialog(QtWidgets.QDialog, Ui_ClusteringDialog):
    def __init__(self, project, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.project = project

    def accept(self):
        try:
            k_min, k_max, want_all_elements = self.get_values()

            if k_min > k_max:
                raise RuntimeError('Maximum k must be equal to or greater than minimum k.')

            if not want_all_elements:
                proj = self.project
                elements = set(proj.common_elements).intersection(proj.elements)
                if len(elements) == 0:
                    raise RuntimeError("Project does not contain any of the common elements.  Select 'All elements' instead.")

            # Close dialog.
            super().accept()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Error', str(e))

    def get_values(self):
        # Returns tuple of (k_min, k_max, want_all_elements).
        return (self.kMinimumSpin.value(), self.kMaximumSpin.value(),
                self.allElementsRadioButton.isChecked())
