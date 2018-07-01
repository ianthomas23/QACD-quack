from matplotlib.patches import Ellipse, Rectangle
import numpy as np
from PyQt5 import QtCore, QtWidgets


# Classes to handle different interactive modes in matplotlib_widget.

class ModeHandler:
    def __init__(self, matplotlib_widget):
        self.matplotlib_widget = matplotlib_widget

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


# Abstract base class for all region handlers.
class RegionHandler(ModeHandler):
    def __init__(self, matplotlib_widget):
        super().__init__(matplotlib_widget)
        self._editing = False
        self._patch = None         # Outline patch used for editing.
        self._region_image = None  # Image showing region.

    def on_axes_enter(self, event):
        if (event.inaxes is not None and
            event.inaxes == self.matplotlib_widget._map_axes):

            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CrossCursor)

    def on_axes_leave(self, event):
        if (event.inaxes is not None and
            event.inaxes == self.matplotlib_widget._map_axes):

            QtWidgets.QApplication.restoreOverrideCursor()

    def on_mouse_down(self, event):
        if (not self._editing and
            self.matplotlib_widget._map_axes is not None and
            event.button == 1 and event.dblclick == False and
            event.inaxes == self.matplotlib_widget._map_axes):

            if self._patch is not None:
                self.tidy_up()

            self._editing = True
            patch = self._create_patch(event.xdata, event.ydata)
            self._patch = self.matplotlib_widget.add_patch(patch)
            self.matplotlib_widget._redraw()

    def on_mouse_move(self, event):
        if (self._editing and self._patch is not None and
            event.inaxes == self.matplotlib_widget._map_axes):

            self._move_patch(event.xdata, event.ydata)
            self.matplotlib_widget._redraw()

    def on_mouse_up(self, event):
        if (self._editing and self._patch is not None and
            event.button == 1 and event.dblclick == False):

            self._editing = False
            region = self._calculate_region()
            if region is not None:
                masked = np.ma.masked_equal(region, True)

                cmap = self.matplotlib_widget._create_white_colormap()
                self._region_image = self.matplotlib_widget._map_axes.imshow( \
                    masked, alpha=0.9, cmap=cmap)
                self.matplotlib_widget._redraw()

    def tidy_up(self):
        if self.matplotlib_widget._map_axes is not None:
            if self._patch:
                self.matplotlib_widget.remove_patch(self._patch)
                self._patch = None

            if self._region_image:
                self.matplotlib_widget.remove_image(self._region_image)
                self._region_image = None

            self._editing = False

            self.matplotlib_widget._redraw()


class EllipseRegionHandler(RegionHandler):
    def __init__(self, matplotlib_widget):
        super().__init__(matplotlib_widget)
        self._start_xy = None

    def _calculate_region(self):
        project = self.matplotlib_widget._owning_window._project
        if project is not None:
            centre = self._patch.center
            size = (self._patch.width, self._patch.height)
            return project.calculate_region_ellipse(centre, size)
        else:
            return None

    def _create_patch(self, x, y):
        self._start_xy = (x, y)

        ellipse = Ellipse(self._start_xy, width=0, height=0,
                          fc='none', ec='k', ls='--')
        return ellipse

    def _move_patch(self, x, y):
        self._patch.width  = abs(x - self._start_xy[0])
        self._patch.height = abs(y - self._start_xy[1])
        self._patch.center = (0.5*(x + self._start_xy[0]),
                              0.5*(y + self._start_xy[1]))
        self._patch.stale = True


class RectangleRegionHandler(RegionHandler):
    def __init__(self, matplotlib_widget):
        super().__init__(matplotlib_widget)

    def _calculate_region(self):
        project = self.matplotlib_widget._owning_window._project
        if project is not None:
            corner0 = self._patch.get_xy()
            corner1 = (corner0[0] + self._patch.get_width(),
                       corner0[1] + self._patch.get_height())
            return project.calculate_region_rectangle(corner0, corner1)
        else:
            return None

    def _create_patch(self, x, y):
        rectangle = Rectangle((x, y), width=0, height=0,
                              fc='none', ec='k', ls='--')
        return rectangle

    def _move_patch(self, x, y):
        self._patch.set_width( x - self._patch.get_x())
        self._patch.set_height(y - self._patch.get_y())


class ZoomHandler(ModeHandler):
    def __init__(self, matplotlib_widget):
        super().__init__(matplotlib_widget)
        self._zoom_rectangle = None  # Only set when zooming.

    def on_axes_enter(self, event):
        if (event.inaxes is not None and
            event.inaxes == self.matplotlib_widget._map_axes):

            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CrossCursor)

    def on_axes_leave(self, event):
        if (event.inaxes is not None and
            event.inaxes == self.matplotlib_widget._map_axes):

            QtWidgets.QApplication.restoreOverrideCursor()

    def on_mouse_down(self, event):
        if (self._zoom_rectangle is None and
            self.matplotlib_widget._map_axes is not None and
            event.button == 1 and event.dblclick == False and
            event.inaxes == self.matplotlib_widget._map_axes):

            rectangle = Rectangle((event.xdata, event.ydata), width=0, height=0,
                                  fc='none', ec='k', ls='--')
            self._zoom_rectangle = self.matplotlib_widget.add_patch(rectangle)
            self.matplotlib_widget._redraw()

    def on_mouse_move(self, event):
        if (self._zoom_rectangle is not None and
            event.inaxes == self.matplotlib_widget._map_axes):

            x = event.xdata
            y = event.ydata
            self._zoom_rectangle.set_width(x - self._zoom_rectangle.get_x())
            self._zoom_rectangle.set_height(y - self._zoom_rectangle.get_y())
            self.matplotlib_widget._redraw()

    def on_mouse_up(self, event):
        if (self._zoom_rectangle is not None and event.button == 1 and
            event.dblclick == False):

            width = self._zoom_rectangle.get_width()
            height = self._zoom_rectangle.get_height()
            if abs(width) > 1e-10 and abs(height) > 1e-10:
                x = self._zoom_rectangle.get_x()
                y = self._zoom_rectangle.get_y()
                zoom_xs = sorted([x, x+width])
                zoom_ys = sorted([y, y+height], reverse=True)

                from_ = (self.matplotlib_widget._map_axes.get_xlim(),
                         self.matplotlib_widget._map_axes.get_ylim())

                self.matplotlib_widget._owning_window.zoom_append( \
                    from_=from_, to=(zoom_xs, zoom_ys))

            self.tidy_up()

    def tidy_up(self):
        if (self._zoom_rectangle is not None and
            self.matplotlib_widget._map_axes is not None):

            self.matplotlib_widget.remove_patch(self._zoom_rectangle)
            self._zoom_rectangle = None

            self.matplotlib_widget._redraw()
