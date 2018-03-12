from enum import Enum, unique
from matplotlib.backends.backend_qt5agg import FigureCanvas
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from matplotlib.figure import Figure
import numpy as np
from PyQt5 import QtWidgets


# Same values as in plotTypeComboBox.
@unique
class PlotType(Enum):
    INVALID   = -1
    MAP       =  0
    HISTOGRAM =  1
    BOTH      =  2


class MatplotlibWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(MatplotlibWidget, self).__init__(parent)

        self._canvas = FigureCanvas(Figure())
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.addWidget(self._canvas)
        self.setLayout(self._layout)

    def clear(self):
        self._canvas.figure.clear()
        self._canvas.draw()

    def update(self, plot_type, array, array_stats, title):
        figure = self._canvas.figure
        figure.clear()

        map_axes = None
        histogram_axes = None
        if plot_type == PlotType.MAP:
            map_axes = figure.subplots()
        elif plot_type == PlotType.HISTOGRAM:
            histogram_axes = figure.subplots()
        elif plot_type == PlotType.BOTH:
            map_axes, histogram_axes = figure.subplots( \
                nrows=2, gridspec_kw={'height_ratios': (3,1)})
        else:
            raise RuntimeError('Invalid plot type')

        cmap = cm.get_cmap('rainbow')
        norm = Normalize(array_stats['min'], array_stats['max'])
        show_stats = True

        if map_axes is not None:
            image = map_axes.imshow(array, cmap=cmap, norm=norm)
            colorbar = figure.colorbar(image, ax=map_axes)
            #map_axes.set_xlabel('x')
            #map_axes.set_ylabel('y')
            map_axes.set_title(title + ' element map')

        if histogram_axes is not None:
            hist, bin_edges = np.histogram(array, bins='sqrt')
            width = bin_edges[1] - bin_edges[0]
            bin_centres = bin_edges[:-1] + 0.5*width
            colors = cmap(norm(bin_centres))
            histogram_axes.bar(bin_centres, hist, width, color=colors)
            if show_stats:
                mean = array_stats.get('mean')
                median = array_stats.get('median')
                std = array_stats.get('std')
                if mean is not None:
                    histogram_axes.axvline(mean, c='k', ls='-', label='mean')
                    if std is not None:
                        histogram_axes.axvline(mean-std, c='k', ls='-.',
                                               label='mean +/- std')
                        histogram_axes.axvline(mean+std, c='k', ls='-.')
                if median is not None:
                    histogram_axes.axvline(median, c='k', ls='--',
                                           label='median')
                histogram_axes.legend()

            if map_axes is None:
                histogram_axes.set_title(title + ' histogram')

        self._canvas.draw()
