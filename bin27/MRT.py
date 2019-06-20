# coding=utf-8

import os

this_root = os.getcwd()+'\\..\\'

class MRT:

    def __init__(self,download_folder):
        # self.date = date
        self.download_folder = download_folder
        self.temp_folder = this_root+'\\temp\\'
        self.product = self.download_folder.split('\\')[-2]
        self.output = this_root+'\\data_tif\\'
        self.product_output_folder = self.output+self.product

        self.mk_dir(self.temp_folder)
        self.mk_dir(self.output)
        self.mk_dir(self.product_output_folder)
        pass


    def mk_dir(self,dir):
        if not os.path.isdir(dir):
            os.mkdir(dir)


    def gen_dates(self):
        dates = os.listdir(self.download_folder)
        return dates
        # pass

    def MRT_mosaic(self,date):
        # 生成要拼接的文件列表
        # dates = self.gen_dates()
        d = date
        f_dir = self.download_folder + d + '\\'
        f_list = os.listdir(f_dir)
        temp_file_list_folder = self.temp_folder +'\\'+self.product+'\\'
        self.mk_dir(temp_file_list_folder)
        file_list = temp_file_list_folder + d +'_files.txt'
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

        f = open(file_list, 'w')

        for fi in f_list:
            # 是否选择中国
            # 否
            # f.write(f_dir + fi + '\n')

            for c in china:
                # 是
                if c in fi:
                    f.write(f_dir + fi + '\n')
                    print f_dir+fi
                # else:
                #     print(f_dir+fi,'*****')

        f.close()
        # exit()
        # MRT 拼接命令行
        mrt_mosaic = os.path.join(this_root,'MRT\\bin\\mrtmosaic.exe')
        mosaic_cmd_line = mrt_mosaic + ' -i ' + file_list + ' -s "1 0 0 0 0 0 0 0 0 0 0 0 0" -o ' + temp_file_list_folder + d + '_mosaic.hdf'
        # print cmd_line
        print mosaic_cmd_line
        os.system(mosaic_cmd_line)


    def MRT_resample(self,date,conf_file):

        # MRT 投影重采样
        temp_file_list_folder = self.temp_folder +'\\'+self.product+'\\'
        mrt_resample = os.path.join(this_root,'MRT\\bin\\resample.exe')
        # dates = self.gen_dates()
        d = date
        output_file = self.product_output_folder+'\\'+d+'.tif'
        resample_cmd_line = mrt_resample + ' -i ' + temp_file_list_folder + d +'_mosaic.hdf -p ' + conf_file + ' -o ' + output_file
        print resample_cmd_line
        os.system(resample_cmd_line)


    def delete_temp_hdf(self):
        temp_file_list_folder = self.temp_folder + '\\' + self.product + '\\'
        f = temp_file_list_folder + d + '_mosaic.hdf'
        try:
            os.remove(f)
        except:
            pass
        # print(f)

    def loop_mosaic(self):

        pass

    def loop_resample(self):

        pass


# MRT().MRT_mosaic('2003.01.01','D:\\MODIS\\download_data\\MOD11A2.006\\','D:\\MODIS\\temp\\').
# download_folder = 'D:\\MODIS\\download_data\\MOD09A1\\'
download_folder = 'D:\\MODIS\\bin\\download_data\\MCD12Q1.006\\'
# MRT(download_folder).MRT_mosaic('2003.01.01')
M = MRT(download_folder)
# print MRT(download_folder).download_folder.split('\\')[-2]
dates = M.gen_dates()
conf_file = this_root+'conf\\landcover.prm'
for d in dates:
    M.MRT_mosaic(d)
    M.MRT_resample(d,conf_file)
    M.delete_temp_hdf()
    # break