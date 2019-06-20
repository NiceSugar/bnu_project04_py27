# coding=utf-8
import os
import time

this_root = os.getcwd()

def check(dir):
    date_folders = os.listdir(dir)
    flag = 0
    for date in date_folders:
        # print(date)
        file_list = os.listdir(os.path.join(dir,date))
        if len(file_list) != 20:
            flag += 1
            print(date,'missing some files',20-len(file_list))

    print('all files are checked')
    if flag == 0:
        print('no missing files')
    else:
        pass
    pass


def check_date(url_dir,download_dir):
    date_url = []
    for d in os.listdir(url_dir):
        d=d.split('_')[0]
        date_url.append(d)
    date_data = []
    for d in os.listdir(download_dir):
        date_data.append(d)

    flag = 0
    for d in date_data:
        if not d in date_url:
            print(d)
            flag += 1
    print('all dates are checked')
    if flag == 0:
        print('no missing dates')
    else:
        pass
    pass


def main():
    product = 'MOD11A2.006'
    dir = os.path.join(this_root,'download_data',product)
    url_dir = os.path.join(this_root,'urls',product)
    # print(os.listdir(url_dir))
    check(dir)
    check_date(url_dir,dir)


if __name__ == '__main__':
    main()



