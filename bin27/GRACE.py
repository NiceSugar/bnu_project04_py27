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

    # print ncin.variables

        # print(i)
    # exit()
    lat = ncin['lat']
    lon = ncin['lon']
    longitude_grid_distance = abs((lon[-1] - lon[0]) / (len(lon) - 1))
    latitude_grid_distance = -abs((lat[-1] - lat[0]) / (len(lat) - 1))
    longitude_start = lon[0]
    latitude_start = lat[0]

    time = ncin.variables['time']
    time_bounds = ncin.variables['time_bounds']
    # print(time_bounds)
    start = datetime.datetime(2002, 01, 01)
    # a = start + datetime.timedelta(days=5459)
    # print(a)
    print(len(time_bounds))
    print(len(time))
    # exit()
    nc_dic = {}
    flag = 0
    for i in range(len(time_bounds)):
        flag += 1
        # print(time[i])
        date = start + datetime.timedelta(days=int(time[i]))
        year = str(date.year)
        month = '%02d'%date.month
        date_str = year+month
        print(date_str)
        grid = ncin.variables['lwe_thickness'][i][::-1]
        # print(type(grid))
        # exit()
        grid = np.array(grid)
        # plt.imshow(grid)
        # plt.show()
        nc_dic[date_str] = grid
    print(len(nc_dic))
    print(flag)
    # np.savez(npz_out,**nc_dic)


    pass


def CSR_GFZ_JPL_compose():
    npzs_dir = this_root+'GRACE\\raw_npz\\'
    npzs_list = os.listdir(npzs_dir)
    save_fname = this_root+'GRACE\\3_GRACE_product_mean.npz'
    date_list = []
    for year in range(2003,2017):
        year = str(year)
        for mon in range(1,13):
            mon = '%02d'%mon
            date_list.append(year+mon)
    # for i in date_list:
    #     print(i)
    # exit()
    npzs = []
    for f in npzs_list:
        npzs.append(np.load(npzs_dir+f))

    # print('200306' in npzs[0])
    # exit()
    compose_dic = {}
    for date in date_list:
        print(date)
        flag = 0.
        if date in npzs[0]:
            flag += 1
            npz1 = npzs[0][date]
        else:
            npz1 = np.zeros_like(npzs[0]['200305'])

        if date in npzs[1]:
            flag += 1
            npz2 = npzs[1][date]
        else:
            npz2 = np.zeros_like(npzs[0]['200305'])

        if date in npzs[2]:
            flag += 1
            npz3 = npzs[2][date]
        else:
            npz3 = np.zeros_like(npzs[0]['200305'])

        if flag == 0.:
            print('missing ',date)
            continue
        elif flag == 4:
            plt.figure()
            plt.imshow(npz1)
            plt.colorbar()
            plt.title('npz1')

            plt.figure()
            plt.imshow(npz2)
            plt.colorbar()
            plt.title('npz2')

            plt.figure()
            plt.imshow(npz3)
            plt.colorbar()
            plt.title('npz3')


            mean = (npz1 + npz2 + npz3) / flag
            plt.figure()
            plt.imshow(mean)
            plt.colorbar()
            plt.title('mean')

            plt.show()
        mean = (npz1+npz2+npz3)/flag
        # plt.imshow(mean)
        # plt.colorbar()
        # plt.show()
        compose_dic[date] = mean
    np.savez(save_fname,**compose_dic)
    # print(len(date_list))
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


def gen_mask_template(nc):

    ncin = Dataset(nc, 'r')

    # print ncin.variables

    # print(i)
    # exit()
    lat = ncin['lat']
    lon = ncin['lon']
    longitude_grid_distance = abs((lon[-1] - lon[0]) / (len(lon) - 1))
    latitude_grid_distance = abs((lat[-1] - lat[0]) / (len(lat) - 1))
    longitude_start = lon[0]
    latitude_start = lat[0]
    print(longitude_start)
    print(latitude_start)
    print(longitude_grid_distance)
    print(latitude_grid_distance)
    array = ncin.variables['lwe_thickness'][0]
    array2raster('GRACE_template.tif',longitude_start,latitude_start,longitude_grid_distance,latitude_grid_distance,array)
    pass



def rasterize_shp(tif,shp,output):
    # tif = 'D:\\MODIS\\data_tif\\MOD11A2.006\\2003.01.09.LST_Day_1km.tif'
    # shp = 'D:\\MODIS\\shp\\china_dissolve.shp'
    # output = 'D:\\MODIS\\my.tif'

    data = gdal.Open(tif, gdalconst.GA_ReadOnly)
    geo_transform = data.GetGeoTransform()
    #source_layer = data.GetLayer()
    x_min = geo_transform[0]

    y_max = geo_transform[3]


    x_max = x_min - geo_transform[1] * data.RasterXSize
    y_min = y_max + geo_transform[5] * data.RasterYSize
    x_res = data.RasterXSize
    y_res = data.RasterYSize



    # print(x_min)
    # print(geo_transform[5])
    # print(data.RasterYSize)

    mb_v = ogr.Open(shp)
    mb_l = mb_v.GetLayer()
    pixel_width = geo_transform[1]
    print(x_min, pixel_width, 0, y_max, 0, pixel_width)


    # exit()
    target_ds = gdal.GetDriverByName('GTiff').Create(output, x_res, y_res, 1, gdal.GDT_Byte)
    target_ds.SetGeoTransform((x_min, pixel_width, 0, y_max, 0, pixel_width))
    band = target_ds.GetRasterBand(1)
    NoData_value = -99
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


def gen_mask_array():
    rasterized_tif = this_root+'/conf/GRACE_mask.tif'
    array = tif_to_array(rasterized_tif)[0][::-1]
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
    np.save('D:\\MODIS\\conf\\china_T_F_GRACE.npy',new_array)


def gen_lon_lat_list(start_lon_lat,step,length):
    lon_lat_list = []
    for i in range(length):
        lon_lat_list.append(start_lon_lat+step*i)
    return lon_lat_list
    pass



def gen_lon_lat_dic():
    '''
    生成栅格和经纬度对应的字典
    数据格式:
    dic[str(x.y)] = [lon,lat]
    :return:
    '''
    rasterized_tif = this_root+'/conf/GRACE_mask.tif'
    array, im_width, im_height, im_geotrans, im_proj = tif_to_array(rasterized_tif)
    # print(im_width, im_height, im_geotrans, im_proj)
    # array = array[::-1]
    # plt.imshow(array)
    # plt.show()
    # exit()
    clip_array = np.load(this_root+'\\conf\\china_T_F_GRACE.npy')

    print(im_geotrans)

    lon_lat_dic = {}
    for y in range(len(clip_array)):
        print(y)
        for x in range(len(clip_array[y])):
            if clip_array[y][x]:
                lon_start = im_geotrans[0]
                lon_step = im_geotrans[1]
                lon = lon_start + lon_step * x

                lat_start = im_geotrans[3]
                lat_step = im_geotrans[5]
                lat = lat_start + 179*lat_step - lat_step * y
                # print(lat_start)
                # print(lat_step)
                # print(lat)
                #
                # print(y)
                # exit()

                lon_lat_dic[str(x)+'.'+str(y)] = [lon,lat]

    np.save(this_root+'\\conf\\lon_lat_dic_GRACE',lon_lat_dic)

        # break

    # plt.imshow(clip_array)
    # plt.show()




def plot_lon_lat():
    rasterized_tif = this_root+'/conf/GRACE_mask.tif'
    array,im_width,im_height,im_geotrans,im_proj = tif_to_array(rasterized_tif)
    print(im_geotrans)
    # exit()
    # clip_dir = this_root+'\\clipped\\MOD11A2.006\\'

    npy = np.load(this_root+'conf\\china_T_F_GRACE.npy')
    lon_length = np.shape(npy)[1]
    lat_length = np.shape(npy)[0]

    lon_start = im_geotrans[0]
    lon_step = im_geotrans[1]

    lat_start = im_geotrans[3]
    lat_step = im_geotrans[5]

    interval = 1
    npy = np.ma.masked_where(npy==0,npy)
    plt.imshow(npy,'jet')
    lon_list = gen_lon_lat_list(lon_start,lon_step,lon_length)
    lat_list = gen_lon_lat_list(lat_start,lat_step,lat_length)[::-1]

    plt.xticks(range(lon_length)[::interval],lon_list[::interval])
    plt.yticks(range(lat_length)[::interval],lat_list[::interval])

    plt.grid(1)
    plt.show()



def transform_data_npz(lon_lat_dic):
    f = this_root+'GRACE\\3_GRACE_product_mean.npz'
    grace_npz = np.load(f)
    flag1 = 0

    flatten_dic = {}

    for date in grace_npz:
        print(date)
        flag1 += 1

        # start = time.time()
        npy = grace_npz[date]
        flag = 0
        # dic_key_index = []
        for pix in lon_lat_dic:
            flag += 1.
            x = int(pix.split('.')[0])
            y = int(pix.split('.')[1])
            val = npy[y][x]
            dic_key = str(lon_lat_dic[pix][0])+'_'+str(lon_lat_dic[pix][1])

            if dic_key in flatten_dic:
                flatten_dic[dic_key].append(val)
                pass
            else:
                flatten_dic[dic_key] = [val]
                pass
            # if flag == 100000:
            #     break
        # np.save(data_transform_split_folder+f,dic_key_index)

    # return flatten_dic
    print 'saving npz...'
    save_name = this_root+'GRACE\\transform_data\\data_transform'
    np.savez(save_name,**flatten_dic)
    # end = time.time()
    print(save_name)


def insert_val(val):

    f_date = this_root + 'GRACE\\3_GRACE_product_mean.npz'
    date_raw = np.load(f_date)
    date_generate = []
    for year in range(2003, 2017):
        year = str(year)
        for m in range(1, 13):
            m = '%02d' % m
            d = year + m
            date_generate.append(d)
    insert_index = []
    flag = 0
    for i in date_generate:
        if i not in date_raw:
            insert_index.append(flag)
        flag += 1

    for index in insert_index:
        val = np.insert(val, index, -999)
    return val



def interp_1d(val):
    # 1、插缺失值
    x = []
    val_new = []
    for i in range(len(val)):
        if val[i] >= -99:
            index = i
            x = np.append(x,index)
            val_new = np.append(val_new,val[i])

    interp = interpolate.interp1d(x, val_new, kind='nearest', fill_value="extrapolate")

    xi = range(len(val))
    yi = interp(xi)


    # 2、利用三倍sigma，去除离群值
    # print(len(yi))
    val_mean = np.mean(yi)
    sigma = np.std(yi)
    n = 3
    yi[(val_mean - n * sigma) > yi] = -999999
    yi[(val_mean + n * sigma) < yi] = 999999
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
        if -999999 < yi[i] < 999999:
            index = i
            xii = np.append(xii, index)
            val_new_ii = np.append(val_new_ii, yi[i])

    interp_1 = interpolate.interp1d(xii, val_new_ii, kind='nearest', fill_value="extrapolate")

    xiii = range(len(val))
    yiii = interp_1(xiii)


    # for i in range(len(yi)):
    #     if yi[i] == -999999:
    #         val_new_ii = np.append(val_new_ii, bottom)
    #     elif yi[i] == 999999:
    #         val_new_ii = np.append(val_new_ii, top)
    #     else:
    #         val_new_ii = np.append(val_new_ii, yi[i])

    return yiii


def interp_1d_spline(val):
    x = []
    val_new = []
    for i in range(len(val)):
        if val[i] >= -99:
            index = i
            x = np.append(x, index)
            val_new = np.append(val_new, val[i])

    interp = InterpolatedUnivariateSpline(x, val_new)

    xi = range(len(val))
    yi = interp(xi)

    return yi
    # interp = InterpolatedUnivariateSpline()


def time_interp():
    f = this_root + 'GRACE\\transform_data\\data_transform.npz'

    npz = np.load(f)
    interp_dic = {}
    flag = 0
    for i in npz:
        flag += 1
        print(flag,'/',len(npz))
        val = npz[i]
        val = insert_val(val)
        val_interp_spline = interp_1d_spline(val)
        interp_dic[i] = val_interp_spline
    np.savez(this_root+'GRACE\\interp_data',**interp_dic)
        # break
    pass



def normalize():
    datatrans = np.load(this_root + 'GRACE\\interp_data.npz')
    origin = []
    for i in datatrans:
        val = datatrans[i]
        origin.append(val)
    min = np.min(origin)
    max = np.max(origin)
    print(min)
    print(max)

def main():
    # grace_lon_lat_dic = np.load(this_root+'conf\\lon_lat_dic_GRACE.npy').item()
    # grace_lon_lat_dic = dict(grace_lon_lat_dic)
    # transform_data_npz(grace_lon_lat_dic)
    # time_interp()
    # datatrans = np.load(this_root+'GRACE\\interp_data.npz')
    # for i in datatrans:
    #     print(len(datatrans[i]))
    #     plt.plot(datatrans[i])
    #     plt.title(i)
    #     plt.show()
    normalize()



if __name__ == '__main__':
    main()