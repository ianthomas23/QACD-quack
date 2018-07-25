import matplotlib.cm as cm
import weakref


class DisplayOptions:
    def __init__(self, project):
        self._project = weakref.ref(project)

        # Colourmap options.
        self._valid_colourmap_names = self._determine_valid_colourmap_names()
        self._colourmap_name = 'rainbow'

        # Label options.
        self._valid_scale_bar_locations = \
            ['upper left', 'upper right', 'lower left', 'lower right']
        self._show_ticks_and_labels = True

        # Scale options.
        self._valid_units = ['mm', '\u03BCm', 'nm']
        self._use_scale = False
        self._pixel_size = 1.0
        self._units = self._valid_units[1]
        self._show_scale_bar = True
        self._scale_bar_location = 'lower left'

        self._listeners = weakref.WeakSet()

    def _determine_valid_colourmap_names(self):
        # Exclude reversed cmaps which have names ending with '_r'.
        all_ = set(filter(lambda s: not s.endswith('_r'), cm.cmap_d.keys()))

        # Exclude qualitative and repeating cmaps, and the deprecated
        # 'spectral' which has been replaced with 'nipy_spectral'.
        exclude = set(['Accent', 'Dark2', 'Paired', 'Pastel1', 'Pastel2',
                       'Set1', 'Set2', 'Set3', 'Vega10', 'Vega20', 'Vega20b',
                       'Vega20c', 'flag', 'prism', 'spectral', 'tab10',
                       'tab20', 'tab20b', 'tab20c'])
        return sorted(all_.difference(exclude))

    @property
    def colourmap_name(self):
        return self._colourmap_name

    @colourmap_name.setter
    def colourmap_name(self, colourmap_name):
        name_to_check = colourmap_name
        if name_to_check.endswith('_r'):
            name_to_check = name_to_check[:-2]
        if name_to_check not in self._valid_colourmap_names:
            raise RuntimeError('Not such colourmap: {}'.format(name_to_check))
        self._colourmap_name = colourmap_name

        self._project().save_display_options()

        for listener in self._listeners:
            listener.update_colourmap_name()

    def get_next_larger_units(self, units):
        index = self._valid_units.index(units)
        if index == 0:
            return 'm'
        else:
            return self._valid_units[index-1]

    @property
    def pixel_size(self):
        return self._pixel_size

    def register_listener(self, listener):
        if listener is not None and listener not in self._listeners:
            self._listeners.add(listener)

    @property
    def scale(self):
        if self._use_scale:
            return self._pixel_size
        else:
            return 1.0

    @property
    def scale_bar_location(self):
        return self._scale_bar_location

    def set_labels_and_scale(self, show_ticks_and_labels, use_scale, pixel_size,
                             units, show_scale_bar, scale_bar_location):
        # Validation.
        if units not in self.valid_units:
            raise RuntimeError('Unrecognised units {}'.format(units))
        if scale_bar_location not in self._valid_scale_bar_locations:
            raise RuntimeError('Unrecognised scale bar location {}'.format(scale_bar_location))

        # Labels.
        self._show_ticks_and_labels = show_ticks_and_labels

        # Scale.
        self._use_scale = use_scale
        self._pixel_size = pixel_size
        self._units = units
        self._show_scale_bar = show_scale_bar
        self._scale_bar_location = scale_bar_location

        self._project().save_display_options()

        for listener in self._listeners:
            listener.update_labels_and_scale()

    @property
    def show_scale_bar(self):
        return self._show_scale_bar

    @property
    def show_ticks_and_labels(self):
        return self._show_ticks_and_labels

    def unregister_listener(self, listener):
        self._listeners.discard(listener)

    @property
    def use_scale(self):
        return self._use_scale

    @property
    def units(self):
        return self._units

    @property
    def valid_colourmap_names(self):
        return self._valid_colourmap_names

    @property
    def valid_units(self):
        return self._valid_units
