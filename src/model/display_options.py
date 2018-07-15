import matplotlib.cm as cm


class DisplayOptions:
    def __init__(self):
        self._valid_colourmap_names = self._determine_valid_colourmap_names()
        self._colourmap_name = 'rainbow'
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

    def remove_listener(self, listener):
        try:
            self._listeners.remove(listener)
        except ValueError:
            pass  # listener may not be in list.

    @property
    def valid_colourmap_names(self):
        return self._valid_colourmap_names
