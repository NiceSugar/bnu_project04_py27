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
def cal_NDDI_kernel(NDVI,NDWI):
    # NDVI/LST
    NDDI = (NDVI-NDWI)/(NDVI+NDWI)
    # if b2+(b6-b7) == 0:
    #     print(b2,b6,b7)
    return NDDI

def mk_dir(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)



def loop_NDDI(NDVI,NDWI,save_folder,save_name,func):
    # import tool
    NDVI_npz = np.load(NDVI)
    NDWI_npz = np.load(NDWI)
    # lst_scale_factor = 0.02
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
            vals_NDVI = NDVI_npz[npy]*ndvi_scale_factor
            vals_NDWI = NDWI_npz[npy]
        except:
            vals_NDVI = []
            vals_NDWI = []

        try:
            if len(vals_NDVI) > 1 and len(vals_NDWI) > 1:

                normalized_vals_dic[npy] = func(vals_NDVI,vals_NDWI)
                # plt.figure()
                plt.plot(vals_NDVI)
                plt.title('ndvi')
                plt.figure()
                plt.plot(vals_NDWI)
                plt.title('NDWI')
                plt.figure()
                plt.plot(func(vals_NDVI,vals_NDWI))
                plt.title('NDDI')
                # plt.figure()
                # plt.scatter(vals_NDVI,vals_LST)
                plt.show()
            else:
                normalized_vals_dic[npy] = []

        except:
            normalized_vals_dic[npy] = []
    print('saving '+save_path)
    np.savez(save_path,**normalized_vals_dic)
    print 'save '+save_path+' success\ntime:','%02f'%(time.time()-start)


def main():
    # data_root ='D:\\OneDrive - business-cn(1)\\project04_monthly_data\\'
    save_folder = this_root + 'monthly_data_npz_NDDI\\'

    ndvi_dir = 'D:\\OneDrive - business-cn(1)\\project04_data\\project04_monthly_data\\monthly_data_npz_ndvi\\'
    ndwi_dir = 'D:\\OneDrive - business-cn(1)\\project04_data\\drought_indices\\monthly_data_npz_NDWI\\'
    flist = os.listdir(ndvi_dir)
    # print(flist)
    pool = mp.Pool(processes=1)
    for f in flist:
        print(f)
        # exit()
        NDVI = ndvi_dir+f
        NDWI = ndwi_dir+f
        save_name = f
        func = cal_NDDI_kernel
        loop_NDDI(NDVI,NDWI,save_folder,save_name,func)
        # NDVI_npz, LST_npz, save_folder, save_name, func

        # pool.apply_async(func=loop_VSWI, args=(NDVI,NDWI,save_folder,save_name,func,))

    pool.close()
    pool.join()

if __name__ == '__main__':
    main()