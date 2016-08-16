import tables as tb
import numpy as np
import os.path as path
from sklearn.cluster import MiniBatchKMeans
import gc
from tempfile import mkdtemp
from PyQt4 import QtGui

filters = tb.Filters(complevel=5, complib='blosc')

def monte_carlo(K): #Main function for carrying out Kmeans clustering
    filters = tb.Filters(complevel=5, complib='blosc')
    t = tb.open_file("temp.h5", mode="a") #opening tempfile for retrieving the variables of interest
    varProj = t.get_node(t.root, "varProj").read()
    clust = t.get_node(t.root, "clust").read()
    t.close()
    Message = 'Map Stacking'
    w = QtGui.QWidget()
    Question = 'Do you want to include all of the loaded maps (including minor elements) in the clustering calculation?\nWARNING:\nThis can add a significant amount of time to the calculation!'
    reply = QtGui.QMessageBox.question(w, Message,Question,QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
    if reply == QtGui.QMessageBox.Yes:
        fp, x, y = prepare_data2(varProj)
    else:
        fp, x, y = prepare_data(varProj)
    batch_size=100
    f = tb.open_file(varProj, mode="a")
    Clust = f.get_node(f.root, clust)
    for k in K:
        mbk = MiniBatchKMeans(init='k-means++', n_clusters=k, batch_size=batch_size,
                              n_init=10, max_no_improvement=10)
        mbk.fit(fp)
        centroids = mbk.cluster_centers_
        labels = mbk.labels_
        pmap = (labels.reshape(y,x)).astype(np.uint8)
        var = str(k) + " Phases"
        grp = f.create_group(Clust, var)
        f.create_array(grp, "centroids", centroids)
        f.create_array(grp, "labels", labels)
        atom2 = tb.Atom.from_dtype(pmap.dtype)
        dset = f.createCArray(grp,"pmap",atom2,pmap.shape,filters=filters)
        dset[:] = pmap
        string = 'Finished with ' + str(k)
        del centroids, labels, mbk,  var
        print string
        del pmap
        gc.collect()
    print 'Finished'
    del fp
    gc.collect()
    f.close()
    return
def prepare_data2(varProj): #Retrieval of data if choose to use all loaded elements
    f = tb.open_file(varProj, mode="a")
    Filt = f.root.Filtered
    d = f.get_node(Filt,'Ca').read()
    x, y = d.shape[1],d.shape[0]
    del d
    ds = f.get_node(f.root, "Stack2").read()
    fname = path.join(mkdtemp(),'kfile.dat')
    el_sh = ds.shape
    fp = np.memmap(fname,dtype='float64',mode='w+',shape=(el_sh))
    fp[:] = ds[:]
    del ds, fname, el_sh, 
    f.close()
    gc.collect()
    return fp, x, y
def prepare_data(varProj): #Retrieval of data if choose to use 5 common elements only
    f = tb.open_file(varProj, mode="a")
    Filt = f.root.Filtered
    d = f.get_node(Filt,'Ca').read()
    x, y = d.shape[1],d.shape[0]
    del d
    ds = f.get_node(f.root, "Stack1").read()
    fname = path.join(mkdtemp(),'kfile.dat')
    el_sh = ds.shape
    fp = np.memmap(fname,dtype='float64',mode='w+',shape=(el_sh))
    fp[:] = ds[:]
    del ds, fname, el_sh, 
    f.close()
    gc.collect()
    return fp, x, y
