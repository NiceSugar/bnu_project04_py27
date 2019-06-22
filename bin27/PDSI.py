# coding=gbk

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



def main():
    # gen_temp_anomaly()
    # gen_precip_anomaly()
    correlation_temp_pre_pdsi()




if __name__ == '__main__':
    # tem_dic = np.load(this_root + 'PDSI\\tem_dic.npz')
    # for i in tem_dic:
    #     for d in tem_dic[i].item():
    #         print(d)
    main()
    # gen_dependent_pdsi1()
    # pdsi = np.load(this_root + 'PDSI\\PDSI_result_filter.npz')
    # for arr in pdsi:
    #     print(pdsi[arr].item())