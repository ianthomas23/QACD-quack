#Load Project Data Script
from __future__ import division
import pandas as pd
from pandas import *
import numpy as np
import gc
import tables as tb
import dask.array as da
from scipy.ndimage.filters import median_filter as medfilt

filters = tb.Filters(complevel=5, complib='blosc')

def Data_Load1(d, l):
    filters = tb.Filters(complevel=5, complib='blosc')
    Dict = d
    Length = l
    varProj = Dict['varProj']
    names = Dict['Names']
    pxszopt = Dict['pxszopt']
    f = tb.open_file(varProj, mode = 'a')
    Param = f.root.parameters
    ellsO = f.get_node(Param,"ElementList")
    ells = ellsO.read()
    Filt = f.root.Filtered
    elmp = [0]*Length
    for i in xrange(0,Length):
        var = ells[i]
        name = names[i]
        #Load and format element maps
        datamat = (pd.read_csv(name,header=None)).as_matrix(columns=None)
        sizeX, sizeY = np.shape(datamat)
        ds1 = (np.delete(datamat,(sizeY - 1),1)).astype(np.int32)
        elmp[i]=ds1
        del datamat,ds1
        print var
    del names
    gc.collect()
    Total = sum(elmp)
    vector = Total.reshape(1,(Total.shape[0]*Total.shape[1]))
    Total_m = (Total>((np.median(vector)) - (2*(np.std(vector))))) & (Total<((np.median(vector)) + (np.std(vector))))
    del Total,vector
    for i in xrange(0,Length):
        var = ells[i]
        ds1 = elmp[i]
        ds1_m = ds1/Total_m
        del ds1
        ds1_f = medfilt(ds1_m,size=(3,3),mode='nearest')
        atom = tb.Atom.from_dtype(ds1_f.dtype)
        dset = f.create_carray(Filt,var,atom,ds1_f.shape,filters=filters)
        dset[:] = ds1_f
        dset.attrs.Size = (sizeX,sizeY)
        del ds1_m,ds1_f
        print var
    del elmp
    f.close()
    gc.collect()
    r = stack_arrays(varProj)
    print r
    statcalc(varProj,pxszopt)
    return

def Data_Load2(d, l):
    filters = tb.Filters(complevel=5, complib='blosc')
    Dict = d
    Length = l
    varProj = Dict['varProj']
    names = Dict['Names']
    pxszopt = Dict['pxszopt']
    f = tb.open_file(varProj, mode = 'a')
    Param = f.root.parameters
    ellsO = f.get_node(Param,"ElementList")
    ells = ellsO.read()
    Filt = f.root.Filtered
    elmp = [0]*Length
    for i in xrange(0,Length):
        var = ells[i]
        name = names[i]
        #Load and format element maps
        datamat = (pd.read_csv(name,header=None)).as_matrix(columns=None)
        sizeX, sizeY = np.shape(datamat)
        ds1 = (np.delete(datamat,(sizeY - 1),1)).astype(np.int32)
        elmp[i]=ds1
        del datamat,ds1
        print var
    del names
    gc.collect()
    Total = sum(elmp)
    vector = Total.reshape(1,(Total.shape[0]*Total.shape[1]))
    Total_m = (Total>((np.median(vector)) - (2*(np.std(vector))))) & (Total<((np.median(vector)) + (np.std(vector))))
    del Total,vector
    for i in xrange(0,Length):
        var = ells[i]
        ds1 = elmp[i]
        ds1_f = ds1/Total_m
        del ds1
        atom = tb.Atom.from_dtype(ds1_f.dtype)
        dset = f.create_carray(Filt,var,atom,ds1_f.shape,filters=filters)
        dset[:] = ds1_f
        dset.attrs.Size = (sizeX,sizeY)
        del ds1_f
        print var
    del elmp
    f.close()
    gc.collect()
    r = stack_arrays(varProj)
    print r
    statcalc(varProj,pxszopt)
    return

def Data_Load3(d, l):
    ffilters = tb.Filters(complevel=5, complib='blosc')
    Dict = d
    Length = l
    varProj = Dict['varProj']
    names = Dict['Names']
    pxszopt = Dict['pxszopt']
    f = tb.open_file(varProj, mode = 'a')
    Param = f.root.parameters
    ellsO = f.get_node(Param,"ElementList")
    ells = ellsO.read()
    Filt = f.root.Filtered
    elmp = [0]*Length
    for i in xrange(0,Length):
        var = ells[i]
        name = names[i]
        #Load and format element maps
        datamat = (pd.read_csv(name,header=None)).as_matrix(columns=None)
        sizeX, sizeY = np.shape(datamat)
        ds1 = (np.delete(datamat,(sizeY - 1),1)).astype(np.int32)
        del datamat
        ds1_f = medfilt(ds1,size=(3,3),mode='nearest')
        del ds1
        atom = tb.Atom.from_dtype(ds1_f.dtype)
        dset = f.create_carray(Filt,var,atom,ds1_f.shape,filters=filters)
        dset[:] = ds1_f
        dset.attrs.Size = (sizeX,sizeY)
        del ds1_f
        print var
    del elmp
    f.close()
    gc.collect()
    r = stack_arrays(varProj)
    print r
    statcalc(varProj,pxszopt)
    return
def stack_arrays(varProj):
    print "Stacking Arrays"
    filters = tb.Filters(complevel=5, complib='blosc')
    f = tb.open_file(varProj, mode="a")
    Filt = f.root.Filtered
    ells1 = []
    lis = Filt._v_children
    if 'Ca' in lis.keys():
        ells1.append('Ca')
    if 'Mg' in lis.keys():
        ells1.append('Mg')
    if 'Al' in lis.keys():
        ells1.append('Al')
    if 'Si' in lis.keys():
        ells1.append('Si')
    if 'Fe' in lis.keys():
        ells1.append('Fe')
    ells2 = f.get_node(f.root.parameters,'ElementList').read()
    mlis = []
    mlis2 = []
    v = ells1[0]
    d = f.get_node(Filt,v)
    x, y = d.shape[1],d.shape[0]
    el_sh = x*y
    del d
    for item in ells2:
        tp = f.get_node(Filt,item).read()
        tp[np.isnan(tp)] = 0
        tp[np.isinf(tp)] = 0
        tp = tp.reshape(el_sh,1)
        d = da.from_array(tp, chunks=(10000, 1))
        mlis.append(d)
        if item in ells1:
            mlis2.append(d)
        del d, tp
        print item
    del el_sh, ells1, ells2
    fp = da.concatenate(mlis2, axis=1)
    atom = tb.Atom.from_dtype(fp.dtype)
    dset = f.create_carray(f.root,"Stack1",atom,fp.shape,filters=filters)
    dset.attrs.Size=(x,y)
    da.store(fp, dset)
    del fp, mlis2, atom
    fp = da.concatenate(mlis, axis=1)
    atom = tb.Atom.from_dtype(fp.dtype)
    dset = f.create_carray(f.root,"Stack2",atom,fp.shape,filters=filters)
    dset.attrs.Size=(x,y)
    da.store(fp, dset)
    del fp, mlis, atom,
    f.close()
    gc.collect()
    string = 'Stacked'
    return string
def statcalc(varProj,pxszopt):
    f = tb.open_file(varProj, mode = 'a')
    Filt = f.root.Filtered
    Para = f.root.parameters
    el = f.get_node(Para,'ElementList')
    ells = el.read()
    log = f.get_node(f.root,'Log').read()
    for item in ells:
        tmp = f.get_node(Filt, item)
        ds1 = tmp.read()
        y, x = ds1.shape[0], ds1.shape[1]
        pix = y*x
        ds1[np.isnan(ds1)] = 0
        ds1[np.isinf(ds1)] = 0
        mean = np.mean(ds1)
        median = np.median(ds1)
        maxi = np.max(ds1)
        mini = np.min(ds1)
        std = np.std(ds1)
        tmp.attrs.sizeY = y
        tmp.attrs.sizeX = x
        tmp.attrs.pixels = pix
        tmp.attrs.mean = mean
        tmp.attrs.median = median
        tmp.attrs.max = maxi
        tmp.attrs.min = mini
        tmp.attrs.std = std
        #insert a new particle record
        string = "Project: "+str(varProj)+"\nElement Map: "+item+"\nWidth/Height: "+str(x)+"x"+str(y)+"\nPixels(n): "+str(pix)
        string2 = "\nMean: "+str(mean)+"\nMedian: "+str(median)+"\nMin/Max: "+str(mini)+":"+str(maxi)+"\nStDev: "+str(std)
        string3 = string + string2
        tmp.attrs.stats = string3
        del mean,median,maxi,mini,std,ds1
        #insert a new particle record
    if pxszopt == 'Yes':
        pixsz = f.get_node(f.root,'PixSize').read()
        pix1 = pixsz[0]
        un = pixsz[1]
        sizeY = int(y)*float(pix1)
        sizeX = int(x)*float(pix1)
        area = sizeY*sizeX
        sarea = str(area)+un+"^2"
        sYs = str(sizeY)+un+" "+str(y)+"pixels"
        sXs = str(sizeX)+un+" "+str(x)+"pixels"
        log[5]=sXs
        log[6]=sYs
        log[7]=sarea
        log[8]=pix
    elif pxszopt == 'No':
        sYs = str(y)+"pixels"
        sXs = str(x)+"pixels"
        log[5]=sXs
        log[6]=sYs
        log[8]=pix
    del y,x,pix
    f.remove_node(f.root,'Log')
    f.create_array(f.root,'Log', log)
    f.close()
    gc.collect()
    print 'Stats Calculated'
    return

