__author__ = 'Matthew Loocke'
__version__= '0.0.1'

#import python standard modules
#import 3rd party libraries
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import tables as tb
import numpy as np
import gc
from tempfile import mkdtemp
import os.path as path
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.ticker import AutoMinorLocator
import utils

utils.set_style()

def savefig_map(Settings):
    figtitle = Settings['figtitle']
    filetitle = Settings['filetitle']
    filefmt = Settings['filefmt']
    filename = str(filetitle) + "." + str(filefmt)
    height = Settings['height']
    width = Settings['width']
    autoth = Settings['threshold']
    dpi = Settings['dpi']
    varProj = Settings['varProj']
    mapvar = Settings['mapvar']
    dataset = Settings['dataset']
    datagroup = Settings['datagroup']
    phase = Settings['phase']
    f = tb.open_file(varProj,mode='a')
    pxsz = f.get_node(f.root,'PixSize').read()
    ells = f.get_node(f.root.parameters,'ElementList').read()
    PixSize = float(pxsz[0])
    pixun = pxsz[1]
    f.close()
    print phase
    if dataset == 'Phase':
        dsm = data_ret(varProj,phase, mapvar, datagroup)
    else:
        dsm = data_ret2(varProj,dataset,phase, mapvar, datagroup)
    print dsm
    my_cmap = cm.get_cmap('gnuplot')
    my_cmap.set_under('k', alpha=0)
    my_cmap.set_over('k', alpha=0)
    plt.hold(False)
    fig = plt.figure(figsize=(width,height),dpi=dpi)
    axes = fig.add_subplot(111)
    if width <= 10.0:
        sz = "3%"
    else:
        sz = 0.3
    print sz
    if mapvar in ells:
        im = axes.imshow(dsm,cmap=my_cmap,interpolation='nearest',aspect='equal')
        axes.set_title(figtitle)
        divider = make_axes_locatable(axes)
        cax = divider.append_axes("right", size=sz, pad=0.1)
        cb = fig.colorbar(im,cax=cax)
        cb.ax.tick_params(labelsize=10)
        fig.tight_layout()
    elif autoth == 0:
        im = axes.imshow(dsm,cmap=my_cmap,vmin=0, vmax=1.0, interpolation='nearest',aspect='equal')
        axes.set_title(figtitle)
        divider = make_axes_locatable(axes)
        cax = divider.append_axes("right", size=sz, pad=0.1)
        cb = fig.colorbar(im,cax=cax)
        cb.set_clim(0.0, 1.0)
        cb.ax.tick_params(labelsize=10)
        fig.tight_layout()
    elif autoth == 1:
        mx, mn = np.nanmax(dsm), np.nanmin(dsm)
        im = axes.imshow(dsm,cmap=my_cmap,vmin=mn, vmax=mx, interpolation='nearest',aspect='equal')
        axes.set_title(figtitle)
        divider = make_axes_locatable(axes)
        cax = divider.append_axes("right", size=sz, pad=0.1)
        fig.colorbar(im,cax=cax)
        fig.tight_layout()
    axes.yaxis.set_ticks_position('left')
    axes.xaxis.set_ticks_position('bottom')
    xmin,xmax = axes.get_xlim()
    ymin,ymax = axes.get_ylim()
    xstep = ((xmax+0.5) / 5.0)
    ystep = ((ymin+0.5) / 4.0)
    xticks = np.arange(xmin,(xmax + xstep), xstep)
    yticks = np.arange(ymin,(ymax - ystep), -ystep)
    axes.xaxis.set_ticks(xticks)
    axes.yaxis.set_ticks(yticks)
    Length = len(xticks)
    Length2 = len(yticks)
    xlabels = ['Some']*Length
    ylabels = ['Some']*Length2
    xlabels[0] = '0' + str(pixun)
    for i in xrange(1,Length):
        val = xticks[i]
        val = int(val*PixSize)
        print val
        string = str(val) + str(pixun)
        xlabels[i]=string
    print xlabels
    for i in xrange(0,Length2):
        if i == (Length2-1):
            ylabels[i] = '0' + str(pixun)
        else:
            val = yticks[i]
            val = int(val*PixSize)
            print val
            string = str(val) + str(pixun)
            ylabels[i]=string
    print ylabels
    fig.canvas.draw()
    axes.set_xticklabels(xlabels)
    axes.set_yticklabels(ylabels)
    axes.tick_params(labelsize=12)
    fig.savefig(filename, dpi=dpi, format=filefmt)
    string = 'Map Saved'
    plt.close()
    gc.collect()
    return
def data_ret(varProj,phase,mapvar,datagroup):
        if phase == 'No Phase':
            f = tb.open_file(varProj,mode='a')
            Filt = f.root._f_get_child(datagroup)
            tp = f.get_node(Filt,mapvar)
            dsm = tp.read()
            dsm[np.isnan(dsm)]=0
            dsm[np.isnan(dsm)]=0
            dsm[np.isinf(dsm)]=0
            fname = path.join(mkdtemp(),'pmap.dat')
            y, x = dsm.shape[0], dsm.shape[1]
            dty = dsm.dtype
            dsx = np.memmap(fname,dtype=dty,mode='w+',shape=(y,x))
            dsx[:] = dsm[:]
            del dsm, y, x, dty, fname
            f.close()
        else:
            f = tb.open_file(varProj,mode='a')
            Filt = f.root._f_get_child(datagroup)
            tp = f.get_node(Filt,mapvar)
            ds = tp.read()
            ds[np.isnan(ds)]=0
            tm = f.get_node(f.root.Phase,phase)
            mask = tm.read()
            dsm = ds/mask
            del ds
            dsm[np.isnan(dsm)]=np.nan
            dsm[np.isinf(dsm)]=np.nan
            fname = path.join(mkdtemp(),'pmap.dat')
            y, x = dsm.shape[0], dsm.shape[1]
            dty = dsm.dtype
            dsx = np.memmap(fname,dtype=dty,mode='w+',shape=(y,x))
            dsx[:] = dsm[:]
            del dsm, mask, dty, y, x, fname
            f.close()
        gc.collect()
        return dsx
def data_ret2(varProj, dataset, phase, mapvar, datagroup):
    if phase == 'No Phase':
        f = tb.open_file(varProj,mode='a')
        Filt = f.root._f_get_child(datagroup)
        tp = f.get_node(Filt,mapvar)
        dsm = tp.read()
        dsm[np.isnan(dsm)]=0
        dsm[np.isnan(dsm)]=0
        dsm[np.isinf(dsm)]=0
        fname = path.join(mkdtemp(),'pmap.dat')
        y, x = dsm.shape[0], dsm.shape[1]
        dty = dsm.dtype
        dsx = np.memmap(fname,dtype=dty,mode='w+',shape=(y,x))
        dsx[:] = dsm[:]
        del dsm, dty, y, x, fname
        f.close()
    else:
        f = tb.open_file(varProj,mode='a')
        Filt = f.root._f_get_child(datagroup)
        tp = f.get_node(Filt,mapvar)
        ds = tp.read()
        ds[np.isnan(ds)]=0
        grp = f.root._f_get_child(dataset)
        grp2 = grp._f_get_child('PhaseMap')
        Phase = grp2._f_get_child('masks')
        tm = f.get_node(Phase,phase)
        mask = tm.read()
        dsm = ds/mask
        del ds
        dsm[np.isnan(dsm)]=np.nan
        dsm[np.isinf(dsm)]=np.nan
        fname = path.join(mkdtemp(),'pmap.dat')
        y, x = dsm.shape[0], dsm.shape[1]
        dty = dsm.dtype
        dsx = np.memmap(fname,dtype=dty,mode='w+',shape=(y,x))
        dsx[:] = dsm[:]
        del dsm, mask, dty, y, x, fname
        f.close()
    gc.collect()
    return dsx
def savefig_hist(Settings):
    figtitle = Settings['figtitle']
    filetitle = Settings['filetitle']
    samplenm = Settings['sample']
    filefmt = Settings['filefmt']
    filename = str(filetitle) + "." + str(filefmt)
    height = Settings['height']
    width = Settings['width']
    dpi = Settings['dpi']
    dataset = Settings['dataset']
    datagroup = Settings['datagroup']
    varProj = Settings['varProj']
    mapvar = Settings['mapvar']
    phase = Settings['phase']
    statck = Settings['options']
    expt = Settings['export']
    f = tb.open_file(varProj, mode='a')
    ells = f.get_node(f.root.parameters, 'ElementList').read()
    f.close()
    if statck == 0:
        if dataset == 'Phase':
            dsm, num = data_hist(varProj, mapvar, phase, datagroup)
        else:
            dsm, num = data_hist2(varProj, mapvar,phase,dataset, datagroup)
        plt.hold(False)
        fig = plt.figure(figsize=(width,height),dpi=dpi)
        ax = fig.add_subplot(111)
        if mapvar in ells:
            ax.hist(dsm,bins=100)
            if expt == 10:
                his, bed = np.histogram(dsm, bins=100)
                z = (bed[1]-bed[0])/2
                bin2 = [bed[i] + z for i in range(len(his))]
                from pandas import DataFrame
                datdic = {'bin_centers':bin2,'frequency':his}
                coltitles = ['bin_centers','frequency']
                df = DataFrame(datdic,columns=coltitles)
                fname = str(filetitle)+".csv"
                df.to_csv(fname, header=True, index=False)
            else:
                print "continue"
        else:
            ax.hist(dsm,bins=100,range=(0.0, 1.0))
            if expt == 10:
                his, bed = np.histogram(dsm, bins=100, range=(0.0, 1.0))
                z = (bed[1]-bed[0])/2
                bin2 = [bed[i] + z for i in range(len(his))]
                from pandas import DataFrame
                datdic = {'bin_centers':bin2,'frequency':his}
                coltitles = ['bin_centers','frequency']
                df = DataFrame(datdic,columns=coltitles)
                fname = str(filetitle)+".csv"
                df.to_csv(fname, header=True, index=False)
            else:
                print "continue"
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_ylabel("Frequency (N)")
        xmin, xmax = ax.get_xlim()
        if xmax == 1.0:
            ax.xaxis.set_ticks(np.arange(xmin, (xmax + 0.1), 0.1))
        else:
            print 'Not a ratio'
        ax.xaxis.set_minor_locator(AutoMinorLocator(5))
        ax.spines['top'].set_visible(False)
        ax.tick_params(labelsize=12)
        ax.set_title(figtitle)
        fig.tight_layout()
        fig.savefig(filename, dpi=dpi, format=filefmt)
        plt.close()
    if statck == 1:
        if dataset == 'Phase':
            dsm, num = data_hist(varProj, mapvar, phase, datagroup)
            annot = annot_ret(dsm, num, samplenm)
        else:
            dsm, num = data_hist2(varProj, mapvar,phase,dataset, datagroup)
            annot = annot_ret(dsm, num, samplenm)
        plt.hold(False)
        fig = plt.figure(figsize=(width,height),dpi=dpi)
        ax = fig.add_subplot(111)
        if mapvar in ells:
            ax.hist(dsm,bins=100)
            if expt == 10:
                his, bed = np.histogram(dsm, bins=100)
                z = (bed[1]-bed[0])/2
                bin2 = [bed[i] + z for i in range(len(his))]
                from pandas import DataFrame
                datdic = {'bin_centers':bin2,'frequency':his}
                coltitles = ['bin_centers','frequency']
                df = DataFrame(datdic,columns=coltitles)
                fname = str(filetitle)+".csv"
                df.to_csv(fname, header=True, index=False)
        else:
            ax.hist(dsm,bins=100,range=(0.0, 1.0))
            if expt == 10:
                his, bed = np.histogram(dsm, bins=100, range=(0.0, 1.0))
                z = (bed[1]-bed[0])/2
                bin2 = [bed[i] + z for i in range(len(his))]
                from pandas import DataFrame
                datdic = {'bin_centers':bin2,'frequency':his}
                coltitles = ['bin_centers','frequency']
                df = DataFrame(datdic,columns=coltitles)
                fname = str(filetitle)+".csv"
                df.to_csv(fname, header=True, index=False)
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_ylabel("Frequency (N)")
        xmin, xmax = ax.get_xlim()
        if xmax == 1.0:
            ax.xaxis.set_ticks(np.arange(xmin, (xmax + 0.1), 0.1))
        else:
            print 'Not a ratio'
        ax.xaxis.set_minor_locator(AutoMinorLocator(5))
        ax.axvline(np.nanmean(dsm),color='r',linestyle='dashed',linewidth=4)
        bbox_props = dict(boxstyle="square,pad=0.3",fc="bisque",ec="k",lw=0.5)
        ax.annotate(annot,xy=(0.05,0.95),xycoords='axes fraction',va="top",ha="left",bbox=bbox_props)
        ax.tick_params(labelsize=12)
        ax.set_title(figtitle)
        fig.tight_layout()
        fig.savefig(filename, dpi=dpi, format=filefmt)
        plt.close()
    gc.collect()
    return
def annot_ret(dsm, num,  samplenm):
    mean = round(np.nanmean(dsm),4)
    median = round(np.nanmedian(dsm),4)
    stdev = round(np.nanstd(dsm),4)
    #num = num
    num = np.count_nonzero(~np.isnan(dsm))
    annot = ("$" + str(samplenm) + "$\n$Mean = " + str(mean) + "$\n$Median = " + str(median) + "$\n$\sigma = " + str(stdev) + "$\n$N = " + str(num) +"$")
    return annot
def data_hist(varProj, mapvar, phase, datagroup):
    if phase == 'No Phase':
        f = tb.open_file(varProj,mode='a')
        Filt = f.root._f_get_child(datagroup)
        tp = f.get_node(Filt,mapvar)
        num = tp.attrs.pixels
        ds = tp.read()
        el_sh = tp.attrs.pixels
        ds.reshape(el_sh,1)
        ds[ds==0] = np.nan
        dsm = ds[np.isfinite(ds)]
        del ds
        fname = path.join(mkdtemp(),'pmap.dat')
        y= dsm.shape
        dty = dsm.dtype
        dsx = np.memmap(fname,dtype=dty,mode='w+',shape=y)
        dsx[:] = dsm[:]
        del dsm, dty, y, fname
        f.close()
    else:
        f = tb.open_file(varProj,mode='a')
        Filt = f.root._f_get_child(datagroup)
        tp = f.get_node(Filt,mapvar)
        num = tp.attrs.pixels
        ds = tp.read()
        ds[np.isnan(ds)]=0
        tm = f.get_node(f.root.Phase,phase)
        mask = tm.read()
        el_sh = tp.attrs.pixels
        dsm = ds/mask
        del ds
        dsm[np.isnan(dsm)]=np.nan
        dsm[np.isinf(dsm)]=np.nan
        dsm.reshape(el_sh,1)
        dsm = dsm[np.isfinite(dsm)]
        fname = path.join(mkdtemp(),'pmap.dat')
        y= dsm.shape
        dty = dsm.dtype
        dsx = np.memmap(fname,dtype=dty,mode='w+',shape=y)
        dsx[:] = dsm[:]
        del dsm, mask, dty, y, fname
        f.close()
    gc.collect()
    return dsx, num
def data_hist2(varProj, mapvar, phase, dataset,  datagroup):
    if phase == 'No Phase':
        f = tb.open_file(varProj,mode='a')
        Filt = f.root._f_get_child(datagroup)
        tp = f.get_node(Filt,mapvar)
        num = tp.attrs.pixels
        ds = tp.read()
        el_sh = tp.attrs.pixels
        ds.reshape(el_sh,1)
        ds[ds==0] = np.nan
        dsm = ds[np.isfinite(ds)]
        del ds
        fname = path.join(mkdtemp(),'pmap.dat')
        y= dsm.shape
        dty = dsm.dtype
        dsx = np.memmap(fname,dtype=dty,mode='w+',shape=y)
        dsx[:] = dsm[:]
        del dsm, dty, y, fname
        f.close()
    else:
        f = tb.open_file(varProj,mode='a')
        Filt = f.root._f_get_child(datagroup)
        tp = f.get_node(Filt,mapvar)
        num = tp.attrs.pixels
        el_sh = tp.attrs.pixels
        ds = tp.read()
        ds[np.isnan(ds)]=0
        grp = f.root._f_get_child(dataset)
        grp2 = grp._f_get_child('PhaseMap')
        Phase = grp2._f_get_child('masks')
        tm = f.get_node(Phase,phase)
        mask = tm.read()
        dsm = ds/mask
        del ds
        dsm[np.isnan(dsm)]=np.nan
        dsm[np.isinf(dsm)]=np.nan
        dsm.reshape(el_sh,1)
        dsm = dsm[np.isfinite(dsm)]
        fname = path.join(mkdtemp(),'pmap.dat')
        y= dsm.shape
        dty = dsm.dtype
        dsx = np.memmap(fname,dtype=dty,mode='w+',shape=y)
        dsx[:] = dsm[:]
        del dsm, mask, dty, y, fname
        f.close()
    gc.collect()
    return dsx, num
def savefig_pmap(Settings):
    figtitle = Settings['figtitle']
    filetitle = Settings['filetitle']
    filefmt = Settings['filefmt']
    filename = str(filetitle) + "." + str(filefmt)
    height = float(Settings['height'])
    width = float(Settings['width'])
    dpi = int(Settings['dpi'])
    varProj = Settings['varProj']
    mapvar = Settings['mapvar']
    dataset = Settings['dataset']

    f = tb.open_file(varProj,mode='a')
    tm = f.root._f_get_child(dataset)
    Grp = tm._f_get_child(mapvar)
    masks = Grp._f_get_child('masks')
    pxsz = f.get_node(f.root,'PixSize').read()
    PixSize = float(pxsz[0])
    pixun = pxsz[1]
    tmp = masks._v_children
    annot=[]
    names = []
    mskls = []
    phpix = []
    phmod = []
    for item in tmp.keys():
        if item == 'PhaseMap':
            print 'Not a phase'
        else:
            names.append(item)
            ds = f.get_node(masks,item).read()
            ds1 = ds * 1.0
            num = np.sum(ds)
            string = str(item) + ", "+str(num)+" pixels"
            phpix.append(int(num))
            annot.append(string)
            mskls.append(ds1)
    print mskls
    Total = np.sum(phpix)
    for i in xrange(0,len(mskls)):
        j = i+1
        ds = mskls[i]
        ds[ds==1.0]=j
        mskls[i]=ds
        t = phpix[i]
        mod = t/float(Total)
        mode = round(mod, 4)
        phmod.append(mode)
    print mskls
    phasemap = mskls[0]
    for i in xrange(1,len(mskls)):
        ds = mskls[i]
        phasemap = phasemap + ds
    print phasemap
    phasemap[phasemap==0]=np.nan
    f.close()
    names.append('PhaseMap')
    phpix.append(Total)
    phmod.append(1.0)

    dat = np.column_stack((names, phpix, phmod))
    np.savetxt('PhaseMap_Stats.csv', dat, delimiter="\t", fmt=('%s','%s','%s'), header='Phase\tPixels(N)\tMode', comments='')

    mini = np.nanmin(phasemap)
    maxi = np.nanmax(phasemap)

    my_cmap = cm.get_cmap('gnuplot',maxi-mini+1)
    my_cmap.set_under('k', alpha=0)
    my_cmap.set_over('k', alpha=0)

    if width <= 10.0:
        sz = "3%"
    else:
        sz = 0.3
    print sz
    plt.hold(False)
    fig = plt.figure(figsize=(width,height),dpi=dpi)
    axes = fig.add_subplot(111)
    im = axes.imshow(phasemap,cmap=my_cmap,interpolation='nearest',vmin = mini-0.5,vmax = maxi+0.5)
    axes.set_title(figtitle)
    divider = make_axes_locatable(axes)
    cax = divider.append_axes("right", size=sz, pad=0.1)
    cb = fig.colorbar(im,ticks=np.arange(mini,maxi+1),cax=cax)
    cb.ax.set_yticklabels(annot)
    cb.ax.tick_params(labelsize=10)
    fig.tight_layout()

    xmin,xmax = axes.get_xlim()
    xticks = axes.get_xticks()
    Length = len(xticks)
    xlabels = ['Some']*len(xticks)
    xlabels[0] = ''
    xlabels[Length-1]=''
    for i in xrange(1,Length-1):
        val = xticks[i]
        if pixun == 'um':
            val = int((val*PixSize)/1000)
        elif pixun == 'nm':
            val = int((val*PixSize)/1000000000)
        elif pixun == 'mm':
            val = int(val*PixSize)
        print val
        string = str(val) + "mm"
        xlabels[i]=string
    print xlabels
    fig.canvas.draw()
    axes.yaxis.set_ticks_position('left')
    axes.xaxis.set_ticks_position('bottom')
    axes.set_xticklabels(xlabels)
    axes.set_yticklabels([])
    fig.savefig(filename, dpi=dpi, format=filefmt)
    string = 'Map Saved'
    plt.close()
    gc.collect()
    return

