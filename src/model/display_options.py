import matplotlib.cm as cm


class DisplayOptions:
    def __init__(self):
        # Colourmap options.
        self._valid_colourmap_names = self._determine_valid_colourmap_names()
        self._colourmap_name = 'rainbow'

        # Scale options.
        self._valid_units = ['mm', '\u03BCm', 'nm']
        self._use_scale = False
        self._pixel_size = 10.0
        self._units = self._valid_units[1]
        self._show_scale_bar = True

        self._listeners = []

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

    def add_listener(self, listener):
        if listener is not None and listener not in self._listeners:
            self._listeners.append(listener)

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

        for listener in self._listeners:
            listener.update_colourmap_name()

    @property
    def pixel_size(self):
        return self._pixel_size

    def remove_listener(self, listener):
        try:
            self._listeners.remove(listener)
        except ValueError:
            pass  # listener may not be in list.

    def set_scale(self, use_scale, pixel_size, units, show_scale_bar):
        if units not in self.valid_units:
            raise RuntimeError('Unrecognised units {}'.format(units))

        self._use_scale = use_scale
        self._pixel_size = pixel_size
        self._units = units
        self._show_scale_bar = show_scale_bar

       # for listener in self._listeners:
       #     listener.update_scale()

    @property
    def show_scale_bar(self):
        return self._show_scale_bar

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
