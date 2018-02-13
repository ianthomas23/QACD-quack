import numpy as np
import numba
from sklearn.cluster import MiniBatchKMeans

import matplotlib.pyplot as plt
from matplotlib import cm


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
            output_array[j, i] = np.nanmedian(input_array[jm:jp, im:ip])
    return output_array


def k_means_clustering(all_elements, k_min, k_max):
    print('==> k_means_clustering', all_elements.shape, k_min, k_max)
    ny, nx, nelements = all_elements.shape
    all_elements.shape = (ny*nx, nelements)
    print('==> k_means_clustering', all_elements.shape)

    # Cannot deal with NaN or infinity!!!!!
    all_elements[np.isnan(all_elements)] = 0.0 #1e6

    k = k_min
    #k = k_max-1
    kmeans = MiniBatchKMeans(n_clusters=k, random_state=1234, n_init=10,
                             #verbose=True,
                             )
    # Labels gives cluster of each pixel in range 0 to k-1.
    labels = kmeans.fit_predict(all_elements).astype(np.uint8)
    labels.shape = (ny, nx)
    print(labels.shape, labels)

    centroids = kmeans.cluster_centers_
    print(centroids.shape, centroids.dtype)  # 5x3 float64
    print(centroids)

    # Count number of pixels in each cluster?
    for i in range(k):
        print(i, np.sum(labels==i))


    # Does one cluster correspond to NaNs????????
    # If so, can I delete it?????

    cmap = cm.get_cmap('brg', k)  # k discrete levels
    plt.imshow(labels, cmap=cmap, vmin=-0.5, vmax=k-0.5)
    plt.colorbar()
    plt.title('k={}'.format(k))
    plt.show()
