from enum import Enum, unique
import math
from matplotlib.backends.backend_qt5agg import FigureCanvas
import matplotlib.cm as cm
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.figure import Figure
import numpy as np
from PyQt5 import QtCore, QtWidgets
import warnings

from src.model.display_options_listener import DisplayOptionsListener
from src.model.utils import adaptive_interp, calculate_transect
from .enums import ArrayType, ModeType, PlotType
from .mode_handler import *
from .scale_bar import ScaleBar


class MatplotlibWidget(QtWidgets.QWidget, DisplayOptionsListener):
    def __init__(self, parent):
        super(MatplotlibWidget, self).__init__(parent)

        self._canvas = FigureCanvas(Figure())
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.addWidget(self._canvas)
        self.setLayout(self._layout)

        self._display_options = None
        self._map_axes = None
        self._histogram_axes = None
        self._transect_axes = None

        # Variables set by call to update()
        self._plot_type = PlotType.INVALID
        self._array_type = ArrayType.INVALID
        self._array = None
        self._array_stats = None
        self._title = None
        self._name = None
        self._map_zoom = None       # None or float array of shape (2,2).
        self._map_pixel_zoom = None # None or int array ((imin,imax), (jmin,jmax))

        self._image = None          # Image used for element map.
        self._bar = None            # Bar used for histogram.
        self._bar_norm_x = None     # Normalised x-positions of centres of bars
                                    #   in range 0 (= min) to 1.0 (= max value).
        self._cmap_int_max = None   # One beyond end, as in numpy slicing.
        self._scale_bar = None
        self._colourbar = None
        self._histogram = None      # Latest (histogram, bin_edges, bin_width).

        self._map_line_points = None  # Line drawn on map (showing transect).
        self._map_line = None
        self._transect = None       # Latest transect values before interpolation.

        # Scale and units initially from display options, but may need to
        # change them if distances are too large, e.g. 1000 mm goes to 1 m.
        self._scale = None
        self._units = None

        # Initialised in initialise().
        self._owning_window = None
        self._mode_type = ModeType.INVALID
        self._mode_handler = None

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

    def _create_scale_bar(self):
        if self._scale_bar:
            # Clear old scale bar.
            if self._map_axes and self._scale_bar in self._map_axes.artists:
                self._scale_bar.remove()
            self._scale_bar = None

        if self._map_axes is not None:
            options = self._display_options
            xticks = self._map_axes.get_xticks()
            size = xticks[1] - xticks[0]
            label = '{:g} {}'.format(size, self._units)
            self._scale_bar = ScaleBar( \
                ax=self._map_axes, size=size, label=label,
                loc=options.scale_bar_location, colour=options.scale_bar_colour)
            self._map_axes.add_artist(self._scale_bar)

    def _create_white_colourmap(self):
        if self._white_colourmap == None:
            colours = [(1, 1, 1), (1, 1, 1)]
            self._white_colourmap = \
                LinearSegmentedColormap.from_list('white', colours, N=1)
        return self._white_colourmap

    def _get_scaled_extent(self):
        # Return extent rectangle (for imshow), corrected for scale and units
        # if using physical units.  self._scale and self._units are updated,
        # and may be different from display_options if showing a particularly
        # large or small extent.
        options = self._display_options
        ny, nx = self._array.shape
        extent = np.array([0.0, nx, ny, 0.0])

        if options.use_scale:
            self._scale = options.scale
            self._units = options.units
            extent *= self._scale
            if self._map_zoom is not None:
                display_rectangle = self._map_zoom*self._scale
            else:
                display_rectangle = extent
            max_dimension = np.absolute(np.diff(display_rectangle.reshape((2,2)))).max()
            if max_dimension > 1000.0:
                self._scale /= 1000.0
                self._units = options.get_next_larger_units(self._units)
                extent /= 1000.0
        else:
            self._scale = 1.0
            self._units = 'pixels'

        return extent

    def _redraw(self):
        with warnings.catch_warnings():
            # Ignore RuntimeWarning when determining colour from colourmap if
            # value is NaN.
            warnings.filterwarnings( \
                'ignore', message='invalid value encountered in less')
            self._canvas.draw()

    def _update_draw(self, refresh=True):
        # Draw using cached variables.

        # Derived quantities.
        show_colourbar = True
        cmap_int_max = None
        if self._array_type == ArrayType.CLUSTER:
            if 'k' in self._array_stats:
                cmap_int_max = self._array_stats['k'] + 1
            else:
                cmap_int_max = self._array_stats['max'] + 1
        elif self._array_type in (ArrayType.PHASE, ArrayType.REGION):
            show_colourbar = False
            cmap_int_max = 2

        self._cmap_int_max = cmap_int_max

        figure = self._canvas.figure
        figure.clear()

        options = self._display_options
        self._map_axes = None
        self._histogram_axes = None
        self._transect_axes = None
        if self._plot_type == PlotType.INVALID:
            return
        elif self._plot_type == PlotType.MAP:
            self._map_axes = figure.subplots()
        elif self._plot_type == PlotType.HISTOGRAM:
            self._histogram_axes = figure.subplots()
        elif self._plot_type == PlotType.MAP_AND_HISTOGRAM:
            self._map_axes, self._histogram_axes = figure.subplots( \
                nrows=2, gridspec_kw={'height_ratios': (3,1)})
        elif self._plot_type == PlotType.MAP_AND_TRANSECT:
            self._map_axes, self._transect_axes = figure.subplots( \
                nrows=2, gridspec_kw={'height_ratios': (3,1)})
        else:
            raise RuntimeError('Invalid plot type')

        cmap = self.create_colourmap()

        cmap_limits = None
        if cmap_int_max is None:
            show_stats = True
            if options.manual_colourmap_zoom:
                cmap_limits = (options.lower_colourmap_limit,
                               options.upper_colourmap_limit)
            else:
                cmap_limits = (self._array_stats['min'],
                               self._array_stats['max'])
            norm = Normalize(cmap_limits[0], cmap_limits[1])
            cmap_ticks = None
        else:
            show_stats = False
            norm = Normalize(-0.5, cmap_int_max-0.5)
            cmap_ticks = np.arange(0, cmap_int_max)
            if cmap_int_max >= 15:
                cmap_ticks = cmap_ticks[::2]

        if show_stats:
            show_stats = options.show_mean_median_std_lines

        if self._map_axes is None:
            self._image = None
            self._scale = None
            self._units = None
            self._colourbar = None
        else:
            extent = self._get_scaled_extent()
            self._image = self._map_axes.imshow(self._array, cmap=cmap,
                                                norm=norm, extent=extent)

            if self._map_line is not None and self.has_transect_axes():
                # Redraw existing map_line on new map_axes.
                self._map_line.remove()
                path_effects = self._map_line.get_path_effects()
                self._map_line = self._map_axes.plot( \
                    self._map_line_points[:, 0]*self._scale,
                    self._map_line_points[:, 1]*self._scale, '-', c='k',
                    path_effects=path_effects)[0]

            if self._map_zoom is not None:
                self._map_axes.set_xlim(self._map_zoom[0]*self._scale)
                self._map_axes.set_ylim(self._map_zoom[1]*self._scale)

            if show_colourbar:
                self._colourbar = figure.colorbar(self._image, ax=self._map_axes,
                                                  ticks=cmap_ticks)

            if self._title is not None:
                self._map_axes.set_title(self._title + ' map')

            if options.use_scale and options.show_scale_bar:
                self._create_scale_bar()

            # Hide ticks only after creating scale bar as use tick locations
            # to determine scale bar size.
            self._update_map_axes_ticks_and_labels()

        if self._histogram_axes is None:
            self._bar = None
            self._bar_norm_x = None
            self._histogram = None
        else:
            # May only want histogram of zoomed sub array.
            subarray = self._array
            if options.zoom_updates_stats and self._map_pixel_zoom is not None:
                ((imin, imax), (jmin, jmax)) = self._map_pixel_zoom
                subarray = subarray[jmin:jmax, imin:imax]

            if cmap_int_max is not None:
                bins = np.arange(0, cmap_int_max+1)-0.5
            elif options.use_histogram_bin_count:
                bins = options.histogram_bin_count
            else:
                # Use bin width, but only if max count not exceeded.
                bin_width = options.histogram_bin_width

                if options.manual_colourmap_zoom:
                    subarray_limits = cmap_limits
                else:
                    subarray_limits = (subarray.min(), subarray.max())
                if (subarray_limits[0] is np.ma.masked or
                    subarray_limits[1] is np.ma.masked or
                    subarray_limits[0] == subarray_limits[1]):
                    # Subarray is all masked out, so cannot display histogram.
                    bins = 1
                else:
                    min_index = math.floor(subarray_limits[0] / bin_width)
                    max_index = math.ceil(subarray_limits[1] / bin_width) - 1
                    bins = max_index - min_index
                    if bins < options.histogram_max_bin_count:
                        bins = bin_width*np.arange(min_index, max_index+2)
                    else:
                        bins = options.histogram_max_bin_count

            hist, bin_edges = np.histogram(np.ma.compressed(subarray),
                                           bins=bins, range=cmap_limits)
            bin_width = bin_edges[1] - bin_edges[0]
            self._histogram = (hist, bin_edges, bin_width)
            bin_centres = bin_edges[:-1] + 0.5*bin_width
            self._bar_norm_x = norm(bin_centres)
            colours = cmap(self._bar_norm_x)
            self._bar = self._histogram_axes.bar(bin_centres, hist, bin_width,
                                                 color=colours)
            if cmap_ticks is not None:
                self._histogram_axes.set_xticks(cmap_ticks)

            if show_stats:
                mean = self._array_stats.get('mean')
                median = self._array_stats.get('median')
                std = self._array_stats.get('std')
                if mean is not None:
                    self._histogram_axes.axvline(mean, c='k', ls='-', label='mean')
                    if std is not None:
                        self._histogram_axes.axvline(mean-std, c='k', ls='-.',
                                                     label='mean \u00b1 std')
                        self._histogram_axes.axvline(mean+std, c='k', ls='-.')
                if median is not None:
                    self._histogram_axes.axvline(median, c='k', ls='--',
                                                 label='median')

                if mean is not None or median is not None:
                    self._histogram_axes.legend()

            if self._map_axes is None and self._title is not None:
                self._histogram_axes.set_title(self._title + ' histogram')

        if self.has_transect_axes() and self._map_line is not None:
            x, y = self._map_line.get_data()
            points = np.stack((x, y), axis=1)/self._scale
            self.set_transect(points)

        figure.suptitle(options.overall_title)
        if options.show_project_filename:
            figure.text(0.01, 0.01, options.project_filename)
        if options.show_date:
            figure.text(0.99, 0.01, options.date, ha='right')

        self._adjust_layout()

        if self._mode_handler:
            self._mode_handler.move_to_new_axes()

        if refresh:
            self._redraw()

    def _update_map_axes_ticks_and_labels(self):
        if self._display_options.show_ticks_and_labels:
            self._map_axes.set_xlabel(self._units)
            self._map_axes.set_ylabel(self._units)
        else:
            self._map_axes.set_xticks([])
            self._map_axes.set_yticks([])

    def clear(self):
        # Clear current plots.
        self._canvas.figure.clear()
        self._map_axes = None
        self._histogram_axes = None
        self._transect_axes = None
        self._plot_type = PlotType.INVALID
        self._array_type = ArrayType.INVALID
        self._array = None
        self._array_stats = None
        self._title = None
        self._name = None
        self._image = None
        self._bar = None
        self._bar_norm_x = None
        self._cmap_int_max = None
        self._scale_bar = None
        self._colourbar = None
        self._histogram = None
        self._map_line_points = None
        self._map_line = None
        self._transect = None
        self._scale = None
        self._units = None

        self._redraw()

    def clear_all(self):
        # Clear everything, including cached zoom extent, etc.
        self.clear_map_zoom()
        self.clear()

    def clear_map_zoom(self):
        self._map_zoom = None
        self._map_pixel_zoom = None

    def create_colourmap(self):
        if self._array_type in (ArrayType.PHASE, ArrayType.REGION):
            return self._create_black_colourmap()
        if self._cmap_int_max is None:
            return cm.get_cmap(self._display_options.colourmap_name)
        else:
            return cm.get_cmap(self._display_options.colourmap_name,
                               self._cmap_int_max)

    def create_map_line(self, points, path_effects):
        if self._map_line is not None:
            self._map_line_points = None
            self._map_line.remove()
            self._map_line = None

        if self._map_axes is not None:
            self._map_line_points = points
            self._map_line = self._map_axes.plot( \
                points[:, 0]*self._scale, points[:, 1]*self._scale, '-', c='k',
                path_effects=path_effects)[0]

            self._redraw()

    def export_to_file(self, filename):
        figure = self._canvas.figure
        figure.savefig(filename)

    def get_histogram_at_x(self, x):
        # Return histogram data at specified x value.
        if self._histogram is None:
            return None

        hist, bin_edges, bin_width = self._histogram
        nbins = len(hist)
        i = math.floor((x - bin_edges[0]) / bin_width)
        if i < 0 or i >= len(bin_edges)-1:
            # In histogram, but not within a bin.
            return [bin_width, nbins]
        else:
            # Within a histogram bin.
            bin_low = bin_edges[i]
            bin_high = bin_edges[i+1]
            count = hist[i]
            return [bin_width, nbins, bin_low, bin_high, count]

    def get_transect_at_lambda(self, lambda_):
        if self._transect is not None:
            points = self._map_line_points
            xy = (points[0] + lambda_*(points[1] - points[0])).astype(np.int)
            x, y = xy
            value = self.get_value_at_position(x, y)
            return [x, y, value]
        else:
            return None

    def get_value_at_position(self, x, y):
        # Return value at (x, y) indices of the current array, or None if there
        # is no such value or the value is masked.
        if self._array is not None:
            value = self._array[y, x]
            if value is not np.ma.masked:
                return value
        return None

    def has_content(self):
        return self._plot_type != PlotType.INVALID

    def has_histogram_axes(self):
        return self._histogram_axes is not None

    def has_map_axes(self):
        return self._map_axes is not None

    def has_transect_axes(self):
        return self._transect_axes is not None

    def initialise(self, owning_window, display_options, zoom_enabled=True,
                   status_callback=None):
        self._owning_window = owning_window
        self.set_display_options(display_options)
        self._status_callback = status_callback

        if zoom_enabled:
            self._canvas.mpl_connect('axes_enter_event', self.on_axes_enter)
            self._canvas.mpl_connect('axes_leave_event', self.on_axes_leave)
            self._canvas.mpl_connect('button_press_event', self.on_mouse_down)
            self._canvas.mpl_connect('button_release_event', self.on_mouse_up)
            self._canvas.mpl_connect('motion_notify_event', self.on_mouse_move)

            self.set_default_mode_type()
        else:
            self.set_mode_type(ModeType.INVALID)

        self._canvas.mpl_connect('resize_event', self.on_resize)

    def is_region_mode_type(self):
        return self._mode_type in (ModeType.REGION_RECTANGLE,
                                   ModeType.REGION_ELLIPSE,
                                   ModeType.REGION_POLYGON)

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
        # Ticks may have changed, so need to recalculate scale bar.
        if self._scale_bar:
            self._create_scale_bar()

        self._adjust_layout()

    def set_colourmap_limits(self, lower, upper):
        # Needed for new_phase_filtered_dialog only.
        if self._image is not None:
            self._image.set_clim(lower, upper)
            cmap = self._image.get_cmap()
            cmap.set_over('w')
            cmap.set_under('w')
            self._redraw()

    def set_default_mode_type(self):
        # Return True if need to call reset on mode_handler after widget is
        # drawn.
        if self._plot_type == PlotType.MAP_AND_TRANSECT:
            self.set_mode_type(ModeType.TRANSECT)
        else:
            self.set_mode_type(ModeType.ZOOM)

    def set_display_options(self, display_options):
        if self._display_options is not None:
            self._display_options.unregister_listener(self)
        self._display_options = display_options
        if self._display_options is not None:
            self._display_options.register_listener(self)

        if self._mode_handler is not None:
            self._mode_handler.set_display_options(display_options)

    def set_mode_type(self, mode_type, listener=None):
        if mode_type != self._mode_type:
            self._mode_type = mode_type

            if self._mode_handler:
                self._mode_handler.clear()

            options = self._display_options

            if mode_type == ModeType.ZOOM:
                self._mode_handler = ZoomHandler(self, options, \
                    self._status_callback)
            elif mode_type == ModeType.REGION_RECTANGLE:
                self._mode_handler = RectangleRegionHandler(self, options,
                    self._status_callback, listener)
            elif mode_type == ModeType.REGION_ELLIPSE:
                self._mode_handler = EllipseRegionHandler(self, options,
                    self._status_callback, listener)
            elif mode_type == ModeType.REGION_POLYGON:
                self._mode_handler = PolygonRegionHandler(self, options,
                    self._status_callback, listener)
            elif mode_type == ModeType.TRANSECT:
                self._mode_handler = TransectHandler(self, options,
                    self._status_callback)
            else:
                self._mode_handler = None

    def set_transect(self, points):
        if not self.has_transect_axes():
            raise RuntimeError('MatplotlibWidget does not have transect axes')

        lambdas, values = calculate_transect(self._array, points[0], points[1])

        axes = self._transect_axes
        axes.clear()

        if self._display_options.transect_uses_colourmap:
            lambdas, values = adaptive_interp(lambdas, values, 19)

            points = np.array([lambdas, values]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)
            lines = LineCollection(segments,
                                   cmap=self.create_colourmap(),
                                   norm=self._image.norm)
            # Set the array that is used to determine colours.
            lines.set_array(0.5*(points[:-1, 0, 1] + points[1:, 0, 1]))

            lines = axes.add_collection(lines)
            axes.autoscale_view(scalex=False, scaley=True)
        else:
            axes.plot(lambdas, values)

        self._transect = values
        axes.set_xlim(0.0, 1.0)  # Needed in case end points are masked out.

    def update(self, plot_type, array_type, array, array_stats, title, name,
               map_zoom=None, map_pixel_zoom=None, refresh=True):
        self._plot_type = plot_type
        self._array_type = array_type
        self._array = array
        self._array_stats = array_stats
        self._title = title
        self._name = name
        self._map_zoom = map_zoom
        self._map_pixel_zoom = map_pixel_zoom

        if not self.is_region_mode_type():
            self.set_default_mode_type()

        self._update_draw(refresh)

    def update_colourmap_name(self):
        # Handler for DisplayOptions callback.
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

        if (self.has_transect_axes() and
            self._display_options.transect_uses_colourmap):
            line_collection = self._transect_axes.collections[0]
            line_collection.set_cmap(cmap)

        self._redraw()

    def update_map_line(self, points):
        if self._map_line is not None and self._map_axes is not None:
            self._map_line_points = points
            self._map_line.set_data(points[:, 0]*self._scale,
                                    points[:, 1]*self._scale)
            self._redraw()
