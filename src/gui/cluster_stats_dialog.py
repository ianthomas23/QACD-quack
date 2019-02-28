import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

from .numeric_table_widget_item import NumericTableWidgetItem
from .ui_cluster_stats_dialog import Ui_ClusterStatsDialog


class ClusterStatsDialog(QtWidgets.QDialog, Ui_ClusterStatsDialog):
    def __init__(self, project, k, cmap, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle('k={} Cluster Stats Dialog'.format(k))

        #self.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)

        self._project = project
        self._k = k
        self._cmap = cmap
        self._elements, self._centroids = \
            self._project.get_cluster_centroids(self._k)
        self._show_cluster = np.ones(self._k, dtype=np.bool)

        self._latest_callback_data = None

        self.tabWidget.setCurrentIndex(0)
        self.fill_tabs()

        self.showClusterTableWidget.itemChanged.connect(self.on_checkbox)
        self.showAllButton.clicked.connect(self.on_show_all)
        self.hideAllButton.clicked.connect(self.on_hide_all)
        self.showXAxisLabelsCheckBox.stateChanged.connect(self.on_show_x_axis_labels)

        self.update_buttons()

    def fill_tabs(self):
        ## Table tab.
        table = self.table

        nelements = len(self._elements)
        table.setRowCount(self._k)
        table.setColumnCount(nelements+1)

        colours = self._cmap(np.arange(self._k) / (self._k-1.0))
        colours = (np.asarray(colours[:, :3])*255).astype(np.int)
        is_dark = [QtGui.qGray(*colour) < 128 for colour in colours]
        qt_colours = [QtGui.QColor(*colour) for colour in colours]
        qt_white = QtGui.QColor(255, 255, 255)

        # Column headings.
        table.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('Cluster'))
        for i in range(nelements):
            text = self._elements[i]
            table.setHorizontalHeaderItem(i+1, QtWidgets.QTableWidgetItem(text))

        # Row headings.
        for k in range(self._k):
            item = QtWidgets.QTableWidgetItem(str(k))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setBackground(qt_colours[k])
            if is_dark[k]:
                item.setForeground(qt_white)
            table.setItem(k, 0, item)

        # Cell contents.
        for k in range(self._k):
            for i in range(nelements):
                item = NumericTableWidgetItem(self._centroids[k, i], '{:.1f}')
                item.setBackground(qt_colours[k])
                if is_dark[k]:
                    item.setForeground(qt_white)
                table.setItem(k, i+1, item)

        # Reset cells.
        table.resizeColumnsToContents()
        #table.resizeRowsToContents()

        ## Plot tab.

        # Table widget.
        table = self.showClusterTableWidget
        table.setColumnCount(2)
        table.setRowCount(self._k)
        for k in range(self._k):
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setBackground(qt_colours[k])
            item.setCheckState(QtCore.Qt.Checked)
            table.setItem(k, 0, item)

            item = QtWidgets.QTableWidgetItem(str(k))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setBackground(qt_colours[k])
            if is_dark[k]:
                item.setForeground(qt_white)
            table.setItem(k, 1, item)

        table.resizeColumnsToContents()

        # Matplotlib widget.
        widget = self.clusterStatsWidget
        widget.initialise(self, self._project, self._elements, self._centroids,
                          colours, self.on_status_callback)
        widget.update()

    def on_checkbox(self, item):
        k = item.row()
        checked = item.checkState() == QtCore.Qt.Checked

        self._show_cluster[k] = checked
        self.clusterStatsWidget.show_clusters([k], checked)

        self.update_buttons()

    def on_hide_all(self):
        need_to_hide = self._show_cluster.nonzero()[0]

        self._show_cluster.fill(False)
        self.clusterStatsWidget.show_clusters(need_to_hide, False)

        table = self.showClusterTableWidget
        for k in need_to_hide:
            table.item(k, 0).setCheckState(QtCore.Qt.Unchecked)
        self.update_buttons()

    def on_show_all(self):
        need_to_show = (~self._show_cluster).nonzero()[0]

        self._show_cluster.fill(True)
        self.clusterStatsWidget.show_clusters(need_to_show, True)

        table = self.showClusterTableWidget
        for k in need_to_show:
            table.item(k, 0).setCheckState(QtCore.Qt.Checked)
        self.update_buttons()

    def on_show_x_axis_labels(self):
        self.clusterStatsWidget.show_x_axis_labels( \
            self.showXAxisLabelsCheckBox.isChecked())

    def on_status_callback(self, callback_data):
        if callback_data != self._latest_callback_data:
            self._latest_callback_data = callback_data
            msg = ''
            if self._latest_callback_data is not None:
                msg = 'element={}, value={:.1f}'.format(*self._latest_callback_data)
            self.statusLabel.setText(msg)

    def update_buttons(self):
        show_count = self._show_cluster.sum()
        self.showAllButton.setEnabled(show_count < self._k)
        self.hideAllButton.setEnabled(show_count > 0)
