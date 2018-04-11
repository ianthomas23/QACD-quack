import fnmatch
import os
import numpy as np
import pytest

from src.model.qacd_project import QACDProject, State


test_dir = 'test_data'
temp_filename = 'test.quack'


def test_sequence():
    # Test that sequence of operations is correct, which is mostly controlled
    # by project state.
    p = QACDProject()
    assert p.state == State.INVALID

    # INVALID -> EMPTY.
    p.set_filename(temp_filename)
    assert p.state == State.EMPTY
    assert p.elements is None
    with pytest.raises(RuntimeError):
        p.get_raw('Mg')
    with pytest.raises(RuntimeError):
        p.get_raw_total()

    # EMPTY -> RAW.
    p.import_raw_csv_files(test_dir,
                           [el+' K series.csv' for el in ['Na', 'Mg', 'Ca']])
    assert p.state == State.RAW
    with pytest.raises(RuntimeError):
        p.set_filename('')
    assert sorted(p.elements) == p.elements
    assert p.elements == ['Ca', 'Mg', 'Na']
    raw = p.get_raw('Mg')
    raw_total = p.get_raw_total()
    with pytest.raises(RuntimeError):
        p.get_raw('Aa')
    with pytest.raises(RuntimeError):
        p.get_filtered('Mg')

    # RAW -> FILTERED.
    p.filter(pixel_totals=True, median=True)
    assert p.state == State.FILTERED
    with pytest.raises(RuntimeError):
        p.import_raw_csv_files(test_dir)
    p.get_filtered('Mg')
    p.get_filtered_total()
    with pytest.raises(RuntimeError):
        p.get_filtered('Aa')
    with pytest.raises(RuntimeError):
        p.get_normalised('Mg')

    # FILTERED -> NORMALISED.
    p.normalise()
    assert p.state == State.NORMALISED
    with pytest.raises(RuntimeError):
        p.filter(pixel_totals=True, median=True)
    p.get_normalised('Mg')
    with pytest.raises(RuntimeError):
        p.get_normalised('Aa')
    with pytest.raises(RuntimeError):
        p.get_h_factor()
    k_min = 5
    k_max = 8
    with pytest.raises(RuntimeError):
        p.k_means_clustering(k_min, k_max)
    with pytest.raises(RuntimeError):
        p.create_ratio_map('some_ratio', ['Mg', 'Ca'])

    # NORMALISED -> H_FACTOR.
    p.calculate_h_factor()
    assert p.state == State.H_FACTOR
    with pytest.raises(RuntimeError):
        p.normalise()
    p.get_h_factor()

    # H_FACTOR -> CLUSTERING.
    p.k_means_clustering(k_min, k_max)
    assert p.state == State.CLUSTERING
    with pytest.raises(RuntimeError):
        p.calculate_h_factor()
    p.get_cluster_indices(k_min)
    p.get_cluster_indices(k_max)
    with pytest.raises(RuntimeError):
        p.get_cluster_indices(k_min-1)
    with pytest.raises(RuntimeError):
        p.get_cluster_indices(k_max+1)

    # Ratio maps.
    p.create_ratio_map('some_ratio', ['Mg', 'Ca'])
    p.get_ratio_by_name('some_ratio')
    ratios = p.ratios
    assert len(ratios) == 1
    assert 'some_ratio' in ratios
    assert ratios['some_ratio'][0] == 'Mg/(Mg+Ca)'
    with pytest.raises(RuntimeError):
        p.create_ratio_map('some_ratio', ['Mg', 'Ca'])  # Already exists.
    with pytest.raises(RuntimeError):
        p.create_ratio_map('ratio_no_such_element', ['Mg', 'Aa'])
    p.create_ratio_map('corrected_ratio', ['Mg', 'Na'],
                       correction_model='feldspar')
    assert len(ratios) == 2
    assert 'corrected_ratio' in ratios
    assert ratios['corrected_ratio'][0] == 'Mg/(Mg+Na)'
    with pytest.raises(RuntimeError):
        p.create_ratio_map('invalid_correction', ['Mg', 'Ca'],
                           correction_model='no_such_correction_name')

    # Cleanup.
    if os.path.isfile(temp_filename):
        os.remove(temp_filename)


def check_masked_array(array, shape, dtype, mask, masked_value):
    assert np.ma.isMaskedArray(array)
    assert array.shape == shape
    assert array.dtype == dtype
    np.testing.assert_equal(array.mask, mask)
    np.testing.assert_equal(array.fill_value, masked_value)
    np.testing.assert_equal(array.data[mask], masked_value)
    if np.isnan(masked_value):
        np.testing.assert_array_equal(np.isnan(array.data), array.mask)
    else:
        np.testing.assert_array_equal(array.data == masked_value, array.mask)


def check_stats(array, stats, which):
    # Check each stat in turn, and that haven't missed any.
    which = which.split()
    for key in which:
        if key == 'min':
            assert stats[key] == np.ma.min(array)
        elif key == 'max':
            assert stats[key] == np.ma.max(array)
        elif key == 'mean':
            assert stats[key] == np.ma.mean(array)
        elif key == 'median':
            assert stats[key] == np.ma.median(array)
        elif key == 'std':
            assert stats[key] == np.ma.std(array)
        elif key == 'invalid':
            assert stats[key] == np.ma.count_masked(array)
        elif key == 'valid':
            assert stats[key] == np.ma.count(array)
        else:
            raise RuntimeError('Unrecognised stats key: ' + key)
    assert len(which) == len(stats)


def consistency_impl(directory, pixel_totals, median):
    # Test that project is consistent, e.g. size of arrays, common masks.
    # This test works on all models regardless of elements, etc.
    p = QACDProject()
    p.set_filename(temp_filename)
    p.import_raw_csv_files(directory)#, [el+' K series.csv' for el in ['Mg', 'Ca', 'Na']])
    p.filter(pixel_totals=pixel_totals, median=median)
    p.normalise()
    p.calculate_h_factor()

    elements = p.elements
    files = fnmatch.filter(os.listdir(directory), '* K series.csv')
    assert elements == sorted([file_.split()[0] for file_ in files])

    for i, element in enumerate(elements):
        raw, raw_stats = p.get_raw(element, want_stats=True)
        filtered, filtered_stats = p.get_filtered(element, want_stats=True)
        normalised, normalised_stats = p.get_normalised(element, want_stats=True)
        if i == 0:
            ny, nx = raw.shape
            raw_cumulative = raw.copy()
            raw_mask = raw.mask
            filtered_cumulative = filtered.copy()
            filtered_mask = filtered.mask
            normalised_cumulative = normalised.copy()
            normalised_mask = normalised.mask
        else:
            raw_cumulative += raw
            filtered_cumulative += filtered
            normalised_cumulative += normalised

        check_masked_array(raw, (ny, nx), np.int32, raw_mask, -1)
        check_stats(raw, raw_stats, 'min max mean median std invalid valid')

        check_masked_array(filtered, (ny, nx), np.float64, filtered_mask, np.nan)
        check_stats(filtered, filtered_stats,
                    'min max mean median std invalid valid')

        check_masked_array(normalised, (ny, nx), np.float64, normalised_mask, np.nan)
        check_stats(normalised, normalised_stats,
                    'min max mean median std invalid valid')

        # Check raw masked carry across to filtered and normalised.
        assert np.all(filtered.data[raw.mask] == np.nan)
        assert np.all(normalised.data[raw.mask] == np.nan)

    raw_total, raw_total_stats = p.get_raw_total(want_stats=True)
    assert np.allclose(raw_total, raw_cumulative)
    check_masked_array(raw_total, (ny, nx), np.int32, raw_mask, -1)
    check_stats(raw_total, raw_total_stats,
                'min max mean median std invalid valid')

    filtered_total, filtered_total_stats = p.get_filtered_total(want_stats=True)
    assert np.allclose(filtered_total, filtered_cumulative)
    check_masked_array(filtered_total, (ny, nx), np.float64, filtered_mask,
                       np.nan)
    check_stats(filtered_total, filtered_total_stats,
                'min max mean median std invalid valid')

    assert np.allclose(normalised_cumulative, 1.0)
    np.testing.assert_array_equal(normalised.mask, filtered.mask)

    # h factor.
    h_factor, h_factor_stats = p.get_h_factor(want_stats=True)
    np.testing.assert_array_equal(h_factor.mask, filtered.mask)
    check_masked_array(h_factor, (ny, nx), np.float64, h_factor.mask, np.nan)
    check_stats(h_factor, h_factor_stats,
                'min max mean median std invalid valid')

    # Ratio.
    ratio_elements = ['Ca', 'Mg']
    formula = '{0}/({0}+{1})'.format(ratio_elements[0], ratio_elements[1])
    for name, correction_model in zip(['ratioA', 'ratioB'], [None, 'garnet']):
        p.create_ratio_map(name, ratio_elements, correction_model=correction_model)
        ratio_entry = p.ratios[name]
        assert formula, name == ratio_entry
        ratio, ratio_stats = p.get_ratio_by_name(name, want_stats=True)
        ratio_stats.pop('name')
        ratio_stats.pop('formula')
        ratio_stats.pop('correction_model')
        ratio_stats.pop('is_preset')

        check_masked_array(ratio, (ny, nx), np.float64, ratio.mask, np.nan)
        check_stats(ratio, ratio_stats, 'min max mean median std invalid valid')

    # k-means clustering
    k_min = 5
    k_max = 10
    p.k_means_clustering(k_min, k_max)
    for k in range(k_min, k_max+1):
        cluster, cluster_stats = p.get_cluster_indices(k, want_stats=True)
        np.testing.assert_array_equal(cluster.mask, filtered.mask)
        check_masked_array(cluster, (ny, nx), np.int8, cluster.mask, -1)
        check_stats(cluster, cluster_stats, 'min max invalid valid')

    # Cleanup.
    if os.path.isfile(temp_filename):
        os.remove(temp_filename)


def test_consistent():
    consistency_impl(test_dir, True, True)
    consistency_impl(test_dir, True, False)
    consistency_impl(test_dir, False, True)
    consistency_impl(test_dir, False, False)


def test_load_from_file():
    directory = 'test_data'
    files = ['out{}'.format(index) for index in range(5)]
    for filename in files:
        full_filename = os.path.join(directory, filename)
        p = QACDProject()
        p.load_file(full_filename)


def test_accuracy():
    # Different filter options.
    pass
