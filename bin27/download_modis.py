# coding=utf-8
# 181224 更新
# 加入重新连接功能，可以解决多线程下载时服务器拒绝下载
import urllib2
from cookielib import CookieJar
import os
import re
from multiprocessing import Process
from threading import Thread
import time
import psutil
# from pyhdf.SD import SD, SDC
from matplotlib import pyplot as plt
import numpy as np

from scipy import interpolate


class ModisDownload:
    def __init__(self, url, date):
        self.url = url

        self.mode = self.url.split('/')[-2]

        self.this_root = os.getcwd()+'\\'
        self.download_folder = self.this_root+'download_data\\'+self.mode+'\\'
        self.temp_folder = self.this_root+'temp_folder\\'
        self.url_folder = self.this_root+'urls\\'
        self.make_dir(self.this_root+'download_data\\')
        self.make_dir(self.download_folder)
        self.make_dir(self.temp_folder)
        self.make_dir(self.url_folder)
        self.date = date
        print('this_root',self.this_root)
        print('download_folder',self.download_folder)
        print('temp_folder',self.temp_folder)
        print('url_folder',self.url_folder)
        # exit()
        pass


    def make_dir(self,dirname):
        if not os.path.isdir(dirname):
            os.mkdir(dirname)


    def download_file(self, urls, log):
        username = 'vivian920525'
        password = 'America2018'

        password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_manager.add_password(None, "https://urs.earthdata.nasa.gov", username, password)
        cookie_jar = CookieJar()
        opener = urllib2.build_opener(
            urllib2.HTTPBasicAuthHandler(password_manager),
            # urllib2.HTTPHandler(debuglevel=1),    # Uncomment these two lines to see
            # urllib2.HTTPSHandler(debuglevel=1),   # details of the requests/responses
            urllib2.HTTPCookieProcessor(cookie_jar))
        urllib2.install_opener(opener)
        for url in urls:
            # print 'downloading',url
            fname = url.split('/')[-1]
            save_path = self.download_folder + url.split('/')[-2] + '/'
            if not os.path.isdir(save_path):
                os.mkdir(save_path)

            attempts = 0
            while 1:
                success = 0
                try:
                    if not os.path.isfile(save_path + fname):
                        request = urllib2.Request(url)
                        response = urllib2.urlopen(request)
                        body = response.read()
                        with open(save_path + fname, 'wb') as f:
                            f.write(body)
                        print url,'done'
                        success = 1
                    else:
                        pass
                        print fname, 'is already existed'
                        success = 1
                except Exception as e:
                    time.sleep(1)
                    print 'x' * 30
                    print e
                    attempts += 1
                    print 'try ',attempts
                    success = 0

                if success == 1 or attempts > 10:

                    break

    def gen_download_list(self):

        # if not os.path.isdir(self.download_folder):
        #     os.mkdir(self.download_folder)
        selected_dates = self.date
        url_text_file = self.url_folder + '/' +selected_dates+'_'+ self.mode + '_url.txt'

        attempts = 0
        while 1:
            success = 0
            try:
                url = self.url
                request = urllib2.Request(url)
                response = urllib2.urlopen(request)
                success = 1
                body = response.read()
                p = re.findall('/">.*?/</a>', body)
                # date = []
                all_url = []
                # 清空下载地址文件
                fw = open(url_text_file, 'w')
                fw.close()
                flag = 0
                for i in p:
                    flag += 1
                    # print i[3:-5], flag, '/', len(p)
                    date = i[3:-5] + '/'
                    d = i[3:-5]
                    if len(selected_dates) != 0:
                        if d not in selected_dates:
                            continue
                    url_i = url + date
                    request = urllib2.Request(url_i)
                    response = urllib2.urlopen(request)
                    body = response.read()
                    # print body
                    p1 = re.findall('">.*?">', body)
                    temp = []

                    f = open(url_text_file, 'r')
                    lines = f.readlines()
                    f.close()
                    fw = open(url_text_file, 'w')
                    for line in lines:
                        fw.write(line)
                    for pi in p1:
                        if '.hdf' in pi and not '.xml' in pi:
                            # if 0:
                            fname = pi[12:-2]
                            download_url = url_i + fname
                            fw.write(download_url + '\n')
                            # print download_url
                            temp.append(download_url)
                    fw.close()
                    all_url.append(temp)
                return all_url
            except:
                success = 0
                attempts += 1
            if attempts > 10 or success == 1:
                break


    def gen_download_dates(self):
        url = self.url
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        body = response.read()
        p = re.findall('/">.*?/</a>', body)
        date = []

        flag = 0
        for i in p:
            flag += 1
            print i[3:-5], flag, '/', len(p)
            date.append(i[3:-5])
        # print(date)
        return date

        pass


    def concurrent_download(self, process):
        '''
        并行下载
        '''
        url_text_file = self.url_folder + '/' +self.date+'_'+ self.mode + '_url.txt'
        f = open(url_text_file, 'r')
        lines = f.readlines()
        f.close()
        lines_new = []

        china = ['h23v04', 'h23v05',
                 'h24v04', 'h24v05',
                 'h25v03', 'h25v04', 'h25v05', 'h25v06',
                 'h26v03', 'h26v04', 'h26v05', 'h26v06',
                 'h27v04', 'h27v05', 'h27v06',
                 'h28v05', 'h28v06', 'h28v07',
                 'h29v06', 'h29v07']

        # mid_asia = ['h21v03','h21v04','h21v05',
        #             'h22v03','h22v04','h22v05',
        #             'h23v03','h23v04','h23v05',
        #             'h24v03','h24v04','h24v05'
        #             ]

        # 是否筛选中国
        for l in lines:
            if '.hdf' in l:
                l = l.split('\n')[0]
                # 全球
                # lines_new.append(l)
                # 中国
                for c in china:
                    if c in l:
                        lines_new.append(l)



        url_split = []
        parts = process
        split_num = len(lines_new) / parts
        # print(len(lines_new))
        # exit()
        if split_num == 0:
            for lin in lines_new:
                url_split.append([lin])
            # print(url_split)
            # exit()
            for i in range(len(url_split)):
                time.sleep(1)
                p = Thread(target=self.download_file, args=(url_split[i], ''))
                p.start()
            # url_split.append()
        else:
            for i in range(len(lines_new) / split_num):
                url_split.append(lines_new[i * split_num:(i + 1) * split_num])
            tail = len(lines_new) - len(url_split) * split_num
            url_split.append(lines_new[-tail:])
            # for u in url_split:
            #     print(u)
            #     print(len(u))
            # exit()
            flag = 0
            log_list = []
            for i in range(len(url_split)):
                flag += 1
                fn = self.this_root + '/log/log_' + '%04d' % flag + '.txt'
                if not os.path.isdir(self.this_root + '/log/'):
                    os.mkdir(self.this_root + '/log/')
                f = open(fn, 'w')
                f.close()
                log_list.append(fn)
            for i in range(len(url_split)):
                time.sleep(1)
                p = Thread(target=self.download_file, args=(url_split[i], log_list[i]))
                p.start()



        return len(lines_new)

    def debug(self):

        f_dir = self.this_root + '/log/'
        f_list = os.listdir(f_dir)
        failed_hdf = []
        for fi in f_list:
            if fi.endswith('.txt'):
                f = open(f_dir + fi, 'r')
                lines = f.readlines()
                for l in lines:
                    failed_hdf.append(l)
                f.close()
                os.remove(f_dir + fi)
        if not os.path.isdir(self.this_root + '/log/log/'):
            os.mkdir(self.this_root + '/log/log/')
        f = open(self.this_root + '/log/log/log.txt', 'w')
        for l in failed_hdf:
            # print l
            f.write(l)
        f.close()

    def run_download(self, process):
        '''

        Args:
            process: 开启的进程数

        Returns:

        '''
        # url = 'https://e4ftl01.cr.usgs.gov/MOLT/MOD17A2.005/2000.02.18/MOD17A2.A2000049.h24v05.005.2006333230015.hdf.xml'
        download_number = self.concurrent_download(process)
        # 监测下载文件数量，每一秒监测一次
        second = -1
        download_files_len = 0
        start = time.time()
        all_num = download_number

        while 1:
            download_files_dir = os.listdir(self.download_folder)
            # download_files_len1 = len(download_files)
            flag = 0
            # 监测已下载的文件数量
            for d in download_files_dir:
                d_list = os.listdir(self.download_folder + '/' + d)
                for di in d_list:
                    if di.endswith('.hdf'):
                        flag += 1
            if download_files_len == flag:
                second += 1
            download_files_len = 0 + flag
            print 'timeout', second
            # print '*'*8
            end = time.time()

            print '\t', flag, '/', all_num, '\t', int(end - start), 's'
            # 如果下载文件的数量达到需要下载的视频数量则停止监测
            if flag >= all_num:
                break
            # 暂停一秒            # 结束文件数量监测
            #             if breakflag == 1:
            #                 print 'break'
            #                 break
            time.sleep(1)

    def MRT_mosaic(self):
        # 生成要拼接的文件列表
        # f_dir = 'E:\\LY_ZW_02\\data\\' + self.mode + '\\file\\' + date + '\\'
        date = self.date
        f_dir = self.download_folder+date+'\\'
        f_list = os.listdir(f_dir)
        temp_folder = self.temp_folder

        file_list = temp_folder + 'files.txt'


        china = ['h23v03', 'h23v05',
                 'h24v04', 'h24v05',
                 'h25v03', 'h25v04', 'h25v05', 'h25v06',
                 'h26v03', 'h26v04', 'h26v05', 'h26v06',
                 'h27v04', 'h27v05', 'h27v06',
                 'h28v05', 'h28v06', 'h28v07',
                 'h29v06', 'h29v07']

        # mid_asia = ['h21v03','h21v04','h21v05',
        #             'h22v03','h22v04','h22v05',
        #             'h23v03','h23v04','h23v05',
        #             'h24v03','h24v04','h24v05'
        #             ]

        f = open(file_list, 'w')

        for fi in f_list:
            # 是否选择中国
            # 否
            # f.write(f_dir + fi + '\n')


            for c in china:
                # 是
                if c in fi:
                    f.write(f_dir + fi + '\n')
                    # print f_dir+fi
        # exit()
        f.close()
        # MRT 拼接命令行
        mrt_mosaic = 'H:\\LY_ZW_02\\program\\MRT\\bin\\mrtmosaic.exe'
        mosaic_cmd_line = mrt_mosaic + ' -i ' + file_list + ' -s "1 0 0 0 0 0 0 0 0 0 0 0 0" -o ' + temp_folder + date +'_mosaic.hdf'
        # print cmd_line
        print mosaic_cmd_line
        os.system(mosaic_cmd_line)

    def MRT_resample(self):
        date = self.date
        # MRT 投影重采样
        temp_folder = self.temp_folder
        mrt_resample = 'H:\\LY_ZW_02\\program\\MRT\\bin\\resample.exe'
        # output_file = 'H:\\LY_ZW_02\\data\\' + self.mode + '\\output\\' + date + '.tif'
        output_file = self.this_root+'mid_asia_tif\\'+'mid_asia_'+date+'.tif'
        resample_cmd_line = mrt_resample + ' -i ' + temp_folder + date +'_mosaic.hdf -p ' + self.this_root + 'midasia0.1.prm -o ' + output_file
        print resample_cmd_line
        os.system(resample_cmd_line)

    def check_temp(self):
        if self.mode == 'gpp':
            f_dir = 'E:\\LY_ZW_02\\data\\GPP\\temp\\'
        elif self.mode == 'ndvi':
            f_dir = 'E:\\LY_ZW_02\\data\\NDVI\\temp\\'
        else:
            f_dir = None
        f_list = os.listdir(f_dir)
        missing_dates = []
        for date in f_list:
            file_number = len(os.listdir(f_dir + date))
            if not file_number == 2:
                # print date,file_number
                missing_dates.append(date)
        return missing_dates

    def check_out_put(self):
        if self.mode == 'gpp':
            f_dir = 'E:\\LY_ZW_02\\data\\GPP\\temp\\'
        elif self.mode == 'ndvi':
            f_dir = 'E:\\LY_ZW_02\\data\\NDVI\\temp\\'
        else:
            f_dir = None
        f_list = os.listdir(f_dir)
        for y in range(2002, 2016):
            y = str(y)
            count = 0
            for f in f_list:
                f_split = f.split('.')
                if f_split[0] == y:
                    count += 1
            print y, count

    def delete_hdf(self):
        '''
        删除多余的HDF
        Returns:

        '''
        f_dir = self.download_folder
        f_list = os.listdir(f_dir)
        china = ['h23v04', 'h23v05',
                 'h24v04', 'h24v05',
                 'h25v03', 'h25v04', 'h25v05', 'h25v06',
                 'h26v03', 'h26v04', 'h26v05', 'h26v06',
                 'h27v04', 'h27v05', 'h27v06',
                 'h28v05', 'h28v06', 'h28v07',
                 'h29v06', 'h29v07']
        for folder in f_list:
            hdf_list = os.listdir(f_dir + folder)
            for hdf in hdf_list:
                code = hdf.split('.')[2]
                if not code in china:
                    os.remove(f_dir + folder + '\\' + hdf)
                    print folder, hdf, 'removed'

        # 检查每天 modis hdf 数量
        for folder in f_list:
            hdf_list = os.listdir(f_dir + folder)
            count = 0
            for hdf in hdf_list:
                if hdf.endswith('.hdf'):
                    count += 1
            if count != 20:
                print folder, count

    def delete_dates(self, selected_dates):
        flist = os.listdir(self.download_folder)
        for folder in flist:
            if folder in selected_dates:
                folder_list = os.listdir(self.download_folder + folder)
                for f in folder_list:
                    os.remove(self.download_folder + folder + '\\' + f)
                    # print 'removing',self.download_folder+folder+'\\'+f
                os.rmdir(self.download_folder + folder)
                print folder, 'removed'
                # break

        pass

    def selected_h_v(self):
        china = ['h23v04', 'h23v05',
                 'h24v04', 'h24v05',
                 'h25v03', 'h25v04', 'h25v05', 'h25v06',
                 'h26v03', 'h26v04', 'h26v05', 'h26v06',
                 'h27v04', 'h27v05', 'h27v06',
                 'h28v05', 'h28v06', 'h28v07',
                 'h29v06', 'h29v07']
        url_txt = open(self.this_root + '\\config\\gpp_url.txt', 'r')
        lines = url_txt.readlines()
        url_txt.close()
        fw = open(self.this_root + '\\config\\gpp_url_new.txt', 'w')
        for line in lines:
            line_split = line.split('.')
            if line_split[-4] in china:
                fw.write(line)
        fw.close()

        pass

    def interpolation_1d(self, x, y, xnew):
        # ["nearest","zero","slinear","quadratic","cubic"]
        # "nearest","zero"为阶梯插值
        # slinear 线性插值
        # "quadratic","cubic" 为2阶、3阶B样条曲线插值
        f = interpolate.interp1d(x, y, kind='nearest')
        # ‘slinear’, ‘quadratic’ and ‘cubic’ refer to a spline interpolation of first, second or third order)
        ynew = f(xnew)
        return ynew
        pass

    def modis_time_interpolate(self):
        '''
        时间差值
        Returns:

        '''

        if self.mode == 'gpp':
            f_dir = self.this_root + '\\data\\GPP\\GPP_clip\\'
        elif self.mode == 'ndvi':
            f_dir = self.this_root + '\\data\\NDVI\\NDVI_clip\\'
        elif self.mode == 'et':
            f_dir = self.this_root + '\\data\\ET\\ET_clip\\'
        else:
            f_dir = None
        f_list = os.listdir(f_dir)
        height, width = np.shape(np.load(f_dir + f_list[0]))
        print (height, width)
        for y in range(2004, 2016):
            if y in [2004, 2008, 2012]:
                f = open(self.this_root + 'config\\date_dic_2004', 'r')
                date_dic = f.read()
                date_dic = eval(date_dic)
            else:
                f = open(self.this_root + 'config\\date_dic_2001', 'r')
                date_dic = f.read()
                date_dic = eval(date_dic)
            print y
            arrs = []
            arrs_x = []
            for f in range(len(f_list)):
                if f_list[f].split('.')[0] == str(y):
                    # print f_list[f]
                    date = '.'.join(f_list[f].split('.')[1:3])
                    x = date_dic[date]
                    arr = np.load(f_dir + f_list[f])
                    arrs.append(arr)
                    arrs_x.append(x)

            iis = []
            for i in range(height):
                # print i,'/',height
                # if not i == 92:
                #     continue
                jjs = []
                for j in range(width):
                    # start = time.time()
                    pixels = []
                    x_list = []

                    for d in range(len(arrs)):
                        pix = arrs[d][i][j]
                        if -999999 < pix < 30000:
                            # if 1:
                            pixels.append(pix)
                            x_list.append(arrs_x[d])
                        else:
                            #     print 123
                            break
                    if not len(pixels) <= 20:
                        # print pixels
                        x_list_interp = np.linspace(x_list[0], x_list[-1], 52)
                        y_list_interp = self.interpolation_1d(x_list, pixels, x_list_interp)
                        jjs.append(y_list_interp)
                    else:
                        jjs.append([np.nan] * 52)
                        pass
                iis.append(jjs)
            iis = np.array(iis)
            print np.shape(iis)
            np.save(self.this_root + '\\data\\GPP\\GPP_clip_temporal_interpolate\\' + str(y), iis)


def main():
    url = 'https://e4ftl01.cr.usgs.gov/MOLT/MOD15A2H.006/'
    china = ['h23v04', 'h23v05',
             'h24v04', 'h24v05',
             'h25v03', 'h25v04', 'h25v05', 'h25v06',
             'h26v03', 'h26v04', 'h26v05', 'h26v06',
             'h27v04', 'h27v05', 'h27v06',
             'h28v05', 'h28v06', 'h28v07',
             'h29v06', 'h29v07']
    M = ModisDownload(url, '')
    dates = M.gen_download_dates()
    print(dates)
    for year in range(2001,2016):

        str_year = str(year)
        for d in dates:
            if str_year == d[:4]:
                start = time.time()
                date = d
                print(date)
                Md = ModisDownload(url,date)
                Md.gen_download_list()
                download_file_num = Md.concurrent_download(10)
                print('files number',download_file_num)
                while 1:
                    time.sleep(1)
                    end = time.time()
                    print len(os.listdir(M.download_folder + date)),'/',download_file_num,int(end-start)
                    if len(os.listdir(M.download_folder+date)) == download_file_num or end-start > 1000:
                        break
                # M.MRT_mosaic()
                # M.MRT_resample()
if __name__ == '__main__':
    main()
    # url = 'https://e4ftl01.cr.usgs.gov/MOLT/MOD16A2.006/'
    # date = '2008.03.29'
    # Md = ModisDownload(url, date)
    # Md.gen_download_list()
    # Md.concurrent_download(10)