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
def cal_VHI_kernel(VCI,TCI):
    # NDVI/LST
    VHI = 0.5*VCI+0.5*TCI
    return VHI


def mk_dir(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)




def loop_VHI(VCI,TCI,save_folder,save_name,func):
    # import tool
    VCI_npz = np.load(VCI)
    TCI_npz = np.load(TCI)
    # lst_scale_factor = 0.02
    # ndvi_scale_factor = 0.0001
    mk_dir(save_folder)

    # save_name = npz_file.split('\\')[-1]
    save_path = save_folder+'\\'+save_name
    start = time.time()
    # npz = np.load(npz_file)

    normalized_vals_dic = {}

    npy_flag = 0
    for npy in VCI_npz:
        # print(npy)
        npy_flag += 1.
        if npy_flag % 1000 == 0:
            print save_name,npy_flag/len(VCI_npz)*100,'%','%02f'%(time.time()-start)
        try:
            vals_VCI = VCI_npz[npy]
            vals_TCI = TCI_npz[npy]
        except:
            vals_VCI = []
            vals_TCI = []

        try:
            if len(vals_VCI) > 1 and len(vals_TCI) > 1:
                normalized_vals_dic[npy] = func(vals_VCI,vals_TCI)
                plt.figure()
                plt.plot(vals_VCI)
                plt.title('vals_VCI')
                plt.figure()
                plt.plot(vals_TCI)
                plt.title('vals_TCI')
                plt.figure()
                plt.plot(func(vals_VCI,vals_TCI))
                plt.title('VHI')
                plt.show()
            else:
                normalized_vals_dic[npy] = []

        except:
            normalized_vals_dic[npy] = []
    print('saving '+save_path)
    np.savez(save_path,**normalized_vals_dic)
    print 'save '+save_path+' success\ntime:','%02f'%(time.time()-start)





def main():
    data_root ='D:\\OneDrive - business-cn(1)\\project04_data\\project04_monthly_data\\'
    save_folder = this_root + 'monthly_data_npz_VHI\\'

    VCI_dir = 'D:\\OneDrive - business-cn(1)\\project04_data\\drought_indices\\monthly_data_npz_ndvi_normalize\\'
    TCI_dir = 'D:\\OneDrive - business-cn(1)\\project04_data\\drought_indices\\monthly_data_npz_lst_normalize\\'
    flist = os.listdir(VCI_dir)
    # print(flist)
    pool = mp.Pool(processes=2)
    for f in flist:
        print(f)
        # exit()
        vci_npz = VCI_dir+f
        tci_npz = TCI_dir+f

        save_name = f
        func = cal_VHI_kernel
        # loop_VHI(vci_npz,tci_npz,save_folder,save_name,func)
        # NDVI_npz, LST_npz, save_folder, save_name, func

        pool.apply_async(func=loop_VHI, args=(vci_npz,tci_npz,save_folder,save_name,func,))

    pool.close()
    pool.join()

if __name__ == '__main__':
    main()