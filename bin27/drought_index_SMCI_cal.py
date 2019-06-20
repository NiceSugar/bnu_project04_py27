# coding=utf-8

import os
this_root = os.getcwd()+'\\..\\'
import numpy as np
import time
from matplotlib import pyplot as plt
from multiprocessing import Process
import multiprocessing as mp
import psutil
import numba as nb
from numba import float64



def mk_dir(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)


@nb.jit()
def normalize(val):

    val_normal = np.array([0.]*len(val))
    for i in range(len(val)):
        v_i = (val[i]-np.min(val))/(np.max(val)-np.min(val))
        val_normal[i] = v_i

    return val_normal



def loop_normalize(npz_file,save_folder):
    mk_dir(save_folder)
    save_name = npz_file.split('\\')[-1]
    save_path = save_folder+'\\'+save_name
    start = time.time()
    npz = np.load(npz_file)

    normalized_vals_dic = {}

    npy_flag = 0
    for npy in npz:
        # print(npy)
        npy_flag += 1.
        if npy_flag % 1000 == 0:
            print npz_file,npy_flag/len(npz)*100,'%','%02f'%(time.time()-start)
        vals = npz[npy]

        try:
            if len(vals) > 1:
                normalized_vals_dic[npy] = normalize(vals)
                # plt.plot(normalize(vals))
                # plt.show()
                # normalized_vals_dic[npy] = pool.apply_async(func=normalize, args=(vals,)).get()
        except:
            normalized_vals_dic[npy] = []
    print('saving '+save_path)
    np.savez(save_path,**normalized_vals_dic)
    print('save '+save_path+' success\ntime:','%02f'%(time.time()-start))


def main():
    # npz = this_root+'CCI\\time_interp.npz'
    save_folder = this_root+'CCI\\SMCI\\time_interp.npz'
    dic = np.load(save_folder)
    for k in dic:
        print(k)
        # print(dic[k])
        plt.plot(dic[k])
        plt.show()
    # flist = os.listdir(f_dir)
    # pool = mp.Pool(processes=1)
    # for f in flist:

        # npz = f_dir+f
        # pool.apply_async(func=loop_normalize, args=(npz,save_folder,))
    # loop_normalize(npz,save_folder)

    # pool.close()
    # pool.join()


if __name__ == '__main__':
    # loop_normalize()
    main()