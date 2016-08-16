#---------------------------------------------------------------------------------------
#module of functions for correcting elemental intensities to normalised and 
#Hfactor-corrected data
#---------------------------------------------------------------------------------------
from __future__ import division
import os
import sys
import tables as tb
import numpy as np
import math
import gc
import dask.array as da
#Build the dictionary of atomic number, atomic weight, and density for elements Z=1 to 92
filters = tb.Filters(complevel=5, complib='blosc')
def periodic(ells):
    #A function which retrieves the atomic number (Z), weight (A) and density (p) for the elements of interest
    zap_dic = {"H":{"Z":1,"A":1.0079,"p":"-"},"He":{"Z":2,"A":4.003,"p":"-"},
               "Li":{"Z":3,"A":6.941,"p":0.534},"Be":{"Z":4,"A":9.012,"p":1.848},
               "B":{"Z":5,"A":10.81,"p":2.5},"C":{"Z":6,"A":12.01,"p":2.34},
               "N":{"Z":7,"A":14.01,"p":"-"},"O":{"Z":8,"A":15.999,"p":"-"},
               "F":{"Z":9,"A":19,"p":"-"},"Ne":{"Z":10,"A":20.18,"p":"-"},
               "Na":{"Z":11,"A":22.98977,"p":0.97},"Mg":{"Z":12,"A":24.305,"p":1.74},
               "Al":{"Z":13,"A":26.98154,"p":2.7},"Si":{"Z":14,"A":28.0855,"p":2.34},
               "P":{"Z":15,"A":30.97376,"p":2.2},"S":{"Z":16,"A":32.06,"p":2.07},
               "Cl":{"Z":17,"A":35.45,"p":"-"},"Ar":{"Z":18,"A":39.95,"p":"-"},
               "K":{"Z":19,"A":39.0983,"p":0.86},"Ca":{"Z":20,"A":40.08,"p":1.54},
               "Sc":{"Z":21,"A":44.9559,"p":2.99},"Ti":{"Z":22,"A":47.88,"p":4.5},
               "V":{"Z":23,"A":50.9415,"p":6.1},"Cr":{"Z":24,"A":51.996,"p":7.1},
               "Mn":{"Z":25,"A":54.938,"p":7.4},"Fe":{"Z":26,"A":55.847,"p":7.87},
               "Co":{"Z":27,"A":58.9332,"p":8.9},"Ni":{"Z":28,"A":58.69,"p":8.9},
               "Cu":{"Z":29,"A":63.546,"p":8.96},"Zn":{"Z":30,"A":65.38,"p":7.14},
               "Ga":{"Z":31,"A":69.72,"p":5.91},"Ge":{"Z":32,"A":72.59,"p":5.32},
               "As":{"Z":33,"A":74.92,"p":5.72},"Se":{"Z":34,"A":78.96,"p":4.79},
               "Br":{"Z":35,"A":79.9,"p":3.12},"Kr":{"Z":36,"A":83.8,"p":"-"},
               "Rb":{"Z":37,"A":85.4678,"p":1.53},"Sr":{"Z":38,"A":87.62,"p":2.6},
               "Y":{"Z":39,"A":88.91,"p":4.472},"Zr":{"Z":40,"A":91.22,"p":6.49},
               "Nb":{"Z":41,"A":92.91,"p":8.6},"Mo":{"Z":42,"A":95.94,"p":10.2},
               "Tc":{"Z":43,"A":98.91,"p":11.46},"Ru":{"Z":44,"A":101.1,"p":12.2},
               "Rh":{"Z":45,"A":102.9,"p":12.4},"Pd":{"Z":46,"A":106.4,"p":12},
               "Ag":{"Z":47,"A":107.9,"p":10.5},"Cd":{"Z":48,"A":112.4,"p":8.64},
               "In":{"Z":49,"A":114.8,"p":7.3},"Sn":{"Z":50,"A":118.7,"p":7.3},
               "Sb":{"Z":51,"A":121.8,"p":6.68},"Te":{"Z":52,"A":127.6,"p":6.24},
               "I":{"Z":53,"A":126.9,"p":4.94},"Xe":{"Z":54,"A":131.3,"p":"-"},
               "Cs":{"Z":55,"A":132.9,"p":1.87},"Ba":{"Z":56,"A":137.3,"p":3.5},
               "La":{"Z":57,"A":138.9,"p":6.189},"Ce":{"Z":58,"A":140.1,"p":6.75},
               "Pr":{"Z":59,"A":140.9,"p":6.769},"Nd":{"Z":60,"A":144.2,"p":7},
               "Pm":{"Z":61,"A":145,"p":"-"},"Sm":{"Z":62,"A":150.4,"p":7.49},
               "Eu":{"Z":63,"A":152,"p":5.245},"Gd":{"Z":64,"A":157.3,"p":7.86},
               "Tb":{"Z":65,"A":158.9,"p":8.25},"Dy":{"Z":66,"A":160.5,"p":8.55},
               "Ho":{"Z":67,"A":164.9,"p":8.79},"Er":{"Z":68,"A":167.3,"p":9.15},
               "Tm":{"Z":69,"A":168.9,"p":9.31},"Yb":{"Z":70,"A":173,"p":6.959},
               "Lu":{"Z":71,"A":175,"p":9.849},"Hf":{"Z":72,"A":178.5,"p":13.1},
               "Ta":{"Z":73,"A":180.9,"p":16.6},"W":{"Z":74,"A":183.9,"p":19.3},
               "Re":{"Z":75,"A":186.2,"p":21},"Os":{"Z":76,"A":190.2,"p":22.5},
               "Ir":{"Z":77,"A":192.2,"p":22.4},"Pt":{"Z":78,"A":195.1,"p":21.45},
               "Au":{"Z":79,"A":197,"p":19.3},"Hg":{"Z":80,"A":200.6,"p":13.55},
               "Tl":{"Z":81,"A":204.4,"p":11.85},"Pb":{"Z":82,"A":207.25,"p":11.34},
               "Bi":{"Z":83,"A":209,"p":9.8},"Po":{"Z":84,"A":210,"p":9.24},
               "At":{"Z":85,"A":210,"p":"-"},"Rn":{"Z":86,"A":222,"p":"-"},
               "Fr":{"Z":87,"A":223,"p":"-"},"Ra":{"Z":88,"A":226,"p":5},
               "Ac":{"Z":89,"A":227,"p":"-"},"Th":{"Z":90,"A":232,"p":11.5},
               "Pa":{"Z":91,"A":231,"p":15.4},"U":{"Z":92,"A":238,"p":19.05}
               }
    el_z = {}
    el_a = {}
    for item in ells:
        tmp = zap_dic[item]
        el_z[item] = tmp["Z"]
        el_a[item] = tmp["A"]
        del tmp
    print el_z, el_a
    return el_z, el_a

def elratio(varProj): #This function normalises the element maps to the calculated total
    f = tb.open_file(varProj,mode='a')
    ells = f.get_node(f.root.parameters,"ElementList").read() #retrieve the element list
    stack = f.get_node(f.root,"Stack2")#.read() #retrieve the stack of flattened vectors for all elements
    tmpfile = tb.open_file('temp.h5', mode='a')
    atom = tb.Atom.from_dtype(stack.dtype)
    shaper = (stack.shape[0],)
    total = f.createCArray(tmpfile.root,'Total',atom,shaper,filters=filters)
    total[:] = np.sum(stack,axis=1) #add together every element for each pixel
    stackR = f.createCArray(f.root,"NormStack",atom,stack.shape,filters=filters)
    stackR.attrs.Size=(stack.shape)
    st1 = f.get_node(f.root,"Stack2")
    stackR.attrs.Shape=(st1.attrs.Size)
    del st1#,d
    stackR.attrs.Cols=(ells)
    for i in xrange(0,len(ells)):
        stackR[:,i] = stack[:,i] / total
    print 'Elements Normalised'
    del total, stack
    f.close()
    gc.collect()
    string = "Normalised"
    return string
def h_factor(varProj): #This function produces the h-factor from Philibert (1967) for correcting normalised data
    f = tb.open_file(varProj,mode='a')
    ells = f.get_node(f.root.parameters,"ElementList").read() #retrieve the element list
    el_z, el_a = periodic(ells)
    stack = f.get_node(f.root,"NormStack")
    stz = np.zeros((stack.shape[0],))
    sta = np.zeros((stack.shape[0],))
    for i in xrange(0,len(ells)):
        var = ells[i]
        print var
        stz = stz[:,] + (stack[:,i] * (el_z[var]))
        sta = sta[:,] + (stack[:,i] * (el_a[var]))
    hfac = 1.2 * (sta / (stz**2))    
    atom = tb.Atom.from_dtype(hfac.dtype)
    factor = f.createCArray(f.root,"HFactor",atom,hfac.shape,filters=filters)
    factor.attrs.Size=(hfac.shape)
    factor[:] = hfac
    del hfac
    f.close()
    gc.collect()
    string = "H-factor calculated"
    return string

    
    
    

