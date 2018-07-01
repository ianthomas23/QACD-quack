from matplotlib.patches import Ellipse, Rectangle
import numpy as np
import numba


def apply_correction_model(correction_model, element_or_preset_name, array):
    correction = correction_model[element_or_preset_name]
    if correction[0] != 'poly':
        raise RuntimeError('Unrecognised correction type: {}'.format(correction[0]))
    poly = list(reversed(correction[1]))  # Decreasing power order.
    poly = np.poly1d(poly)
    return poly(array)


def calculate_region_ellipse(x, y, centre, size):
    # Return boolean array of same shape as x and y.
    xy = np.stack((x.ravel(), y.ravel()), axis=1)  # Shape (npoints, 2)
    ellipse = Ellipse(centre, width=size[0], height=size[1])
    region = ellipse.contains_points(xy)           # Shape (2*npoints)
    region.shape = x.shape                         # Shape (npoints, 2)
    return region


def calculate_region_rectangle(x, y, corner0, corner1):
    # Return boolean array of same shape as x and y.
    xy = np.stack((x.ravel(), y.ravel()), axis=1)  # Shape (npoints, 2)
    rectangle = Rectangle(corner0,
                          width=corner1[0]-corner0[0],
                          height=corner1[1]-corner0[1])
    region = rectangle.contains_points(xy)           # Shape (2*npoints)
    region.shape = x.shape                         # Shape (npoints, 2)
    return region


# 3x3 median filter, ignoring nans.
# Would like to use scipy.ndimage.filters.median_filter but it treats nans as
# finite numbers.  scipy.ndimage.filters.generic_filter using np.nanmedian works
# correctly but is very slow.  Here using explicit loops but sped up using
# numba.
@numba.jit
def median_filter_with_nans(input_array):
    ny, nx = input_array.shape
    output_array = np.empty_like(input_array)
    for j in range(ny):
        jm = j-1 if j > 0 else 0
        jp = j+2 if j < ny-1 else j+1
        for i in range(nx):
            im = i-1 if i > 0 else 0
            ip = i+2 if i < nx-1 else i+1
            subarray = input_array[jm:jp, im:ip]
            if np.isnan(subarray).sum() > subarray.size // 2:
                output_array[j, i] = np.nan
            else:
                output_array[j, i] = np.nanmedian(subarray)
    return output_array


# Read csv file as 2D array.  np.genfromtxt is quite slow.  Would like to use
# faster np.loadtxt but it does not like empty final column.
# shape is optional, if specified it speeds up the reading.
def read_csv(full_filename, dtype, shape):
    with open(full_filename, 'r') as f:
        if shape:
            x = np.empty(shape, dtype=dtype)
        else:
            x = []

        for row, line in enumerate(f):
            fields = line.split(',')[:-1]

            if shape:
                if row >= shape[0]:
                    raise RuntimeError('CSV file has {} rows, expected {}'.format( \
                        row, shape[0]))
                if len(fields) != shape[1]:
                    raise RuntimeError('CSV file has {} columns, expected {}'.format( \
                        len(fields), shape[1]))

            fields = [dtype(field) for field in fields]
            if shape:
                x[row] = fields
            else:
                x.append(fields)

    if shape:
        return x
    else:
        return np.array(x, dtype=dtype)
