# coding=utf-8

import os
import numpy as np
import time
from matplotlib import pyplot as plt
import clip
from multiprocessing import Process
import multiprocessing as mp
import psutil
import threading
from scipy.interpolate import InterpolatedUnivariateSpline
from scipy import interpolate
# from numba import jit



def interp_1d(val):
    # 1、插缺失值
    x = []
    val_new = []
    for i in range(len(val)):
        if val[i] >= 100:
            index = i
            x = np.append(x,index)
            val_new = np.append(val_new,val[i])

    interp = interpolate.interp1d(x, val_new, kind='nearest', fill_value="extrapolate")

    xi = range(len(val))
    yi = interp(xi)


    # 2、利用三倍sigma，去除离群值
    # print(len(yi))
    val_mean = np.mean(yi)
    sigma = np.std(yi)
    n = 3
    yi[(val_mean - n * sigma) > yi] = -999999
    yi[(val_mean + n * sigma) < yi] = 999999
    # bottom = val_mean - n * sigma
    # top = val_mean + n * sigma
    # plt.scatter(range(len(yi)),yi)
    # print(len(yi),123)
    # plt.scatter(range(len(yi)),yi)
    # plt.plot(yi)
    # plt.show()
    # print(len(yi))

    # 3、插离群值
    xii = []
    val_new_ii = []

    for i in range(len(yi)):
        if -999999 < yi[i] < 999999:
            index = i
            xii = np.append(xii, index)
            val_new_ii = np.append(val_new_ii, yi[i])

    interp_1 = interpolate.interp1d(xii, val_new_ii, kind='nearest', fill_value="extrapolate")

    xiii = range(len(val))
    yiii = interp_1(xiii)


    # for i in range(len(yi)):
    #     if yi[i] == -999999:
    #         val_new_ii = np.append(val_new_ii, bottom)
    #     elif yi[i] == 999999:
    #         val_new_ii = np.append(val_new_ii, top)
    #     else:
    #         val_new_ii = np.append(val_new_ii, yi[i])

    return yiii



def interp_1d_3_sigma(val):
    # 1、插缺失值
    x = []
    val_new = []
    for i in range(len(val)):
        # print(val[i])
        if not np.isnan(val[i]):
            index = i
            x = np.append(x,index)
            val_new = np.append(val_new,val[i])

    interp = interpolate.interp1d(x, val_new, kind='nearest', fill_value="extrapolate")

    xi = range(len(val))
    yi = interp(xi)


    # 2、利用三倍sigma，去除离群值
    # print(len(yi))
    val_mean = np.mean(yi)
    sigma = np.std(yi)
    n = 3
    yi[(val_mean - n * sigma) > yi] = -999999
    yi[(val_mean + n * sigma) < yi] = 999999

    # 3、插离群值
    xii = []
    val_new_ii = []

    for i in range(len(yi)):
        if -9999 < yi[i] < 9999 and not np.isnan(yi[i]):
            index = i
            xii = np.append(xii, index)
            val_new_ii = np.append(val_new_ii, yi[i])

    interp_1 = interpolate.interp1d(xii, val_new_ii, kind='nearest', fill_value="extrapolate")

    xiii = range(len(val))
    yiii = interp_1(xiii)


    return yiii