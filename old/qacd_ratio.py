__author__ = 'Matthew Loocke'
__version__= '0.0.1'

#import python standard modules
#import 3rd party libraries
import tables as tb
import numpy as np
import gc
import math
import correction as qc

def h_correction(hfac,mname):
    y, x = mname.shape[0], mname.shape[1]
    hfac = np.reshape(hfac, (y, x))
    temp = mname * hfac
    return temp

def map_calc1(varProj, mapname, mapDic):
    va = mapDic['A']
    vb = mapDic['B']
    val = mapDic['function']
    val2 = mapDic['val2']
    corr = mapDic['correction']
    print('==> map_calc1', va, vb, val, val2, corr, 'STRANGE')
    print va, vb, val
    mapname = mapname
    print mapname
    f = tb.open_file(varProj, mode='a')
    hfac = f.get_node(f.root, "HFactor").read()
    Filt = f.root.Filtered
    da = f.get_node(Filt, va).read()
    da = h_correction(hfac,da)
    db = f.get_node(Filt, vb).read()
    db = h_correction(hfac,db)
    da[np.isnan(da)]=0
    db[np.isnan(db)]=0
    ds = (da / (da + (db)))
    cor1 = (-0.125*(ds**2))+(0.125*ds)
    ds = ds - cor1
    del da, db, hfac
    if corr == 'None':
        tpd = f.create_array(Filt, mapname, ds)
        y, x = ds.shape[0], ds.shape[1]
        mean = np.nanmean(ds)
        median = np.nanmedian(ds)
        maxi = np.nanmax(ds)
        mini = np.nanmin(ds)
        std = np.nanstd(ds)
    else:
        tmp = f.root
        lis = tmp._v_children
        if 'Concentration' in lis.keys():
            Filt2 = f.root.Concentration
        else:
            Filt2 = f.create_group(f.root,"Concentration","Concentration")
            print 'New group, Concentration, created!'
        Filt2 = f.root.Concentration
        chdic = qc.equations(corr)
        xdic = chdic[val2]
        calc = corr_proc(ds, xdic)
        tpd = f.create_array(Filt2, mapname, calc)
        y, x = calc.shape[0], calc.shape[1]
        mean = np.nanmean(calc)
        median = np.nanmedian(calc)
        maxi = np.nanmax(calc)
        mini = np.nanmin(calc)
        std = np.nanstd(calc)
    tpd.attrs.sizeY = y
    tpd.attrs.sizeX = x
    pix = y*x
    tpd.attrs.pixels = pix
    tpd.attrs.mean = mean
    tpd.attrs.median = median
    tpd.attrs.max = maxi
    tpd.attrs.min = mini
    tpd.attrs.std = std
    print pix, mean, median, maxi, mini,  std
    #insert a new particle record
    string = "Project: "+str(varProj)+"\nElement Map: "+mapname+"\nWidth/Height: "+str(x)+"x"+str(y)+"\nPixels(n): "+str(pix)
    string2 = "\nMean: "+str(mean)+"\nMedian: "+str(median)+"\nMin/Max: "+str(mini)+":"+str(maxi)+"\nStDev: "+str(std)
    string3 = string + string2
    tpd.attrs.stats = string3
    f.close()
    stringer = 'Map Created!'
    gc.collect()
    return stringer
def map_calc2(varProj, mapname, mapDic):
    va = mapDic['A']
    vb = mapDic['B']
    val = mapDic['function']
    val2 = mapDic['val2']
    corr = mapDic['correction']
    print('==> map_calc2', va, vb, val, val2, corr)
    print va, vb, val
    mapname = mapname
    print mapname
    f = tb.open_file(varProj, mode='a')
    hfac = f.get_node(f.root, "HFactor").read()
    Filt = f.root.Filtered
    da = f.get_node(Filt, va).read()
    da = h_correction(hfac,da)
    if corr == 'None':
        da = f.get_node(Filt, va).read()
        da = h_correction(hfac,da)
        db = f.get_node(Filt, vb).read()
        db = h_correction(hfac,db)
        #da[np.isnan(da)]=0
        #db[np.isnan(db)]=0
        ds = da / (da + (db))
        tpd = f.create_array(Filt, mapname, ds)
        y, x = ds.shape[0], ds.shape[1]
        mean = np.nanmean(ds)
        median = np.nanmedian(ds)
        maxi = np.nanmax(ds)
        mini = np.nanmin(ds)
        std = np.nanstd(ds)
    else:
        chdic = qc.equations(corr)
        ds = f.get_node(Filt, va).read()
        ds = h_correction(hfac,ds)
        xdic = chdic[va]
        da = corr_proc(ds, xdic)
        del ds, xdic
        ds = f.get_node(Filt, vb).read()
        ds = h_correction(hfac,ds)
        xdic = chdic[vb]
        db = corr_proc(ds, xdic)
        del ds, xdic
        #da[np.isnan(da)]=0
        #db[np.isnan(db)]=0
        calc = da / (da + (db))
        del da,  db, hfac
        tmp = f.root
        lis = tmp._v_children
        if 'Concentration' in lis.keys():
            Filt2 = f.root.Concentration
        else:
            Filt2 = f.create_group(f.root,"Concentration","Concentration")
            print 'New group, Concentration, created!'
        tpd = f.create_array(Filt2, mapname, calc)
        y, x = calc.shape[0], calc.shape[1]
        mean = np.nanmean(calc)
        median = np.nanmedian(calc)
        maxi = np.nanmax(calc)
        mini = np.nanmin(calc)
        std = np.nanstd(calc)
    tpd.attrs.sizeY = y
    tpd.attrs.sizeX = x
    pix = y*x
    tpd.attrs.pixels = pix
    tpd.attrs.mean = mean
    tpd.attrs.median = median
    tpd.attrs.max = maxi
    tpd.attrs.min = mini
    tpd.attrs.std = std
    print pix, mean, median, maxi, mini,  std
    #insert a new particle record
    string = "Project: "+str(varProj)+"\nElement Map: "+mapname+"\nWidth/Height: "+str(x)+"x"+str(y)+"\nPixels(n): "+str(pix)
    string2 = "\nMean: "+str(mean)+"\nMedian: "+str(median)+"\nMin/Max: "+str(mini)+":"+str(maxi)+"\nStDev: "+str(std)
    string3 = string + string2
    tpd.attrs.stats = string3
    f.close()
    stringer = 'Map Created!'
    gc.collect()
    return stringer
def map_calc3(varProj, mapname, mapDic):
    va = mapDic['A']
    val = mapDic['function']
    val2 = mapDic['val2']
    corr = mapDic['correction']
    print('==> map_calc3', va, val, val2, corr, 'A only')
    chdic = qc.equations(corr)
    print va, val
    mapname = mapname
    print mapname
    f = tb.open_file(varProj, mode='a')
    hfac = f.get_node(f.root, "HFactor").read()
    Filt = f.root.Filtered
    ds = f.get_node(Filt, va).read()
    ds = h_correction(hfac,ds)
    xdic = chdic[va]
    calc = corr_proc(ds, xdic)
    del ds, hfac
    tmp = f.root
    lis = tmp._v_children
    if 'Concentration' in lis.keys():
        Filt2 = f.root.Concentration
    else:
        Filt2 = f.create_group(f.root,"Concentration","Concentration")
        print 'New group, Concentration, created!'
    tpd = f.create_array(Filt2, mapname, calc)
    y, x = calc.shape[0], calc.shape[1]
    tpd.attrs.sizeY = y
    tpd.attrs.sizeX = x
    pix = y*x
    tpd.attrs.pixels = pix
    mean = np.nanmean(calc)
    tpd.attrs.mean = mean
    median = np.nanmedian(calc)
    tpd.attrs.median = median
    maxi = np.nanmax(calc)
    tpd.attrs.max = maxi
    mini = np.nanmin(calc)
    tpd.attrs.min = mini
    std = np.nanstd(calc)
    tpd.attrs.std = std
    print pix, mean, median, maxi, mini,  std
    #insert a new particle record
    string = "Project: "+str(varProj)+"\nElement Map: "+mapname+"\nWidth/Height: "+str(x)+"x"+str(y)+"\nPixels(n): "+str(pix)
    string2 = "\nMean: "+str(mean)+"\nMedian: "+str(median)+"\nMin/Max: "+str(mini)+":"+str(maxi)+"\nStDev: "+str(std)
    string3 = string + string2
    tpd.attrs.stats = string3
    f.close()
    stringer = 'Map Created!'
    gc.collect()
    return stringer
def map_calc4(varProj, mapname, mapDic):
    va = mapDic['A']
    vb = mapDic['B']
    vc = mapDic['C']
    val = mapDic['function']
    val2 = mapDic['val2']
    corr = mapDic['correction']
    print('==> map_calc4', va, vb, vc, val, val2, corr, 'STRANGE')
    print va, vb, vc, val
    mapname = mapname
    print mapname
    f = tb.open_file(varProj, mode='a')
    hfac = f.get_node(f.root, "HFactor").read()
    Filt = f.root.Filtered
    da = f.get_node(Filt, va).read()
    da = h_correction(hfac,da)
    db = f.get_node(Filt, vb).read()
    db = h_correction(hfac,db)
    dc = f.get_node(Filt, vc).read()
    dc = h_correction(hfac,dc)
    da[np.isnan(da)]=0
    db[np.isnan(db)]=0
    dc[np.isnan(dc)]=0
    ds = da / (da + db + dc)
    cor1 = (-0.0417*(ds**2))+(0.0417*ds)
    ds = ds - cor1
    del da, db, dc, hfac
    if corr == 'None':
        tpd = f.create_array(Filt, mapname, ds)
        y, x = ds.shape[0], ds.shape[1]
        mean = np.nanmean(ds)
        median = np.nanmedian(ds)
        maxi = np.nanmax(ds)
        mini = np.nanmin(ds)
        std = np.nanstd(ds)
    else:
        tmp = f.root
        lis = tmp._v_children
        if 'Concentration' in lis.keys():
            Filt2 = f.root.Concentration
        else:
            Filt2 = f.create_group(f.root,"Concentration","Concentration")
            print 'New group, Concentration, created!'
        Filt2 = f.root.Concentration
        chdic = qc.equations(corr)
        xdic = chdic[val2]
        calc = corr_proc(ds, xdic)
        tpd = f.create_array(Filt2, mapname, calc)
        y, x = calc.shape[0], calc.shape[1]
        mean = np.nanmean(calc)
        median = np.nanmedian(calc)
        maxi = np.nanmax(calc)
        mini = np.nanmin(calc)
        std = np.nanstd(calc)
    tpd.attrs.sizeY = y
    tpd.attrs.sizeX = x
    pix = y*x
    tpd.attrs.pixels = pix
    tpd.attrs.mean = mean
    tpd.attrs.median = median
    tpd.attrs.max = maxi
    tpd.attrs.min = mini
    tpd.attrs.std = std
    print pix, mean, median, maxi, mini,  std
    #insert a new particle record
    string = "Project: "+str(varProj)+"\nElement Map: "+mapname+"\nWidth/Height: "+str(x)+"x"+str(y)+"\nPixels(n): "+str(pix)
    string2 = "\nMean: "+str(mean)+"\nMedian: "+str(median)+"\nMin/Max: "+str(mini)+":"+str(maxi)+"\nStDev: "+str(std)
    string3 = string + string2
    tpd.attrs.stats = string3
    f.close()
    stringer = 'Map Created!'
    gc.collect()
    return stringer
def map_calc5(varProj, mapname, mapDic):
    va = mapDic['A']
    vb = mapDic['B']
    vc = mapDic['C']
    val = mapDic['function']
    val2 = mapDic['val2']
    corr = mapDic['correction']
    print('==> map_calc5', va, vb, vc, val, val2, corr)
    print va, vb, vc, val
    mapname = mapname
    print mapname
    f = tb.open_file(varProj, mode='a')
    hfac = f.get_node(f.root, "HFactor").read()
    Filt = f.root.Filtered
    if corr == 'None':
        da = f.get_node(Filt, va).read()
        da = h_correction(hfac,da)
        db = f.get_node(Filt, vb).read()
        db = h_correction(hfac,db)
        dc = f.get_node(Filt, vc).read()
        dc = h_correction(hfac,dc)
        da[np.isnan(da)]=0
        db[np.isnan(db)]=0
        dc[np.isnan(dc)]=0
        ds = da / (da + db + dc)
        tpd = f.create_array(Filt, mapname, ds)
        y, x = ds.shape[0], ds.shape[1]
        mean = np.nanmean(ds)
        median = np.nanmedian(ds)
        maxi = np.nanmax(ds)
        mini = np.nanmin(ds)
        std = np.nanstd(ds)
    else:
        chdic = qc.equations(corr)
        ds = f.get_node(Filt, va).read()
        ds = h_correction(hfac,ds)
        xdic = chdic[va]
        da = corr_proc(ds, xdic)
        del ds, xdic
        ds = f.get_node(Filt, vb).read()
        ds = h_correction(hfac,ds)
        xdic = chdic[vb]
        db = corr_proc(ds, xdic)
        del ds, xdic
        ds = f.get_node(Filt, vc).read()
        ds = h_correction(hfac,ds)
        xdic = chdic[vc]
        dc = corr_proc(ds, xdic)
        del ds, xdic
        da[np.isnan(da)]=0
        db[np.isnan(db)]=0
        dc[np.isnan(dc)]=0
        calc = da / (da + db + dc)
        del da, db, dc, hfac
        tmp = f.root
        lis = tmp._v_children
        if 'Concentration' in lis.keys():
            Filt2 = f.root.Concentration
        else:
            Filt2 = f.create_group(f.root,"Concentration","Concentration")
            print 'New group, Concentration, created!'
        tpd = f.create_array(Filt2, mapname, calc)
        y, x = calc.shape[0], calc.shape[1]
        mean = np.nanmean(calc)
        median = np.nanmedian(calc)
        maxi = np.nanmax(calc)
        mini = np.nanmin(calc)
        std = np.nanstd(calc)
    tpd.attrs.sizeY = y
    tpd.attrs.sizeX = x
    pix = y*x
    tpd.attrs.pixels = pix
    tpd.attrs.mean = mean
    tpd.attrs.median = median
    tpd.attrs.max = maxi
    tpd.attrs.min = mini
    tpd.attrs.std = std
    print pix, mean, median, maxi, mini,  std
    #insert a new particle record
    string = "Project: "+str(varProj)+"\nElement Map: "+mapname+"\nWidth/Height: "+str(x)+"x"+str(y)+"\nPixels(n): "+str(pix)
    string2 = "\nMean: "+str(mean)+"\nMedian: "+str(median)+"\nMin/Max: "+str(mini)+":"+str(maxi)+"\nStDev: "+str(std)
    string3 = string + string2
    tpd.attrs.stats = string3
    f.close()
    stringer = 'Map Created!'
    gc.collect()
    return stringer
def map_calc6(varProj, mapname, mapDic):
    va = mapDic['A']
    vb = mapDic['B']
    vc = mapDic['C']
    vd = mapDic['D']
    val = mapDic['function']
    val2 = mapDic['val2']
    corr = mapDic['correction']
    print('==> map_calc6', va, vb, vc, vd, val, val2, corr)
    print va, vb, vc, vd, val
    mapname = mapname
    print mapname
    f = tb.open_file(varProj, mode='a')
    hfac = f.get_node(f.root, "HFactor").read()
    Filt = f.root.Filtered
    da = f.get_node(Filt, va).read()
    da = h_correction(hfac,da)
    db = f.get_node(Filt, vb).read()
    db = h_correction(hfac,db)
    dc = f.get_node(Filt, vc).read()
    dc = h_correction(hfac,dc)
    dd = f.get_node(Filt, vd).read()
    dd = h_correction(hfac,dd)
    da[np.isnan(da)]=0
    db[np.isnan(db)]=0
    dc[np.isnan(dc)]=0
    dd[np.isnan(dd)]=0
    ds = da / (da + db + dc + dd)
    del da, db, dc, dd, hfac
    if corr == 'None':
        tpd = f.create_array(Filt, mapname, ds)
        y, x = ds.shape[0], ds.shape[1]
        mean = np.nanmean(ds)
        median = np.nanmedian(ds)
        maxi = np.nanmax(ds)
        mini = np.nanmin(ds)
        std = np.nanstd(ds)
    else:
        tmp = f.root
        lis = tmp._v_children
        if 'Concentration' in lis.keys():
            Filt2 = f.root.Concentration
        else:
            Filt2 = f.create_group(f.root,"Concentration","Concentration")
            print 'New group, Concentration, created!'
        Filt2 = f.root.Concentration
        chdic = qc.equations(corr)
        xdic = chdic[val2]
        calc = corr_proc(ds, xdic)
        tpd = f.create_array(Filt2, mapname, calc)
        y, x = calc.shape[0], calc.shape[1]
        mean = np.nanmean(calc)
        median = np.nanmedian(calc)
        maxi = np.nanmax(calc)
        mini = np.nanmin(calc)
        std = np.nanstd(calc)
    tpd.attrs.sizeY = y
    tpd.attrs.sizeX = x
    pix = y*x
    tpd.attrs.pixels = pix
    tpd.attrs.mean = mean
    tpd.attrs.median = median
    tpd.attrs.max = maxi
    tpd.attrs.min = mini
    tpd.attrs.std = std
    print pix, mean, median, maxi, mini,  std
    #insert a new particle record
    string = "Project: "+str(varProj)+"\nElement Map: "+mapname+"\nWidth/Height: "+str(x)+"x"+str(y)+"\nPixels(n): "+str(pix)
    string2 = "\nMean: "+str(mean)+"\nMedian: "+str(median)+"\nMin/Max: "+str(mini)+":"+str(maxi)+"\nStDev: "+str(std)
    string3 = string + string2
    tpd.attrs.stats = string3
    f.close()
    stringer = 'Map Created!'
    gc.collect()
    return stringer
def corr_proc(ds, xdic):
    model = xdic["model"]
    if model == "line":
        ds1 = linecor(ds, xdic)
    elif model == "power":
        ds1 = powercor(ds, xdic)
    elif model == "log":
        ds1 = logcor(ds, xdic)
    elif model == "exp":
        ds1 = expcor(ds, xdic)
    elif model == "poly":
        ds1 = polycor(ds, xdic)
    return ds1
def linecor(ds,xdic):
    intc = xdic["int"]
    a = xdic["a"]
    ds1 = intc + (a*ds)
    del ds
    return ds1
def powercor(ds,xdic):
    a = xdic["a"]
    b = xdic["b"]
    ds1 = a * (ds**b)
    del ds
    return ds1
def logcor(ds,xdic):
    intc = xdic["int"]
    a = xdic["a"]
    ds1 = intc + a*(math.log(ds))
    del ds
    return ds1
def expcor(ds,xdic):
    a = xdic["a"]
    b = xdic["b"]
    ds1 = a * math.exp((b*ds))
    del ds
    return ds1
def polycor(ds,xdic):
    print('==> polycor', np.sum(~np.isfinite(ds)))
    order = xdic["order"]
    intc = xdic["int"]
    if order == 2:
        a = xdic["a"]
        b = xdic["b"]
        print('==> polycor 2', intc, a, b)
        ds1 = intc+(a*ds)+(b*(ds**2))
    elif order == 3:
        a = xdic["a"]
        b = xdic["b"]
        c = xdic["c"]
        print('==> polycor 3', intc, a, b, c)
        ds1 = intc+(a*ds)+(b*(ds**2))+(c*(ds**3))
    elif order == 4:
        a = xdic["a"]
        b = xdic["b"]
        c = xdic["c"]
        d = xdic["d"]
        print('==> polycor 4', intc, a, b, c, d)
        ds1 = intc+(a*ds)+(b*(ds**2))+(c*(ds**3))+(d*(ds**4))
    elif order == 5:
        a = xdic["a"]
        b = xdic["b"]
        c = xdic["c"]
        d = xdic["d"]
        e = xdic["e"]
        print('==> polycor 5', intc, a, b, c, d, e)
        ds1 = intc+(a*ds)+(b*(ds**2))+(c*(ds**3))+(d*(ds**4))+(e*(ds**5))
    elif order == 6:
        a = xdic["a"]
        b = xdic["b"]
        c = xdic["c"]
        d = xdic["d"]
        e = xdic["e"]
        f = xdic["f"]
        print('==> polycor 6', intc, a, b, c, d, e, f)
        ds1 = intc+(a*ds)+(b*(ds**2))+(c*(ds**3))+(d*(ds**4))+(e*(ds**5))+(f*(ds**6))
    print order
    del ds
    return ds1
