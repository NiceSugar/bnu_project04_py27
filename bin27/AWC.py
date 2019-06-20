# coding=utf-8

import os
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



this_root = os.getcwd()+'\\..\\'

def mk_dir(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)


def nc_to_npz(nc,npz_out):
    # print(nc)
    # exit()
    ncin = Dataset(nc, 'r')
    print(ncin)
    # print ncin.variables

        # print(i)
    # exit()
    lat = ncin['lat']
    lon = ncin['lon']
    pixelWidth = abs((lon[-1] - lon[0]) / (len(lon) - 1))
    pixelHeight = abs((lat[-1] - lat[0]) / (len(lat) - 1))
    longitude_start = lon[0]
    latitude_start = lat[0]
    print(longitude_start)
    print(latitude_start)
    print(pixelWidth)
    print(pixelHeight)
    grid = ncin.variables['AWC_CLASS']
    grid = np.array(grid)
    return longitude_start,latitude_start,pixelWidth,pixelHeight,grid
    # plt.imshow(grid)
    # plt.colorbar()
    # plt.show()
    # exit()

    # np.savez(npz_out,**nc_dic)


    pass



def array2raster(newRasterfn,longitude_start,latitude_start,pixelWidth,pixelHeight,array):
    cols = array.shape[1]
    rows = array.shape[0]
    originX = longitude_start
    originY = latitude_start
    # open geotiff
    driver = gdal.GetDriverByName('GTiff')
    if os.path.exists(newRasterfn):
        os.remove(newRasterfn)
    outRaster = driver.Create(newRasterfn, cols, rows, 1, gdal.GDT_Float32)
    # Add Color Table
    # outRaster.GetRasterBand(1).SetRasterColorTable(ct)
    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))
    # Write Date to geotiff
    outband = outRaster.GetRasterBand(1)
    ndv = -999999
    outband.SetNoDataValue(ndv)
    outband.WriteArray(array)
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromEPSG(4326)
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    # Close Geotiff
    outband.FlushCache()
    del outRaster




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




def gen_lon_lat_dic(tif,out_dic):
    '''
    生成栅格和经纬度对应的字典
    数据格式:
    dic[str(x.y)] = [lon,lat]
    :return:
    '''
    # rasterized_tif = this_root + '/conf/my.tif'
    # DEM = this_root+'DEM\\china_1km_dem_wgs1984_resample.tif'
    array, im_width, im_height, im_geotrans, im_proj = tif_to_array(tif)

    # array = np.ma.masked_where(array>200,array)
    # plt.imshow(array)
    #
    # plt.colorbar()
    # plt.show()
    # array = np.load(this_root+'DEM\\dem_normalize.npy')
    # normalize(array)
    # exit()
    # clip_array = np.load(this_root+'\\conf\\china_T_F.npy')
    print(array)
    # array = np.ma.masked_where(array>200,array)
    # plt.imshow(array)
    # plt.colorbar()
    # plt.show()
    print(im_geotrans)

    lon_lat_dic = {}
    for y in range(len(array)):
        if y % 100 == 0:
            print(float(y)/len(array)*100,'%')
        for x in range(len(array[y])):
            if -1 < array[y][x] < 10000:
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



def standard_awc():
    out_dic = np.load(this_root + 'AWC\\from_wujianjun\\awc_dic.npy').item()
    dic = dict(out_dic)

    origin = []
    for i in dic:
        # print(i)
        # print(dic[i])
        origin.append(dic[i])
    min = float(np.min(origin))
    max = float(np.max(origin))
    standard_dic = {}
    for i in dic:
        val = dic[i]
        standard_dic[i] = (val-min)/(max-min)

    np.save(this_root + 'AWC\\from_wujianjun\\awc_dic_standardize.npy',standard_dic)
    # for i in standard_dic:
    #     print(i)
    #     print(standard_dic[i])
    #     print('*'*8)

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
    tif = this_root+'AWC\\from_wujianjun\\awc_CHINA_84.tif'
    out_dic = this_root+'AWC\\from_wujianjun\\awc_dic'
    gen_lon_lat_dic(tif,out_dic)
    # array, im_width, im_height, im_geotrans, im_proj = tif_to_array(tif)
    # array = np.ma.masked_where(array<0,array)
    # array = np.ma.masked_where(array>1000,array)
    # plt.imshow(array,'jet')
    # plt.colorbar()
    # plt.show()
    standard_awc()





    pass


if __name__ == '__main__':
    main()