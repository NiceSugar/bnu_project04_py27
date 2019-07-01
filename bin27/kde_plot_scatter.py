# coding=utf-8
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import gaussian_kde as kde
import matplotlib as mpl
import math


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

def linefit(x, y):
    '''
    最小二乘法拟合直线
    :param x:
    :param y:
    :return:
    '''
    N = float(len(x))
    sx, sy, sxx, syy, sxy = 0, 0, 0, 0, 0
    for i in range(0, int(N)):
        sx += x[i]
        sy += y[i]
        sxx += x[i] * x[i]
        syy += y[i] * y[i]
        sxy += x[i] * y[i]
    a = (sy * sx / N - sxy) / (sx * sx / N - sxx)
    b = (sy - a * sx) / N
    r = abs(sy * sx / N - sxy) / math.sqrt((sxx - sx * sx / N) * (syy - sy * sy / N))
    return a, b, r



def plot_fit_line( a, b, r, X, Y, title=''):
    '''
    画拟合直线 y=ax+b
    画散点图 X,Y
    :param a:
    :param b:
    :param X:
    :param Y:
    :param i:
    :param title:
    :return:
    '''
    x = np.linspace(min(X), max(X), 10)
    y = a * x + b
    #
    # plt.subplot(2,2,i)
    # plt.scatter(X,Y,marker='o',s=5,c = 'grey')
    # plt.plot(X, Y)
    plt.plot(x, y, linestyle='dashed', c='black', linewidth=2, alpha=0.7)
    plt.title(title)



def plot_scatter(val1,val2,cmap='Spectral',reverse=1,s=1.):
    plt.figure(figsize=(6,6))
    x = [-1e10,1e10]
    y = [-1e10,1e10]
    plt.plot(x,y,c='r')

    max_x = np.max(val1)
    max_y = np.max(val2)
    maxi = max([max_x,max_y])

    min_x = np.min(val1)
    min_y = np.min(val2)
    mini = min([min_x,min_y])


    length = len(val1)
    print('origin len(val):%s'%length)
    if length > 15000:
        n = len(val1)/15000
    else:
        n = 1
    # print(n)
    n = int(n)
    val1 = val1[::n]
    val2 = val2[::n]
    print('KDE len:%s'%len(val1))
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

    if reverse:
        plt.title(cmap+'_reverse')
    else:
        plt.title(cmap)

    plt.scatter(val1,val2,c=colors,s=s)
    plt.xlim(mini, maxi)
    plt.ylim(mini, maxi)
    # plt.xlim((0.17, 0.30))
    # plt.ylim((0.11, 0.30))
    a, b, r = linefit(val1,val2)
    plot_fit_line(a,b,r,val1,val2)
    print('a:%s,b:%s,r:%s'%(a,b,r))
    # print('showing...')
    # plt.show()