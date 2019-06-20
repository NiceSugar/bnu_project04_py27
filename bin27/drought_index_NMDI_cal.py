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
def cal_NMDI_kernel(b2,b6,b7):
    # NDVI/LST
    NMDI = (b2-(b6-b7))/(b2+(b6-b7))
    # if b2+(b6-b7) == 0:
    #     print(b2,b6,b7)
    return NMDI


def mk_dir(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)


def loop_NMDI(b2,b6,b7,save_folder,save_name,func):
    import tool
    b2_npz = np.load(b2)
    b6_npz = np.load(b6)
    b7_npz = np.load(b7)
    # lst_scale_factor = 0.02
    # ndvi_scale_factor = 0.0001
    mk_dir(save_folder)

    # save_name = npz_file.split('\\')[-1]
    save_path = save_folder+'\\'+save_name
    start = time.time()
    # npz = np.load(npz_file)

    normalized_vals_dic = {}

    npy_flag = 0
    for npy in b2_npz:
        # if not npy == '88.9308542249_38.2295809254':
        #     continue
        # print(npy)
        npy_flag += 1.
        if npy_flag % 1000 == 0:
            print save_name,npy_flag/len(b2_npz)*100,'%','%02f'%(time.time()-start)
        try:
            vals_b2 = b2_npz[npy]
            vals_b6 = b6_npz[npy]
            vals_b7 = b7_npz[npy]
        except:
            vals_b2 = []
            vals_b6 = []
            vals_b7 = []

        try:
            if len(vals_b2) > 1 and len(vals_b6) > 1 and len(vals_b7) > 1:

                nmdi = func(vals_b2,vals_b6,vals_b7)
                # nmdi = []
                # for i in range(len(vals_b2)):
                #     b2_i = vals_b2[i]
                #     b6_i = vals_b6[i]
                #     b7_i = vals_b7[i]
                #     nmdi_i = (b2_i-(b6_i-b7_i))/(b2_i+(b6_i-b7_i))
                #     if b2_i+(b6_i-b7_i) == 0:
                #         print(b2_i,b6_i,b7_i)
                #         print(nmdi_i)
                #         print(npy)
                #     nmdi.append(nm di_i)
                # 3 sigma clean
                nmdi_clean = tool.interp_1d_3_sigma(nmdi)
                nmdi_clean1 = tool.interp_1d_3_sigma(nmdi_clean)

                normalized_vals_dic[npy] = nmdi_clean1

            else:
                normalized_vals_dic[npy] = []

        except:
            normalized_vals_dic[npy] = []
    print('saving '+save_path)
    np.savez(save_path,**normalized_vals_dic)
    print 'save '+save_path+' success\ntime:','%02f'%(time.time()-start)



def main():
    data_root ='D:\\OneDrive - business-cn(1)\\project04_data\\project04_monthly_data\\'
    save_folder = this_root + 'monthly_data_npz_NMDI\\'

    b2_dir = data_root+'monthly_data_npz_b02\\'
    b6_dir = data_root+'monthly_data_npz_b06\\'
    b7_dir = data_root+'monthly_data_npz_b07\\'
    flist = os.listdir(b2_dir)
    # print(flist)
    pool = mp.Pool(processes=1)
    for f in flist:
        print(f)
        # exit()
        b2_npz = b2_dir+f
        b6_npz = b6_dir+f
        b7_npz = b7_dir+f

        save_name = f
        func = cal_NMDI_kernel
        loop_NMDI(b2_npz,b6_npz,b7_npz,save_folder,save_name,func)
        # NDVI_npz, LST_npz, save_folder, save_name, func

        # pool.apply_async(func=loop_NMDI, args=(b2_npz,b6_npz,b7_npz,save_folder,save_name,func,))

    pool.close()
    pool.join()

if __name__ == '__main__':
    main()