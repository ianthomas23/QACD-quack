# Polynomials are in increasing order of exponent starting at zero.
correction_models = {
    'general': {
        'Na' : ('poly', (0.0, 4.45, 0.2859)),
        'Mg' : ('poly', (0.0, 4.2108, 0.1399, -203.08, 1086.3)),
        'Al' : ('poly', (0.0, 4.3819, -41.598, 380.13, -731.79)),
        'Si' : ('poly', (0.0, 5.8851, -58.159, -555.07, 26657, -256525, 765507)),
        'K'  : ('poly', (0.0, 3.3929, 15.967, 261.31, -7425.6, 49467)),
        'Ca' : ('poly', (0.0, 2.8423, 60.484, -1050.2, 7699.1)),
        'Ti' : ('poly', (0.0, 4.723, 1.8096, 23.201)),
        'Cr' : ('poly', (0.0, 6.742, -93.156, 2836.7, -35741, 179471)),
        'Mn' : ('poly', (0.0, 6.7417, 33.599, -939.34, 8222.2)),
        'Fe' : ('poly', (0.0, 8.3325, -41.372, 2007.8, -38873, 248454)),
        'Ni' : ('poly', (0.0, 10.438, 6.8542)),
        'MgN': ('poly', (0.0, 1.3724, -0.1887, -2.0433, 4.0434, -3.0574, 0.8726)),
        'CrN': ('poly', (0.0, 0.8829, -1.1073, 5.6513, -11.767, 11.014, -3.6742)),
        'AnK': ('poly', (0.0, 1.1542, -4.8113, 11.49, -10.631, 3.5928, 0.2041)),
        'An' : ('poly', (0.0, 0.8293, -1.2037, -2.5782, 14.405, -17.165, 6.7126)),
        'Or' : ('poly', (0.0, 0.6009, -0.742, 5.3859, -12.558, 13.372, -5.0543)),
        'Py' : ('poly', (0.0, 1.7323, -2.9634, 8.42, -16.098, 15.745, -5.8352)),
        'Gro': ('poly', (0.0, 0.6034, 0.6004, -2.5324, 6.8051, -7.2473, 2.7709)),
        'Alm': ('poly', (0.0, 1.4812, -2.7985, 7.3318, -8.2609, 3.2458)),
        'Sp' : ('poly', (0.0, 0.9365, 0.6445, -2.98, 4.3223, -1.9233)),
    },
    'feldspar': {
        'Na' : ('poly', (0.0, 4.6477, -1.1503)),
        'Mg' : ('poly', (0.0, 4.2108, 0.1399, -203.08, 1086.3)),
        'Al' : ('poly', (0.0, 3.2991, -7.601, 92.007)),
        'Si' : ('poly', (0.0, -0.2251, 135.31, -1607.6, 5960.9)),
        'K'  : ('poly', (0.0, 3.6144, 2.8353, 363.56, -1106.7)),
        'Ca' : ('poly', (0.0, 3.3859, 19.947, -464.09, 5316.4)),
        'Ti' : ('poly', (0.0, 4.723, 1.8096, 23.201)),
        'Cr' : ('poly', (0.0, 6.742, -93.156, 2836.7, -35741, 179471)),
        'Mn' : ('poly', (0.0, 6.7417, 33.599, -939.34, 8222.2)),
        'Fe' : ('poly', (0.0, 8.6479, 14.517)),
        'Ni' : ('poly', (0.0, 10.438, 6.8542)),
        'AnK': ('poly', (0.0, 1.1542, -4.8113, 11.49, -10.631, 3.5928, 0.2041)),
        'An' : ('poly', (0.0, 0.8293, -1.2037, -2.5782, 14.405, -17.165, 6.7126)),
        'Or' : ('poly', (0.0, 0.6009, -0.742, 5.3859, -12.558, 13.372, -5.0543)),
    },
    'garnet': {
        'Na' : ('poly', (0.0, 4.45, 0.2859)),
        'Mg' : ('poly', (0.0, 4.2407, -11.265, -247.81, 1581.9)),
        'Al' : ('poly', (0.0, 4.3647, -22.46, -89.451, 1200.4)),
        'Si' : ('poly', (0.0, 4.7799, -22.662, -117.34, 1652.6)),
        'K'  : ('poly', (0.0, 3.3929, 15.967, 261.31, -7425.6, 49467)),
        'Ca' : ('poly', (0.0, 3.4792, -13.136, 1262, -19788, 107983)),
        'Ti' : ('poly', (0.0, 3.3892, 42.224)),
        'Cr' : ('poly', (0.0, 6.8046, -32.421, 505.85)),
        'Mn' : ('poly', (0.0, 5.7545, 158.5, -5354.1, 66170, -251058)),
        'Fe' : ('poly', (0.0, 7.8598, 60.692, -2880.6, 38070, -130149)),
        'Ni' : ('poly', (0.0, 10.438, 6.8542)),
        'MgN': ('poly', (0.0, 1.6313, -3.477, 9.5905, -13.491, 8.7033, -1.9552)),
        'CrN': ('poly', (0.0, 0.8829, -1.1073, 5.6513, -11.767, 11.014, -3.6742)),
        'Py' : ('poly', (0.0, 1.7323, -2.9634, 8.42, -16.098, 15.745, -5.8352)),
        'Gro': ('poly', (0.0, 0.6034, 0.6004, -2.5324, 6.8051, -7.2473, 2.7709)),
        'Alm': ('poly', (0.0, 1.4812, -2.7985, 7.3318, -8.2609, 3.2458)),
        'Sp' : ('poly', (0.0, 0.9365, 0.6445, -2.98, 4.3223, -1.9233)),
    },
    'olivine': {
        'Na' : ('poly', (0.0, 4.45, 0.2859)),
        'Mg' : ('poly', (0.0, 4.5875, 2.6004, -322.73, 1572.1)),
        'Al' : ('poly', (0.0, 4.3819, -41.598, 380.13, -731.79)),
        'Si' : ('poly', (0.0, 5.3108, -52.734, 323.74)),
        'K'  : ('poly', (0.0, 3.3929, 15.967, 261.31, -7425.6, 49467)),
        'Ca' : ('poly', (0.0, 3.5413, -13.119, 439.41)),
        'Ti' : ('poly', (0.0, 4.723, 1.8096, 23.201)),
        'Cr' : ('poly', (0.0, 6.742, -93.156, 2836.7, -35741, 179471)),
        'Mn' : ('poly', (0.0, 7.7678, -45.708, 587.19)),
        'Fe' : ('poly', (0.0, 7.0266, -49.288, 3091.7, -52548, 297778)),
        'Ni' : ('poly', (0.0, 10.438, 6.8542)),
        'MgN': ('poly', (0.0, 1.8607, -6.7247, 31.199, -64.308, 58.122, -19.161)),
        'CrN': ('poly', (0.0, 0.8829, -1.1073, 5.6513, -11.767, 11.014, -3.6742)),
    },
    'oxide': {
        'Na' : ('poly', (0.0, 4.45, 0.2859)),
        'Mg' : ('poly', (0.0, 6.1159, -86.3665, 581.918, -909.617)),
        'Al' : ('poly', (0.0, 5.131, -35.588, 467.34, -5511.4, 33859, -66277)),
        'Si' : ('poly', (0.0, 5.8851, -58.159, -555.07, 26657, -256525, 765507)),
        'K'  : ('poly', (0.0, 3.3929, 15.967, 261.31, -7425.6, 49467)),
        'Ca' : ('poly', (0.0, 2.8423, 60.484, -1050.2, 7699.1)),
        'Ti' : ('poly', (0.0, 2.8327, 200.3958, -7694.66, 134149.7, -1090215, 3492036)),
        'Cr' : ('poly', (0.0, 3.1701, 123.6, -2054, 13168)),
        'Mn' : ('poly', (0.0, 10.506, -122.96, 1073.2)),
        'Fe' : ('poly', (0.0, 8.5879, -62.077, 3934.006, -69706.8, 202476.6, 1813126)),
        'Ni' : ('poly', (0.0, 10.438, 6.8542)),
        'MgN': ('poly', (0.0, 1.5254, -1.0576, 0.5312)),
        'CrN': ('poly', (0.0, 0.8447, -0.2757, 0.431)),
    },
    'pyroxene': {
        'Na' : ('poly', (0.0, 6.5503, -180.17, 3194.9)),
        'Mg' : ('poly', (0.0, 4.3981, -9.9551, -211.05, 1349.5)),
        'Al' : ('poly', (0.0, 4.6133, -60.47, 612.83, -1564.1)),
        'Si' : ('poly', (0.0, 5.6179, -38.924, 11.523, 1288.3)),
        'K'  : ('poly', (0.0, 3.3929, 15.967, 261.31, -7425.6, 49467)),
        'Ca' : ('poly', (0.0, 3.8574, -6.5147, 362.51)),
        'Ti' : ('poly', (0.0, 4.6436, -2.6209, 290.33)),
        'Cr' : ('poly', (0.0, 6.1369, -40.793, 640.31)),
        'Mn' : ('poly', (0.0, 8.3296, -62.804, 698.82)),
        'Fe' : ('poly', (0.0, 8.8463, -43.239, 214.04, 3513.9)),
        'Ni' : ('poly', (0.0, 10.438, 6.8542)),
        'MgN': ('poly', (0.0, 1.5411, -0.3916, -3.8151, 9.1045, -7.6833, 2.2414)),
        'CrN': ('poly', (0.0, 0.9069, -0.4597, 0.5529)),
    }
}