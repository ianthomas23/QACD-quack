from enum import Enum, unique
from matplotlib.backends.backend_qt5agg import FigureCanvas
import matplotlib.cm as cm
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.figure import Figure
import numpy as np
from PyQt5 import QtCore, QtWidgets

from .enums import ArrayType, ModeType, PlotType
from .mode_handler import *
from .scale_bar import ScaleBar


class MatplotlibWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(MatplotlibWidget, self).__init__(parent)

        self._canvas = FigureCanvas(Figure())
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.addWidget(self._canvas)
        self.setLayout(self._layout)

        self._display_options = None
        self._map_axes = None

        # Variables set by call to update()
        self._plot_type = PlotType.INVALID
        self._array_type = ArrayType.INVALID
        self._array = None
        self._array_stats = None
        self._title = None

        self._image = None       # Image used for element map.
        self._bar = None         # Bar used for histogram.
        self._bar_norm_x = None  # Normalised x-positions of centres of bars
                                 #   in range 0 (= min) to 1.0 (= max value).
        self._cmap_int_max = None  # One beyond end, as in numpy slicing.

        # Initialised in initialise().
        self._owning_window = None
        self._mode_type = ModeType.INVALID
        self._mode_handler = None

        self._map_xlim = None        # Zoom to this when create new map.
        self._map_ylim = None

        # Created when first needed.
        self._black_colourmap = None
        self._white_colourmap = None

    def __del__(self):
        self.set_display_options(None)

    def _adjust_layout(self):
        #self._canvas.figure.tight_layout(pad=1.5)
        pass

    def _create_black_colourmap(self):
        if self._black_colourmap == None:
            colours = [(0, 0, 0), (0, 0, 0)]
            self._black_colourmap = \
                LinearSegmentedColormap.from_list('black', colours, N=1)
        return self._black_colourmap

    def _create_white_colourmap(self):
        if self._white_colourmap == None:
            colours = [(1, 1, 1), (1, 1, 1)]
            self._white_colourmap = \
                LinearSegmentedColormap.from_list('white', colours, N=1)
        return self._white_colourmap

    def _redraw(self):
        self._canvas.draw()
        #self._canvas.draw_idle()

    def _update_draw(self):
        # Draw using cached variables.

        # Derived quantities.
        show_colourbar = True
        cmap_int_max = None
        if self._array_type == ArrayType.CLUSTER:
            cmap_int_max = self._array_stats['max'] + 1
        elif self._array_type in (ArrayType.PHASE, ArrayType.REGION):
            show_colourbar = False
            cmap_int_max = 2

        self._cmap_int_max = cmap_int_max

        figure = self._canvas.figure
        figure.clear()

        options = self._display_options
        map_axes = None
        histogram_axes = None
        if self._plot_type == PlotType.INVALID:
            return
        elif self._plot_type == PlotType.MAP:
            map_axes = figure.subplots()
        elif self._plot_type == PlotType.HISTOGRAM:
            histogram_axes = figure.subplots()
        elif self._plot_type == PlotType.BOTH:
            map_axes, histogram_axes = figure.subplots( \
                nrows=2, gridspec_kw={'height_ratios': (3,1)})
        else:
            raise RuntimeError('Invalid plot type')

        cmap = self.create_colourmap()

        if cmap_int_max is None:
            show_stats = True
            norm = Normalize(self._array_stats['min'], self._array_stats['max'])
            cmap_ticks = None
        else:
            show_stats = False
            norm = Normalize(-0.5, cmap_int_max-0.5)
            cmap_ticks = np.arange(0, cmap_int_max)
            if cmap_int_max >= 15:
                cmap_ticks = cmap_ticks[::2]

        if map_axes is None:
            self._image = None
        else:
            ny, nx = self._array.shape
            extent = np.array([0.0, nx, ny, 0.0])
            if options.use_scale:
                units = options.units
                extent *= options.scale
                if extent.max() >= 1000.0:
                    units = options.get_next_larger_units(units)
                    extent /= 1000.0
            else:
                units = 'pixels'

            self._image = map_axes.imshow(self._array, cmap=cmap, norm=norm,
                                          extent=extent)

            if show_colourbar:
                colourbar = figure.colorbar(self._image, ax=map_axes,
                                            ticks=cmap_ticks)
            if self._title is not None:
                map_axes.set_title(self._title + ' map')

            if self._map_xlim is not None:
                scale = self._display_options.scale
                map_axes.set_xlim(self._map_xlim*scale)
                map_axes.set_ylim(self._map_ylim*scale)

            if options.use_scale and options.show_scale_bar:
                xticks = map_axes.get_xticks()
                size = xticks[1] - xticks[0]
                label = '{:g} {}'.format(size, units)
                scale_bar = ScaleBar(ax=map_axes, size=size, label=label,
                                     loc=options.scale_bar_location)
                map_axes.add_artist(scale_bar)

            # Hide ticks only after creating scale bar as use tick locations
            # to determine scale bar size.
            if options.show_ticks_and_labels:
                map_axes.set_xlabel(units)
                map_axes.set_ylabel(units)
            else:
                map_axes.set_xticks([])
                map_axes.set_yticks([])

        if histogram_axes is None:
            self._bar = None
            self._bar_norm_x = None
        else:
            if cmap_int_max is None:
                bins = 100
            else:
                bins = np.arange(0, cmap_int_max+1)-0.5
            hist, bin_edges = np.histogram(np.ma.compressed(self._array),
                                           bins=bins)
            width = bin_edges[1] - bin_edges[0]
            bin_centres = bin_edges[:-1] + 0.5*width
            self._bar_norm_x = norm(bin_centres)
            colours = cmap(self._bar_norm_x)
            self._bar = histogram_axes.bar(bin_centres, hist, width,
                                           color=colours)
            if cmap_ticks is not None:
                histogram_axes.set_xticks(cmap_ticks)

            if show_stats:
                mean = self._array_stats.get('mean')
                median = self._array_stats.get('median')
                std = self._array_stats.get('std')
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

            if map_axes is None and self._title is not None:
                histogram_axes.set_title(self._title + ' histogram')

        self._map_axes = map_axes
        self._adjust_layout()

        if self._mode_handler:
            self._mode_handler.move_to_new_axes()

        self._redraw()

    def clear(self):
        # Clear current plots.
        self._zoom_rectangle = None
        self._canvas.figure.clear()
        self._map_axes = None
        self._plot_type = PlotType.INVALID
        self._array_type = ArrayType.INVALID
        self._array = None
        self._array_stats = None
        self._title = None
        self._image = None
        self._bar = None
        self._bar_norm_x = None
        self._cmap_int_max = None  # One beyond end, as in numpy slicing.

        self._redraw()

    def clear_all(self):
        # Clear everything, including cached zoom limits, etc.
        self._map_xlim = None
        self._map_ylim = None
        self.clear()

    def create_colourmap(self):
        if self._array_type in (ArrayType.PHASE, ArrayType.REGION):
            return self._create_black_colourmap()
        if self._cmap_int_max is None:
            return cm.get_cmap(self._display_options.colourmap_name)
        else:
            return cm.get_cmap(self._display_options.colourmap_name,
                               self._cmap_int_max)

    def initialise(self, owning_window, display_options, zoom_enabled=True):
        self._owning_window = owning_window
        self.set_display_options(display_options)
        if zoom_enabled:
            self._canvas.mpl_connect('axes_enter_event', self.on_axes_enter)
            self._canvas.mpl_connect('axes_leave_event', self.on_axes_leave)
            self._canvas.mpl_connect('button_press_event', self.on_mouse_down)
            self._canvas.mpl_connect('button_release_event', self.on_mouse_up)
            self._canvas.mpl_connect('motion_notify_event', self.on_mouse_move)

            self.set_mode_type(ModeType.ZOOM)
        else:
            self.set_mode_type(ModeType.INVALID)

        self._canvas.mpl_connect('resize_event', self.on_resize)

    def on_axes_enter(self, event):
        if self._mode_handler:
            self._mode_handler.on_axes_enter(event)

    def on_axes_leave(self, event):
        if self._mode_handler:
            self._mode_handler.on_axes_leave(event)

    def on_mouse_down(self, event):
        if self._mode_handler:
            self._mode_handler.on_mouse_down(event)

    def on_mouse_move(self, event):
        if self._mode_handler:
            self._mode_handler.on_mouse_move(event)

    def on_mouse_up(self, event):
        if self._mode_handler:
            self._mode_handler.on_mouse_up(event)

    def on_resize(self, event):
        self._adjust_layout()

    def set_colourmap_limits(self, lower, upper):
        if self._image is not None:
            self._image.set_clim(lower, upper)
            cmap = self._image.get_cmap()
            cmap.set_over('w')
            cmap.set_under('w')
            self._redraw()

    def set_display_options(self, display_options):
        if self._display_options is not None:
            self._display_options.unregister_listener(self)
        self._display_options = display_options
        if self._display_options is not None:
            self._display_options.register_listener(self)

        if self._mode_handler is not None:
            self._mode_handler.set_display_options(display_options)

    def set_map_zoom(self, xs, ys):
        if self._map_axes is not None:
            scale = self._display_options.scale

            xs = np.asarray(xs)
            ys = np.asarray(ys)

            self._map_xlim = xs
            self._map_ylim = ys

            self._map_axes.set_xlim(xs*scale)
            self._map_axes.set_ylim(ys*scale)
            self._redraw()

    def set_mode_type(self, mode_type, listener=None):
        if mode_type != self._mode_type:
            self._mode_type = mode_type

            if self._mode_handler:
                self._mode_handler.clear()

            options = self._display_options

            if mode_type == ModeType.ZOOM:
                self._mode_handler = ZoomHandler(self, options)
            elif mode_type == ModeType.REGION_RECTANGLE:
                self._mode_handler = RectangleRegionHandler(self, options, listener)
            elif mode_type == ModeType.REGION_ELLIPSE:
                self._mode_handler = EllipseRegionHandler(self, options, listener)
            elif mode_type == ModeType.REGION_POLYGON:
                self._mode_handler = PolygonRegionHandler(self, options, listener)
            else:
                self._mode_handler = None

    def update(self, plot_type, array_type, array, array_stats, title):
        self._plot_type = plot_type
        self._array_type = array_type
        self._array = array
        self._array_stats = array_stats
        self._title = title

        self._update_draw()

    def update_colourmap_name(self):
        colourmap_name = self._display_options.colourmap_name
        cmap = self.create_colourmap()

        if self._array_type == ArrayType.PHASE:
            return

        if self._image is not None:
            self._image.set_cmap(cmap)

        if self._bar is not None:
            colours = cmap(self._bar_norm_x)
            for index, item in enumerate(self._bar):
                item.set_color(colours[index])

        self._redraw()

    def update_labels_and_scale(self):
        self._update_draw()
