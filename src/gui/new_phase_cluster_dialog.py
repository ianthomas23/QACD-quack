import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

from .matplotlib_widget import PlotType
from .ui_new_phase_cluster_dialog import Ui_NewPhaseClusterDialog


class NewPhaseClusterDialog(QtWidgets.QDialog, Ui_NewPhaseClusterDialog):
    def __init__(self, project, cluster_map, cluster_map_stats, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window)

        self.clearButton.clicked.connect(self.clear_selections)
        self.deleteButton.clicked.connect(self.delete_phases)
        self.mergeButton.clicked.connect(self.merge_phases)
        self.tableWidget.itemSelectionChanged.connect(self.change_selection)

        self.project = project

        # Copy cluster_map and cluster_map_stats as do not want to alter
        # originals owned by parent.
        self.cluster_map = cluster_map.copy()
        self.cluster_map_stats = cluster_map_stats.copy()
        self.k = cluster_map_stats['max'] + 1

        # Count of pixels in each cluster.
        _, self.pixels = np.unique(np.ma.compressed(self.cluster_map),
                                   return_counts=True)

        self.matplotlibWidget.initialise(owning_window=self, zoom_enabled=False)
        self.update_matplotlib_widget()

        self.fill_table_widget()  # After mpl widget as uses its colormap.
        self.update_buttons()

    def accept(self):
        try:
            # Validation.


            # Create new phase maps.

            #self.project.create_phase_map_by_thresholding( \
            #    name, elements_and_thresholds, phase_map=self.phase_map)

            # Close dialog.
            super().accept()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Error', str(e))

    def change_selection(self):
        self.tableWidget.setCurrentItem(None)
        self.update_buttons()

    def clear_selections(self):
        self.tableWidget.clearSelection()

    def delete_phases(self):
        rows = self.get_selected_rows()
        print('selected rows', rows)
        #delete_count = len(rows)
        for row in rows:
            value = int(self.tableWidget.item(row, 1).text())
            print(row, value)
            self.cluster_map = np.ma.masked_equal(self.cluster_map, value)



        self.update_matplotlib_widget()

    def fill_table_widget(self):
        # Correct table widget properties.
        table_widget = self.tableWidget
        horiz = table_widget.horizontalHeader()
        horiz.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        horiz.setDefaultAlignment(QtCore.Qt.AlignLeft)
        vert = table_widget.verticalHeader()
        vert.setDefaultSectionSize(vert.minimumSectionSize())

        # Should cache pixel counts.............
        _, pixels = np.unique(np.ma.compressed(self.cluster_map),
                              return_counts=True)

        pixmap_size = (40, vert.minimumSectionSize()-1)
        cmap = self.matplotlibWidget.create_colormap()

        table_widget.setRowCount(self.k)
        for value in range(self.k):
            row = self.k-1 - value

            rgba = np.asarray(cmap(value)[:3])*255.0
            rgba = rgba.astype(np.int)
            pixmap = QtGui.QPixmap(pixmap_size[0], pixmap_size[1])
            pixmap.fill(QtGui.QColor(rgba[0], rgba[1], rgba[2], 255))

            self.set_table_widget_cell(table_widget, row, 0, 'phase {}'.format(value))
            self.set_table_widget_cell(table_widget, row, 1, value)
            self.set_table_widget_cell(table_widget, row, 2, pixmap)
            #self.set_table_widget_cell(table_widget, row, 3, pixels[value])

    def get_selected_rows(self):
        selected = self.tableWidget.selectionModel().selectedRows()
        rows = [model_index.row() for model_index in selected]
        return rows

    def merge_phases(self):
        pass

    def set_table_widget_cell(self, table_widget, row, column, contents):
        if contents is None:
            table_widget.setItem(row, column, None)
        elif isinstance(contents, QtGui.QPixmap):
            item = QtWidgets.QTableWidgetItem(None)
            item.setData(QtCore.Qt.DecorationRole, contents)
            table_widget.setItem(row, column, item)
        else:
            item = QtWidgets.QTableWidgetItem(str(contents))
            if column != 0:
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
            table_widget.setItem(row, column, item)

    def update_buttons(self):
        rows = self.get_selected_rows()
        nrows = len(rows)
        self.clearButton.setEnabled(nrows > 0)
        self.deleteButton.setEnabled(nrows > 0)
        self.mergeButton.setEnabled(nrows > 1)

    def update_matplotlib_widget(self):
        title = 'k={} cluster'.format(self.k)
        self.matplotlibWidget.update( \
            PlotType.MAP, self.cluster_map, self.cluster_map_stats, title,
            show_colorbar=True, cmap_int_max = self.k)
