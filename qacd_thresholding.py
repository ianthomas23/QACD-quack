__author__ = 'Matthew Loocke'
__version__= '0.0.1'

#import python standard modules
#import 3rd party libraries
import tables as tb
import numpy as np
import gc
    
def worker2(threshDic, varProj, phase):
    filters = tb.Filters(complevel=5, complib='blosc')
    thd = threshDic
    print thd
    varProj = varProj
    print varProj
    phasename = phase
    tmp = {}
    els = thd.keys()
    dmax = {}
    dmin = {}
    for item in els:
        var = str(item)
        ds = thd[var]
        dmax[var]=ds['max']
        dmin[var]=ds['min']
    print dmax
    f = tb.open_file(varProj, mode='a')
    Filt = f.root.Filtered
    Phas = f.root.Phase
    mks = []
    for item in els:
        var = str(item)
        ds1 = f.get_node(Filt, var).read()
        mx = dmax[var] * 1
        print mx
        mn = dmin[var] * 1
        print mn
        m1 = (ds1 < mx)
        if mn == 0:
            tp = (m1*1)
            msk = (tp == 1)
            print 'no lower threshold'
        else:
            m2 = (ds1 > mn)
            tp = (m1 * 1) + (m2 * 1)
            msk = (tp == 2)
        mks.append(msk.astype(int))
    print mks
    mask10 = mks[0]
    for i in xrange(1, len(mks)):
        ds = mks[i]
        mask10 = mask10 + ds
    print mask10
    mask = mask10/(len(mks))
    atom2 = tb.Atom.from_dtype(mask.dtype)
    tmp = f.createCArray(Phas,phasename,atom2,mask.shape,filters=filters)
    tmp[:] = mask
    y, x = mask.shape[0], mask.shape[1]
    tmp.attrs.sizeY = y
    tmp.attrs.sizeX = x
    pix = np.sum(mask)
    tmp.attrs.pixels = pix
    print 'PhaseMaps masked and saved'
    f.close()
    gc.collect()
    string4 = 'Stats Calculated'
    return string4
    
        
    
    
    
    
