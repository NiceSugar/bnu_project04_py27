# coding=utf-8

import psutil
import os
import numpy as np
from matplotlib import pyplot as plt
this_root = os.getcwd()+'\\..\\'
import time
import datetime
from osgeo import ogr,osr,gdal



def point_to_shp(inputlist,outSHPfn):
    # gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    ############重要#################
    gdal.SetConfigOption("SHAPE_ENCODING", "GBK")
    ############重要#################
    fieldType = ogr.OFTString
    # fieldType.set
    # Create the output shapefile
    shpDriver = ogr.GetDriverByName("ESRI Shapefile")
    if os.path.exists(outSHPfn):
        shpDriver.DeleteDataSource(outSHPfn)
    outDataSource = shpDriver.CreateDataSource(outSHPfn)
    outLayer = outDataSource.CreateLayer(outSHPfn, geom_type=ogr.wkbPoint)


    # create a field
    idField1 = ogr.FieldDefn('val1',fieldType)
    idField2 = ogr.FieldDefn('val2', fieldType)
    idField3 = ogr.FieldDefn('val3', fieldType)
    # idField4 = ogr.FieldDefn('val4', fieldType)
    # idField5 = ogr.FieldDefn('val5', fieldType)

    outLayer.CreateField(idField1)
    outLayer.CreateField(idField2)
    outLayer.CreateField(idField3)
    # outLayer.CreateField(idField4)
    # outLayer.CreateField(idField5)

    # Create the feature and set values

    for i in range(len(inputlist)):
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(inputlist[i][0],inputlist[i][1])

        featureDefn = outLayer.GetLayerDefn()
        outFeature = ogr.Feature(featureDefn)
        outFeature.SetGeometry(point)
        outFeature.SetField('val1', inputlist[i][2])
        outFeature.SetField('val2', inputlist[i][3])
        outFeature.SetField('val3', inputlist[i][4])
        # outFeature.SetField('val4', inputlist[i][5].encode('gbk'))
        # outFeature.SetField('val5', inputlist[i][6].encode('gbk'))

        outLayer.CreateFeature(outFeature)
        outFeature.Destroy()
    outFeature = None



def gen_points():


    f_dir = this_root+r'train_test_data\index\intermediate\\'

    flist = os.listdir(f_dir)
    flag = 0
    for f in flist:
        flag+=1
        # print()
        print(f,flag,'/',len(flist))
        arr = np.load(f_dir+f)
        in_list = []
        for p in arr:
            lon_i = float(p[1].split('_')[0])
            lat_i = float(p[1].split('_')[1])
            # print(lon_i,lat_i)
            # print(lat_i)
            in_list.append([lon_i,lat_i,'','',''])
        point_to_shp(in_list,this_root+'190522_test\\'+f+'.shp')
        # exit()


def main():
    gen_points()

if __name__ == '__main__':
    main()