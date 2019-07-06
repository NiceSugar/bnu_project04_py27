# coding=utf-8
import os
import numpy as np
# import time
from matplotlib import pyplot as plt
from netCDF4 import Dataset
from osgeo import gdalconst
import datetime
import osr, ogr
import gdal
import log_process
import time
import kde_plot_scatter

this_root = 'e:\\MODIS\\'



def mk_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def nc_to_npz(nc,npz_out):
    # print(nc)
    # exit()
    ncin = Dataset(nc, 'r')

    print ncin.variables

        # print(i)
    # exit()
    lat = ncin['lat']
    lon = ncin['lon']
    longitude_grid_distance = abs((lon[-1] - lon[0]) / (len(lon) - 1))
    latitude_grid_distance = -abs((lat[-1] - lat[0]) / (len(lat) - 1))
    longitude_start = lon[0]
    latitude_start = lat[0]

    time = ncin.variables['time']

    # print(time)
    # exit()
    # time_bounds = ncin.variables['time_bounds']
    # print(time_bounds)
    start = datetime.datetime(1900, 01, 01)
    # a = start + datetime.timedelta(days=5459)
    # print(a)
    # print(len(time_bounds))
    print(len(time))
    # exit()
    nc_dic = {}
    flag = 0

    valid_year = []
    for i in range(2003,2017):
        valid_year.append(str(i))

    for i in range(len(time)):

        flag += 1
        # print(time[i])
        date = start + datetime.timedelta(days=int(time[i]))
        year = str(date.year)
        month = '%02d'%date.month
        # day = '%02d'%date.day
        date_str = year+month
        if not date_str[:4] in valid_year:
            continue
        print(date_str)
        # print(date_str[:4])

        # continue
        grid = ncin.variables['pre'][i][::-1]
        # print(type(grid))
        # exit()
        grid = np.array(grid)
        # grid = np.ma.masked_where(grid>9999,grid)
        # plt.imshow(grid,vmin=0,vmax=200)
        # plt.colorbar()
        # plt.show()
        nc_dic[date_str] = grid


    print(len(nc_dic))
    print(flag)
    np.savez(npz_out,**nc_dic)


    pass


def rasterize_shp(shp, output ,x_min, y_min , x_size, y_size, x_res, y_res):
    # tif = 'D:\\MODIS\\data_tif\\MOD11A2.006\\2003.01.09.LST_Day_1km.tif'
    # shp = 'D:\\MODIS\\shp\\china_dissolve.shp'
    # output = 'D:\\MODIS\\my.tif'
    # x_min, y_min, x_size, y_size, x_res, y_res = -179.875, -89.875, 1440, 720, 0.25, 0.25
    mb_v = ogr.Open(shp)
    mb_l = mb_v.GetLayer()

    target_ds = gdal.GetDriverByName('GTiff').Create(output, x_size, y_size, 1, gdal.GDT_Byte)
    target_ds.SetGeoTransform((x_min, x_res, 0, y_min, 0, y_res))
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


def gen_mask_array(rasterized_tif,out_arr):
    # rasterized_tif = this_root+'/conf/my.tif'
    array = tif_to_array(rasterized_tif)[0]
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
    np.save(out_arr,new_array)


def clip(input_arr,clip_array,out_array):
    # tif = 'D:\\MODIS\\data_tif\\MOD11A2.006\\2003.01.01.LST_Day_1km.tif'
    # array = np.load('D:\\MODIS\\conf\\china_T_F.npy')
    input_arr[np.logical_not(clip_array)] = -1
    np.save(out_array,input_arr)
    return input_arr



def plot_annual_mean():
    npy = np.load(this_root+'CRU_warm_season_sum_new.npy').T
    annual = []
    for y in npy:
        annual.append(np.sum(y))
    # plt.plot(annual)
    # plt.show()
    fw = open('cru_pre.txt','w')
    for i in annual:
        fw.write(str(i)+'\n')
    fw.close()
    # plt.bar(range(len(annual)),annual)
    # plt.ylim(18,22)
    # plt.show()
# def do_clip():
#     fdir = 'D:\\project04\\CCI\\composed\\'
#     clipped_dir = 'D:\\project04\\CCI\\midasia_clipped\\'
#     mk_dir(clipped_dir)
#     flist = os.listdir(fdir)
#     for y in flist:
#         mk_dir(clipped_dir+y)
#         if y != '1982':
#             continue
#         for f in os.listdir(fdir+y):
#             print(fdir+y+'\\'+f)
#             arr = np.load(fdir+y+'\\'+f)
#             clip_arr = np.load('midasia.npy')[::-1]
#             out_arr = clipped_dir+y+'\\'+f
#             # print(arr, clip_arr, out_arr)
#             # exit()
#             clip(arr, clip_arr, out_arr)





def do_clip_main():
    # x_min, y_min, x_size, y_size, x_res, y_res = -179.875, -89.875, 1440, 720, 0.25, 0.25
    # shp = 'D:\\OneDrive - cug.edu.cn\\G\\project01\\project_LY_ZW\\mid_aisa\\dissolve.shp'
    # output = this_root+'midasia_shp_raster.tif'
    # x_min, y_min, x_size, y_size, x_res, y_res = -179.750, -89.750, 720, 360, 0.5, 0.5
    # rasterize_shp(shp, output, x_min, y_min, x_size, y_size, x_res, y_res)
    # rasterized_tif = this_root+'midasia_shp_raster.tif'
    # out_arr = this_root+'midasia_clip.npy'
    # arr = np.load(out_arr)

    # gen_mask_array(rasterized_tif, out_arr)
    clip_arr = np.load(this_root+'conf\\china_CRU_mask.npy')[::-1]
    # plt.imshow(clip_arr)
    # plt.show()
    npz = np.load(this_root+'CRU_precip\\pre.npz')
    for mon in npz:
        print(mon)
        npy = npz[mon]
        input_arr = npy
        clip_array = clip_arr
        out_dir = this_root+'CRU_precip\\clipped\\'
        # input_arr_ma = np.ma.masked_where(input_arr>9999,input_arr)
        # plt.imshow(input_arr_ma,vmin=0,vmax=600)
        # plt.colorbar()
        # plt.figure()
        mk_dir(out_dir)
        out_array = out_dir+mon
        clipped = clip(input_arr,clip_array,out_array)
        # clipped = np.ma.masked_where(clipped>9999,clipped)
        # clipped = np.ma.masked_where(clipped<0,clipped)
        # plt.imshow(clipped)
        # plt.colorbar()
        # plt.show()

    pass




def CRU_mean():
    '''
    把空间缩成一个点
    :return:
    '''
    year = range(1992,2016)
    valid_year = []
    for y in year:
        valid_year.append(str(y))
    mon = range(5,10)
    f_dir = this_root+'midasia_clipped\\'
    file_list = os.listdir(f_dir)
    CCI_warm_season_sum = []
    for m in mon:
        temp = []
        m = '%02d'%m
        for f in file_list:
            yi = f[:4]
            # print(yi)
            if not yi in valid_year:
                continue
            # print(f)

            # continue
            # exit()
            if m+'.npy' in f:
                print f
                # shutil.copy(this_root+'/ERA/sum/'+f,this_root+'/ERA/sum_warm_season_layer/')
                arr = np.load(f_dir+f)
                arr_sum = []
                flag = 0.
                # plt.imshow(arr)
                # plt.show()
                for i in arr:
                    for j in i:
                        if 0<j<99999:
                            flag+=1.
                            arr_sum.append(j)

                mean = sum(arr_sum)/flag
                # print mean
                temp.append(mean)
        # exit()
        CCI_warm_season_sum.append(temp)
    CCI_warm_season_sum = np.array(CCI_warm_season_sum)
    np.save(this_root+'/CRU_warm_season_sum_new',CCI_warm_season_sum)



def CRU_climatology_anomaly():
    import analysis
    layer1 = np.load(this_root+'/CRU_warm_season_sum_new'+'.npy')
    # plt.imshow(layer1)
    # plt.show()
    # exit()
    mon_mean = []
    mon_std = []
    for mon in layer1:
        mon_mean.append(np.mean(mon))
        mon_std.append(np.std(mon))
    sum_layerT = layer1.T
    # print(sum_layerT)
    # print(np.shape(sum_layerT))
    # exit()
    climat_anomaly = []


    for year in sum_layerT:
        # print len(year)
        for i in range(len(mon_mean)):
            # add std
            climat_anomaly.append((year[i]-mon_mean[i])/mon_std[i])
            # not add std
            # climat_anomaly.append(year[i]-mon_mean[i])

    mon_window = 15
    climat_anomaly_convolve = analysis.Calculate().smooth_convolve(climat_anomaly,mon_window)

    plt.figure(figsize=(16,4))
    plt.subplot(1,2,1)
    plt.plot(range(len(climat_anomaly)),climat_anomaly,linewidth = 3,alpha = 1,label = 'origin')
    plt.plot(range(len(climat_anomaly_convolve)),climat_anomaly_convolve,linewidth = 3,label = 'filter with '+str(mon_window))
    plt.title('CRU climatology anomaly')
    plt.legend()
    plt.grid()

    year_mean = []
    i = 0
    j = 0
    for y in range(len(climat_anomaly)):
        j += 1
        temp = climat_anomaly[i:i+5]
        # print np.mean(temp)
        year_mean.append(np.mean(temp))
        i += 5
        if i == len(climat_anomaly):
            break

    plt.subplot(1,2,2)
    year_window = 5
    year_mean_convolve = analysis.Calculate().smooth_convolve(year_mean,year_window)


    plt.plot(range(len(year_mean)),year_mean,linewidth = 3,alpha = 1,label = 'origin')
    plt.plot(range(len(year_mean_convolve)),year_mean_convolve,linewidth = 3,label = 'filter with '+str(year_window))


    plt.title('CCI year mean climatology anomaly')
    plt.grid()
    plt.legend()
    plt.show()

    lines = []
    for i in range(len(climat_anomaly)):
        if i < len(year_mean):
            lines.append([str(climat_anomaly[i]),str(climat_anomaly_convolve[i]),str(year_mean[i]),str(year_mean_convolve[i])])
        else:
            lines.append([str(climat_anomaly[i]),str(climat_anomaly_convolve[i]),' ',' '])

    f = open(this_root+'/CRU_std.txt','w')
    for line in lines:
        print line
        line = '\t'.join(line)+'\n'
        f.write(line)
    f.close()



def gen_lon_lat_list(start_lon_lat,step,length):
    lon_lat_list = []
    for i in range(length):
        lon_lat_list.append(start_lon_lat+step*i)
    return lon_lat_list
    pass



def gen_lon_lat_dic(rasterized_tif,mask_array,out_dic):
    '''
    生成栅格和经纬度对应的字典
    数据格式:
    dic[str(x.y)] = [lon,lat]
    :return:
    '''
    # rasterized_tif = this_root+'/conf/GRACE_mask.tif'
    # clip_array = np.load(this_root + '\\conf\\china_T_F_GRACE.npy')
    # out_dic = this_root+'\\conf\\lon_lat_dic_GRACE'

    array, im_width, im_height, im_geotrans, im_proj = tif_to_array(rasterized_tif)
    # print(im_width, im_height, im_geotrans, im_proj)
    # array = array[::-1]
    # plt.imshow(array)
    # plt.show()
    # exit()


    print(im_geotrans)
    mask_array = mask_array[::-1]
    # plt.imshow(mask_array)
    # plt.show()
    lon_lat_dic = {}
    for y in range(len(mask_array)):
        # print(y)
        for x in range(len(mask_array[y])):
            if mask_array[y][x]:
                lon_start = im_geotrans[0]
                lon_step = im_geotrans[1]
                lon = lon_start + lon_step * x

                lat_start = im_geotrans[3]
                lat_step = im_geotrans[5]
                lat = lat_start + (len(mask_array)-1)*lat_step - lat_step * y

                # print(lat_start + (len(mask_array)-1)*lat_step)
                # print(lat_step * y)
                # exit()
                # print(len(mask_array))
                # print(lat_start)
                # print(lat_step)
                # print(lat)
                # print(lon)
                # print(x)
                # print(y)
                # plt.imshow(mask_array)
                # plt.show()
                # exit()

                lon_lat_dic[str(x)+'.'+str(y)] = [lon,lat]

    np.save(out_dic,lon_lat_dic)

        # break

    # plt.imshow(clip_array)
    # plt.show()



def transform_data_npz(in_npz,lon_lat_dic,out_npz_name):
    # f = this_root+'GRACE\\3_GRACE_product_mean.npz'
    grace_npz = np.load(in_npz)
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
    # save_name = this_root+'GRACE\\transform_data\\data_transform'
    np.savez(out_npz_name,**flatten_dic)
    # end = time.time()
    print(out_npz_name)





def trans_nc_to_lon_lat_list():
    nc = r'E:\MODIS\CRU_precip\cru_ts4.02.1901.2017.pre.dat.nc'
    ncin = Dataset(nc, 'r')
    # print ncin.variables
    lon = ncin['lon']
    lat = ncin['lat']
    lon_origin = lon[0]
    lat_origin = lat[-1]
    lon_size = lon[1]-lon[0]
    lat_size = lat[1]-lat[0]
    print(lon_origin)
    print(lat_origin)
    print(lon_size)
    print(lat_size)
    # exit()
    npz = np.load(r'E:\MODIS\CRU_precip\2001.2018.npz')

    time_init = time.time()
    flag = 0
    for date in npz:
        # print(date)
        time_start = time.time()
        transform_dic = {}
        arr = npz[date]
        for i in range(len(arr)):
            for j in range(len(arr[i])):
                # print(i,j)
                lon_i = lon_origin+lon_size*j
                lat_i = lat_origin-lat_size*i
                val = arr[i][j]
                key = str(lon_i)+'_'+str(lat_i)
                # print(key)
                transform_dic[key] = val
        np.save(this_root+r'CRU_precip\transform\\'+date,transform_dic)
        time_end = time.time()
        log_process.process_bar(flag,len(npz),time_init,time_start,time_end)
        flag += 1
        # f.close()

        # plt.imshow(arr)
        # plt.colorbar()
        # plt.title(date)
        # plt.show()


def extract_value_from_stations():
    # 1、获取站点经纬度，设置50km范围lon_min,lon_max,lat_min,lat_max，存入字典
    # 2、建立空字典
    sta_pos_dic = np.load(this_root + 'ANN_input_para\\00_PDSI\\sta_pos_dic.npz')
    sta_pos_dic_range = {}
    sta_pos_dic_void = {}
    for sta in sta_pos_dic:
        # print(sta)
        sta_pos_dic_void[sta] = []
        lat = sta_pos_dic[sta][0]
        lon = sta_pos_dic[sta][1]

        lon_min = lon-0.5
        lon_max = lon+0.5

        lat_min = lat-0.5
        lat_max = lat+0.5
        sta_pos_dic_range[sta] = [[lon_min,lon_max],
                                  [lat_min,lat_max]]


    #3、读取每个月的CRU数据

    fdir = r'E:\MODIS\CRU_precip\transform\\'
    flist = os.listdir(fdir)

    CRU_vals_dic = {}
    time_init = time.time()
    flag = 0
    for f in flist:
        time_start = time.time()
        arr = np.load(fdir + f).item()
        dic = dict(arr)
        # flag = 0
        for key in dic:

            key_split = key.split('_')
            lon = float(key_split[0])
            lat = float(key_split[1])

            for sta in sta_pos_dic_range:
                sta_pos_dic_range_dic = sta_pos_dic_range[sta]
                lon_range = sta_pos_dic_range_dic[0]
                lat_range = sta_pos_dic_range_dic[1]
                lon_min = lon_range[0]
                lon_max = lon_range[1]
                lat_min = lat_range[0]
                lat_max = lat_range[1]
                if lon_min < lon < lon_max and lat_min < lat < lat_max:
                    val = dic[key]
                    sta_pos_dic_void[sta].append(val)
        for sta in sta_pos_dic_void:
            vals_list = sta_pos_dic_void[sta]
            if len(vals_list) > 0:
                key_name = sta+'_'+f[:-4]
                val = np.mean(vals_list)
                CRU_vals_dic[key_name] = val
        time_end = time.time()
        log_process.process_bar(flag,len(flist),time_init,time_start,time_end)
        flag += 1




    print('\nsaving dic...')
    np.save(r'E:\MODIS\CRU_precip\CRU_precip_dic',CRU_vals_dic)



def corr_with_insitu():
    # load insitu
    npy = np.load(r'E:\MODIS\in_situ_data\new_transform\pre_monthly_composite_dic.npy')
    dic_insitu = dict(npy.item())

    # load CRU
    npy = np.load(r'E:\MODIS\CRU_precip\CRU_precip_dic.npy')
    dic_cru = dict(npy.item())

    # corr
    insitu = []
    cru = []
    for key in dic_cru:
        if key in dic_insitu:
            val_cru = dic_cru[key]
            val_insitu = dic_insitu[key]
            if val_cru < 99999:
                cru.append(val_cru)
                insitu.append(val_insitu)
    # import random
    # random.shuffle(insitu)
    kde_plot_scatter.plot_scatter(insitu,cru)
    plt.show()


    pass



def gen_3_months_average():
    # 用CRU数据
    # this_root = os.getcwd()+'\\'

    mode = 'pre'
    if mode == 'tmp':
        data = np.load('E:\\MODIS\\CRU_tmp\\CRU_tmp_dic_filter_inf.npy').item()
        data = dict(data)
        path = 'CRU_tmp\\tmp'
    elif mode == 'pre':
        data = np.load('E:\\MODIS\\CRU_precip\\CRU_precip_dic_filter_inf.npy').item()
        data = dict(data)
        path = 'CRU_precip\\pre'
    else:
        data = None
        path = None
    # temp = dict(temp)

    date_list = []
    for year in range(2000, 2017):
        for mon in range(1, 13):
            date_list.append(str(year) + '%02d' % mon)

    new_dic = {}
    time_init = time.time()
    flag = 0
    for key in data:
        time_start = time.time()
        key_split = key.split('_')
        sta = key_split[0]
        date_str = key_split[1]
        year = int(date_str[:4])
        mon = int(date_str[-2:])

        date = datetime.datetime(year, mon, 15)
        time_delta = datetime.timedelta(30)

        date_1 = date - time_delta
        date_1_str = '%s%02d' % (date_1.year, date_1.month)

        date_2 = date - time_delta * 2
        date_2_str = '%s%02d' % (date_2.year, date_2.month)

        # print(date_1_str)
        # print(date_2_str)
        try:
            val1 = data[sta + '_' + date_str]
            # print(val1)
            val2 = data[sta + '_' + date_1_str]
            val3 = data[sta + '_' + date_2_str]
            val_mean = np.mean([val1, val2, val3])
            # print(val_mean)

            new_dic[key] = val_mean
        except Exception as e:
            # print(e)
            pass
        time_end = time.time()
        log_process.process_bar(flag, len(data), time_init, time_start, time_end)
        flag += 1
    print('saving dic...')
    np.save('E:\\MODIS\\'+ path +'_3_months_average_new', new_dic)




def gen_6_months_average():
    # 用CRU数据
    # this_root = os.getcwd()+'\\'

    mode = 'tmp'
    if mode == 'tmp':
        data = np.load('E:\\MODIS\\CRU_tmp\\CRU_tmp_dic_filter_inf.npy').item()
        data = dict(data)
        path = 'CRU_tmp\\tmp'
    elif mode == 'pre':
        data = np.load('E:\\MODIS\\CRU_precip\\CRU_precip_dic_filter_inf.npy').item()
        data = dict(data)
        path = 'CRU_precip\\pre'
    else:
        data = None
        path = None
    # temp = dict(temp)

    date_list = []
    for year in range(2000, 2017):
        for mon in range(1, 13):
            date_list.append(str(year) + '%02d' % mon)

    new_dic = {}
    time_init = time.time()
    flag = 0
    for key in data:
        time_start = time.time()
        key_split = key.split('_')
        sta = key_split[0]
        date_str = key_split[1]
        year = int(date_str[:4])
        mon = int(date_str[-2:])

        date = datetime.datetime(year, mon, 15)
        time_delta = datetime.timedelta(30)

        date_1 = date - time_delta * 1
        date_1_str = '%s%02d' % (date_1.year, date_1.month)

        date_2 = date - time_delta * 2
        date_2_str = '%s%02d' % (date_2.year, date_2.month)

        date_3 = date - time_delta * 3
        date_3_str = '%s%02d' % (date_2.year, date_3.month)

        date_4 = date - time_delta * 4
        date_4_str = '%s%02d' % (date_2.year, date_4.month)

        date_5 = date - time_delta * 5
        date_5_str = '%s%02d' % (date_2.year, date_5.month)

        # print(date_1_str)
        # print(date_2_str)
        try:
            val1 = data[sta + '_' + date_str]
            val2 = data[sta + '_' + date_1_str]
            val3 = data[sta + '_' + date_2_str]
            val4 = data[sta + '_' + date_3_str]
            val5 = data[sta + '_' + date_4_str]
            val6 = data[sta + '_' + date_5_str]
            val_mean = np.mean([val1, val2, val3, val4, val5, val6])
            # print(val_mean)

            new_dic[key] = val_mean
        except Exception as e:
            # print(e)
            pass
        time_end = time.time()
        log_process.process_bar(flag, len(data), time_init, time_start, time_end)
        flag += 1
    print('saving dic...')
    np.save('E:\\MODIS\\'+ path +'_6_months_average', new_dic)




def filter_inf():
    # CRU中存在无限值 去掉inf
    # this_root = os.getcwd()+'\\'

    mode = 'tmp'
    if mode == 'tmp':
        data = np.load('E:\\MODIS\\CRU_tmp\\CRU_tmp_dic.npy').item()
        data = dict(data)
        path = 'E:\\MODIS\\CRU_tmp\\CRU_tmp_dic_filter_inf.npy'
    elif mode == 'pre':
        data = np.load('E:\\MODIS\\CRU_precip\\CRU_precip_dic.npy').item()
        data = dict(data)
        path = 'E:\\MODIS\\CRU_precip\\CRU_precip_dic_filter_inf.npy'
    else:
        data = None
        path = None

    new_dic = {}
    for key in data:
        val = data[key]
        if val < 9999:
            new_dic[key] = val
    np.save(path,new_dic)






def main():
    # extract_value_from_stations()
    # nc = this_root + 'CRU_tmp\\nc\\cru_ts4.03.2011.2018.tmp.dat.nc'
    # nc_out = this_root+'CRU_tmp\\npz\\2011.2018'
    # nc_to_npz(nc,nc_out)
    # shp = this_root+'shp\\china_dissolve.shp'
    # print(shp)
    # nc = this_root+'CRU_precip\\cru_ts4.02.1901.2017.pre.dat.nc'
    # out = this_root+'CRU_precip\\pre'
    # nc_to_npz(nc,out)
    # output = this_root+'conf\\china_CRU.tif'
    # out_arr = this_root+'conf\\china_CRU_mask'
    # x_min, y_min, x_size, y_size, x_res, y_res = -179.875, -89.875, 720, 360, 0.5, 0.5
    # rasterize_shp(shp, output, x_min, y_min, x_size, y_size, x_res, y_res)
    # gen_mask_array(output,out_arr)
    # clip(input_arr, clip_array, out_array)
    # arr = np.load(this_root+'/CRU_warm_season_sum_new.npy')
    # plt.imshow(arr)
    # plt.colorbar()
    # plt.show()
    # CRU_climatology_anomaly()
    # do_clip_main()
    # rasterized_tif = this_root+'/conf/china_CRU.tif'
    # mask_array = np.load(this_root + '\\conf\\china_CRU_mask.npy')

    # print(flag)
    # plt.imshow(mask_array)
    # plt.show()
    # out_dic = this_root+'\\conf\\lon_lat_dic_CRU'
    # in_npz = this_root+'CRU_precip\\pre.npz'
    # lon_lat_dic = np.load(out_dic+'.npy').item()
    # lon_lat_dic = dict(lon_lat_dic)
    # out_npz_name = this_root+'CRU_precip\\cru_transfomed'
    # transform_data_npz(in_npz,lon_lat_dic,out_npz_name)
    # gen_lon_lat_dic(rasterized_tif, mask_array, out_dic)

    # arr = np.load(out_dic+'.npy').item()
    # for i in arr:
    #     print(i)
    #     print(arr[i])
    # plt.imshow(mask_array[::-1])
    # plt.show()
    # npz_name = this_root + 'CRU_precip\\cru_transfomed.npz'
    # npz = np.load(npz_name)
    # for i in npz:
    #     print(len(npz[i]))
    #     plt.plot(npz[i])
    #     plt.title(i)
    #     plt.show()
    # nc = r'E:\MODIS\CRU_precip\cru_ts4.02.1901.2017.pre.dat.nc'
    # ncout = r'E:\MODIS\CRU_precip\2001.2008'
    # nc_to_npz(nc,ncout)
    # trans_nc_to_lon_lat_list()
    # extract_value_from_stations()
    gen_6_months_average()

    pass


if __name__ == '__main__':
    # npy = np.load(r'E:\MODIS\CRU_tmp\transform\200506.npy').item()
    # dic = dict(npy)
    # for key in dic:
    #     print(key)
    #     print(dic[key])
    #     print('*'*8)
    main()
    # path = 'E:\\MODIS\\CRU_precip\\CRU_precip_dic_filter_inf.npy'
    # npy = np.load(path).item()
    # for i in npy:
    #     print(i,npy[i])
