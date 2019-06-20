# coding=utf-8
import os
this_root = os.getcwd()+'\\..\\'
import numpy as np
import time
from scipy import interpolate
from matplotlib import pyplot as plt
from multiprocessing import Process
import multiprocessing as mp
# import psutil
import numba as nb
from numba import float64

from climate_indices import indices
from climate_indices import compute


def mk_dir(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)

class PCI:
    def __init__(self):

        pass

    def cal_kernel(self,val):
        val_normal = np.array([0.] * len(val))
        for i in range(len(val)):
            v_i = (val[i] - np.min(val)) / (np.max(val) - np.min(val))
            val_normal[i] = v_i

        return val_normal

    def loop(self, pre, save_folder, save_name, func):
        # import tool
        pre_npz = np.load(pre)
        mk_dir(save_folder)

        # save_name = npz_file.split('\\')[-1]
        save_path = save_folder + '\\' + save_name
        start = time.time()
        # npz = np.load(npz_file)

        normalized_vals_dic = {}
        npy_flag = 0
        for npy in pre_npz:
            # print(npy)
            npy_flag += 1.
            if npy_flag % 1000 == 0:
                print(save_name, npy_flag / len(pre_npz) * 100, '%', '%02f' % (time.time() - start))
            try:
                vals_pre = pre_npz[npy]
            except:
                vals_pre = []
            try:
                if len(vals_pre) > 1:
                    normalized_vals_dic[npy] = func(vals_pre)
                    # plt.figure()
                    # plt.plot(vals_NDVI)
                    # plt.title('ndvi')
                    # plt.figure()
                    # plt.plot(vals_pre)
                    # plt.title('pre')
                    # plt.figure()
                    # plt.plot(func(vals_pre))
                    # plt.title('pci')
                    # plt.figure()
                    # plt.scatter(vals_NDVI,vals_LST)
                    # plt.show()
                else:
                    normalized_vals_dic[npy] = []

            except:
                normalized_vals_dic[npy] = []
        print('saving ' + save_path)
        np.savez(save_path, **normalized_vals_dic)
        print('save ' + save_path + ' success\ntime:', '%02f' % (time.time() - start))


    def run(self):

        save_folder = this_root + 'CRU_precip\\'

        # print(f)
        # exit()
        pre_npz = this_root+'CRU_precip\\cru_transfomed.npz'
        pre = pre_npz
        save_name = 'pci'
        func = self.cal_kernel
        self.loop(pre, save_folder, save_name, func)





class SPI:

    def __init__(self):

        pass


    def cal_kernel(self,val):
        # values = val
        scale = 1
        distribution = indices.Distribution.gamma
        data_start_year = 2003
        calibration_year_initial = 2003
        calibration_year_final = 2016
        periodicity = compute.Periodicity.monthly

        spi = indices.spi(val,
                          scale,
                          distribution,
                          data_start_year,
                          calibration_year_initial,
                          calibration_year_final, periodicity
                          )
        return spi


    def loop(self, pre, save_folder, save_name, func):
        # import tool
        pre_npz = np.load(pre)
        mk_dir(save_folder)

        # save_name = npz_file.split('\\')[-1]
        save_path = save_folder + '\\' + save_name
        start = time.time()
        # npz = np.load(npz_file)

        normalized_vals_dic = {}
        npy_flag = 0
        for npy in pre_npz:
            # print(npy)
            npy_flag += 1.
            if npy_flag % 1000 == 0:
                print(save_name, npy_flag / len(pre_npz) * 100, '%', '%02f' % (time.time() - start))
            try:
                vals_pre = pre_npz[npy]
            except:
                vals_pre = []
            try:
                if len(vals_pre) > 1:
                    normalized_vals_dic[npy] = func(vals_pre)
                    # plt.figure()
                    # plt.plot(vals_NDVI)
                    # plt.title('ndvi')
                    # plt.figure()
                    # plt.plot(vals_pre)
                    # plt.title('pre')
                    # plt.figure()
                    # plt.plot(func(vals_pre))
                    # plt.title('pci')
                    # # plt.figure()
                    # plt.show()
                else:
                    normalized_vals_dic[npy] = []

            except:
                normalized_vals_dic[npy] = []
        print('saving ' + save_path)
        np.savez(save_path, **normalized_vals_dic)
        print('save ' + save_path + ' success\ntime:', '%02f' % (time.time() - start))


    def run(self):

        save_folder = this_root + 'CRU_precip\\'

        # print(f)
        # exit()
        pre_npz = this_root+'CRU_precip\\cru_transfomed.npz'
        pre = pre_npz
        save_name = 'spi'
        func = self.cal_kernel
        self.loop(pre, save_folder, save_name, func)

    def interp_1d(self,val):
        # 1、插缺失值
        x = []
        val_new = []
        for i in range(len(val)):
            if val[i] >= 100:
                index = i
                x = np.append(x, index)
                val_new = np.append(val_new, val[i])

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



def interp_1d(val):
    # 1、插缺失值
    x = []
    val_new = []
    for i in range(len(val)):
        # if val[i] >= 100:
        if not np.isnan(val[i]) and val[i]>0:
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


def interp_nan():
    npz = np.load('D:\\MODIS\\bin\\..\\CRU_precip\\spi.npz')
    print(len(npz))
    vals_dic = {}
    for npy in npz:
        vals = npz[npy]
        interp = interp_1d(vals)
        vals_dic[npy] = interp
        # print(npy)
        # plt.plot(vals,alpha=0.5)
        # plt.plot(interp,alpha=0.5)
        # plt.show()
        # print('*'*8)
        # time.sleep(1)
    print('saving dic')
    np.savez('D:\\MODIS\\bin\\..\\CRU_precip\\pci_no_nan.npz',**vals_dic)


def main():
    # interp_nan()
        # break

    # PCI().run()
    npz = np.load('D:\\MODIS\\bin\\..\\in_situ_data\\pre_dic.npz')

    # fig = plt.figure()
    # ax = fig.add_subplot(1,1,1)
    # plt.ion()
    count = 0
    spi_dic = {}
    for k,i in enumerate(npz):
        # plt.pause(0.01)
        # print(i)
        vals = []
        flag = 0

        for y in range(2003,2017):
            for m in range(1,13):
                y = str(y)
                m = '%02d'%m
                date = y+m
                val_dic = dict(npz[i].item())
                try:
                    vals.append(val_dic[date])
                except:
                    vals.append(-999999)
                    flag = 1
        if flag == 1:
            count += 1
        print(k,'/',len(npz),count)
        if flag:
            pass
        else:
            vals = np.array(vals)
            vals = interp_1d(vals)
            spi = SPI().cal_kernel(vals)
            # print(spi)
            # exit()

            # try:
            #     ax.lines.remove(line[0])
            # except:
            #     pass

            date_spi_index = 0
            for y in range(2003, 2017):
                for m in range(1, 13):
                    y = str(y)
                    m = '%02d' % m
                    date = y + m
                    key = i+'_'+date
                    # print(key)
                    spi_dic[key] = spi[date_spi_index]
                    date_spi_index += 1

            # line = ax.plot(spi,c='b')
            # plt.title(i)

        # plt.ioff()
        #     plt.show()
    print('saving spi_dic')
    np.save('spi_dic',spi_dic)

if __name__ == '__main__':
    main()

