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


def add_plot_scatter_colors(x,y,z):
    colors = []
    flag = 0
    min = float(np.min(z))
    max = float(np.max(z))
    for i in z:
        flag += 1
        if flag % 1000 == 0:
            print(flag, '/', len(z))
        colors.append((i - min) / (max - min))
    colors = np.array(colors)
    plt.figure()
    plt.scatter(x, y, c=z, cmap='jet',data=z)
    plt.colorbar()
    plt.show()


def smci():
    pix_width = 0.25
    npz = np.load(this_root + 'ANN_input_para\\07_SMCI\\SMCI.npz')
    dic_out_path = this_root+'train_test_data\\07_SMCI_dic'
    sta_pos_dic = np.load(this_root + 'ANN_input_para\\00_PDSI\\sta_pos_dic.npz')
    sta_vals = {}
    flag = 0
    for sta in sta_pos_dic:
        flag+=1.
        if flag%100 == 0:
            print('%00.2f'%(100*flag/len(sta_pos_dic))+' %')
        lon_sta = sta_pos_dic[sta][1]
        lat_sta = sta_pos_dic[sta][0]
        for i in npz:
            lon_i = float(i.split('_')[0])
            lat_i = float(i.split('_')[1])
            if lon_sta - pix_width/2 < lon_i < lon_sta + pix_width/2 and lat_sta - pix_width/2 < lat_i < lat_sta + pix_width/2:
                arr = np.reshape(npz[i],(len(npz[i])/12,12))
                for year in range(len(arr)):
                    for m in range(len(arr[year])):
                        key = sta+'_'+str(year+2003)+'%02d'%(m+1)
                        v = arr[year][m]
                        sta_vals[key] = v
    print('saving dic...')
    np.save(dic_out_path,sta_vals)


def spi():
    pix_width = 0.5
    npz = np.load(this_root + 'ANN_input_para\\04_SPI\\spi_no_nan.npz')
    dic_out_path = this_root + 'train_test_data\\04_SPI_dic'
    sta_pos_dic = np.load(this_root + 'ANN_input_para\\00_PDSI\\sta_pos_dic.npz')
    sta_vals = {}
    flag = 0
    for sta in sta_pos_dic:
        flag+=1.
        if flag%100 == 0:
            print('%00.2f'%(100*flag/len(sta_pos_dic))+' %')
        lon_sta = sta_pos_dic[sta][1]
        lat_sta = sta_pos_dic[sta][0]
        for i in npz:
            lon_i = float(i.split('_')[0])
            lat_i = float(i.split('_')[1])
            if lon_sta - pix_width/2 < lon_i < lon_sta + pix_width/2 and lat_sta - pix_width/2 < lat_i < lat_sta + pix_width/2:
                arr = np.reshape(npz[i],(len(npz[i])/12,12))
                for year in range(len(arr)):
                    for m in range(len(arr[year])):
                        key = sta+'_'+str(year+2003)+'%02d'%(m+1)
                        v = arr[year][m]
                        sta_vals[key] = v
    print('saving dic...')
    np.save(dic_out_path,sta_vals)



def pci():
    pix_width = 0.5
    npz = np.load(this_root + 'ANN_input_para\\08_PCI\\PCI.npz')
    dic_out_path = this_root + 'train_test_data\\08_PCI_dic'
    sta_pos_dic = np.load(this_root + 'ANN_input_para\\00_PDSI\\sta_pos_dic.npz')
    sta_vals = {}
    flag = 0
    for sta in sta_pos_dic:
        flag += 1.
        if flag % 100 == 0:
            print('%00.2f' % (100 * flag / len(sta_pos_dic)) + ' %')
        lon_sta = sta_pos_dic[sta][1]
        lat_sta = sta_pos_dic[sta][0]
        for i in npz:
            lon_i = float(i.split('_')[0])
            lat_i = float(i.split('_')[1])
            if lon_sta - pix_width / 2 < lon_i < lon_sta + pix_width / 2 and lat_sta - pix_width / 2 < lat_i < lat_sta + pix_width / 2:
                arr = np.reshape(npz[i], (len(npz[i]) / 12, 12))
                for year in range(len(arr)):
                    for m in range(len(arr[year])):
                        key = sta + '_' + str(year + 2003) + '%02d' % (m + 1)
                        v = arr[year][m]
                        sta_vals[key] = v
    print('saving dic...')
    np.save(dic_out_path, sta_vals)


def grace_tws():
    pix_width = 1.
    npz = np.load(this_root + 'ANN_input_para\\13_TWS\\GRACE_data_transform.npz')
    dic_out_path = this_root + 'train_test_data\\13_TWS'
    sta_pos_dic = np.load(this_root + 'ANN_input_para\\00_PDSI\\sta_pos_dic.npz')
    sta_vals = {}
    flag = 0
    for sta in sta_pos_dic:
        flag += 1.
        if flag % 100 == 0:
            print('%00.2f' % (100 * flag / len(sta_pos_dic)) + ' %')
        lon_sta = sta_pos_dic[sta][1]
        lat_sta = sta_pos_dic[sta][0]
        for i in npz:
            lon_i = float(i.split('_')[0])
            lat_i = float(i.split('_')[1])
            if lon_sta - pix_width / 2 < lon_i < lon_sta + pix_width / 2 and lat_sta - pix_width / 2 < lat_i < lat_sta + pix_width / 2:
                arr = np.reshape(npz[i], (len(npz[i]) / 12, 12))
                for year in range(len(arr)):
                    for m in range(len(arr[year])):
                        key = sta + '_' + str(year + 2003) + '%02d' % (m + 1)
                        v = arr[year][m]
                        sta_vals[key] = v
    print('saving dic...')
    np.save(dic_out_path, sta_vals)
    pass


def main():
    grace_tws()


if __name__ == '__main__':
    main()