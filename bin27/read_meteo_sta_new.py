# coding=utf-8

import os
import numpy as np
import multiprocessing as mp
from matplotlib import pyplot as plt
import time
import log_process
import kde_plot_scatter
from scipy import stats
import datetime

this_root = os.getcwd()+'\\'

def mk_dir(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)


def gen_sta_num_list():
    f_dir = this_root+'data\\PRE18\\'
    # dic_output = this_root+'in_situ_data\\PRE_transform\\'
    # mk_dir(dic_output)
    f_list = os.listdir(f_dir)
    sta_num_list = []
    time_init = time.time()
    flag = 0
    for f in f_list:
        time_start = time.time()
        fr = open(f_dir+f,'r')
        lines = fr.readlines()
        fr.close()
        # flag = 0
        for line in lines:
            line = line.split()
            sta = line[0]
            sta_num_list.append(sta)
        time_end = time.time()
        log_process.process_bar(flag,len(f_list),time_init,time_start,time_end)
        flag += 1
    sta_num_list = set(sta_num_list)
    print('len(sta_num_list):%s'%len(sta_num_list))
    print('saving...')
    np.save(this_root+'data\\sta_num_list',sta_num_list)


def gen_pre_raw_dic():
    sta_list = np.load(this_root+'data\\sta_num_list.npy').item()
    sta_list = list(sta_list)
    sta_list.sort()
    sta_val_dic = {}
    for sta in sta_list:
        sta_val_dic[sta] = {}
    # exit()
    f_dir = this_root + 'data\\PRE18\\'
    dic_output = this_root+'data\\PRE_transform\\'
    mk_dir(dic_output)
    f_list = os.listdir(f_dir)
    flag = 0
    time_init = time.time()
    for f in f_list:
        time_start = time.time()
        fr = open(f_dir+f,'r')
        lines = fr.readlines()
        fr.close()
        # flag = 0
        for line in lines:
            line = line.split()
            # print(line)
            sta = line[0]
            year = int(line[4])
            mon = int(line[5])
            day = int(line[6])
            val_str = float(line[-4])
            if val_str < 3000:
                pre = val_str/10.
                key = str(year)+'%02d'%mon+'%02d'%day
                sta_val_dic[sta][key] = pre
        time_end = time.time()
        log_process.process_bar(flag,len(f_list),time_init,time_start,time_end,f)
        flag += 1


    print('\nsaving dic...')
    np.savez(this_root+'data\\pre_sta_val_dic_raw',**sta_val_dic)


def gen_tmp_raw_dic():
    sta_list = np.load(this_root + 'data\\sta_num_list.npy').item()
    sta_list = list(sta_list)
    sta_list.sort()
    sta_val_dic = {}
    for sta in sta_list:
        sta_val_dic[sta] = {}
    # exit()
    f_dir = this_root + 'data\\TEM18\\'
    f_list = os.listdir(f_dir)
    flag = 0
    time_init = time.time()
    for f in f_list:
        time_start = time.time()
        fr = open(f_dir + f, 'r')
        lines = fr.readlines()
        fr.close()
        # flag = 0
        for line in lines:
            line = line.split()
            # print(line)
            sta = line[0]
            year = int(line[4])
            mon = int(line[5])
            day = int(line[6])
            val_str = float(line[-6])
            if val_str < 3000:
                tmp = val_str / 10.
                key = str(year) + '%02d' % mon + '%02d' % day
                # print(sta,key,tmp)
                # print(tmp)
                sta_val_dic[sta][key] = tmp
        time_end = time.time()
        log_process.process_bar(flag, len(f_list), time_init, time_start, time_end, f)
        flag += 1

    print('\nsaving dic...')
    np.savez(this_root + 'data\\tmp_sta_val_dic_raw', **sta_val_dic)


def composite_tmp_monthly():
    npz = np.load(this_root + 'data\\tmp_sta_val_dic_raw.npz')

    date_list_gen = []

    for year in range(1951,2018):
        for mon in range(1,13):
            date_list_gen.append(str(year)+'%02d'%mon)

    tmp_monthly_composite_dic = {}
    time_init = time.time()
    flag = 0
    for sta in npz:
        time_start = time.time()
        npy = npz[sta]
        one_sta_dic = dict(npy.item())
        for date_str in date_list_gen:

            one_mon_sum = 0.
            days = 0.
            for date in one_sta_dic:
                year_mon = date[:6]
                if year_mon == date_str:
                    days += 1
                    val = one_sta_dic[date]
                    one_mon_sum += val
            if days > 0:
                one_mon_mean = one_mon_sum/days
                key = sta+'_'+date_str
                tmp_monthly_composite_dic[key] = one_mon_mean
        time_end = time.time()
        log_process.process_bar(flag,len(npz),time_init,time_start,time_end)
        flag+=1
    print('\nsaving dic...')
    np.save(this_root+'data\\tmp_monthly_composite_dic',tmp_monthly_composite_dic)



def composite_pre_monthly():
    npz = np.load(this_root + 'data\\pre_sta_val_dic_raw.npz')

    date_list_gen = []

    for year in range(1951,2018):
        for mon in range(1,13):
            date_list_gen.append(str(year)+'%02d'%mon)

    pre_monthly_composite_dic = {}
    time_init = time.time()
    flag = 0
    for sta in npz:
        time_start = time.time()
        npy = npz[sta]
        one_sta_dic = dict(npy.item())
        for date_str in date_list_gen:

            one_mon_sum = 0.
            days = 0.
            for date in one_sta_dic:
                year_mon = date[:6]
                if year_mon == date_str:
                    days += 1
                    val = one_sta_dic[date]
                    one_mon_sum += val
            if days > 0:
                one_mon_mean = one_mon_sum
                key = sta+'_'+date_str
                pre_monthly_composite_dic[key] = one_mon_mean
        time_end = time.time()
        log_process.process_bar(flag,len(npz),time_init,time_start,time_end)
        flag+=1
    print('\nsaving dic...')
    np.save(this_root+'data\\pre_monthly_composite_dic',pre_monthly_composite_dic)





def main():
    composite_pre_monthly()
    # npz = np.load(this_root+'data\\tmp_sta_val_dic_raw.npz')
    # for sta in npz:
    #     npy = npz[sta]
    #     one_sta_dic = dict(npy.item())
    #     for date in one_sta_dic:
    #         print(sta,date,one_sta_dic[date])
    #     exit()
    pass
if __name__ == '__main__':
    main()