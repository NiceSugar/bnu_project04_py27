# coding=utf-8
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import gaussian_kde as kde
import matplotlib as mpl


def reverse_colourmap(cmap, name = 'my_cmap_r'):
    """
    In:
    cmap, name
    Out:
    my_cmap_r

    Explanation:
    t[0] goes from 0 to 1
    row i:   x  y0  y1 -> t[0] t[1] t[2]
                   /
                  /
    row i+1: x  y0  y1 -> t[n] t[1] t[2]

    so the inverse should do the same:
    row i+1: x  y1  y0 -> 1-t[0] t[2] t[1]
                   /
                  /
    row i:   x  y1  y0 -> 1-t[n] t[2] t[1]
    """
    reverse = []
    k = []

    for key in cmap._segmentdata:
        k.append(key)
        channel = cmap._segmentdata[key]
        data = []

        for t in channel:
            data.append((1-t[0],t[2],t[1]))
        reverse.append(sorted(data))

    LinearL = dict(zip(k,reverse))
    my_cmap_r = mpl.colors.LinearSegmentedColormap(name, LinearL)
    return my_cmap_r


def makeColours(vals,cmap,reverse=0):
    norm = []
    for i in vals:
        norm.append((i-np.min(vals))/(np.max(vals)-np.min(vals)))
    colors = []
    cmap = plt.get_cmap(cmap)
    if reverse:
        cmap = reverse_colourmap(cmap)
    else:
        cmap = cmap

    for i in norm:
        colors.append(cmap(i))
    return colors




def plot_scatter(val1,val2,cmap='RdYlBu',reverse=1,s=1.,title = ''):

    kde_val = np.array([val1,val2])
    print('doing kernel density estimation... ')
    densObj = kde(kde_val)
    # print(densObj)
    dens_vals = densObj.evaluate(kde_val)

    colors = makeColours(dens_vals,cmap,reverse=reverse)
    # print(colors)
    print('ploting...')
    # fig = plt.figure(figsize=(5,2))

    # set background color
    # ax = plt.gca()
    # ax.set_facecolor('black')
    plt.figure()
    if reverse:
        # plt.title(cmap+'_reverse')
        plt.title(title)
    else:
        plt.title(title)

    plt.scatter(val1,val2,c=colors,s=s)
    # plt.xlim((0.17, 0.30))
    # plt.ylim((0.11, 0.30))
    print('showing...')
    # plt.show()