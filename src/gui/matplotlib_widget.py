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

        self._image = None       # Image used for element map.
        self._bar = None         # Bar used for histogram.
        self._bar_norm_x = None  # Normalised x-positions of centres of bars
                                 #   in range 0 (= min) to 1.0 (= max value).

        self._valid_colormap_names = self._determine_valid_colormap_names()
        self._colormap = cm.get_cmap('rainbow')

    def _determine_valid_colormap_names(self):
        # Exclude reversed cmaps which have names ending with '_r'.
        all_ = set(filter(lambda s: not s.endswith('_r'), cm.cmap_d.keys()))

        # Exclude qualitative and repeating cmaps, and the deprecated
        # 'spectral' which has been replaced with 'nipy_spectral'.
        exclude = set(['Accent', 'Dark2', 'Paired', 'Pastel1', 'Pastel2',
                       'Set1', 'Set2', 'Set3', 'Vega10', 'Vega20', 'Vega20b',
                       'Vega20c', 'flag', 'prism', 'spectral', 'tab10',
                       'tab20', 'tab20b', 'tab20c'])
        return sorted(all_.difference(exclude))

    def clear(self):
        self._canvas.figure.clear()
        self._canvas.draw()

    def get_colormap_name(self):
        return self._colormap.name

    def get_valid_colormap_names(self):
        return self._valid_colormap_names

    def set_colormap(self, colormap):
        self._colormap = cm.get_cmap(colormap)

        if self._image is not None:
            self._image.set_cmap(self._colormap)

        if self._bar is not None:
            colors = self._colormap(self._bar_norm_x)
            for index, item in enumerate(self._bar):
                item.set_color(colors[index])

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

        norm = Normalize(array_stats['min'], array_stats['max'])
        show_stats = True

        if map_axes is None:
            self._image = None
        else:
            self._image = map_axes.imshow(array, cmap=self._colormap, norm=norm)
            colorbar = figure.colorbar(self._image, ax=map_axes)
            #map_axes.set_xlabel('x')
            #map_axes.set_ylabel('y')
            map_axes.set_title(title + ' element map')

        if histogram_axes is None:
            self._bar = None
            self._bar_norm_x = None
        else:
            hist, bin_edges = np.histogram(np.ma.compressed(array), bins='sqrt')
            width = bin_edges[1] - bin_edges[0]
            bin_centres = bin_edges[:-1] + 0.5*width
            self._bar_norm_x = norm(bin_centres)
            colors = self._colormap(self._bar_norm_x)
            self._bar = histogram_axes.bar(bin_centres, hist, width, color=colors)
            if show_stats:
                mean = array_stats.get('mean')
                median = array_stats.get('median')
                std = array_stats.get('std')
                if mean is not None:
                    histogram_axes.axvline(mean, c='k', ls='-', label='mean')
                    if std is not None:
                        histogram_axes.axvline(mean-std, c='k', ls='-.',
                                               label='mean \u00b1 std')
                        histogram_axes.axvline(mean+std, c='k', ls='-.')
                if median is not None:
                    histogram_axes.axvline(median, c='k', ls='--',
                                           label='median')
                histogram_axes.legend()

            if map_axes is None:
                histogram_axes.set_title(title + ' histogram')

        self._canvas.draw()

