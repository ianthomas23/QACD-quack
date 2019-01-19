import math
from matplotlib.patches import Ellipse, Polygon, Rectangle
import numpy as np
import numba


def adaptive_interp(x, y, max_extra):
    # Interpolate 1D arrays x,y with from 0 to max_extra points between each
    # original point depending on abs(diff(y)) between adjacent points.  The
    # largest abs(diff) has max_extra points inserted, decreasing down to no
    # extra points for low abs(diff).
    npts = len(x)
    diff = np.absolute(np.diff(y))
    normalised_diff = diff / diff.max()  # In range 0 to 1.
    extras = (normalised_diff*max_extra).astype(np.int)  # In range 0 to max_extra.
    extra_points = extras.sum()
    new_npts = npts + extra_points
    new_x = np.empty(new_npts)
    new_y = np.full(new_npts, np.nan)
    j = 0
    for i in range(npts-1):
        new_x[j] = x[i]
        new_y[j] = y[i] if y[i] is not np.ma.masked else np.nan
        extra = extras[i]
        if extra is np.ma.masked:
            extra = 0
        elif extra > 0:
            ks = np.arange(extra+1)
            fractions = (ks + 1) / (extra + 1.0)
            new_x[j+1:j+extra+2] = (1.0-fractions)*x[i] + fractions*x[i+1]
            new_y[j+1:j+extra+2] = (1.0-fractions)*y[i] + fractions*y[i+1]
        j += 1 + extra
    if j != new_npts-1:
        raise RuntimeError('Interpolation error')
    new_x[j] = x[-1]
    new_y[j] = y[-1] if y[-1] is not np.ma.masked else np.nan
    return new_x, new_y


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


def calculate_region_polygon(x, y, points):
    # Return boolean array of same shape as x and y.
    xy = np.stack((x.ravel(), y.ravel()), axis=1)  # Shape (npoints, 2)
    polygon = Polygon(points, closed=False)        # Already closed.
    region = polygon.contains_points(xy)           # Shape (2*npoints)
    region.shape = x.shape                         # Shape (npoints, 2)
    return region


def calculate_region_rectangle(x, y, corner0, corner1):
    # Return boolean array of same shape as x and y.
    xy = np.stack((x.ravel(), y.ravel()), axis=1)  # Shape (npoints, 2)
    rectangle = Rectangle(corner0,
                          width=corner1[0]-corner0[0],
                          height=corner1[1]-corner0[1])
    region = rectangle.contains_points(xy)         # Shape (2*npoints)
    region.shape = x.shape                         # Shape (npoints, 2)
    return region


def calculate_transect(array, start, end):
    # Calculate transect through pixel array from start xy to end xy.
    # Returns two 1D arrays, lambdas from 0 to 1 (start to end) and values the
    # nearest values from the array.
    n = 1 + int(np.absolute(end - start).max())

    lambdas = np.linspace(0.0, 1.0, n)
    xs = start[0] + (end[0] - start[0])*lambdas
    ys = start[1] + (end[1] - start[1])*lambdas
    i = np.floor(xs).astype(np.int32)
    j = np.floor(ys).astype(np.int32)
    values = array[j, i]

    return lambdas, values


def get_mask_extent(mask):
    # mask is a 2D boolean array.  Want min and max i and j indices of True
    # values.
    rows = np.where(mask.sum(axis=1) > 0)[0]
    if len(rows) == 0:
        return (None, )
    jmin, jmax = rows[0], rows[-1]+1

    cols = np.where(mask[jmin:jmax].sum(axis=0) > 0)[0]
    if len(cols) == 0:
        return (None, )
    imin, imax = cols[0], cols[-1]+1

    return [[imin-1, imax+1], [jmin-1, jmax+1]]


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
