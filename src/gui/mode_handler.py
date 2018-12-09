import copy
from enum import Enum, unique
from matplotlib.patches import Ellipse, Rectangle
from matplotlib.patheffects import Normal, Stroke
import numpy as np
from PyQt5 import QtCore, QtWidgets

from .enums import ArrayType



# Classes to handle different interactive modes in matplotlib_widget.

class ModeHandler:
    def __init__(self, matplotlib_widget, display_options, status_callback):
        self.matplotlib_widget = matplotlib_widget
        self.display_options = display_options
        self._status_callback = status_callback
        self._shadow_colour = 'w'
        self._shadow_alpha = 0.75

    def clear(self):
        pass

    def _get_path_effects(self):
        return [Stroke(linewidth=3, foreground=self._shadow_colour,
                       alpha=self._shadow_alpha),
                Normal()]

    def move_to_new_axes(self):
        pass

    def on_axes_enter(self, event):
        pass

    def on_axes_leave(self, event):
        pass

    def on_mouse_down(self, event):
        pass

    def on_mouse_up(self, event):
        pass

    def on_mouse_move(self, event):
        pass

    def send_status_callback(self, event):
        if self._status_callback is not None:
            callback_data = None
            if event is not None and event.inaxes is not None:
                if event.inaxes == self.matplotlib_widget._map_axes:
                    x = int(event.xdata / self.display_options.scale)
                    y = int(event.ydata / self.display_options.scale)
                    value = self.matplotlib_widget.get_value_at_position(x, y)
                    callback_data = ('pixel', x, y, value)
                elif event.inaxes == self.matplotlib_widget._histogram_axes:
                    x = event.xdata
                    callback_data = self.matplotlib_widget.get_histogram_at_x(x)
                    if callback_data is not None:
                        callback_data.insert(0, 'histogram')

            self._status_callback(self.matplotlib_widget, callback_data)

    def set_display_options(self, display_options):
        self.display_options = display_options


# Abstract base class for all region handlers.
class RegionHandler(ModeHandler):
    def __init__(self, matplotlib_widget, display_options, status_callback,
                 listener):
        super().__init__(matplotlib_widget, display_options, status_callback)
        self._listener = listener
        self._line_colour = 'k'
        self._region_alpha = 0.75

        self._editing = False
        self._points = np.empty((0, 2))
        self._artists = []         # List of artists.
        self._region = None        # Boolean array.
        self._region_image = None  # Image showing region.

    def _create_region_image(self):
        if self._region is not None:
            masked = np.ma.masked_equal(self._region, True)

            cmap = self.matplotlib_widget._create_white_colourmap()

            ny, nx = masked.shape
            extent = np.array([0.0, nx, ny, 0.0])*self.matplotlib_widget._scale
            return self.matplotlib_widget._map_axes.imshow( \
                masked, alpha=self._region_alpha, cmap=cmap, extent=extent)
        else:
            return None

    def _finish_editing(self):
        self._editing = False
        self._region = self._calculate_region()
        self._region_image = self._create_region_image()

        self.matplotlib_widget._redraw()
        self.update_listener()

    def clear(self):
        if self.matplotlib_widget._map_axes is not None:
            self._points = np.empty((0, 2))

            for artist in self._artists:
                if artist is not None:
                    artist.remove()
            self._artists = []

            if self._region is not None:
                self._region = None

            if self._region_image is not None:
                self._region_image.remove()
                self._region_image = None

            self._editing = False
            self.matplotlib_widget._redraw()
            self.update_listener()

        self.send_status_callback(None)

    def get_region(self):
        return self._region

    def has_region(self):
        return self._region is not None

    def move_to_new_axes(self):
        self._artists = None
        self._region_image = None

        if self.matplotlib_widget._map_axes:
            self._artists = self._create_artists()
            if self._region is not None:
                self._region_image = self._create_region_image()

    def on_axes_enter(self, event):
        if (event.inaxes is not None and
            event.inaxes == self.matplotlib_widget._map_axes):

            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CrossCursor)

    def on_axes_leave(self, event):
        if (event.inaxes is not None and
            event.inaxes == self.matplotlib_widget._map_axes):

            QtWidgets.QApplication.restoreOverrideCursor()

        self.send_status_callback(None)

    def update_listener(self):
        if self._listener:
            self._listener.update_from_mode_handler()


# Abstract base class for region handlers that are controlled by a single drag
# of the mouse.
class MouseDragRegionHandler(RegionHandler):
    def __init__(self, matplotlib_widget, display_options, status_callback,
                 listener):
        super().__init__(matplotlib_widget, display_options, status_callback,
                         listener)

    def on_mouse_down(self, event):
        if (not self._editing and
            self.matplotlib_widget._map_axes is not None and
            event.button == 1 and event.dblclick == False and
            event.inaxes == self.matplotlib_widget._map_axes):

            if self._artists:
                self.clear()

            self._editing = True
            self._points = np.asarray([[event.xdata, event.ydata],
                                       [event.xdata, event.ydata]])
            self._points /= self.display_options.scale
            self._artists = self._create_artists()
            self.matplotlib_widget._redraw()

    def on_mouse_move(self, event):
        if (self._editing and self._artists and
            event.inaxes == self.matplotlib_widget._map_axes):

            self._points[1] = (event.xdata, event.ydata)
            self._points[1] /= self.display_options.scale
            self._move_artists()
            self.matplotlib_widget._redraw()

        self.send_status_callback(event)

    def on_mouse_up(self, event):
        if (self._editing and self._artists and
            event.button == 1 and event.dblclick == False):

            self._finish_editing()


class EllipseRegionHandler(MouseDragRegionHandler):
    def __init__(self, matplotlib_widget, display_options, status_callback,
                 listener):
        super().__init__(matplotlib_widget, display_options, status_callback,
                         listener)

    def _calculate_region(self):
        project = self.matplotlib_widget._owning_window._project
        if project is not None:
            centre, size = self._get_centre_and_size(False)
            ratio = self.display_options.scale / self.matplotlib_widget._scale
            centre *= ratio
            size *= ratio
            return project.calculate_region_ellipse(centre, size)
        else:
            return None

    def _create_artists(self):
        if len(self._points) < 2:
            return []

        scale = self.display_options.scale
        centre, size = self._get_centre_and_size(True)
        ellipse = Ellipse(centre, width=size[0], height=size[1],
                          fc='none', ec=self._line_colour)
        ellipse = self.matplotlib_widget._map_axes.add_patch(ellipse)
        ellipse.set_path_effects(self._get_path_effects())
        return [ellipse]

    def _get_centre_and_size(self, scaled):
        start = self._points[0]
        end = self._points[1]
        centre = (start + end)*0.5
        size = end - start
        if scaled:
            centre *= self.display_options.scale
            size *= self.display_options.scale
        return centre, size

    def _move_artists(self):
        centre, size = self._get_centre_and_size(True)
        self._artists[0].center = centre
        self._artists[0].width  = size[0]
        self._artists[0].height = size[1]
        self._artists[0].stale = True

    def get_shape_string(self):
        return 'ellipse'


class RectangleRegionHandler(MouseDragRegionHandler):
    def __init__(self, matplotlib_widget, display_options, status_callback,
                 listener):
        super().__init__(matplotlib_widget, display_options, status_callback,
                         listener)

    def _calculate_region(self):
        project = self.matplotlib_widget._owning_window._project
        if project is not None:
            ratio = self.display_options.scale / self.matplotlib_widget._scale
            corner0 = self._points[0]*ratio
            corner1 = self._points[1]*ratio
            return project.calculate_region_rectangle(corner0, corner1)
        else:
            return None

    def _create_artists(self):
        if len(self._points) < 2:
            return []

        start = self._points[0]*self.display_options.scale
        size  = self._points[1]*self.display_options.scale - start
        rectangle = Rectangle(start, width=size[0], height=size[1],
                              fc='none', ec=self._line_colour)
        rectangle = self.matplotlib_widget._map_axes.add_patch(rectangle)
        rectangle.set_path_effects(self._get_path_effects())
        return [rectangle]

    def _move_artists(self):
        start = self._points[0]*self.display_options.scale
        end   = self._points[1]*self.display_options.scale
        self._artists[0].set_width( end[0] - start[0])
        self._artists[0].set_height(end[1] - start[1])

    def get_shape_string(self):
        return 'rectangle'


class PolygonRegionHandler(RegionHandler):
    # 3 artists: lines, markers and highlight marker.
    def __init__(self, matplotlib_widget, display_options, status_callback,
                 listener):
        super().__init__(matplotlib_widget, display_options, status_callback,
                         listener)

    def _add_point(self, point):
        # Add point to end of self._points, but only if it is not the same as
        # the last point.
        if len(self._points) == 0 or not np.allclose(point, self._points[-1]):
            self._points = np.vstack((self._points, point))

            if not self._artists:
                self._artists = self._create_artists()
            else:
                scale = self.display_options.scale
                self._artists[0].set_data(self._points[:, 0]*scale,
                                          self._points[:, 1]*scale)
                self._artists[1].set_data(self._points[:, 0]*scale,
                                          self._points[:, 1]*scale)
            self.matplotlib_widget._redraw()

    def _calculate_region(self):
        project = self.matplotlib_widget._owning_window._project
        if project is not None:
            ratio = self.display_options.scale / self.matplotlib_widget._scale
            points = self._points*ratio
            return project.calculate_region_polygon(points)
        else:
            return None

    def _close_polygon(self):
        if self._artists:
            self._points = np.vstack((self._points, self._points[0]))
            x = self._points[:, 0]*self.display_options.scale
            y = self._points[:, 1]*self.display_options.scale
            self._artists[0].set_data(x, y)
            self._artists[1].set_data(x, y)

            self._finish_editing()

    def _create_artists(self):
        colour = self._line_colour
        scale = self.display_options.scale
        lines = self.matplotlib_widget._map_axes.plot( \
            self._points[:, 0]*scale, self._points[:, 1]*scale, '-', c=colour)[0]
        markers = self.matplotlib_widget._map_axes.plot(\
            self._points[:, 0]*scale, self._points[:, 1]*scale, 'o', c=colour)[0]

        path_effects = self._get_path_effects()
        lines.set_path_effects(path_effects)
        markers.set_path_effects(path_effects)
        return [lines, markers, None]

    def get_shape_string(self):
        return 'polygon'

    def on_axes_leave(self, event):
        self.send_status_callback(None)

    def on_mouse_down(self, event):
        if (event.button == 1 and event.inaxes is not None and
            event.inaxes == self.matplotlib_widget._map_axes):

            if not self._editing:
                self.clear()
                self._editing = True

            if event.dblclick or (self._artists and self._artists[2]):
                self._close_polygon()
            else:
                scale = self.display_options.scale
                point = np.asarray((event.xdata, event.ydata)) / scale
                self._add_point(point)

    def on_mouse_move(self, event):
        if (self._artists and self._artists[0] is not None and
            len(self._artists[0].get_xdata()) > 1):

            inside, matches = self._artists[1].contains(event)
            if inside:
                if self._artists[2] is None and 0 in matches['ind']:
                    scale = self.display_options.scale
                    self._artists[2] = self.matplotlib_widget._map_axes.plot(\
                        self._points[0, 0]*scale, self._points[0, 1]*scale,
                        'o', c='yellow')[0]
                    self.matplotlib_widget._redraw()
            elif self._artists[2]:
                self._artists[2].remove()
                self._artists[2] = None
                self.matplotlib_widget._redraw()

        self.send_status_callback(event)


class ZoomHandler(ModeHandler):
    @unique
    class Type(Enum):
        INVALID   = -1
        MAP       =  0
        COLOURBAR =  1
        HISTOGRAM =  2

    def __init__(self, matplotlib_widget, display_options, status_callback):
        super().__init__(matplotlib_widget, display_options, status_callback)
        self._zoom_rectangle = None  # Only set when zooming.
        self._type = self.Type.INVALID

    def clear(self):
        if (self._zoom_rectangle is not None and
            self.matplotlib_widget._map_axes is not None):

            self._zoom_rectangle.remove()
            self._zoom_rectangle = None

            self._type = self.Type.INVALID
            self.matplotlib_widget._redraw()

        self.send_status_callback(None)

    def on_axes_enter(self, event):
        if (event.inaxes is not None and
            (event.inaxes == self.matplotlib_widget._map_axes or
             (self.matplotlib_widget._array_type != ArrayType.CLUSTER and
              (event.inaxes == self.matplotlib_widget.get_colourbar_axes() or
               event.inaxes == self.matplotlib_widget._histogram_axes)))):

            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CrossCursor)

    def on_axes_leave(self, event):
        if (event.inaxes is not None and
            (event.inaxes == self.matplotlib_widget._map_axes or
             event.inaxes == self.matplotlib_widget.get_colourbar_axes() or
             event.inaxes == self.matplotlib_widget._histogram_axes)):

            QtWidgets.QApplication.restoreOverrideCursor()

        self.send_status_callback(None)

    def on_mouse_down(self, event):
        if (self._zoom_rectangle is not None or event.button != 1 or
            event.dblclick):
            return

        if (self.matplotlib_widget._map_axes is not None and
            event.inaxes == self.matplotlib_widget._map_axes):

            rectangle = Rectangle((event.xdata, event.ydata), width=0, height=0,
                                  fc='none', ec='k', ls='--')
            self._zoom_rectangle = \
                self.matplotlib_widget._map_axes.add_patch(rectangle)
            self._zoom_rectangle.set_path_effects(self._get_path_effects())
            self._type = self.Type.MAP

        elif (self.matplotlib_widget._colourbar is not None and
              event.inaxes == self.matplotlib_widget.get_colourbar_axes() and
              self.matplotlib_widget._array_type != ArrayType.CLUSTER):

            rectangle = Rectangle((0.0, event.ydata), width=1.0, height=0,
                                  fc='none', ec='k', ls='--')
            self._zoom_rectangle = \
                self.matplotlib_widget.get_colourbar_axes().add_patch(rectangle)
            self._zoom_rectangle.set_path_effects(self._get_path_effects())
            self._type = self.Type.COLOURBAR

        elif (self.matplotlib_widget._histogram_axes is not None and
              event.inaxes == self.matplotlib_widget._histogram_axes and
              self.matplotlib_widget._array_type != ArrayType.CLUSTER):

            ylim = self.matplotlib_widget._histogram_axes.get_ylim()
            rectangle = Rectangle( \
                (event.xdata, ylim[0]), width=0.0, height=ylim[1] - ylim[0],
                fc='none', ec='k', ls='--')
            self._zoom_rectangle = \
                self.matplotlib_widget._histogram_axes.add_patch(rectangle)
            self._zoom_rectangle.set_path_effects(self._get_path_effects())
            self._type = self.Type.HISTOGRAM

        self.matplotlib_widget._redraw()

    def on_mouse_move(self, event):
        if self._zoom_rectangle is not None:  # Zooming
            if (self._type == self.Type.MAP and
                event.inaxes == self.matplotlib_widget._map_axes):
                x = event.xdata
                y = event.ydata
                self._zoom_rectangle.set_width(x - self._zoom_rectangle.get_x())
                self._zoom_rectangle.set_height(y - self._zoom_rectangle.get_y())
            elif (self._type == self.Type.COLOURBAR and
                  event.inaxes == self.matplotlib_widget.get_colourbar_axes()):
                y = event.ydata
                self._zoom_rectangle.set_height(y - self._zoom_rectangle.get_y())
            elif (self._type == self.Type.HISTOGRAM and
                  event.inaxes == self.matplotlib_widget._histogram_axes):
                x = event.xdata
                self._zoom_rectangle.set_width(x - self._zoom_rectangle.get_x())

            self.matplotlib_widget._redraw()

        self.send_status_callback(event)

    def on_mouse_up(self, event):
        if self._zoom_rectangle is None or event.button != 1 or event.dblclick:
            return

        if self._type == self.Type.MAP:
            width = self._zoom_rectangle.get_width()
            height = self._zoom_rectangle.get_height()
            if abs(width) > 1e-10 and abs(height) > 1e-10:
                x = self._zoom_rectangle.get_x()
                y = self._zoom_rectangle.get_y()
                zoom_xs = sorted([x, x+width])
                zoom_ys = sorted([y, y+height], reverse=True)

                scale = self.matplotlib_widget._scale
                from_ = np.asarray((self.matplotlib_widget._map_axes.get_xlim(),
                                    self.matplotlib_widget._map_axes.get_ylim())) / scale
                to = np.asarray((zoom_xs, zoom_ys)) / scale

                self.matplotlib_widget._owning_window.zoom_append( \
                    self.matplotlib_widget, from_=from_, to=to)
                self.clear()
        elif self._type == self.Type.COLOURBAR:
            height = self._zoom_rectangle.get_height()
            if abs(height) > 1e-10:
                y = self._zoom_rectangle.get_y()
                zoom_ys = sorted([y, y+height])
                zoom_ys = (self.matplotlib_widget._colourbar.norm.inverse(zoom_ys[0]),
                           self.matplotlib_widget._colourbar.norm.inverse(zoom_ys[1]))

                self.clear()  # Must be before matplotlib widget update.
                self.matplotlib_widget._owning_window.zoom_colourmap_append( \
                    from_=self.matplotlib_widget._colourmap_limits, to=zoom_ys)
                QtWidgets.QApplication.restoreOverrideCursor()
            else:
                self.clear()
        elif self._type == self.Type.HISTOGRAM:
            width = self._zoom_rectangle.get_width()
            if abs(width) > 1e-10:
                x = self._zoom_rectangle.get_x()
                zoom_xs = sorted([x, x+width])

                self.clear()  # Must be before matplotlib widget update.
                self.matplotlib_widget._owning_window.zoom_colourmap_append( \
                    from_=self.matplotlib_widget._colourmap_limits, to=zoom_xs)
                QtWidgets.QApplication.restoreOverrideCursor()
            else:
                self.clear()

        self._type = self.Type.INVALID
