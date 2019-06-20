# coding=utf-8

import os
this_root = os.getcwd()+'\\..\\'
import numpy as np
import time
from scipy import interpolate
from matplotlib import pyplot as plt
# import gdal
# import ogr
from osgeo import gdal
from osgeo import ogr
from osgeo import gdalconst
# import


def readTif(fileName):
    dataset = gdal.Open(fileName)
    if dataset == None:
        print(fileName+"文件无法打开")
        return
    im_width = dataset.RasterXSize #栅格矩阵的列数
    im_height = dataset.RasterYSize #栅格矩阵的行数
    im_bands = dataset.RasterCount #波段数
    im_data = dataset.ReadAsArray(0,0,im_width,im_height)#获取数据
    im_geotrans = dataset.GetGeoTransform()#获取仿射矩阵信息
    im_proj = dataset.GetProjection()#获取投影信息
    return im_width,im_height,im_bands,im_data,im_geotrans,im_proj


def rasterize_shp(tif,shp,output):
    # tif = 'D:\\MODIS\\data_tif\\MOD11A2.006\\2003.01.09.LST_Day_1km.tif'
    # shp = 'D:\\MODIS\\shp\\china_dissolve.shp'
    # output = 'D:\\MODIS\\my.tif'

    data = gdal.Open(tif, gdalconst.GA_ReadOnly)
    geo_transform = data.GetGeoTransform()
    #source_layer = data.GetLayer()
    x_min = geo_transform[0]
    y_max = geo_transform[3]
    x_max = x_min + geo_transform[1] * data.RasterXSize
    y_min = y_max + geo_transform[5] * data.RasterYSize
    x_res = data.RasterXSize
    y_res = data.RasterYSize
    mb_v = ogr.Open(shp)
    mb_l = mb_v.GetLayer()
    pixel_width = geo_transform[1]

    target_ds = gdal.GetDriverByName('GTiff').Create(output, x_res, y_res, 1, gdal.GDT_Byte)
    target_ds.SetGeoTransform((x_min, pixel_width, 0, y_min, 0, pixel_width))
    band = target_ds.GetRasterBand(1)
    NoData_value = -999999
    band.SetNoDataValue(NoData_value)
    band.FlushCache()
    gdal.RasterizeLayer(target_ds, [1], mb_l)
    # gdal.RasterizeLayer(target_ds, [1], mb_l, options=["ATTRIBUTE=hedgerow"])

    target_ds = None

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



def normalize(array):

    valid_range = []
    for i in range(len(array)):
        if i % 100 == 0:
            print(float(i)/len(array)*100,'%')
        for j in range(len(array[i])):
            val = array[i][j]
            if -9000 < val < 99999:
                valid_range.append(val)
    max = np.max(valid_range)
    min = np.min(valid_range)

    normalized = []
    for i in range(len(array)):
        if i % 100 == 0:
            print('normalizing ',float(i)/len(array)*100,'%')
        temp = []
        for j in range(len(array[i])):
            val = float(array[i][j])
            if -9000 < val < 99999:
                temp.append((val-min)/(max-min))
            else:
                temp.append(-99999)
        normalized.append(temp)
    normalized = np.array(normalized)
    np.save(this_root+'DEM\\dem_normalize',normalized)
    plt.imshow(normalized)
    plt.colorbar()
    plt.show()



def gen_lon_lat_dic():
    '''
    生成栅格和经纬度对应的字典
    数据格式:
    dic[str(x.y)] = [lon,lat]
    :return:
    '''
    # rasterized_tif = this_root + '/conf/my.tif'
    DEM = this_root+'DEM\\china_1km_dem_wgs1984_resample.tif'
    array, im_width, im_height, im_geotrans, im_proj = tif_to_array(DEM)
    array = np.load(this_root+'DEM\\dem_normalize.npy')
    # normalize(array)
    # exit()
    # clip_array = np.load(this_root+'\\conf\\china_T_F.npy')
    # print(array)
    # array = np.ma.masked_where(array<-9999,array)
    # plt.imshow(array)
    # plt.colorbar()
    # plt.show()
    print(im_geotrans)

    lon_lat_dic = {}
    for y in range(len(array)):
        if y % 100 == 0:
            print(float(y)/len(array)*100,'%')
        for x in range(len(array[y])):
            if array[y][x] > -9000:
                lon_start = im_geotrans[0]
                lon_step = im_geotrans[1]
                lon = lon_start + lon_step * x

                lat_start = im_geotrans[3]
                lat_step = im_geotrans[5]
                lat = lat_start + lat_step * y
                # print('*'*8)
                # print(str(lon)+'_'+str(lat))
                # print(array[y][x])
                lon_lat_dic[str(lon)+'_'+str(lat)] = array[y][x]

    np.save(this_root+'\\DEM\\DEM_data_transform',lon_lat_dic)


def main():
    # gen_lon_lat_dic()
    dem_dic = np.load(this_root+'\\DEM\\DEM_data_transform.npy').item()
    dem_dic = dict(dem_dic)
    for k in dem_dic:
        print(k)
        print(dem_dic[k])
        print('*'*8)

if __name__ == '__main__':
    main()