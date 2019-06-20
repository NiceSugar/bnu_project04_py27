# coding=utf-8

import os
this_root = os.getcwd()+'\\'
import numpy as np
import time
from matplotlib import pyplot as plt
from multiprocessing import Process
import multiprocessing as mp
import psutil
import numba as nb
from numba import float64

# @nb.jit()
def cal_VSWI_kernel(arr_NDVI,arr_LST):
    # NDVI/LST
    vswi = arr_NDVI/arr_LST
    return vswi


def mk_dir(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)


def loop_VSWI(NDVI,LST,save_folder,save_name,func):
    NDVI_npz = np.load(NDVI)
    LST_npz = np.load(LST)
    lst_scale_factor = 0.02
    ndvi_scale_factor = 0.0001
    mk_dir(save_folder)

    # save_name = npz_file.split('\\')[-1]
    save_path = save_folder+'\\'+save_name
    start = time.time()
    # npz = np.load(npz_file)

    normalized_vals_dic = {}

    npy_flag = 0
    for npy in NDVI_npz:
        # print(npy)
        npy_flag += 1.
        if npy_flag % 1000 == 0:
            print save_name,npy_flag/len(NDVI_npz)*100,'%','%02f'%(time.time()-start)
        try:
            vals_NDVI = NDVI_npz[npy] * ndvi_scale_factor
            vals_LST = LST_npz[npy] * lst_scale_factor
        except:
            vals_NDVI = []
            vals_LST = []

        try:
            if len(vals_NDVI) > 1 and len(vals_LST) > 1:
                normalized_vals_dic[npy] = func(vals_NDVI,vals_LST)
                # plt.figure()
                # plt.plot(vals_NDVI)
                # plt.title('ndvi')
                # plt.figure()
                # plt.plot(vals_LST)
                # plt.title('lst')
                # plt.figure()
                # plt.plot(func(vals_NDVI,vals_LST))
                # plt.title('vswi')
                # plt.figure()
                # plt.scatter(vals_NDVI,vals_LST)
                # plt.show()
            else:
                normalized_vals_dic[npy] = []

        except:
            normalized_vals_dic[npy] = []
    print('saving '+save_path)
    np.savez(save_path,**normalized_vals_dic)
    print 'save '+save_path+' success\ntime:','%02f'%(time.time()-start)



def main():
    data_root = this_root+'project04_monthly_data\\'
    save_folder = this_root + 'monthly_data_npz_VSWI\\'

    ndvi_dir = data_root+'monthly_data_npz_ndvi\\'
    lst_dir = data_root+'monthly_data_npz_lst\\'
    flist = os.listdir(ndvi_dir)
    # print(flist)
    pool = mp.Pool()
    for f in flist:
        print(f)
        # exit()
        NDVI_npz = ndvi_dir+f
        LST_npz = lst_dir+f
        # loop_VSWI(NDVI_npz,LST_npz,save_folder,f,cal_VSWI_kernel)
        # NDVI_npz, LST_npz, save_folder, save_name, func

        pool.apply_async(func=loop_VSWI, args=(NDVI_npz,LST_npz,save_folder,f,cal_VSWI_kernel,))

    pool.close()
    pool.join()

if __name__ == '__main__':
    main()