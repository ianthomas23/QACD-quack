import matplotlib.style as mps
import os


initial_path = None


def set_style():
    style_path = os.path.join(initial_path, 'qacd_xmap.mplstyle')
    mps.use(style_path)
