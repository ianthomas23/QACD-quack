#from matplotlib import cm
#import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import numpy as np

from src.model.qacd_project import QACDProject


want_normalised = False  # Rather than filtered.
want_h_factor = True
want_plot = 1
want_histograms = True;


project = QACDProject()
project.set_filename('example.quack')
if 0:
    project.import_raw_csv_files('test_data')
    #project.import_raw_csv_files('/home/iant/Desktop/Johan_Lissenberg_Xmas2015',
    #                             ['Ca K series.csv', 'Mg K series.csv'])
else:
    project.import_raw_csv_files('test_data', ['Ca K series.csv',
                                               'Na K series.csv',
                                               'Mg K series.csv'])

project.filter(pixel_totals=True, median=True)
project.normalise()
project.calculate_h_factor()

project.create_phase_map_by_thresholding('test', [['Ca', 1500, 1700],
                                                  ['Na', 100, 800]])
project.create_phase_map_by_thresholding('single', [['Mg', 100, 1000]])
print('Phases:', project.phases)
phase = project.get_phase('test')

plt.subplot(211)
plt.imshow(project.get_filtered('Mg'))
plt.colorbar()
plt.subplot(212)

if 1:
    plt.imshow(phase)
else:
    cmap_int_max = 2
    norm = Normalize(-0.5, cmap_int_max-0.5)
    image = plt.imshow(phase, norm=norm)
    cmap_ticks = np.arange(0, cmap_int_max)
    figure = plt.gcf()
    colorbar = figure.colorbar(image, ticks=cmap_ticks)
    #plt.colorbar()

plt.show()
