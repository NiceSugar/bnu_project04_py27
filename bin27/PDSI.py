# coding=utf-8

import os
this_root = os.getcwd()+'\\..\\'
import numpy as np


def composite_pre():
    f_dir = this_root+'PDSI\\in_situ\\PRE18\\'
    dic_output = this_root+'PDSI\\in_situ\\PRE_transform'
    f_list = os.listdir(f_dir)

    date_dic = {}
    for f in f_list:
        print(f)
        date = f.split('-')[-1].split('.')[-2]

        fr = open(f_dir+f,'r')
        lines = fr.readlines()
        stations = []
        for line in lines:
            line = line.split('\n')[0]
            # print(line)
            sta = line[0:5]
            stations.append(sta)

        stations = set(stations)
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
            if flag>0:
                # print(s)
                mean = monthly_sum
                # print(mean)
                station_dic[s] = mean
                # print(np.mean(monthly_vals))
        date_dic[date] = station_dic
    print('saving '+dic_output+'...')
    np.savez(dic_output,date_dic)



def composite_tem():
    f_dir = this_root+'PDSI\\in_situ\\TEM18\\'
    dic_output = this_root+'PDSI\\in_situ\\TEM_transform'
    f_list = os.listdir(f_dir)

    date_dic = {}
    for f in f_list:
        print(f)
        date = f.split('-')[-1].split('.')[-2]

        fr = open(f_dir+f,'r')
        lines = fr.readlines()
        stations = []
        for line in lines:
            line = line.split('\n')[0]
            # print(line)
            sta = line[0:5]
            stations.append(sta)
        # print(stations)
        # exit()
        stations = set(stations)
        station_dic = {}
        for s in stations:
            monthly_sum = 0.
            flag = 0.
            for line in lines:
                line = line.split('\n')[0]
                sta = line[0:5]
                if sta == s:
                    val = float(line[36:41])
                    # print line[36:41]
                    # print(val)
                    # exit()
                    if val < 20000:
                        monthly_sum += val
                        flag += 1
            if flag>0:
                # print(s)
                mean = monthly_sum/flag/10.
                # print(s)
                # print(mean)
                # exit()
                station_dic[s] = mean
                # print(np.mean(monthly_vals))
        date_dic[date] = station_dic
    print('saving '+dic_output+'...')
    np.savez(dic_output,date_dic)


def main():
    # composite_tem()
    npz = np.load(this_root+'PDSI\\in_situ\\PRE_transform.npz')
    arr = npz['arr_0']
    print(arr)

if __name__ == '__main__':
    main()