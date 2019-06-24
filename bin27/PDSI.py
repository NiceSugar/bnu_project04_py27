# coding=utf-8

import os
this_root = 'e:\\MODIS\\'
import numpy as np
import multiprocessing as mp
from matplotlib import pyplot as plt
import time
import log_process
import kde_plot_scatter
# import scipy
from scipy import stats
import datetime

def mk_dir(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)


def pre_kernel(lines,stations,save_path):
    station_dic = {}
    for s in stations:
        monthly_sum = 0.
        flag = 0.
        for line in lines:
            line = line.split('\n')[0]
            sta = line[0:5]
            if sta == s:
                val = float(line[50:55])
                if val < 20000:
                    monthly_sum += val
                    flag += 1
        if flag > 0:
            # print(s)
            mean = monthly_sum
            # print(mean)
            station_dic[s] = mean
            # return mean
    print('saving '+save_path+'...')
    np.savez(save_path,**station_dic)
    print(save_path,'success')
    # return station_dic
            # print(np.mean(monthly_vals))
    # return 1
    pass

def composite_pre():
    f_dir = this_root+'PDSI\\in_situ\\PRE18\\'
    dic_output = this_root+'PDSI\\PRE_transform\\'
    mk_dir(dic_output)
    f_list = os.listdir(f_dir)

    pool = mp.Pool()
    # date_dic = {}
    flag = 0
    for f in f_list:
        flag += 1

        print(flag,'/',len(f_list))
        date = f.split('-')[-1].split('.')[-2]

        fr = open(f_dir+f,'r')
        lines = fr.readlines()
        stations = []
        for line in lines:
            line = line.split('\n')[0]
            sta = line[0:5]
            stations.append(sta)
        # exit()
        stations = set(stations)

        save_path = dic_output+date
        # print(save_path)
        pool.apply_async(pre_kernel,args=(lines,stations,save_path,))
    pool.close()
    pool.join()



def tem_kernel(lines,stations,save_path):
    station_dic = {}
    for s in stations:
        monthly_sum = 0.
        flag = 0.
        for line in lines:
            line = line.split('\n')[0]
            sta = line[0:5]
            if sta == s:
                val = float(line[50:55])
                if val < 20000:
                    monthly_sum += val
                    flag += 1
        if flag > 0:
            # print(s)
            mean = monthly_sum/flag
            # print(mean)
            station_dic[s] = mean
            # return mean
    print('saving '+save_path+'...')
    np.savez(save_path,**station_dic)
    print(save_path,'success')
    # return station_dic
            # print(np.mean(monthly_vals))
    # return 1
    pass

def composite_tem():
    '''
    **********
    修改最低温
    **********
    :return:
    '''
    f_dir = this_root+'PDSI\\in_situ\\TEM18\\'
    dic_output = this_root+'PDSI\\TEM_transform\\'
    mk_dir(dic_output)
    f_list = os.listdir(f_dir)

    pool = mp.Pool()
    # date_dic = {}
    flag = 0
    for f in f_list:
        flag += 1

        print(flag,'/',len(f_list))
        date = f.split('-')[-1].split('.')[-2]

        fr = open(f_dir+f,'r')
        lines = fr.readlines()
        stations = []
        for line in lines:
            line = line.split('\n')[0]
            print(line)
            sta = line[0:5]
            val = float(line[50:55])
            print(val)
            print('*'*8)
            stations.append(sta)

        stations = set(stations)

        save_path = dic_output+date
        # print(save_path)
        pool.apply_async(tem_kernel,args=(lines,stations,save_path,))
    pool.close()
    pool.join()


def composite_month(fdir,dic_save_path):
    # fdir = this_root+'PDSI\\TEM_transform\\'
    flist = os.listdir(fdir)
    valid_year = []
    sta_npz = np.load(this_root+'ANN_input_para\\00_PDSI\\sta_pos_dic.npz')

    for y in range(1961,2018):
        valid_year.append(str(y))
    all_sta_dic = {}
    for sta in sta_npz:
        all_sta_dic[sta] = {}

    for f in flist:
        date = f.split('.')[0]
        # print(date)
        # exit()
        if f[:4] not in valid_year:
            continue
        print 'loding ',fdir+f
    #     # print(f[4:6])
        one_month = np.load(fdir+f)
        for sta in one_month:
            # all_sta_dic[sta] = []
            val = float(one_month[sta])/10.
            try:
                all_sta_dic[sta][date]=val
            except:
                pass
    print 'saving dic...',dic_save_path
    np.savez(dic_save_path,**all_sta_dic)
    # for i in all_sta_dic:
    #     print(i)
    #     print(all_sta_dic[i])
    #     print('*'*80)
        # print(i)
    # exit()
    # # exit()
    # for sta in sta_npz:
    #     for mon in all_mon_dic:
    #         for i in mon:
    #             print(i)
    #         exit()




    # all_sta_dic = {}
    # for f in flist:
    #     if f[:4] not in valid_year:
    #         continue
    #     # print(f[4:6])
    #     one_month = np.load(fdir+f)
    #     print(f)
    #
    #     for s in one_month:
    #         print(s)
    #         val = one_month[s]/10
    #         lon = sta_npz[s][1]
    #         lat = sta_npz[s][0]
    #
    #     exit()
    #     # for sta in sta_npz:




def preprare_PDSI(mode):

    '''
    生成 monthly_P 和 monthly_T
    :param mode:
    :return:
    '''
    mk_dir(this_root+'PDSI\\PDSI_result\\')
    if mode == 'P':
        tem_dic = np.load(this_root+'PDSI\\pre_dic.npz')
        monthly_file = 'monthly_P'
    elif mode == 'T':
        tem_dic = np.load(this_root + 'PDSI\\tem_dic.npz')
        monthly_file = 'monthly_T'
    else:
        tem_dic=[]
        monthly_file = ''
        print('error')
        exit()
    print(len(tem_dic))

    date = []
    for y in range(1961,2018):
        y = str(y)
        for m in range(1,13):
            m = '%02d'%m
            date_i = y+m
            date.append(date_i)
            # exit()
    flag = 0
    for sta in tem_dic:
        flag+=1
        if flag % 100 == 0:
            print(flag,'/',len(tem_dic))
        # exit()
        mk_dir(this_root+'PDSI\\PDSI_result\\'+sta+'\\')
        one_sta_dic = tem_dic[sta].item()
        one_sta = []

        for d in date:
            try:
                one_sta.append(one_sta_dic[d])
            except:
                one_sta.append(-99.)
        one_sta = np.array(one_sta)
        one_sta = one_sta.reshape(len(one_sta)/12,12)

        fw = open(this_root+'PDSI\\PDSI_result\\'+sta+'\\'+monthly_file,'w')
        for i in range(len(one_sta)):
            year = str(1961+i)
            val_str = []
            for mon in one_sta[i]:
                # print(mon)
                mon = '%0.3f'%mon
                val_str.append(mon)
            # exit()
            fw.write(year+'\t'+'\t'.join(val_str)+'\n')
        fw.close()
        # print(len(one_sta))
        # plt.plot(one_sta)
        # plt.show()
        # exit()
    # npz = np.load(this_root+'PDSI\\in_situ\\PRE_transform.npz')
    # arr = npz['arr_0']
    # print(arr)
    # dic = np.load('test_dic.npz')
    # for i in dic:
    #     # print(i)
    #     # print(dic[i])
    #     onesta = dic[i].item()
    #     # print(len(onesta))
    #     for date in onesta:
    #         print(i,date)
    #         # print(date)
    #         print(onesta[date])
    #         print('*'*80)
        # exit()
    pass



def gen_parameter():
    '''
    生成sc-PDSI参数，AWC 和 站点纬度
    Returns:

    '''
    f = open(this_root+'PDSI\\awc_wujj.txt','r')
    f.readline()
    lines = f.readlines()
    flag = 0
    for line in lines:
        flag += 1
        print(flag)
        line = line.split('\n')[0].split(',')
        sta = str(int(float(line[1])))
        lat = '%0.5f'%float(line[2])
        awc_class = line[-1]
        # print(sta)
        fw = open(this_root+'PDSI\\PDSI_result\\'+sta+'\\parameter','w')
        fw.write(awc_class+'\t'+lat+'\n')
        fw.close()
        # print([sta,lat,awc_class])
        # print(lat)
        # print(awc_class)
        # exit()

def gen_normal_T():

    '''
    生成 monthly_P 和 monthly_T
    :param mode:
    :return:
    '''
    mk_dir(this_root+'PDSI\\PDSI_result\\')
    tem_dic = np.load(this_root + 'PDSI\\tem_dic.npz')
    date = []
    for y in range(1961,2018):
        y = str(y)
        for m in range(1,13):
            m = '%02d'%m
            date_i = y+m
            date.append(date_i)
            # exit()
    flag = 0
    for sta in tem_dic:
        # print(sta)
        flag+=1
        # if flag % 100 == 0:
        print(flag,'/',len(tem_dic))
        # exit()
        mk_dir(this_root+'PDSI\\PDSI_result\\'+sta+'\\')
        one_sta_dic = tem_dic[sta].item()
        one_sta = []

        for d in date:
            try:
                one_sta.append(one_sta_dic[d])
            except:
                one_sta.append(-99.)
        one_sta = np.array(one_sta)
        one_sta = one_sta.reshape(len(one_sta)/12,12).T
        # for
        # print(len(one_sta))
        normal_T = []
        for m in one_sta:
            sum = 0.
            flag_t = 0.
            for y in m:
                if y > -90:
                    sum += y
                    flag_t += 1.
            mean = sum/flag_t
            normal_T.append('%0.3f'%mean)
        fw = open(this_root+'PDSI\\PDSI_result\\'+sta+'\\mon_T_normal','w')
        fw.write('\t'.join(normal_T))
        fw.close()


def cal_PDSI():
    '''
        通过SC-PDSI.exe 计算PDSI
        Returns:

        '''
    PDSI_dir = this_root+'PDSI\\PDSI_result\\'
    sta_list = os.listdir(PDSI_dir)
    flag = 0
    pdsi_exe_path = this_root+'PDSI\\scPDSI\\sc-pdsi.exe'
    start = time.time()
    for sta in sta_list:
        start_i = time.time()
        flag += 1
        print sta, flag, '/', len(sta_list)
        path = PDSI_dir + sta + '\\'
        os.system(pdsi_exe_path + ' -x all -m -s -i' + path + ' -o' + path)
        # print(pdsi_exe_path+' -x all -m -s -i'+path+' -o'+path)
        # exit()
        print '*' * 80
        end_i = time.time()
        duration = end_i - start_i
        left = len(sta_list) - flag
        left_time = left * duration
        elapsed_time = end_i - start
        print 'estimated time left', '%.2f' % (left_time / 60.), 'elapsed time %.2f' % (elapsed_time / 60.)
        # exit()
    pass


def get_PDSI():
    resurlt_dir = this_root+'PDSI\\PDSI_result\\'
    f_list = os.listdir(resurlt_dir)
    all_sta_dic = {}
    for folder in f_list:

        pdsi_f = resurlt_dir+folder+'\\monthly\\self_cal\\PDSI.tbl'
        if not os.path.isfile(pdsi_f):
            continue
        print(folder)
        f = open(pdsi_f,'r')
        lines = f.readlines()
        one_sta_dic = {}
        for line in lines:
            line = line.split('\n')[0].split(' ')
            new_line = []
            # print(line)
            for l in line:
                try:
                    new_line.append(float(l))
                except:
                    pass
            one_sta_dic[int(new_line[0])] = new_line[1:]
        # print(one_sta_dic)
        all_sta_dic[folder] = one_sta_dic
    np.savez(this_root+'PDSI\\PDSI_result.npz',**all_sta_dic)
            # print(len(new_line))
            # print(new_line)
        # exit()



def gen_dependent_pdsi():
    # 去除无效值
    # key = 50136_200411
    pdsi = np.load(this_root + 'PDSI\\PDSI_result.npz')
    pdsi_out = this_root + 'PDSI\\PDSI_result_filter'
    valid_year = []
    for y in range(2000,2018):
        valid_year.append(y)
    independent_pdsi = {}
    time_init = time.time()
    flag = 0
    for sta in pdsi:
        time_start = time.time()
        for year in pdsi[sta].item():
            if year in valid_year:
                # print(type(i))
                # print(year)
                # print(sta,pdsi[sta].item()[year])
                for mon,val in enumerate(pdsi[sta].item()[year]):
                    key = sta+'_'+str(year)+'%02d'%(mon+1)
                    # print(key)
                    # print(val)
                    if -10 < val < 10:
                        independent_pdsi[key] = val
                    # time.sleep(0.3)
        time_end = time.time()
        log_process.process_bar(flag,len(pdsi),time_init,time_start,time_end,str(flag)+'/'+str(len(pdsi)))
        flag += 1
    print 'saving dic...'
    np.save(pdsi_out,independent_pdsi)

    # key = 50136_200411
    # npz = r'D:\ly\MODIS\train_test_data\03_VSWI\03_VSWI.npz'
    # arr = np.load(npz)
    # for i in arr:
    #     print(i)
    #     time.sleep(0.3)


def gen_dependent_pdsi1():
    # 去除无效值
    # key = 2003
    pdsi = np.load(this_root + 'PDSI\\project02_pdsi\\self_cal_all_sta_dic.npz')
    pdsi_out = this_root + 'PDSI\\project02_pdsi\\PDSI_result_filter'
    valid_year = []
    # oneyear_filtered_pdsi = {}
    for y in range(2000, 2018):
        # oneyear_filtered_pdsi[y] = []
        valid_year.append(y)

    time_init = time.time()
    flag = 0

    filtered_pdsi = {}
    for sta in pdsi:
        oneyear_filtered_pdsi = {}
        for y in range(2000, 2018):
            oneyear_filtered_pdsi[y] = []
            valid_year.append(y)
        time_start = time.time()
        onesta_pdsi_dic = pdsi[sta].item()

        for year in onesta_pdsi_dic:
            if year in valid_year:
                vals = onesta_pdsi_dic[year]
                for val in vals:
                    if -10 < val < 10:
                        oneyear_filtered_pdsi[year].append(val)
        # print(oneyear_filtered_pdsi)
        filtered_pdsi[sta] = oneyear_filtered_pdsi
        time_end = time.time()
        log_process.process_bar(flag, len(pdsi), time_init, time_start, time_end, str(flag) + '/' + str(len(pdsi)))
        flag += 1
    print('saving...')
    np.savez(pdsi_out,**filtered_pdsi)



def pre_tem_pdsi_corr():

    valid_year = []
    for y in range(2003,2017):
        valid_year.append(y)
    date_list = []
    for y in valid_year:
        for m in range(1, 13):
            date_list.append(str(y) + '%02d' % m)


    tem_dic = np.load(this_root + 'PDSI\\tem_dic.npz')
    print('processing temperature...')
    sta_tem_dic = {}
    for sta in tem_dic:
        # print(sta)
        # print(tem_dic[sta])
        one_sta_tem_dic = tem_dic[sta].item()
        one_sta = []
        for key in date_list:
            try:
                one_sta.append(one_sta_tem_dic[key])
            except:
                pass
        if len(one_sta) == 168:
            sta_tem_dic[sta] = one_sta


    pre_dic = np.load(this_root + 'PDSI\\pre_dic.npz')
    print('processing precipitation...')
    sta_pre_dic = {}
    for sta in pre_dic:
        # print(sta)
        # print(tem_dic[sta])
        one_sta_pre_dic = pre_dic[sta].item()
        one_sta = []
        for key in date_list:
            try:
                one_sta.append(one_sta_pre_dic[key])
            except:
                pass
        if len(one_sta) == 168:
            sta_pre_dic[sta] = one_sta

    pdsi = np.load(this_root+'PDSI\\PDSI_result_filter.npz')
    X = []
    Y = []
    Z = []
    flag = 0
    for sta in sta_pre_dic:
        flag += 1
        print(flag,'/',len(pdsi))
        # print(sta)
        try:
            onesta = pdsi[sta].item()
        except:
            one_sta = []
            continue
        onesta_tem = sta_tem_dic[sta]
        onesta_pre = sta_pre_dic[sta]
        pdsi_line = []
        for i in onesta:
            if not i in valid_year:
                continue
            # print(i)
            for m in onesta[i]:
                pdsi_line.append(m)
            # pdsi_line.append(onesta[i])
        if len(pdsi_line) == 168:
            for i in range(len(pdsi_line)):
                X.append(onesta_tem[i])
                Y.append(onesta_pre[i])
                Z.append(pdsi_line[i])

    # np.save(this_root+'PDSI\\')
    # r = stats.pearsonr(X,Y)
    # print(r)
    print('saving')
    print(len(X))
    print(len(Y))
    print(len(Z))
    np.save(this_root+'PDSI\\x_temp',X)
    np.save(this_root+'PDSI\\y_pre',Y)
    np.save(this_root+'PDSI\\z_pdsi',Z)
    # kde_plot_scatter.plot_scatter(X[::50],Y[::50])
    # plt.figure()
    # plt.plot(Y)
    # plt.figure()
    # plt.plot(Z)
    # plt.figure()
    # plt.scatter(Y,Z)
    # plt.show()


def pre_tem_pdsi_corr_new():

    # 使用 project02的pdsi

    pdsi = np.load(this_root+'PDSI\\project02_pdsi\\PDSI_result_filter.npz')

    valid_year = []
    for y in range(2003,2016):
        valid_year.append(y)
    date_list = []
    for y in valid_year:
        for m in range(1, 13):
            date_list.append(str(y) + '%02d' % m)


    tem_dic = np.load(this_root + 'PDSI\\tem_dic.npz')
    print('processing temperature...')
    sta_tem_dic = {}
    for sta in tem_dic:
        # print(sta)
        # print(tem_dic[sta])
        one_sta_tem_dic = tem_dic[sta].item()
        one_sta = []
        for key in date_list:
            try:
                one_sta.append(one_sta_tem_dic[key])
            except:
                pass
        if len(one_sta) == 156:
            sta_tem_dic[sta] = one_sta


    pre_dic = np.load(this_root + 'PDSI\\pre_dic.npz')
    print('processing precipitation...')
    sta_pre_dic = {}
    for sta in pre_dic:
        # print(sta)
        # print(tem_dic[sta])
        one_sta_pre_dic = pre_dic[sta].item()
        one_sta = []
        for key in date_list:
            try:
                one_sta.append(one_sta_pre_dic[key])
            except:
                pass
        if len(one_sta) == 156:
            sta_pre_dic[sta] = one_sta

    X = []
    Y = []
    Z = []
    flag = 0
    for sta in sta_pre_dic:
        flag += 1
        print(flag, '/', len(sta_pre_dic))
        # print(sta)
        try:
            onesta = pdsi[sta].item()
        except:
            one_sta = []
            continue
        onesta_tem = sta_tem_dic[sta]
        onesta_pre = sta_pre_dic[sta]
        pdsi_line = []
            # if not i in valid_year:
            #     continue
        for y in range(2003, 2016):
            # print(i)
            # print(type(i))
            for m in onesta[y]:
                # print(m)
                pdsi_line.append(m)

        # print(len(pdsi_line))
        if len(pdsi_line) == 156:
            for i in range(len(pdsi_line)):
                X.append(onesta_tem[i])
                Y.append(onesta_pre[i])
                Z.append(pdsi_line[i])


    print(np.shape(X))
    print(np.shape(Y))
    print(np.shape(Z))


    kde_plot_scatter.plot_scatter(X[::50],Y[::50])
    kde_plot_scatter.plot_scatter(Y[::50],Z[::50])
    kde_plot_scatter.plot_scatter(X[::50],Z[::50])

    plt.figure()
    plt.plot(Z)
    plt.title('pdsi')

    plt.show()



def gen_temp_anomaly():
    valid_year = []
    for y in range(2003, 2016):
        valid_year.append(y)
    date_list = []
    for y in valid_year:
        for m in range(1, 13):
            date_list.append(str(y) + '%02d' % m)


    tem_dic = np.load(this_root + 'PDSI\\tem_dic.npz')
    print('processing temperature...')
    sta_tem_dic = {}

    time_init = time.time()
    flag = 0
    for sta in tem_dic:
        time_start = time.time()
        # print(sta)
        # print(tem_dic[sta])
        one_sta_tem_dic = tem_dic[sta].item()
        one_sta = []
        for key in date_list:
            try:
                one_sta.append(one_sta_tem_dic[key])
            except:
                pass
        one_sta = np.array(one_sta)
        try:
            one_sta = one_sta.reshape(13,12)
        except:
            continue

        one_month_average = []
        one_month_std = []

        for i in one_sta.T:
            mean_val = np.mean(i)
            std_val = np.std(i)
            one_month_average.append(mean_val)
            one_month_std.append(std_val)

        anomaly_val = []
        for i in one_sta:
            val = (i-one_month_average)/one_month_std
            anomaly_val.append(val)
        anomaly_val = np.array(anomaly_val)

        # plt.figure()
        # plt.plot(anomaly_val.flatten())
        #
        # plt.figure()
        # plt.plot(one_sta.flatten())
        # plt.show()

        anomaly_val_result = anomaly_val.flatten()

        # if len(one_sta) == 156:
        sta_tem_dic[sta] = anomaly_val_result
        time_end = time.time()
        log_process.process_bar(flag,len(tem_dic),time_init,time_start,time_end,sta)
        flag+=1
    print('\nsaving...')
    np.save(this_root+'PDSI\\temp_anomaly_2003-2015',sta_tem_dic)


def gen_precip_anomaly():
    valid_year = []
    for y in range(2003, 2016):
        valid_year.append(y)
    date_list = []
    for y in valid_year:
        for m in range(1, 13):
            date_list.append(str(y) + '%02d' % m)

    tem_dic = np.load(this_root + 'PDSI\\pre_dic.npz')
    print('processing temperature...')
    sta_tem_dic = {}

    time_init = time.time()
    flag = 0
    for sta in tem_dic:
        if sta == '56247':
            continue
        time_start = time.time()
        # print(sta)
        # print(tem_dic[sta])
        one_sta_tem_dic = tem_dic[sta].item()
        one_sta = []
        for key in date_list:
            try:
                one_sta.append(one_sta_tem_dic[key])
            except:
                pass
        one_sta = np.array(one_sta)
        try:
            one_sta = one_sta.reshape(13, 12)
        except:
            continue

        one_month_average = []
        one_month_std = []

        for i in one_sta.T:
            mean_val = np.mean(i)
            std_val = np.std(i)
            one_month_average.append(mean_val)
            one_month_std.append(std_val)

        anomaly_val = []
        for i in one_sta:
            val = (i - one_month_average) / one_month_std
            anomaly_val.append(val)
        anomaly_val = np.array(anomaly_val)

        # plt.figure()
        # plt.plot(anomaly_val.flatten())
        #
        # plt.figure()
        # plt.plot(one_sta.flatten())
        # plt.show()

        anomaly_val_result = anomaly_val.flatten()

        # if len(one_sta) == 156:
        sta_tem_dic[sta] = anomaly_val_result
        time_end = time.time()
        log_process.process_bar(flag, len(tem_dic), time_init, time_start, time_end, sta)
        flag += 1
    print('\nsaving...')
    np.save(this_root + 'PDSI\\pre_anomaly_2003-2015', sta_tem_dic)


def correlation_temp_pre_pdsi():
    # 使用 project02的pdsi

    pdsi = np.load(this_root + 'PDSI\\project02_pdsi\\PDSI_result_filter.npz')
    pdsi_dic = {}
    for arr in pdsi:
        pdsi_dic[arr] = pdsi[arr].item()

    t_anomaly = np.load(this_root + 'PDSI\\temp_anomaly_2003-2015.npy').item()
    p_anomaly = np.load(this_root + 'PDSI\\pre_anomaly_2003-2015.npy').item()

    t_anomaly = dict(t_anomaly)
    p_anomaly = dict(p_anomaly)

    x = []
    y = []
    z = []
    for sta in pdsi_dic:
        if sta in t_anomaly and sta in p_anomaly:
            continue_flag = 0
            allyear_pdsi = pdsi_dic[sta]

            for year in range(2003, 2016):
                print(year)
                oneyear = allyear_pdsi[year]
                if len(oneyear) == 12:
                    # print(oneyear)
                    # exit()
                    for m in oneyear:
                        z.append(m)
                else:
                    continue_flag = 1

            if continue_flag == 0:
                oneyear_p = p_anomaly[sta]
                oneyear_t = t_anomaly[sta]
                if not len(oneyear_p) == 156:
                    print(oneyear_p)
                    exit()
                for i in oneyear_p:
                    x.append(i)
                for j in oneyear_t:
                    y.append(j)
            else:
                continue
            # print(sta)
        # except Exception as e:
        #     print('error',e)

    print(len(x))
    print(len(y))
    print(len(z))
    # kde_plot_scatter.plot_scatter(x[::30],y[::30])
    # plt.show()



def gen_new_dic():
    # 将pre tem pdsi 转化为字典
    # 键 xxxxx_200301
    pdsi = np.load(this_root + 'PDSI\\project02_pdsi\\PDSI_result_filter.npz')
    pdsi_dic = {}
    for arr in pdsi:
        pdsi_dic[arr] = pdsi[arr].item()

    t_anomaly = np.load(this_root + 'PDSI\\temp_anomaly_2003-2015.npy').item()
    p_anomaly = np.load(this_root + 'PDSI\\pre_anomaly_2003-2015.npy').item()

    t_anomaly = dict(t_anomaly)
    p_anomaly = dict(p_anomaly)

    # 转化pdsi
    print('transforming pdsi')
    pdsi_dic_trans = {}
    for sta in pdsi_dic:
        # print(sta)
        # print(pdsi[sta])
        one_sta = pdsi_dic[sta]
        for year in range(2003,2016):
            oneyear_val = one_sta[year]
            if len(oneyear_val) == 12:
                for m,val in enumerate(oneyear_val):
                    key = sta+'_'+str(year)+'%02d'%(m+1)
                    # print(key,val)
                    pdsi_dic_trans[key] = val
    # print('len(pdsi_dic_trans):%s'%len(pdsi_dic_trans))

    # 转化 pre
    print('transforming pre')
    pre_dic_trans = {}
    for sta in t_anomaly:
        onesta = t_anomaly[sta]
        baseyear = 2003
        for m,val in enumerate(onesta):
            month = (m)%12+1
            year = int(m/12)
            key = sta+'_'+str(baseyear+year)+'%02d'%month
            # print(key,val)
            pre_dic_trans[key] = val
            # print(2003+year,month)
            # print((m)%12,val)

    # 转化 temp
    print('transforming temp')
    tem_dic_trans = {}
    for sta in p_anomaly:
        onesta = p_anomaly[sta]
        baseyear = 2003
        for m,val in enumerate(onesta):
            month = m%12+1
            year = int(m/12)
            key = sta+'_'+str(baseyear+year)+'%02d'%month
            # print(key,val)
            tem_dic_trans[key] = val

    print('saving arr')
    np.save(this_root+'PDSI\\pdsi_trans',pdsi_dic_trans)
    np.save(this_root+'PDSI\\t_anomaly_trans',tem_dic_trans)
    np.save(this_root+'PDSI\\p_anomaly_trans',pre_dic_trans)


def correlation_temp_pre_pdsi_anomaly():

    pdsi = np.load(this_root+'PDSI\\pdsi_trans.npy').item()
    t = np.load(this_root+'PDSI\\t_anomaly_trans.npy').item()
    p = np.load(this_root+'PDSI\\p_anomaly_trans.npy').item()

    pdsi = dict(pdsi)
    t = dict(t)
    p = dict(p)

    x = []
    y = []
    z = []
    for key in pdsi:
        if key in p and key in t:
            x.append(t[key])
            y.append(p[key])
            z.append(pdsi[key])

    print(len(x))
    print(len(y))
    print(len(z))
    x = x[::156*2]
    y = y[::156*2]
    z = z[::156*2]

    plt.figure()
    plt.scatter(x,z)
    plt.title('t,pdsi')

    plt.figure()
    plt.scatter(y,z)
    plt.title('p,pdsi')

    plt.figure()
    plt.scatter(x,y)
    plt.title('t,p')
    # kde_plot_scatter.plot_scatter(x[:5000],z[:5000],title='temp_pdsi')
    # kde_plot_scatter.plot_scatter(y[:5000],z[:5000],title='pre_pdsi')
    # kde_plot_scatter.plot_scatter(x[:5000],y[:5000],title='temp_pre')
    plt.show()



def read_china_ci_from_files():

    fdir = this_root+'China_CI\\CI2\\'
    flist = os.listdir(fdir)
    date_list = []
    for y in range(10,16):
        for m in range(1,13):
            date_list.append(str(y)+'%02d'%m)

    #建立站点字典

    fr = open(this_root+'China_CI\\CI\\100104.txt','r')
    lines = fr.readlines()
    sta_dic = {}
    for line in lines:
        line = line.split('\n')[0]
        line = line.split()
        sta_dic[line[0]] = {}
    # for sta in sta_dic:
    #     #     print(sta)
    #     # exit()


    for date in date_list:
        print(date)
        flag = 0
        for f in flist:
            if f[:4] == date:
                # print(f)
                fr = open(fdir+f,'r')
                lines = fr.readlines()
                for line in lines:
                    line = line.split('\n')[0]
                    line = line.split()
                    try:
                        sta = line[0]
                    except Exception as e:
                        print(f)
                        print(e)
                        continue
                    # print(sta)
                    if sta in sta_dic:
                        val = float(line[1])
                        sta_dic[sta]['20'+f[:-4]] = val
    print('saving china ci...')
    np.savez(this_root+'PDSI\\china_ci2',**sta_dic)
        # print('len(sta_dic)%s'%len(sta_dic))
        # for i in sta_dic:
        #     print(i)
        #     print(sta_dic[i])
        #     exit()


def china_ci():
    npz = np.load(this_root+'PDSI\\china_ci2.npz')
    china_ci_dic = {}
    for i,sta in enumerate(npz):
        print(i+1,'/',len(npz))
        # print(len(npz[npy].item()))
        sta_dic = npz[sta].item()
        for y in range(2010,2016):
            for m in range(1,13):
                date_gen = str(y)+'%02d'%m
                val_sum = 0.
                flag = 0.
                for date in sta_dic:
                    if date[:6] == date_gen:
                        val = sta_dic[date]
                        if val > -99:
                            val_sum += val
                            flag += 1.
                if flag >0:
                    mean = val_sum/flag
                else:
                    mean = -9999
                # print(sta,date_gen,mean)
                key = sta+'_'+date_gen
                china_ci_dic[key] = mean
    print('saving dic...')
    np.save(this_root+'PDSI\\china_ci_dic2',china_ci_dic)
        # exit()


def ci_pdsi():
    # read_china_ci_from_files()
    # china_ci()
    ci1 = np.load(this_root+'PDSI\\china_ci_dic1.npy').item()
    ci2 = np.load(this_root+'PDSI\\china_ci_dic2.npy').item()
    pdsi = np.load(this_root+'PDSI\\pdsi_trans.npy').item()

    all_ci = {}
    for key in ci1:
        vals = max([ci1[key],ci2[key]])
        all_ci[key] = vals


    x = []
    y = []
    for key in all_ci:
        if key in pdsi:
            pdsi_i = pdsi[key]
            ci_i = all_ci[key]
            if -5 < ci_i < 5:
                x.append(ci_i)
                y.append(pdsi_i)
    print(len(x))
    print(len(y))
    kde_plot_scatter.plot_scatter(x[::3],y[::3])
    plt.figure()
    plt.scatter(x,y,s=0.5)
    r = stats.pearsonr(x,y)
    print(r)
    plt.show()

    #     break
    # for key in ci2:
    #     print(key)
    #     print(ci2[key])
    #     exit()
    # # gen_temp_anomaly()
    # gen_precip_anomaly()
    # china_ci()


def ci_pre_temp_corr():
    ci1 = np.load(this_root + 'PDSI\\china_ci_dic1.npy').item()
    ci2 = np.load(this_root + 'PDSI\\china_ci_dic2.npy').item()
    # pre = np.load(this_root+'PDSI\\p_anomaly_trans.npy').item()
    # pre = np.load(r'C:\Users\ly\PycharmProjects\bnu_project04_py27\bin27\data\pre_monthly_composite_dic.npy').item()
    pre = np.load(r'C:\Users\ly\PycharmProjects\bnu_project04_py27\bin27\data\pre_anomaly_dic.npy').item()
    # temp = np.load(this_root+'PDSI\\t_anomaly_trans.npy').item()
    # temp = np.load(r'C:\Users\ly\PycharmProjects\bnu_project04_py27\bin27\data\tmp_monthly_composite_dic.npy').item()
    temp = np.load(r'C:\Users\ly\PycharmProjects\bnu_project04_py27\bin27\data\tmp_anomaly_dic.npy').item()
    all_ci = {}
    for key in ci1:
        vals = max([ci1[key], ci2[key]])
        all_ci[key] = vals

    x = []
    y = []
    z = []
    # sta_list = ['57872','57657','57776',
    #             '57713','58813','57774',
    #             '57671', '58334', '57789',
    #             '52754', '57732', '57649',
    #             '57761', '57762', '58665',
    #             '57754', '54437', '57669',
    #             '58818', '57720', '58821',
    #             ]

    for key in all_ci:
        sta = int(key.split('_')[0])
        if sta > 51000:
            pass
        # exit()
        # if not key[:5] in sta_list:
        #     continue
        # exit()
        if key in pre and key in temp:
            pre_i = pre[key]
            temp_i = temp[key]
            ci_i = all_ci[key]
            if -5 < ci_i < 5:
                x.append(temp_i)
                y.append(pre_i)
                z.append(ci_i)

    print(len(x))
    print(len(y))
    print(len(y))
    kde_plot_scatter.plot_scatter(x[::10], z[::10],title='temp,ci',s=1)

    # kde_plot_scatter.plot_scatter(x, z,title='temp,ci',s=4)
    kde_plot_scatter.plot_scatter(y[::10], z[::10],title='pre,ci',s=1)
    # kde_plot_scatter.plot_scatter(y, z,title='pre,ci',s=4)
    # kde_plot_scatter.plot_scatter(x, y,title='temp,pre',s=4)
    kde_plot_scatter.plot_scatter(x[::10], y[::10],title='temp,pre',s=1)
    plt.figure()
    plt.scatter(x, z,s=0.1)
    plt.title('tmp,ci')
    plt.figure()
    plt.scatter(y, z,s=0.1)
    plt.title('pre,ci')
    plt.figure()
    plt.scatter(x, y,s=0.1)
    plt.title('tmp,pre')
    # plt.figure()
    # plt.scatter(x, y, s=0.5)
    rxz = stats.pearsonr(x,z)
    ryz = stats.pearsonr(y,z)
    rxy = stats.pearsonr(x,y)
    print('r_xz:%s'%rxz[0])
    print('r_yz:%s'%ryz[0])
    print('r_xy:%s'%rxy[0])
    plt.show()



def ci_pdsi_line_corr():
    ci1 = np.load(this_root + 'PDSI\\china_ci_dic1.npy').item()
    ci2 = np.load(this_root + 'PDSI\\china_ci_dic2.npy').item()

    ci1 = dict(ci1)
    ci2 = dict(ci2)

    pdsi = np.load(this_root + 'PDSI\\pdsi_trans.npy').item()
    pdsi = dict(pdsi)

    pre = np.load(this_root + 'PDSI\\p_anomaly_trans.npy').item()
    temp = np.load(this_root + 'PDSI\\t_anomaly_trans.npy').item()
    pre = dict(pre)
    temp = dict(temp)



    all_ci = {}
    for key in ci1:
        vals = max([ci1[key], ci2[key]])
        all_ci[key] = vals

    date_list = []
    for i in all_ci:
        date = i.split('_')[1]
        date_list.append(date)
    date_list = set(date_list)
    print(len(date_list))
    date_list = list(date_list)
    date_list.sort()



    x = []
    y = []
    a = []
    b = []
    for date in date_list:
        print(date)
        pdsi_sum = 0.
        flag1 = 0.
        for key in pdsi:
            date_i = key.split('_')[1]
            if date == date_i:
                val = pdsi[key]
                if -6 < val < 6:
                    pdsi_sum += val
                    flag1 += 1.
        pdsi_mean = pdsi_sum/flag1
        x.append(pdsi_mean)

        ci_sum = 0.
        flag2 = 0.
        for key in all_ci:
            date_i = key.split('_')[1]
            if date == date_i:
                val = all_ci[key]
                if -5 < val < 5 :
                    ci_sum += val
                    flag2 += 1.
        ci_mean = ci_sum/flag2
        y.append(ci_mean)

        pre_sum = 0.
        flag3 = 0.
        for key in pre:
            date_i = key.split('_')[1]
            if date == date_i:
                val = pre[key]
                pre_sum += val
                flag3 += 1.
        pre_mean = pre_sum/flag3
        a.append(pre_mean)

        temp_sum = 0.
        flag4 = 0.
        for key in temp:
            date_i = key.split('_')[1]
            if date == date_i:
                val = temp[key]
                temp_sum += val
                flag4 += 1.
        temp_mean = temp_sum/flag4
        b.append(temp_mean)


    print(len(x))
    print(len(y))
    print(len(a))
    print(len(b))

    plt.plot(x,label='pdsi')
    plt.plot(y,label='ci')
    # plt.plot(a,label='pre')
    plt.plot(b,label='temp')
    plt.legend()
    r = stats.pearsonr(x,y)
    print(r)
    plt.show()


def gen_3_months_average():
    pre = np.load(this_root + 'PDSI\\p_anomaly_trans.npy').item()
    temp = np.load(this_root + 'PDSI\\t_anomaly_trans.npy').item()
    pre = dict(pre)
    temp = dict(temp)

    date_list = []
    for year in range(2000,2016):
        for mon in range(1,13):
            date_list.append(str(year)+'%02d'%mon)

    new_dic = {}
    time_init = time.time()
    flag = 0
    for key in pre:
        time_start = time.time()
        key_split = key.split('_')
        sta = key_split[0]
        date_str = key_split[1]
        year = int(date_str[:4])
        mon = int(date_str[-2:])

        date = datetime.datetime(year,mon,15)
        time_delta = datetime.timedelta(30)

        date_1 = date-time_delta
        date_1_str = '%s%02d'%(date_1.year,date_1.month)

        date_2 = date - time_delta*2
        date_2_str = '%s%02d' % (date_2.year, date_2.month)

        # print(date_1_str)
        # print(date_2_str)
        try:
            val1 = pre[sta+'_'+date_str]
            val2 = pre[sta+'_'+date_1_str]
            val3 = pre[sta+'_'+date_2_str]
            val_mean = np.mean([val1,val2,val3])
            # print(val_mean)

            new_dic[key] = val_mean
        except Exception as e:
            # print(e)
            pass
        time_end = time.time()
        log_process.process_bar(flag,len(pre),time_init,time_start,time_end)
        flag+=1
    print('saving dic...')
    np.save(this_root+'PDSI\\pre_3_months_average',new_dic)



def gen_3_months_average_new():
    # 用新数据
    this_root = os.getcwd()+'\\'
    # pre = np.load(this_root + 'data\\pre_anomaly_dic.npy').item()
    temp = np.load(this_root + 'data\\tmp_anomaly_dic.npy').item()
    # pre = dict(pre)
    temp = dict(temp)

    date_list = []
    for year in range(2000, 2016):
        for mon in range(1, 13):
            date_list.append(str(year) + '%02d' % mon)

    new_dic = {}
    time_init = time.time()
    flag = 0
    for key in temp:
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
            val1 = temp[sta + '_' + date_str]
            val2 = temp[sta + '_' + date_1_str]
            val3 = temp[sta + '_' + date_2_str]
            val_mean = np.mean([val1, val2, val3])
            # print(val_mean)

            new_dic[key] = val_mean
        except Exception as e:
            # print(e)
            pass
        time_end = time.time()
        log_process.process_bar(flag, len(temp), time_init, time_start, time_end)
        flag += 1
    print('saving dic...')
    np.save(this_root + 'data\\temp_3_months_average_new', new_dic)


def plot_line_3_months_average():
    t = np.load(this_root + 'PDSI\\temp_3_months_average.npy', encoding='latin1').item()
    p = np.load(this_root + 'PDSI\\pre_3_months_average.npy', encoding='latin1').item()
    ci = np.load(this_root + 'PDSI\\all_ci.npy').item()

    ci = dict(ci)
    t = dict(t)
    p = dict(p)

    npz = np.load(this_root + '\\in_situ_data\\pre_dic.npz')

    selected_sta = []
    for sta in npz:
        sta_int = int(sta)
        if sta_int < 51000:
            selected_sta.append(sta)
    print(selected_sta)
    print(len(selected_sta))

    X = []
    Y = []
    for key in ci:
        sta = key.split('_')[0]
        if not sta in selected_sta:
            continue
        # print(key)
        if key in p and key in t:
            X.append(p[key])
            Y.append(ci[key])

    import random
    print(X)
    random.shuffle(X)
    print(X)
    r = stats.pearsonr(X,Y)
    print('stats.pearsonr(X,Y)%s'%r[0])
    kde_plot_scatter.plot_scatter(X,Y)
    plt.show()





    for sta in t:
        print(sta,t[sta])




def plot_line_3_months_average_new():

    ci = np.load(this_root + 'PDSI\\pdsi_trans.npy').item()

    # t = np.load(r'C:\Users\ly\PycharmProjects\bnu_project04_py27\bin27\data\temp_3_months_average_new.npy', encoding='latin1').item()
    p = np.load(r'C:\Users\ly\PycharmProjects\bnu_project04_py27\bin27\data\pre_3_months_average_new.npy', encoding='latin1').item()


    ci = dict(ci)
    # t = dict(t)
    p = dict(p)

    npz = np.load(this_root + '\\in_situ_data\\pre_dic.npz')

    selected_sta = []
    for sta in npz:
        sta_int = int(sta)
        # if 56000 < sta_int < 57000 :
        #     selected_sta.append(sta)
        selected_sta.append(sta)
    # print(selected_sta)
    print(len(selected_sta))

    X = []
    Y = []
    for key in ci:
        sta = key.split('_')[0]
        if not sta in selected_sta:
            continue
        # print(key)
        if key in p:
            X.append(p[key])
            Y.append(ci[key])

    import random
    # print(X)
    # random.shuffle(X)
    # print(X)
    print(len(X))
    r = stats.pearsonr(X,Y)
    print('stats.pearsonr(X,Y)%s'%r[0])
    kde_plot_scatter.plot_scatter(X[::20],Y[::20])
    plt.figure()
    plt.scatter(X,Y,s=1)
    plt.show()





    # for sta in t:
    #     print(sta,t[sta])






def gen_temp_anomaly_new_data():
    this_root = os.getcwd()+'\\'
    tmp_dic = dict(np.load(this_root+'data\\pre_monthly_composite_dic.npy').item())
    sta_dic = np.load(this_root+'data\\sta_num_list.npy').item()
    sta_dic = list(sta_dic)
    sta_dic.sort()

    date_list = []
    for year in range(1951,2018):
        for mon in range(1,13):
            date = str(year)+'%02d'%mon
            date_list.append(date)

    # flag = 0
    mean_std_dic = {}
    for sta in sta_dic:
        # flag+=1
        # print(flag,'/',len(sta_dic))
        for mon in range(1,13):
            mon_str = '%02d'%mon
            vals = []
            for year in range(1951,2018):
                year_str = str(year)
                key = sta+'_'+year_str+mon_str
                try:
                    val = tmp_dic[key]
                except Exception as e:
                    val = None
                    pass
                if val != None:
                    vals.append(val)
                    # print(e)
            if len(vals) > 10:
                mean = np.mean(vals)
                std = np.std(vals)
                # print(sta+'_'+mon_str)
                mean_std_dic[sta+'_'+mon_str] = [mean,std]
            # else:
            #     print(sta,mon_str)
            #     # exit()

    anomaly_dic = {}
    flag = 0
    time_init = time.time()
    for key in tmp_dic:
        # flag+=1
        # print(flag,'/',len(tmp_dic))
        time_start = time.time()
        key_split = key.split('_')
        sta = key_split[0]
        mon = key_split[1][-2:]
        val = tmp_dic[key]
        try:
            mean, std = mean_std_dic[sta+'_'+mon]
            anomaly = (val-mean)/std
            anomaly_dic[key] = anomaly
        except Exception as e:
            pass
        time_end = time.time()
        log_process.process_bar(flag,len(tmp_dic),time_init,time_start,time_end)
        flag += 1
    print('saving ...')
    np.save(this_root+'data\\pre_anomaly_dic',anomaly_dic)







def main():
    plot_line_3_months_average_new()
    # this_root = os.getcwd()+'\\'
    # pre_anomaly = dict(np.load(this_root+'data\\pre_anomaly_dic.npy').item())
    # tmp_anomaly = dict(np.load(this_root+'data\\tmp_anomaly_dic.npy').item())
    #
    # date_list = []
    # for key in pre_anomaly:
    #     sta = key.split('_')[0]
    #     date = key.split('_')[1]





if __name__ == '__main__':
    main()
    # tem_dic = np.load(this_root + 'PDSI\\tem_dic.npz')
    # for i in tem_dic:
    #     for d in tem_dic[i].item():
    #         print(d)
    # gen_dependent_pdsi1()
    # pdsi = np.load(this_root + 'PDSI\\PDSI_result_filter.npz')
    # for arr in pdsi:
    #     print(pdsi[arr].item())