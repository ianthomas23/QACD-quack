import matplotlib.pyplot as plt
import numpy as np

from qacd_project import QACDProject


want_normalised = True  # Rather than filtered.
want_h_factor = True
want_plot = True
want_histograms = True;


project = QACDProject()
project.set_filename('out.quack')
if 0:
    project.import_raw_csv_files('test_data')
else:
    project.import_raw_csv_files('test_data', ['Al K series.csv',
                                               'Ca K series.csv',
                                               'Mg K series.csv',
                                               'O K series.csv'])
project.filter(pixel_totals=True, median=True)
project.normalise()
project.calculate_h_factor()
project.write_debug()


if want_plot:
    element = 'Ca'

    ax = plt.subplot(221)
    raw, raw_stats = project.get_raw(element, want_stats=True)
    plt.imshow(raw)
    plt.colorbar()
    plt.title('{} raw'.format(element))

    plt.subplot(222, sharex=ax, sharey=ax)
    if want_normalised:
        filtered, filtered_stats = project.get_normalised(element, want_stats=True)
        plt.imshow(filtered)
        plt.colorbar()
        plt.title('{} normalised'.format(element))
    else:
        filtered, filtered_stats = project.get_filtered(element, want_stats=True)
        plt.imshow(filtered)
        plt.colorbar()
        plt.title('{} filtered'.format(element))

    if want_histograms:
        plt.subplot(223)
        data = raw.ravel()
        plt.hist(data[np.isfinite(data)], bins=20)
        plt.axvspan(raw_stats['median']-2*raw_stats['std'],
                    raw_stats['median']+  raw_stats['std'], facecolor='y', alpha=0.5)
        plt.axvline(raw_stats['mean'], c='r')
        plt.axvline(raw_stats['mean']-raw_stats['std'], c='r', alpha=0.5)
        plt.axvline(raw_stats['mean']+raw_stats['std'], c='r', alpha=0.5)
        plt.axvline(raw_stats['median'], c='y')

        plt.subplot(224)
        data = filtered.ravel()
        plt.hist(data[np.isfinite(data)], bins=20)
        plt.axvspan(filtered_stats['median']-2*filtered_stats['std'],
                    filtered_stats['median']+  filtered_stats['std'], facecolor='y', alpha=0.5)
        plt.axvline(filtered_stats['mean'], c='r')
        plt.axvline(filtered_stats['mean']-filtered_stats['std'], c='r', alpha=0.5)
        plt.axvline(filtered_stats['mean']+filtered_stats['std'], c='r', alpha=0.5)
        plt.axvline(filtered_stats['median'], c='y')

    if 1:
        plt.figure()
        ax = plt.subplot(221)
        raw_total, raw_total_stats = project.get_raw_total(want_stats=True)
        print('raw_total_stats', raw_total_stats)
        plt.imshow(raw_total)
        plt.colorbar()
        plt.title('Raw total')

        plt.subplot(222, sharex=ax, sharey=ax)
        if want_h_factor:
            f_total, f_total_stats = project.get_h_factor(want_stats=True)
            print('h_factor_total_stats', f_total_stats)
            plt.imshow(f_total)
            plt.colorbar()
            plt.title('H factor')
        else:
            f_total, f_total_stats = project.get_filtered_total(want_stats=True)
            print('filtered_total_stats', f_total_stats)
            plt.imshow(f_total)
            plt.colorbar()
            plt.title('Filtered total')

        if want_histograms:
            plt.subplot(223)
            plt.hist(raw_total.ravel(), bins=40)
            plt.axvspan(raw_total_stats['median']-2*raw_total_stats['std'],
                        raw_total_stats['median']+  raw_total_stats['std'], facecolor='y', alpha=0.5)
            plt.axvline(raw_total_stats['mean'], c='r')
            plt.axvline(raw_total_stats['mean']-raw_total_stats['std'], c='r', alpha=0.5)
            plt.axvline(raw_total_stats['mean']+raw_total_stats['std'], c='r', alpha=0.5)
            plt.axvline(raw_total_stats['median'], c='y')

            plt.subplot(224)
            data = f_total.ravel()
            plt.hist(data[np.isfinite(data)], bins=40)
            plt.axvspan(f_total_stats['median']-2*f_total_stats['std'],
                        f_total_stats['median']+  f_total_stats['std'], facecolor='y', alpha=0.5)
            plt.axvline(f_total_stats['mean'], c='r')
            plt.axvline(f_total_stats['mean']-f_total_stats['std'], c='r', alpha=0.5)
            plt.axvline(f_total_stats['mean']+f_total_stats['std'], c='r', alpha=0.5)
            plt.axvline(f_total_stats['median'], c='y')

    plt.show()
