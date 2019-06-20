# coding=utf-8

import os
this_root = os.getcwd()+'\\..\\'
import numpy as np
# import time
from matplotlib import pyplot as plt
# import clip
# from multiprocessing import Process
# import multiprocessing as mp
# import psutil
# import threading
from scipy.interpolate import InterpolatedUnivariateSpline
from scipy import interpolate
from netCDF4 import Dataset
from osgeo import gdalconst
import datetime
import osr, ogr
import gdal



def tif_to_array(fileName):
    dataset = gdal.Open(fileName)
    if dataset == None:
        print(fileName + "文件无法打开")
        return
    im_width = dataset.RasterXSize  # 栅格矩阵的列数
    im_height = dataset.RasterYSize  # 栅格矩阵的行数
    im_bands = dataset.RasterCount  # 波段数
    im_data = dataset.ReadAsArray(0, 0, im_width, im_height)  # 获取数据
    im_geotrans = dataset.GetGeoTransform()  # 获取仿射矩阵信息
    im_proj = dataset.GetProjection()  # 获取投影信息
    array = np.array(im_data)
    # np.save('D:\\MODIS\\conf\\china',array)
    # print(np.shape(array))
    # plt.imshow(array)
    # plt.show()
    print('im_width','im_height','im_geotrans','im_proj')
    return array,im_width,im_height,im_geotrans,im_proj
    # return


def gen_lon_lat_list(start_lon_lat,step,length):
    lon_lat_list = []
    for i in range(length):
        lon_lat_list.append(start_lon_lat+step*i)
    return lon_lat_list
    pass




def gen_lon_lat_dic(array,tif_template,out_dic):
    '''
    生成栅格和经纬度对应的字典
    数据格式:
    dic[str(x.y)] = [lon,lat]
    :return:
    '''
    # rasterized_tif = this_root + '/conf/my.tif'
    # DEM = this_root+'DEM\\china_1km_dem_wgs1984_resample.tif'
    _, im_width, im_height, im_geotrans, im_proj = tif_to_array(tif_template)
    print(im_geotrans)
    # array = np.ma.masked_where(array>200,array)
    # plt.imshow(array)
    #
    # plt.colorbar()
    # plt.show()
    # array = np.load(this_root+'DEM\\dem_normalize.npy')
    # normalize(array)
    # exit()
    # clip_array = np.load(this_root+'\\conf\\china_T_F.npy')
    # print(array)
    # array = np.ma.masked_where(array>200,array)
    # plt.imshow(array)
    # plt.colorbar()
    # plt.show()


    lon_lat_dic = {}
    for y in range(len(array)):
        if y % 100 == 0:
            print(float(y)/len(array)*100,'%')
        for x in range(len(array[y])):
            if 0 < array[y][x] < 200:
                lon_start = im_geotrans[0]
                lon_step = im_geotrans[1]
                lon = lon_start + lon_step * x

                lat_start = im_geotrans[3]
                lat_step = im_geotrans[5]
                lat = lat_start + lat_step * y
                # print('*'*8)
                # print(str(lon)+'_'+str(lat))
                # print(array[y][x])
                # import time
                # time.sleep(0.5)
                lon_lat_dic[str(lon)+'_'+str(lat)] = array[y][x]

    np.save(out_dic,lon_lat_dic)



def main():
    # nc = this_root+'AWC\HWSD_1247\HWSD_1247\data\\AWC_CLASS.nc4'
    # npz_out = ''
    # newRasterfn = 'AWC_CLASS.tif'
    # longitude_start, latitude_start, pixelWidth, pixelHeight, array = nc_to_npz(nc, npz_out)
    # array2raster(newRasterfn, longitude_start, latitude_start, pixelWidth, pixelHeight, array)
    # tif = this_root + 'AWC\\HWSD_clip1.tif'
    # out_dic = this_root+'AWC\\HWSD_transformed.npy'
    # gen_lon_lat_dic(tif,out_dic).


    # wujianjun
    tif = this_root+'data_tif\\MCD12Q1.006\\2003.01.01.LC_Type1.tif'
    out_dic = this_root+'landcover_dic\\landcover_dic'
    array = np.load(this_root+'clipped\\MCD12Q1.006\\2009.01.01.LC_Type1.tif.npy')
    gen_lon_lat_dic(array,tif,out_dic)
    # array, im_width, im_height, im_geotrans, im_proj = tif_to_array(tif)
    # array = np.ma.masked_where(array<0,array)
    # array = np.ma.masked_where(array>1000,array)
    # plt.imshow(array,'jet')
    # plt.colorbar()
    # plt.show()
    # standard_awc()

    pass


if __name__ == '__main__':
    main()