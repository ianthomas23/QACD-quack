import matplotlib.pyplot as plt
from qacd_project import QACDProject




project = QACDProject()
project.set_filename('out.quack')
project.load_raw_csv_files('test_data', ['Ca K series.csv', 'O K series.csv'])
project.filter(median=True)
print(project.elements)


if 1:
    element = 'Ca'

    plt.subplot(221)
    raw, raw_stats = project.get_raw(element, want_stats=True)
    plt.imshow(raw)
    plt.colorbar()
    plt.title('{} raw'.format(element))

    plt.subplot(222)
    filtered, filtered_stats = project.get_filtered(element, want_stats=True)
    plt.imshow(filtered)
    plt.colorbar()
    plt.title('{} filtered'.format(element))

    plt.subplot(223)
    plt.hist(raw.ravel(), bins=20)
    plt.axvline(raw_stats['mean'], c='r')
    plt.axvline(raw_stats['median'], c='y')

    plt.subplot(224)
    plt.hist(filtered.ravel(), bins=20)
    plt.axvline(filtered_stats['mean'], c='r')
    plt.axvline(filtered_stats['median'], c='y')

    plt.show()
