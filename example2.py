import matplotlib.pyplot as plt
import numpy as np

from qacd_project import QACDProject

element = 'Ca'



p = QACDProject()
p.set_filename('out.quack')
p.import_raw_csv_files('test_data')
p.filter(pixel_totals=True, median=False)
p.normalise()
p.calculate_h_factor()

print(p.elements)


raw = p.get_raw(element)
print(type(raw), raw.dtype, np.ma.is_masked(raw))
filtered = p.get_filtered(element)
print(type(filtered), filtered.dtype, np.ma.is_masked(filtered))
normalised = p.get_normalised(element)
print(type(normalised), normalised.dtype, np.ma.is_masked(normalised))



if 1:
    plt.subplot(2, 3, 1)
    plt.imshow(raw)
    plt.title(element + ' raw')
    plt.colorbar()

    plt.subplot(2, 3, 2)
    plt.imshow(filtered)
    plt.title(element + ' filtered')
    plt.colorbar()

    plt.subplot(2, 3, 3)
    plt.imshow(normalised)
    plt.title(element + ' normalised')
    plt.colorbar()

    if np.ma.is_masked(raw):
        plt.subplot(2, 3, 4)
        plt.imshow(raw.mask)
        plt.title('raw mask')
        plt.colorbar()

    if np.ma.is_masked(filtered):
        plt.subplot(2, 3, 5)
        plt.imshow(filtered.mask)
        plt.title('filtered mask')
        plt.colorbar()

    if np.ma.is_masked(normalised):
        plt.subplot(2, 3, 6)
        plt.imshow(normalised.mask)
        plt.title('normalised mask')
        plt.colorbar()

    plt.show()
