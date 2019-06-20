# coding=utf-8
# 注意：周三周四服务器可能维护，无法连接

# 181224 更新
# 加入重新连接功能，可以解决多线程下载时服务器拒绝下载

# 190212 更新

# 190222 更新
# 改变并行下载策略
# old ver：
# 每个进程：
# [p11,p12,p13,...p1n]
# [p21,p22,p23,...p2n]
#       ...
# [pn1,pn2,pn3,...pnn]
#
# new ver：
# [[p1],[p2],...,[pn]]
# 如果Python进程数小于10：
# 开启新进程
# 如果Python进程数大于10：
# 监测下载
# 注意：进程数p最好在10左右，p>=20时，容易被服务器拒绝
#
# 190301 更新
# 将多进程改为多线程
# 详见函数 ModisDownload().loop_multi_thread()

import urllib2
from cookielib import CookieJar
import os
import re
from multiprocessing import Process
from threading import Thread
import threading
import time
import psutil
# from pyhdf.SD import SD, SDC
from matplotlib import pyplot as plt
import numpy as np


class ModisDownload:
    def __init__(self, url, start_year,end_year):
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
        self.start_year = start_year
        self.end_year = end_year + 1
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
        '''

        :param urls: url list
        :param log: none
        :return: none
        '''

        print 'downloading',urls[0]
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
            # save_path = self.download_folder + 'AIRS'+'/'
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
                    time.sleep(5)
                    print 'sleep 5 seconds'
                    print 'x' * 30
                    print e
                    attempts += 1
                    print 'try ',attempts
                    success = 0

                if success == 1 or attempts > 10:

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


    def gen_download_dates_urls(self):

        # if not os.path.isdir(self.download_folder):
        #     os.mkdir(self.download_folder)
        selected_years = self.gen_download_dates()
        mode_urls_folder = self.url_folder+'\\'+self.mode
        self.make_dir(mode_urls_folder)
        url_text_file_list = []
        url_i_list = []
        # url_i_files_list = []
        for year in range(self.start_year, self.end_year):
            # print(year)
            str_year = str(year)
            for d in selected_years:
                if str_year == d[:4]:
                    url_text_file = mode_urls_folder + '\\' + d +'_'+ self.mode + '_url.txt'
                    url_text_file_list.append(url_text_file)
                    url_i = self.url + d
                    # print(url_i)
                    # exit()
                    url_i_list.append(url_i)
        return url_i_list,url_text_file_list
                #     all_url.append(temp)
                # return all_url

        # attempts = 0
        # while 1:
        #     success = 0
        #     try:
        #         url = self.url
        #         request = urllib2.Request(url)
        #         response = urllib2.urlopen(request)
        #         success = 1
        #         body = response.read()
        #         p = re.findall('/">.*?/</a>', body)
        #         # date = []
        #         all_url = []
        #         # # 清空下载地址文件
        #         # fw = open(url_text_file, 'w')
        #         # fw.close()
        #         flag = 0
        #         for i in p:
        #             flag += 1
        #             # print i[3:-5], flag, '/', len(p)
        #             date = i[3:-5] + '/'
        #             d = i[3:-5]
        #             if len(selected_dates) != 0:
        #                 if d not in selected_dates:
        #                     continue
        #             url_i = url + date
        #             request = urllib2.Request(url_i)
        #             response = urllib2.urlopen(request)
        #             body = response.read()
        #             # print body
        #             p1 = re.findall('">.*?">', body)
        #             temp = []
        #
        #             f = open(url_text_file, 'r')
        #             lines = f.readlines()
        #             f.close()
        #             fw = open(url_text_file, 'w')
        #             for line in lines:
        #                 fw.write(line)
        #             for pi in p1:
        #                 if '.hdf' in pi and not '.xml' in pi:
        #                     # if 0:
        #                     fname = pi[12:-2]
        #                     download_url = url_i + fname
        #                     fw.write(download_url + '\n')
        #                     # print download_url
        #                     temp.append(download_url)
        #             fw.close()
        #             all_url.append(temp)
        #         return all_url
        #     except:
        #         success = 0
        #         attempts += 1
        #     if attempts > 10 or success == 1:
        #         break

    def download_dates_url(self,url_i,url_text_file):
        for i in range(len(url_i)):
            if os.path.isfile(url_text_file[i]):
                print(url_text_file[i],'is already existed')
                continue
            attempts = 0
            while 1:
                success = 0
                try:
                    request = urllib2.Request(url_i[i])
                    response = urllib2.urlopen(request)
                    body = response.read()
                    # print body
                    p1 = re.findall('">.*?">', body)
                    temp = []
                    fw = open(url_text_file[i], 'w')

                    for pi in p1:
                        if '.hdf' in pi and not '.xml' in pi:
                            # if 0:
                            fname = pi[12:-2]
                            download_url = url_i[i] + '/' + fname
                            fw.write(download_url + '\n')
                            temp.append(download_url)
                    fw.close()
                    print url_i[i],'done'
                    success = 1
                except Exception as e:
                    time.sleep(5)
                    print('sleep 5 seconds')
                    print 'x' * 30
                    print e
                    attempts += 1
                    print 'try ', attempts
                    success = 0
                if attempts > 10 or success == 1:
                    break

    def concurrent_split(self,n,process):
        # method of split
        m = []
        parts = process
        split_num = len(n) / parts
        for i in range(len(n) / split_num):
            m.append(n[i * split_num:(i + 1) * split_num])
        tail = len(n) - len(m) * split_num
        m.append(n[-tail:])

        return m


    def download_dates_url_concurrent(self, process):
        url_i_list, url_text_file_list = self.gen_download_dates_urls()
        # print(url_i_list)
        url_split = self.concurrent_split(url_i_list,process)
        url_text_file_list_split = self.concurrent_split(url_text_file_list,process)

        for i in range(len(url_split)):
            time.sleep(1)
            print('starting Thread ',i+1)
            p = Thread(target=self.download_dates_url, args=(url_split[i], url_text_file_list_split[i]))
            p.start()
        len_url = len(url_i_list)

        start = time.time()
        while 1:
            time.sleep(1)
            end = time.time()
            print len(os.listdir(self.url_folder + self.mode)), '/', len_url, int(end - start)
            if len(os.listdir(self.url_folder + self.mode)) == len_url or end - start > 1000:
                break

    def concurrent_download(self, process):
        '''
        并行下载
        '''
        url_text_file_folder = self.url_folder + '\\' +self.mode+'\\'
        print(url_text_file_folder)
        all_lines = []
        for fi in os.listdir(url_text_file_folder):
            f = open(url_text_file_folder+fi, 'r')
            lines = f.readlines()
            for line in lines:
                line = line.split('\n')[0]
                all_lines.append(line)
        print(len(all_lines))
        # all_lines = '\n'.join(all_lines)
        # print(all_lines)
        # exit()
        # f = open(url_text_file, 'r')
        lines = all_lines
        # f.close()
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

            # l = l.split('\n')[0]
            # 全球
            # lines_new.append(l)
            # 中国
            for c in china:
                if c in l:
                    lines_new.append(l)

        # print(len(lines_new))
        # exit()
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
                print 'starting Thread ',i
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


    def count_files_num(self):
        files_number = 0
        for root, dirs, files in os.walk(M.download_folder, topdown=False):
            for name in files:
                files_number += 1
        return files_number
        pass


    def count_python_process(self):
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

    def loop(self):

        url_text_file_folder = self.url_folder + '\\' + self.mode + '\\'
        print(url_text_file_folder)
        all_lines = []
        for fi in os.listdir(url_text_file_folder):
            f = open(url_text_file_folder + fi, 'r')
            lines = f.readlines()
            for line in lines:
                line = line.split('\n')[0]
                all_lines.append(line)
        # print(len(all_lines))
        lines = all_lines
        # f.close()
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
            for c in china:
                if c in l:
                    lines_new.append(l)
        print(len(lines_new))
        start = time.time()
        for i in range(len(lines_new)):
            fname = lines_new[i].split('/')[-1]
            save_path = self.download_folder + lines_new[i].split('/')[-2] + '/'
            if os.path.isfile(save_path + fname):
                print save_path + fname,'is already existed'
                continue
            p = Process(target=self.download_file, args=([lines_new[i]], ''))
            p.start()
            time.sleep(1)
            while 1:

                python_process = self.count_python_process()
                if python_process <= 10:
                    break
                else:
                    end = time.time()
                    # print
                    current_files_len = self.count_files_num()
                    print current_files_len,'/',len(lines_new),int(end-start),'s','/','python_process',python_process
                    # print('init_files_len',init_files_len)
                    time.sleep(1)


    def loop_multi_thread(self):

        url_text_file_folder = self.url_folder + '\\' + self.mode + '\\'
        print(url_text_file_folder)
        all_lines = []
        for fi in os.listdir(url_text_file_folder):
            f = open(url_text_file_folder + fi, 'r')
            lines = f.readlines()
            for line in lines:
                line = line.split('\n')[0]
                all_lines.append(line)
        # print(len(all_lines))
        lines = all_lines
        # f.close()
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
            for c in china:
                if c in l:
                    lines_new.append(l)
        print(len(lines_new))
        start = time.time()
        for i in range(len(lines_new)):
            fname = lines_new[i].split('/')[-1]
            save_path = self.download_folder + lines_new[i].split('/')[-2] + '/'
            if os.path.isfile(save_path + fname):
                print save_path + fname,'is already existed'
                continue
            # 多线程更新
            p = Thread(target=self.download_file, args=([lines_new[i]], ''))
            p.start()
            time.sleep(1)
            while 1:
                # 更新
                # python_process = self.count_python_process()
                python_process = len(threading.enumerate())
                if python_process <= 10:
                    break
                else:
                    end = time.time()
                    # print
                    current_files_len = self.count_files_num()
                    print current_files_len,'/',len(lines_new),int(end-start),'s','/','python_process',python_process
                    # print('init_files_len',init_files_len)
                    time.sleep(1)



def main():
    start = time.time()
    # url = 'https://e4ftl01.cr.usgs.gov/MOLT/MOD11A2.006/'
    url = 'https://e4ftl01.cr.usgs.gov/MOTA/MCD12Q1.006/'
    start_year = 2003
    end_year = 2016
    M = ModisDownload(url,start_year,end_year)
    M.download_dates_url_concurrent(10)
    # exit()
    len_files = M.concurrent_download(20)
    while 1:
        time.sleep(1)
        end = time.time()
        files_number = 0
        for root, dirs, files in os.walk(M.download_folder, topdown=False):
            for name in files:
                files_number += 1
                # print(os.path.join(root, name))
        print files_number, '/', len_files, int(end - start)
        if files_number == len_files:
            break

    pass



if __name__ == '__main__':
    # url = 'https://e4ftl01.cr.usgs.gov/MOTA/MCD12Q1.006/'
    # start_year = 2003
    # end_year = 2016
    # M = ModisDownload(url, start_year, end_year)
    # M.loop()
        # for name in dirs:
        #     print(os.path.join(root, name))
    main()