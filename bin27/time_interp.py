# coding=utf-8
import os
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
# from numba import jit


this_root = os.getcwd()+'\\..\\'
product = 'MOD11A2.006'

def gen_lon_lat_list(start_lon_lat,step,length):
    lon_lat_list = []
    for i in range(length):
        lon_lat_list.append(start_lon_lat+step*i)
    return lon_lat_list
    pass


def mk_dir(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)


def plot_lon_lat():
    rasterized_tif = this_root+'/conf/my.tif'
    array,im_width,im_height,im_geotrans,im_proj = clip.tif_to_array(rasterized_tif)
    print(im_geotrans)
    # exit()
    clip_dir = this_root+'\\clipped\\MOD11A2.006\\'
    clip_dir_list = os.listdir(this_root+'\\clipped\\MOD11A2.006\\')
    for f in clip_dir_list:
        npy = np.load(clip_dir+f)
        lon_length = np.shape(npy)[1]
        lat_length = np.shape(npy)[0]

        lon_start = im_geotrans[0]
        lon_step = im_geotrans[1]

        lat_start = im_geotrans[3]
        lat_step = im_geotrans[5]

        interval = 300
        npy = np.ma.masked_where(npy==0,npy)
        plt.imshow(npy,'jet')
        lon_list = gen_lon_lat_list(lon_start,lon_step,lon_length)
        lat_list = gen_lon_lat_list(lat_start,lat_step,lat_length)[::-1]

        plt.xticks(range(lon_length)[::interval],lon_list[::interval])
        plt.yticks(range(lat_length)[::interval],lat_list[::interval])

        plt.grid(1)
        plt.show()


def gen_lon_lat_dic():
    '''
    生成栅格和经纬度对应的字典
    数据格式:
    dic[str(x.y)] = [lon,lat]
    :return:
    '''
    rasterized_tif = this_root + '/conf/my.tif'
    array, im_width, im_height, im_geotrans, im_proj = clip.tif_to_array(rasterized_tif)
    clip_array = np.load(this_root+'\\conf\\china_T_F.npy')

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
                lat = lat_start + lat_step * y

                lon_lat_dic[str(x)+'.'+str(y)] = [lon,lat]

    np.save(this_root+'\\conf\\lon_lat_dic',lon_lat_dic)

        # break

    # plt.imshow(clip_array)
    # plt.show()

    pass


def write_pix_to_txt(fname,val):
    if not os.path.isfile(fname):
        with open(fname,'w') as f:
            f.write(str(val)+'\n')
        f.close()
    else:
        with open(fname,'r') as f:
            content = f.read()
        f.close()
        with open(fname,'w') as fw:
            fw.write(content)
            fw.write(str(val)+'\n')
        fw.close()

    pass


def count_python_process():
    pids = psutil.pids()
    flag = 0
    for p in pids:
        try:
            if 'python' in psutil.Process(p).name():
                # print(p)
                # print(psutil.Process(p).name())
                flag += 1
        except:
            pass

    return flag


def count_files_num():
    files_number = 0
    for root, dirs, files in os.walk(this_root + '\\data_transform\\', topdown=False):
        for name in files:
            files_number += 1
    return files_number
    pass



def transform_data(lon_lat_dic):
    '''
    将多年栅格图转换为多年像素序列
    并插值，合成月尺度
    :return:
    '''
    cliped_dir = this_root+'\\clipped\\MOD11A2.006\\'
    data_transform_folder = this_root + '\\data_transform\\'
    mk_dir(data_transform_folder)
    cliped_list = os.listdir(cliped_dir)
    flag1 = 0
    flatten_dic = {}
    for f in cliped_list:
        print(f)
        flag1 += 1
        # start = time.time()
        npy = np.load(cliped_dir+f)
        flag = 0
        for pix in lon_lat_dic:
            flag += 1.
            if flag % 100000 == 0:
                print f,round(flag/len(lon_lat_dic)*100,1),'%'
            x = int(pix.split('.')[0])
            y = int(pix.split('.')[1])
            val = npy[y][x]
            dic_key = str(lon_lat_dic[pix][0])+'_'+str(lon_lat_dic[pix][1])
            if dic_key in flatten_dic:
                flatten_dic[dic_key].append(val)
            else:
                flatten_dic[dic_key] = [val]
        if flag1 % 100 == 0:
            print('transform dic to str')
            fw = open(data_transform_folder+str(flag1)+'.dat','w')
            flatten_dic_w = str(flatten_dic)
            print('writing str to dat')
            fw.write(flatten_dic_w)
            fw.close()
            # np.save(data_transform_folder+f,flatten_dic)
            flatten_dic = {}
        elif flag1 == len(cliped_list):
            print('transform dic to str')
            fw = open(data_transform_folder + str(flag1) + '.dat', 'w')
            flatten_dic_w = str(flatten_dic)
            print('writing str to dat')
            fw.write(flatten_dic_w)
            fw.close()

        # elif flag1 == 1:
        #     print('transform dic to str')
        #     fw = open(data_transform_folder + f + '.dat', 'w')
        #     flatten_dic_w = str(flatten_dic)
        #     print('writing str to dat')
        #     fw.write(flatten_dic_w)
        #     fw.close()
        else:
            pass
        npy = None
        # plt.imshow(npy)
        # plt.show()

    pass


def gen_empty_dic_npz(lon_lat_dic):
    # data_transform_folder = this_root + '\\data_transform\\'
    data_transform_folder = 'C:\\Users\\leeya\\modis_test\\'
    empty_dic = {}
    flag = 0
    for pix in lon_lat_dic:
        flag += 1.
        if flag % 100000 == 0:
            print round(flag / len(lon_lat_dic) * 100, 1), '%'
        # x = int(pix.split('.')[0])
        # y = int(pix.split('.')[1])
        dic_key = str(lon_lat_dic[pix][0]) + '_' + str(lon_lat_dic[pix][1])
        empty_dic[dic_key] = []
    print('saving npz...')
    np.savez(data_transform_folder+'transform_data.npz', **empty_dic)
    pass


def transform_data_npz(lon_lat_dic,save_name):
    start = time.time()
    cliped_dir = this_root + '\\clipped\\MOD11A2.006\\'
    data_transform_folder = this_root + '\\data_transform\\'
    data_transform_split_folder = this_root + '\\data_transform\\split\\'
    mk_dir(data_transform_folder)
    mk_dir(data_transform_split_folder)
    cliped_list = os.listdir(cliped_dir)
    flag1 = 0

    flatten_dic = {}

    for f in cliped_list:
        print(f)
        flag1 += 1

        # start = time.time()
        npy = np.load(cliped_dir + f)
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
    np.savez(data_transform_split_folder+save_name,**flatten_dic)
    end = time.time()
    print(data_transform_split_folder + save_name, end - start, 's')



def split_lon_lat_dic(lon_lat_dic):
    flag = 0
    dic_i = {}
    split_dic = {}
    split_flag = 0
    for pix in lon_lat_dic:
        # print(pix)
        # print(lon_lat_dic[pix])
        # exit()
        flag += 1.

        dic_i[pix] = lon_lat_dic[pix]
        if flag % 100000 == 0:
            split_flag += 1
            print 'split ',split_flag
            split_dic[str(split_flag)] = dic_i
            dic_i = {}
        elif flag == len(lon_lat_dic):
            split_flag += 1
            print 'split ', split_flag
            split_dic[str(split_flag)] = dic_i
    np.savez(this_root+'\\conf\\split_lon_lat_dic',**split_dic)


def transform_data_npz_split(split_lon_lat_dic):
    # print('loading dic...')
    # split_lon_lat_dic = np.load(this_root + '\\conf\\split_lon_lat_dic.npz')
    # print('done')
    flag = 0
    for i in split_lon_lat_dic:
        # print(type(i))
        # exit()
        flag += 1
        print(flag)
        lon_lat_dic = split_lon_lat_dic[i].item()
        transform_data_npz(lon_lat_dic,i)



def interp_1d(val):
    # 1、插缺失值
    x = []
    val_new = []
    for i in range(len(val)):
        if val[i] >= 100:
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





def insert_data(val):
    download_date_dir = this_root+'download_data\\'+product+'\\'
    tif_date_dir = this_root+'data_tif\\'+product+'\\'
    download_date_dir_list = os.listdir(download_date_dir)
    tif_date_dir_list = os.listdir(tif_date_dir)
    tif_date_list = []
    for i in tif_date_dir_list:
        tif_date = i[:10]
        tif_date_list.append(tif_date)
    flag = 0
    insert_index = []
    for i in download_date_dir_list:
        if i not in tif_date_list:
            insert_index.append(flag)
        flag += 1
    for index in insert_index:
        val = np.insert(val,index,0)

    return val
    # exit()


def compose_month_data(val):
    # print(val)
    f_dir = this_root+'download_data\\'+product+'\\'
    f_list = os.listdir(f_dir)
    # insert_data()
    # print(f_list)
    # print(len(f_list))
    monthly_val = []
    for y in range(2003,2017):
        for m in range(1,13):
            monthly_sum = []
            for date in f_list:
                if str(y)+'.'+'%02d'%m in date:
                    # print(date)
                    ind = f_list.index(date)
                    monthly_sum.append(val[ind])
            monthly_mean = np.mean(monthly_sum)
            monthly_val.append(monthly_mean)
    # plt.plot(monthly_val)
    # plt.show()
    # exit()
    return monthly_val
    pass


def loop(val):
    val = insert_data(val)
    zero_num = np.count_nonzero(val == 0)
    total_num = len(val)
    percent = float(zero_num) / total_num * 100
    if percent > 50:
        array = []
    else:
        array = interp_1d(val)

    if len(array) > 0:
        # plt.plot(range(len(array)), array)
        array_month = compose_month_data(array)
        return array_month

# @jit
def time_interp():
    npz_dir = this_root+'data_transform\\split_lst\\'
    npz_list = os.listdir(npz_dir)
    save_dir = this_root + 'monthly_data_npz\\'
    mk_dir(save_dir)

    all_interp_dic = {}
    flag = 0
    for f in npz_list:
        if os.path.isfile(save_dir + f):
            print(save_dir + f + ' is already existed')
            continue
        flag += 1
        print(flag)
        if flag == 3:
            break
        print(save_dir + f)
        pool = mp.Pool()
        npz = np.load(npz_dir+f)
        per = []
        flag = 0
        start = time.time()
        interp_dic = {}

        # flag1 = 0
        muti_res = {}
        for i in npz:
            flag += 1
            if flag % 1000 == 0:
                print float(flag)/len(npz)*100,'%'
            # if flag == 1000:
            #     break
            val = npz[i]
            res = pool.apply_async(loop,(val,))
            muti_res[i]=res

        print('fetching results')
        for i in muti_res:
            array = muti_res[i].get()
            interp_dic[i] = array
            # break
        pool.close()
        pool.join()
        end = time.time()
        print(end - start, 's')
        print('saving results')
        all_interp_dic[f] = interp_dic
        # return interp_dic,f
    return all_interp_dic


def save_all_interp_dic(dic,f):
    start = time.time()
    save_dir = this_root + 'monthly_data_npz\\'
    mk_dir(save_dir)
    save_path = save_dir+f
    np.savez(save_path,**dic)
    end = time.time()
    print('save '+save_path+' success, time '+str(end-start)+' s')
    pass


def concurrent_save_all_interp_dic():
    all_interp_dic = time_interp()
    pool = mp.Pool()
    for ind in all_interp_dic:
        dic = all_interp_dic[ind]
        pool.apply_async(save_all_interp_dic, (dic,ind,))
    pool.close()
    pool.join()


def main():
    # gen_lon_lat_dic()
    start = time.time()
    print('loading dic...')
    split_lon_lat_dic = np.load(this_root + '\\conf\\split_lon_lat_dic.npz')
    print('done')

    print(len(split_lon_lat_dic))
    transform_data_npz_split(split_lon_lat_dic)

    end = time.time()
    print(end - start, ' s')

if __name__ == '__main__':
    # start = time.time()
    # f = open('D:\\MODIS\\data_transform\\2003.03.14.LST_Day_1km.tif.npy.dat','r')
    #
    # print('loading dic')
    # dic = eval(f.read())
    # print(len(dic))
    # end = time.time()
    # print(end-start,'s')
    # lon_lat_dic = np.load(this_root + '\\conf\\lon_lat_dic.npy').item()
    # print(len(lon_lat_dic))
    start = time.time()
    concurrent_save_all_interp_dic()
    end = time.time()
    print(end-start,'s')