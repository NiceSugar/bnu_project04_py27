# coding=utf-8


import psutil
import os
import numpy as np
from matplotlib import pyplot as plt
this_root = os.getcwd()+'\\..\\'
import time
import datetime
from osgeo import ogr,osr
# mode =




def point_to_shp(inputlist,outSHPfn):
    fieldType = ogr.OFTString
    # Create the output shapefile
    shpDriver = ogr.GetDriverByName("ESRI Shapefile")
    if os.path.exists(outSHPfn):
        shpDriver.DeleteDataSource(outSHPfn)
    outDataSource = shpDriver.CreateDataSource(outSHPfn)
    outLayer = outDataSource.CreateLayer(outSHPfn, geom_type=ogr.wkbPoint)


    # create a field
    # idField1 = ogr.FieldDefn('val1', fieldType)
    # idField2 = ogr.FieldDefn('val2', fieldType)
    # idField3 = ogr.FieldDefn('val3', fieldType)
    # idField4 = ogr.FieldDefn('val4', fieldType)
    # idField5 = ogr.FieldDefn('val5', fieldType)
    #
    # outLayer.CreateField(idField1)
    # outLayer.CreateField(idField2)
    # outLayer.CreateField(idField3)
    # outLayer.CreateField(idField4)
    # outLayer.CreateField(idField5)

    # Create the feature and set values

    for i in range(len(inputlist)):
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(inputlist[i][0],inputlist[i][1])

        featureDefn = outLayer.GetLayerDefn()
        outFeature = ogr.Feature(featureDefn)
        outFeature.SetGeometry(point)
        # outFeature.SetField('val1', inputlist[i][2].encode('gbk'))
        # outFeature.SetField('val2', inputlist[i][3].encode('gbk'))
        # outFeature.SetField('val3', inputlist[i][4].encode('gbk'))
        # outFeature.SetField('val4', inputlist[i][5].encode('gbk'))
        # outFeature.SetField('val5', inputlist[i][6].encode('gbk'))

        outLayer.CreateFeature(outFeature)
        outFeature.Destroy()
    outFeature = None


def plot_stations_and_invali_sta():
    sta_pos_dic = np.load(this_root + 'ANN_input_para\\00_PDSI\\sta_pos_dic.npz')
    invalid_dir = this_root+'invalid_sta\\'
    flist = os.listdir(invalid_dir)
    x=[]
    y=[]
    for f in flist:
        sta = f.split('.')[0]
        x.append(sta_pos_dic[sta][1])
        y.append(sta_pos_dic[sta][0])
    plt.figure()
    plt.scatter(x,y)

    x = []
    y = []
    for sta in sta_pos_dic:
        # print(sta_pos_dic[sta])
        # exit()
        x.append(sta_pos_dic[sta][1])
        y.append(sta_pos_dic[sta][0])
    plt.figure()
    plt.scatter(x,y)
    plt.show()


def plot_origin_pix():
    fdir = this_root+'data_transform\\split_lst\\'
    flist = os.listdir(fdir)
    in_list = []
    for f in flist:
        npz = np.load(fdir+f)
        x = []
        y = []
        z = []
        flag = 0
        for lon_lat in npz:
            flag+=1
            if flag%1000 == 0:
                print(flag,'/',len(npz))
            if flag > 5000:
                continue
            lon = float(lon_lat.split('_')[1])
            lat = float(lon_lat.split('_')[0])

            in_list.append([lat,lon])
            x.append(lat)
            y.append(lon)
            z.append(npz[lon_lat][0])

        colors = []
        flag = 0
        min = float(np.min(z))
        max = float(np.max(z))
        for i in z:
            flag+=1
            if flag%1000 == 0:
                print(flag,'/',len(z))
            colors.append((i-min)/(max-min))
        colors = np.array(colors)
        plt.figure()
        plt.scatter(x,y,c=colors,cmap='jet')
        plt.colorbar()
        plt.show()
        break

    point_to_shp(in_list,'origin.shp')


def modify_wrong_pix():
    fdir = this_root + 'data_transform\\split_lst\\'
    flist = os.listdir(fdir)

    for f in flist:
        npz = np.load(fdir + f)
        x = []
        y = []
        z = []
        flag = 0
        for lon_lat in npz:
            flag += 1
            if flag % 2000 == 0:
                print(flag, '/', len(npz))
            if flag > 20000:
                continue
            lon = float(lon_lat.split('_')[1])
            lat = float(lon_lat.split('_')[0])

            # in_list.append([lat, lon])
            x.append(lat)
            y.append(lon)
            z.append(npz[lon_lat][0])

        y_mid5 = (60.0000958813812+10.0194697231069)/2
        # print(y_mid1)
        # print(y_mid2)

        in_list = []
        y_new = []
        for i in y:
            y_new.append(2*y_mid5-i)
        for i in range(len(y)):
            in_list.append([x[i],y_new[i]])
        point_to_shp(in_list,'y_mid7.shp')
        break


def grace_pix():
    npz = np.load(this_root+'GRACE\\transform_data\\data_transform.npz')
    x = []
    y = []
    for i in npz:
        lon = float(i.split('_')[0])
        lat = float(i.split('_')[1])
        x.append(lon)
        y.append(lat)
    plt.scatter(x,y)
    plt.show()


def smci_pix():
    npz = np.load(this_root + 'ANN_input_para\\07_SMCI\\SMCI.npz')
    x = []
    y = []
    for i in npz:
        lon = float(i.split('_')[0])
        lat = float(i.split('_')[1])
        x.append(lon)
        y.append(lat)
    plt.scatter(x, y)
    plt.show()


def pci_pix():
    npz = np.load(this_root + 'ANN_input_para\\08_PCI\\PCI.npz')
    x = []
    y = []
    for i in npz:
        lon = float(i.split('_')[0])
        lat = float(i.split('_')[1])
        x.append(lon)
        y.append(lat)
    plt.scatter(x, y)
    plt.show()


def irrigation_pix():
    print('loading npy...')
    npy = np.load(this_root + 'ANN_input_para\\09_Irrigation\\irrigated_data_transform.npy').item()
    print('done')
    x = []
    y = []
    print('transforming dict')
    npy = dict(npy)
    print('done')
    flag = 0
    for i in npy:
        flag+=1
        if flag%100000 == 0:
            print(flag,'/',len(npy))
        if flag % 1000 == 0:
            lon = float(i.split('_')[0])
            lat = float(i.split('_')[1])
            x.append(lon)
            y.append(lat)
    print('ploting...')
    print(len(x))
    plt.scatter(x,y)
    plt.show()



def Landcover_pix():

    print('loading npy...')
    npy = np.load(this_root + 'ANN_input_para\\10_Landcover\\landcover_dic.npy').item()
    print('done')
    x = []
    y = []
    print('transforming dict')
    npy = dict(npy)
    print('done')
    flag = 0
    for i in npy:
        flag+=1
        if flag%100000 == 0:
            print(flag,'/',len(npy))
        if flag<10000:
            lon = float(i.split('_')[0])
            lat = float(i.split('_')[1])
            x.append(lon)
            y.append(lat)
    print('ploting...')
    print(len(x))
    plt.scatter(x,y)
    plt.show()


def DEM_pix():
    print('loading npy...')
    npy = np.load(this_root + 'ANN_input_para\\11_DEM\\DEM_data_transform_normalized.npy').item()
    print('done')
    x = []
    y = []
    print('transforming dict')
    npy = dict(npy)
    print('done')
    flag = 0
    for i in npy:
        flag += 1
        if flag % 100000 == 0:
            print(flag, '/', len(npy))
        if flag % 1000 == 0:
            lon = float(i.split('_')[0])
            lat = float(i.split('_')[1])
            x.append(lon)
            y.append(lat)
    print('ploting...')
    print(len(x))
    plt.scatter(x, y)
    plt.show()



def AWC_pix():
    print('loading npy...')
    # npy = np.load(this_root + 'ANN_input_para\\12_AWC\\awc_dic_standardize.npy').item()
    npy = np.load(this_root + 'AWC\\from_wujianjun\\awc_dic.npy').item()
    print('done')
    x = []
    y = []
    z = []
    print('transforming dict')
    npy = dict(npy)
    print('done')
    flag = 0
    for i in npy:
        flag += 1
        if flag % 1000 == 0:
            print(flag, '/', len(npy))
        if 1:
            lon = float(i.split('_')[0])
            lat = float(i.split('_')[1])
            x.append(lon)
            y.append(lat)
            z.append(npy[i])
    print('ploting...')
    print(len(x))

    colors = []
    flag = 0
    min = float(np.min(z))
    max = float(np.max(z))
    for i in z:
        flag += 1
        if flag % 1000 == 0:
            print(flag, '/', len(z))
        colors.append((i - min) / (max - min))
    colors = np.array(colors)
    plt.figure()
    plt.scatter(x, y, c=colors, cmap='jet')
    plt.colorbar()
    plt.show()
    plt.scatter(x, y)
    plt.show()


def main():
    pdsi_dic = np.load(this_root+'train_test_data\\07_SMCI_dic.npy').item()
    pdsi_dic = dict(pdsi_dic)
    print(len(pdsi_dic))
    # for i in pdsi_dic:
    #     print(i)
    #     print(pdsi_dic[i])
    # npz = np.load(this_root + 'ANN_input_para\\07_SMCI\\SMCI.npz')
    # for npy in npz:
    #     val = npz[npy]
    #     print(val)

        # print(np.shape(npy))


if __name__ == '__main__':
    main()