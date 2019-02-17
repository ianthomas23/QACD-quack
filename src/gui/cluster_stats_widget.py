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

        # Initialised in initialise().
        self._owning_window = None
        self._elements = None
        self._centroids = None
        self._k = None
        self._colours = None
        self._limits = None

        self._canvas.mpl_connect('resize_event', self.on_resize)

    def _adjust_layout(self):
        self._canvas.figure.tight_layout(h_pad=0.1, w_pad=0.1)

    def initialise(self, owning_window, project, elements, centroids, colours):
        self._owning_window = owning_window
        self._elements = elements
        self._centroids = centroids
        self._k = self._centroids.shape[0]
        self._colours = colours / 255.0

        # Limits by element.
        nelements = len(self._elements)
        self._limits = np.empty((nelements, 2))
        for i, element in enumerate(self._elements):
            _, stats = project.get_filtered(element, masked=False,
                                            want_stats=True)
            self._limits[i] = (stats['min'], stats['max'])

    def on_resize(self, event):
        self._adjust_layout()

    def update(self):
        want_triangles = True

        figure = self._canvas.figure
        figure.clear()

        axes = figure.subplots(nrows=len(self._elements))

        for i, element in enumerate(self._elements):
            ax = axes[i]
            for k in range(self._k):
                colour = self._colours[k]
                if want_triangles:
                    w = 0.02*(self._limits[i][1] - self._limits[i][0])
                    x = self._centroids[k, i]
                    ax.fill([x-w/2, x+w/2, x], [0, 0, 1], color=colour,
                            edgecolor=None, lw=None)
                else:
                    ax.axvline(self._centroids[k, i], color=colour, lw=3)
            ax.set_xlim(self._limits[i])
            if want_triangles:
                ax.set_ylim([0, 1])
            ax.set_ylabel(element, rotation=0, ha='right', va='center')
            ax.set_yticks([])

        self._adjust_layout()
