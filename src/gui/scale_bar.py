from matplotlib.lines import Line2D
import matplotlib.offsetbox
from matplotlib.patches import Rectangle
from matplotlib.patheffects import Normal, Stroke


class ScaleBar(matplotlib.offsetbox.AnchoredOffsetbox):
    def __init__(self, size=1, extent=0.025, label="", loc=2, ax=None,
                 pad=0.6, borderpad=0.5, ppad=0, sep=4, prop=None,
                 frameon=False, **kwargs):
        # size: length of bar in data units.
        # extent: height of bar ends in axes units.
        if loc == 'upper right':
            loc = 1
        elif loc == 'upper left':
            loc = 2
        elif loc == 'lower left':
            loc = 3
        elif loc == 'lower right':
            loc = 4

        fc = 'w'  # Foreground colour.
        ec = 'k'  # Edge colour.

        trans = ax.get_xaxis_transform()
        size_bar = matplotlib.offsetbox.AuxTransformBox(trans)

        rectangle = Rectangle((0, 0), width=size, height=extent, fc=fc, ec=ec)
        size_bar.add_artist(rectangle)

        text = matplotlib.offsetbox.TextArea(label, minimumdescent=False,
                                             textprops={'color': fc})
        path_effects = [Stroke(linewidth=2, foreground=ec, alpha=0.75), Normal()]
        text._text.set_path_effects(path_effects)

        self.vpac = matplotlib.offsetbox.VPacker( \
            children=[size_bar, text], align="center", pad=ppad, sep=sep)

        matplotlib.offsetbox.AnchoredOffsetbox.__init__( \
            self, loc, pad=pad, borderpad=borderpad, child=self.vpac,
            prop=prop, frameon=frameon)
