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
def cal_CWSI_kernel(arr_ET,arr_PET):
    # NDVI/LST
    CWSI = 1-(arr_ET/arr_PET)
    return CWSI


def mk_dir(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)



def loop_CWSI(ET,PET,save_folder,save_name,func):
    # import tool
    ET_npz = np.load(ET)
    PET_npz = np.load(PET)
    # lst_scale_factor = 0.02
    # ndvi_scale_factor = 0.0001
    mk_dir(save_folder)

    # save_name = npz_file.split('\\')[-1]
    save_path = save_folder+'\\'+save_name
    start = time.time()
    # npz = np.load(npz_file)

    normalized_vals_dic = {}

    npy_flag = 0
    for npy in ET_npz:
        # print(npy)
        npy_flag += 1.
        if npy_flag % 1000 == 0:
            print save_name,npy_flag/len(ET_npz)*100,'%','%02f'%(time.time()-start)
        try:
            vals_ET = ET_npz[npy]
            vals_PET = PET_npz[npy]
        except:
            vals_ET = []
            vals_PET = []

        try:
            if len(vals_ET) > 1 and len(vals_PET) > 1:
                normalized_vals_dic[npy] = func(vals_ET,vals_PET)
                # plt.figure()
                # plt.plot(vals_ET)
                # plt.title('vals_ET')
                # plt.figure()
                # plt.plot(vals_PET)
                # plt.title('vals_PET')
                # plt.figure()
                # plt.plot(func(vals_ET,vals_PET))
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
    data_root ='D:\\OneDrive - business-cn(1)\\project04_data\\project04_monthly_data\\'
    save_folder = this_root + 'monthly_data_npz_cwsi\\'

    et_dir = data_root+'monthly_data_npz_et\\'
    pet_dir = data_root+'monthly_data_npz_pet\\'
    flist = os.listdir(et_dir)
    # print(flist)
    pool = mp.Pool(processes=1)
    for f in flist:
        print(f)
        # exit()
        ET_npz = et_dir+f
        PET_npz = pet_dir+f
        # loop_VSWI(NDVI_npz,LST_npz,save_folder,f,cal_VSWI_kernel)
        # NDVI_npz, LST_npz, save_folder, save_name, func
        # loop_CWSI(ET_npz,PET_npz,save_folder,f,cal_CWSI_kernel)
        pool.apply_async(func=loop_CWSI, args=(ET_npz,PET_npz,save_folder,f,cal_CWSI_kernel,))

    pool.close()
    pool.join()

if __name__ == '__main__':
    main()