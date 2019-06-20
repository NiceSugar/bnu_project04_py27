# coding=utf-8
import os
import numpy as np
import time
from matplotlib import pyplot as plt
# import gdal
from osgeo import gdal
from osgeo import ogr
from osgeo import gdalconst
# import fiona
# import rasterio
# import rasterio.mask

this_root = os.getcwd()+'\\..\\'

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


def clip(input_tif,clip_array,out_array):
    # tif = 'D:\\MODIS\\data_tif\\MOD11A2.006\\2003.01.01.LST_Day_1km.tif'
    # array = np.load('D:\\MODIS\\conf\\china_T_F.npy')
    lst_array = tif_to_array(input_tif)[0]

    # clip_array = np.load(clip_array)
    lst_array = lst_array.T[:12700].T
    lst_array[np.logical_not(clip_array)] = -1
    np.save(out_array,lst_array)
    # print(lst_array)
    # lst_array = np.ma.masked_where(lst_array>200,lst_array)
    # plt.imshow(lst_array)
    # plt.colorbar()
    # plt.show()


def gen_mask_array():
    rasterized_tif = this_root+'/conf/my.tif'
    array = tif_to_array(rasterized_tif)
    new_array = []
    k=0
    for i in array:
        k+=1
        if k%100 == 0:
            print((k,'/',len(array)))
        # print(k,'/',len(array))
        temp = []
        for j in i:
            if j == 0:
                temp.append(False)
            else:
                temp.append(True)
        new_array.append(temp)
    new_array = np.array(new_array)
    np.save('D:\\MODIS\\conf\\china_T_F.npy',new_array)

# tif = 'D:\\MODIS\\data_tif\\MOD11A2.006\\2003.01.01.LST_Day_1km.tif'
# clip(tif)

def main():
    clip_array = np.load('D:\\MODIS\\conf\\china_T_F.npy')
    f_dir = this_root+'\\data_tif\\MCD12Q1.006\\'
    file_list = os.listdir(f_dir)
    out_dir = this_root+'\\clipped\\MCD12Q1.006\\'
    if not os.path.isdir(this_root+'\\clipped\\'):
        os.mkdir(this_root+'\\clipped\\')
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    flag = 0
    for f in file_list:
        flag += 1
        tif = f_dir+f
        print flag,'/',len(file_list),tif
        clip(tif,clip_array,out_dir+f)
        # exit()
    pass


if __name__ == '__main__':
    # npy = 'D:\\MODIS\\clipped\\MOD11A2.006\\2003.01.01.LST_Day_1km.tif.npy'
    # array = np.load(npy)
    # plt.imshow(array)
    # plt.show()
    main()