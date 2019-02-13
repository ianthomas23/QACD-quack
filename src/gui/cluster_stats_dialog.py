import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

from .numeric_table_widget_item import NumericTableWidgetItem
from .ui_cluster_stats_dialog import Ui_ClusterStatsDialog


class ClusterStatsDialog(QtWidgets.QDialog, Ui_ClusterStatsDialog):
    def __init__(self, project, k, cmap, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

       # self.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)

        self.project = project
        self.k = k
        self.cmap = cmap
        self.elements, self.centroids = self.project.get_cluster_centroids(self.k)

        self.fill_table()

    def fill_table(self):
        table = self.table

        nelements = len(self.elements)
        table.setRowCount(self.k)
        table.setColumnCount(nelements+1)

        colours = self.cmap(np.arange(self.k) / (self.k-1.0))
        colours = (np.asarray(colours[:, :3])*255).astype(np.int)
        is_dark = [QtGui.qGray(*colour) < 128 for colour in colours]
        colours = [QtGui.QColor(*colour) for colour in colours]
        white = QtGui.QColor(255, 255, 255)

        # Column headings.
        table.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('Cluster'))
        for i in range(nelements):
            text = self.elements[i]
            table.setHorizontalHeaderItem(i+1, QtWidgets.QTableWidgetItem(text))

        # Row headings.
        for k in range(self.k):
            item = QtWidgets.QTableWidgetItem(str(k))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setBackground(colours[k])
            if is_dark[k]:
                item.setForeground(white)
            table.setItem(k, 0, item)

        # Cell contents.
        for k in range(self.k):
            for i in range(nelements):
                item = NumericTableWidgetItem(self.centroids[k, i])
                item.setBackground(colours[k])
                if is_dark[k]:
                    item.setForeground(white)
                table.setItem(k, i+1, item)

        # Reset cells.
        table.resizeColumnsToContents()
        #table.resizeRowsToContents()
