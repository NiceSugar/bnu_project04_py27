# coding=utf-8


import psutil
import os
import numpy as np
from matplotlib import pyplot as plt
this_root = os.getcwd()+'\\..\\'
import time
import datetime
from osgeo import ogr,osr
import multiprocessing as mp

def mk_dir(fdir):
    if not os.path.isdir(fdir):
        os.mkdir(fdir)


def construct_modis_kernel(fdir,lon,lat,save_path):
    flist = os.listdir(fdir)
    vals = []
    for f in flist:
        # print(f)
        npz = np.load(fdir + f)
        for lon_lat in npz:
            lon_npz = float(lon_lat.split('_')[0])
            # 维度翻转
            lat_npz = float(lon_lat.split('_')[1])
            lat_mid = (60.0000958813812 + 10.0194697231069) / 2
            lat_npz = 2*lat_mid-lat_npz

            if lon - 0.1 < lon_npz < lon + 0.1 and lat - 0.1 < lat_npz < lat + 0.1:
                vals.append([f,lon_lat])
                print(f,lon_lat)
    print('saving '+save_path)
    np.save(save_path,vals)
    print('done')


def construct_modis(mode='01_VCI'):
    # 确定站点周围9km像素
    sta_pos_dic = np.load(this_root + 'ANN_input_para\\00_PDSI\\sta_pos_dic.npz')
    # fdir = this_root+'ANN_input_para\\'+mode+'\\'
    fdir = this_root+'data_transform\\split_lst\\'
    out_dir = this_root+'train_test_data\\'+mode+'\\'
    mk_dir(out_dir)
    out_dir = this_root + 'train_test_data\\' + mode + '\\intermediate\\'
    mk_dir(out_dir)
    pool = mp.Pool()
    for sta in sta_pos_dic:
        lon = sta_pos_dic[sta][1]
        lat = sta_pos_dic[sta][0]
        save_path = out_dir+sta
        print(save_path)
        # exit()
        construct_modis_kernel(fdir,lon,lat,save_path)
        # pool.apply_async(func=construct_modis_kernel,args=(fdir,lon,lat,save_path,))


    pool.close()
    pool.join()

def main():
    # construct_modis('index')
    sta_pos_dic = np.load(this_root + 'ANN_input_para\\00_PDSI\\sta_pos_dic.npz')
    print(sta_pos_dic['57614'])
    # exit()

    npy = np.load(this_root+'train_test_data\\index\\intermediate\\57614.npy')
    x = []
    y = []
    for i in npy:
        lon = float(i[1].split('_')[0])
        lat = float(i[1].split('_')[1])
        lat_mid = (60.0000958813812 + 10.0194697231069) / 2
        lat = 2 * lat_mid - lat
        x.append(lon)
        y.append(lat)
        # print(lon,lat)
        # break
    print(len(npy))
    plt.scatter(x,y)
    plt.show()
    pass

if __name__ == '__main__':
    main()
