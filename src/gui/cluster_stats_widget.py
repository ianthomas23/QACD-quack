# Matplotlib widget to render cluster stats.

import matplotlib as mpl
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from PyQt5 import QtWidgets


class ClusterStatsWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(ClusterStatsWidget, self).__init__(parent)

        self._canvas = FigureCanvas(Figure())
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.addWidget(self._canvas)
        self.setLayout(self._layout)

        self._want_triangles = True
        self._triangle_width = 0.015

        # Initialised in initialise().
        self._owning_window = None
        self._elements = None
        self._centroids = None
        self._k = None
        self._colours = None
        self._limits = None
        self._symbols = None         # Artists to show/hide for each k.
        self._status_callback = None

        # Initialised in update().
        self._axes = None

        self._canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        self._canvas.mpl_connect('resize_event', self.on_resize)

    def _adjust_layout(self):
        self._canvas.figure.tight_layout(h_pad=0.1, w_pad=0.1)

    def initialise(self, owning_window, project, elements, centroids, colours,
                   status_callback):
        self._owning_window = owning_window
        self._elements = elements
        self._centroids = centroids
        self._k = self._centroids.shape[0]
        self._colours = colours / 255.0
        self._symbols = [[] for k in range(self._k)]
        self._status_callback = status_callback

        # Limits by element.
        nelements = len(self._elements)
        self._limits = np.empty((nelements, 2))
        for i, element in enumerate(self._elements):
            _, stats = project.get_filtered(element, masked=False,
                                            want_stats=True)
            self._limits[i] = (stats['min'], stats['max'])

    def on_mouse_move(self, event):
        if self._status_callback is not None:
            if event.inaxes is not None:
                self._status_callback((event.inaxes.get_ylabel(), event.xdata))
            else:
                self._status_callback(None)

    def on_resize(self, event):
        self._adjust_layout()

    def show_clusters(self, ks, show):
        for k in ks:
            for symbol in self._symbols[k]:
                symbol.set_visible(show)

        self._canvas.draw()

    def show_x_axis_labels(self, show):
        for ax in self._axes:
            ax.xaxis.set_visible(show)

        self._adjust_layout()
        self._canvas.draw()

    def update(self):
        figure = self._canvas.figure
        figure.clear()

        self._axes = figure.subplots(nrows=len(self._elements))

        for i, element in enumerate(self._elements):
            ax = self._axes[i]

            if self._want_triangles:
                # Draw triangles in sorted order, left to right.
                sorted_indices = np.argsort(self._centroids[:, i])
                for k in sorted_indices:
                    x = self._centroids[k, i]
                    w = self._triangle_width*np.diff(self._limits[i])
                    symbol = ax.fill([x-w/2, x+w/2, x], [0, 0, 1], lw=None,
                                     edgecolor=None, color=self._colours[k])[0]
                    self._symbols[k].append(symbol)
            else:
                for k in range(self._k):
                    symbol = ax.axvline(self._centroids[k, i],
                                        c=self._colours[k], lw=3)
                    self._symbols[k].append(symbol)

            ax.set_xlim(self._limits[i])
            if self._want_triangles:
                ax.set_ylim([0, 1])
            ax.set_ylabel(element, rotation=0, ha='right', va='center')
            ax.set_yticks([])

        self._adjust_layout()
