from collections import Counter
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
        self.tableWidget.itemChanged.connect(self.change_name)

        # Correct table widget properties.
        horiz = self.tableWidget.horizontalHeader()
        horiz.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        horiz.setDefaultAlignment(QtCore.Qt.AlignLeft)
        vert = self.tableWidget.verticalHeader()
        vert.setDefaultSectionSize(vert.minimumSectionSize())

        self.project = project

        # Copy cluster_map and cluster_map_stats as do not want to alter
        # originals owned by parent.
        self.cluster_map = cluster_map.copy()
        self.cluster_map.unshare_mask()
        self.cluster_map_stats = cluster_map_stats.copy()
        self.k = cluster_map_stats['max'] + 1
        self.nvalues = self.k

        self.ignore_change_name = True

        # Names, pixel counts and list of original values for each cluster are
        # stored in a cache.
        _, pixels = np.unique(np.ma.compressed(self.cluster_map),
                              return_counts=True)
        self.cache = [[None, pixels[value], [value]] for value in range(self.nvalues)]

        self.matplotlibWidget.initialise(owning_window=self, zoom_enabled=False)

        self.clear_selections()
        self.update_status_label()
        self.update_matplotlib_widget()
        self.fill_table_widget()  # After mpl widget as uses its colormap.
        self.update_buttons()

    def accept(self):
        try:
            # Validation.
            names = [item[0] or self.get_default_name(value) \
                     for value, item in enumerate(self.cache)]
            already_used = []
            for name in names:
                if name in self.project.phases:
                    already_used.append(name)
            if len(already_used) > 0:
                msg = ', '.join(already_used)
                raise RuntimeError('The following phase names have already in use: ' + msg)

            # Create new phase maps one at a time, as unmasked boolean arrays.
            for value in range(self.nvalues):
                name = names[value]
                original_values = self.cache[value][2]
                phase_map = self.cluster_map == value

                self.project.create_phase_map_from_cluster( \
                    name, phase_map, self.k, original_values)

            # Close dialog.
            super().accept()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Error', str(e))

    def change_name(self, item):
        if not self.ignore_change_name and item is not None and item.column() == 0:
            row = item.row()
            name = item.text()
            value = int(self.tableWidget.item(row, 1).text())
            old_name = self.cache[value][0]
            self.cache[value][0] = name
            if self.has_duplicate_names():
                QtWidgets.QMessageBox.warning(self, 'Warning',
                    "Name '{}' is already in use, reverting change.".format(name))
                if not old_name:
                    old_name = self.get_default_name(value)
                self.ignore_change_name = True
                self.set_table_widget_cell(self.tableWidget, row, 0, old_name)
                self.ignore_change_name = False

    def change_selection(self):
        self.tableWidget.setCurrentItem(None)
        self.update_buttons()

    def clear_selections(self):
        self.tableWidget.clearSelection()
        self.tableWidget.setCurrentItem(None)

    def delete_phases(self):
        values = self.get_selected_values()
        values.sort(reverse=True)
        for value in values:
            # Count of deleted pixels.
            count = self.cache[value][1]

            # Mask out deleted pixels.
            self.cluster_map = np.ma.masked_equal(self.cluster_map, value)

            # Reduce values larger than the deleted value by one.
            self.cluster_map[self.cluster_map > value] -= 1
            if self.cluster_map_stats['max'] > 0:
                self.cluster_map_stats['max'] -= 1
            self.nvalues -= 1

            # Delete entry from cache.
            self.cache.pop(value)

            # Correct stats.
            self.cluster_map_stats['valid'] -= count
            self.cluster_map_stats['invalid'] += count

        self.update_status_label()
        self.update_matplotlib_widget()
        self.clear_selections()
        self.fill_table_widget()  # After mpl widget as uses its colormap.
        self.update_buttons()

    def fill_table_widget(self, select_value=None):
        self.ignore_change_name = True
        table_widget = self.tableWidget

        cmap = self.matplotlibWidget.create_colormap()
        pixmap_size = \
            (40, self.tableWidget.verticalHeader().minimumSectionSize()-1)

        table_widget.setRowCount(self.nvalues)
        for value in range(self.nvalues):
            row = self.nvalues-1 - value

            rgba = np.asarray(cmap(value)[:3])*255.0
            rgba = rgba.astype(np.int)
            pixmap = QtGui.QPixmap(pixmap_size[0], pixmap_size[1])
            pixmap.fill(QtGui.QColor(rgba[0], rgba[1], rgba[2], 255))

            name, pixels, original_values = self.cache[value]
            if name is None:
                name = self.get_default_name(value)
            original_values = ', '.join(map(str, original_values))

            self.set_table_widget_cell(table_widget, row, 0, name)
            self.set_table_widget_cell(table_widget, row, 1, value)
            self.set_table_widget_cell(table_widget, row, 2, pixmap)
            self.set_table_widget_cell(table_widget, row, 3, pixels)
            self.set_table_widget_cell(table_widget, row, 4, original_values)

            if select_value == value:
                table_widget.selectRow(row)

        self.ignore_change_name = False

    def get_default_name(self, value):
        return '<phase {}>'.format(value)

    def get_selected_rows(self):
        selected = self.tableWidget.selectionModel().selectedRows()
        rows = [model_index.row() for model_index in selected]
        return rows

    def get_selected_values(self):
        rows = self.get_selected_rows()
        values = [int(self.tableWidget.item(row, 1).text()) for row in rows]
        return values

    def has_duplicate_names(self):
        names = [item[0] for item in self.cache if item[0]]
        counter = Counter(names)
        return len(counter) != len(names)

    def merge_phases(self):
        # Merge into the cluster with the lowest value.
        values = self.get_selected_values()
        values.sort(reverse=True)
        source_values = values[:-1]
        target_value = values[-1]
        for source_value in source_values:
            # Transfer pixels from source to target.
            self.cluster_map[self.cluster_map == source_value] = target_value

            # Correct target pixel count.
            self.cache[target_value][1] += self.cache[source_value][1]

            # Reduce values larger than the source value by one.
            self.cluster_map[self.cluster_map > source_value] -= 1
            if self.cluster_map_stats['max'] > 0:
                self.cluster_map_stats['max'] -= 1
            self.nvalues -= 1

            # Correct target original_values.
            self.cache[target_value][2] += self.cache[source_value][2]
            self.cache[target_value][2].sort()

            # Delete entry from cache.
            self.cache.pop(source_value)

        self.update_status_label()
        self.update_matplotlib_widget()
        self.clear_selections()
        self.fill_table_widget(select_value=target_value)  # After mpl widget as uses its colormap.
        self.update_buttons()

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
            show_colorbar=True, cmap_int_max=self.cluster_map_stats['max']+1)

    def update_status_label(self):
        msg = self.parent().get_status_string(self.cluster_map,
                                              self.cluster_map_stats)
        self.statusLabel.setText(msg)
