import matplotlib.pyplot as plt
import numpy as np
import sys
import tables


if len(sys.argv) != 3:
    raise RuntimeError('Usage: {} <pytables filename> <array node name>')

filename = sys.argv[1]
node_name = sys.argv[2]

h5file = tables.open_file(filename, mode='r')
node = h5file.get_node(node_name)
array = node.read()

if len(array.shape) == 1:
    # File from original quack which has been unnecessarily flattened!
    log = h5file.get_node('/Log').read()
    nx = int(str(log[5], 'utf-8').split()[1].split('pixels')[0])
    ny = int(str(log[6], 'utf-8').split()[1].split('pixels')[0])
    array.shape = (ny, nx)
h5file.close()

number_invalid = np.isnan(array).sum()
min = np.nanmin(array)
max = np.nanmax(array)
mean = np.nanmean(array)
median = np.nanmedian(array)
std = np.nanstd(array)
invalid = number_invalid
valid = array.size - number_invalid

print('shape', array.shape)
print('min', min)
print('max', max)
print('mean', mean)
print('median', median)
print('std', std)
print('invalid', invalid)
print('valid', valid)


plt.subplot(211)
plt.imshow(array)
plt.colorbar()

plt.subplot(212)
data = array.ravel()
plt.hist(data[np.isfinite(data)], bins=40)
plt.axvspan(median-2*std, median+std, facecolor='y', alpha=0.5)
plt.axvline(mean, c='r')
plt.axvline(mean-std, c='r', alpha=0.5)
plt.axvline(mean+std, c='r', alpha=0.5)
plt.axvline(median, c='y')

plt.show()
