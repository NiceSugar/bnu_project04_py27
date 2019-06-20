# coding=utf-8

import os
this_root = os.getcwd()+'\\..\\'
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


def insert_data(val,insert_index_npy):
    insert_index = np.load(insert_index_npy)
    for index in insert_index:
        val = np.insert(val,index,32700)

    return val


def mk_dir(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)


def compose_monthly_data(val,date_tif_dir):

    fdir = date_tif_dir
    flist = os.listdir(fdir)
    date = []
    for f in flist:
        if '.PET_' in f:
            date.append(f[:10])

    f_list = date
    # print(flist)
    # exit()
    monthly_val = []
    for y in range(2003, 2017):
        for m in range(1, 13):
            monthly_sum = []
            for date in f_list:
                if str(y) + '.' + '%02d' % m in date:
                    # print(date)
                    # exit()
                    ind = f_list.index(date)
                    monthly_sum.append(val[ind])
            sum = 0.
            flag = 0.
            for i in monthly_sum:
                # print(i)
                if i < 30000:
                    sum += i
                    flag += 1
            if flag == 0:
                monthly_mean = 32000
            else:
                monthly_mean = sum/flag
            monthly_val.append(monthly_mean)

    monthly_val = np.array(monthly_val)
    # monthly_val = np.ma.masked_where(monthly_val>30000,monthly_val)
    # plt.plot(monthly_val)
    # plt.twiny()
    # val = np.ma.masked_where(val>30000,val)
    # plt.plot(val,c='r',alpha=0.4)

    # plt.show()
    # exit()
    return monthly_val


def interp_1d(val):
    # 1、插缺失值
    x = []
    val_new = []
    for i in range(len(val)):
        if val[i] < 30000:
            index = i
            x = np.append(x, index)
            val_new = np.append(val_new, val[i])

    interp = interpolate.interp1d(x, val_new, kind='nearest', fill_value="extrapolate")

    xi = range(len(val))
    yi = interp(xi)

    # plt.plot(yi, alpha=0.4)


    # 2、利用三倍sigma，去除离群值
    # print(len(yi))
    val_mean = np.mean(yi)
    sigma = np.std(yi)
    n = 3
    yi[(val_mean - n * sigma) > yi] = -32000
    yi[(val_mean + n * sigma) < yi] = 32000
    bottom = val_mean - n * sigma
    top = val_mean + n * sigma
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
        if -32000 < yi[i] < 32000:
            index = i
            xii = np.append(xii, index)
            val_new_ii = np.append(val_new_ii, yi[i])

    interp_1 = interpolate.interp1d(xii, val_new_ii, kind='nearest', fill_value="extrapolate")

    xiii = range(len(val))
    yiii = interp_1(xiii)

    # plt.plot(yiii, alpha=0.4)
    # plt.show()
    # for i in range(len(yi)):
    #     if yi[i] == -999999:
    #         val_new_ii = np.append(val_new_ii, bottom)
    #     elif yi[i] == 999999:
    #         val_new_ii = np.append(val_new_ii, top)
    #     else:
    #         val_new_ii = np.append(val_new_ii, yi[i])

    return yiii

    # return val


def loop(val,insert_index_npy,date_tif_dir):

    arr = val
    arr = insert_data(arr,insert_index_npy)
    month_arr = compose_monthly_data(arr,date_tif_dir)
    month_arr = interp_1d(month_arr)
    return month_arr


def time_interp(npz_dir,save_dir,insert_index_npy,date_tif_dir):
    # npz_dir = this_root + 'data_transform\\split_et\\'
    npz_list = os.listdir(npz_dir)
    # save_dir = this_root + 'monthly_data_npz_et\\'
    mk_dir(save_dir)
    print(npz_dir)
    print(save_dir)
    # exit()
    all_interp_dic = {}
    flag1 = 0

    for f in npz_list:

        if os.path.isfile(save_dir + f):
            print(save_dir + f + ' is already existed')
            continue
        flag1 += 1
        print(flag1)

        pool = mp.Pool()
        flag = 0
        start = time.time()
        interp_dic = {}
        muti_res = {}
        npz = np.load(npz_dir + f)
        for pix in npz:
            flag+=1
            if flag % 1000 == 0:
                print flag1, '/', len(npz_list), '\t', float(flag) / len(npz) * 100, '%'
            if np.mean(npz[pix]) < 32000:
                arr = npz[pix]
                # res = loop(arr)
                res = pool.apply_async(loop, (arr,insert_index_npy,date_tif_dir,))
                muti_res[pix] = res
                # plt.plot(res.get())
                # plt.show()
            else:
                interp_dic[pix] = []
        print('fetching results')
        for i in muti_res:
            array = muti_res[i].get()
            interp_dic[i] = array
        pool.close()
        pool.join()
        end = time.time()
        print(end - start, 's')
        print('saving results')
        all_interp_dic[f] = interp_dic

    return all_interp_dic


def save_all_interp_dic(dic,f,save_dir):

    start = time.time()
    # save_dir = this_root + 'monthly_data_npz_et\\'
    mk_dir(save_dir)
    save_path = save_dir+f
    print('start saving ' + save_path)
    np.savez(save_path,**dic)
    end = time.time()
    print(save_path+' success, time '+str(end-start)+' s')
    pass

# def concurrent_save_all_interp_dic(npz_dir,save_dir):
#     all_interp_dic = time_interp(npz_dir,save_dir)
#     pool = mp.Pool()
#     for ind in all_interp_dic:
#         dic = all_interp_dic[ind]
#         pool.apply_async(save_all_interp_dic, (dic,ind,save_dir,))
#     pool.close()
#     pool.join()



def concurrent_save_all_interp_dic(npz_dir,save_dir,insert_index_npy,date_tif_dir):
    # f_dir = this_root + 'data_transform\\split_lst\\'
    flist = os.listdir(npz_dir)
    for dir in flist:
        all_interp_dic = {}
        dir = npz_dir+dir+'\\'
        # exit()
        all_interp_dic = time_interp(dir,save_dir,insert_index_npy,date_tif_dir)
        pool = mp.Pool()
        for ind in all_interp_dic:
            dic = all_interp_dic[ind]
            pool.apply_async(save_all_interp_dic, (dic, ind,save_dir))
        pool.close()
        pool.join()



def main():
    # npz_dir = this_root + 'data_transform\\split_et\\'
    # save_dir = this_root + 'monthly_data_npz_et\\'
    # insert_index_npy = this_root+'conf\\PET_insert_index.npy'
    # date_tif_dir = 'Z:\\modis_download\\data_tif\\MOD16A2.006\\'
    # concurrent_save_all_interp_dic(npz_dir,save_dir,insert_index_npy,date_tif_dir)
    fdir = 'D:\\project04\\CCI\\composed\\1983\\'
    flist = os.listdir(fdir)
    for f in flist:
        arr = np.load(fdir+f)
        plt.imshow(arr)
        plt.show()

if __name__ == '__main__':
    main()