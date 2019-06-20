# coding=utf-8

import os
import numpy as np
import time
from matplotlib import pyplot as plt
import psycopg2



this_root = os.getcwd()+'\\..\\'
class PostgreSQL:

    def __init__(self):
        '''

        Args:
            mode: PRE or temp

        Returns:

        '''
        self.conn = psycopg2.connect(database='modis', user="ly", password="123", host="127.0.0.1", port="5432")
        print "Opened database successfully"
        self.cur = self.conn.cursor()


    def mk_table(self,table_name):
        table_name = '"'+table_name+'"'
        self.cur.execute("CREATE TABLE "+
                table_name
               +" (OID      INT     PRIMARY KEY     NOT NULL,\
               date          TEXT,\
               val           REAL)")
        self.conn.commit()
        # print "Table created successfully"


    def insert_val(self,table_name,OID,date,val):
        # print "INSERT INTO "+table_name+" (OID,STA,lon,lat,date,val) VALUES ("+OID+","+STA+","+lon+","+lat+","+date+","+val+")"
        table_name = '"'+table_name+'"'
        OID = "'"+OID+"'"
        date = "'"+date+"'"
        val = "'"+val+"'"
        # print "INSERT INTO "+table_name+" (OID,STA,lon,lat,date,val) VALUES ("+OID+","+STA+","+lon+","+lat+","+date+","+val+")"
        self.cur.execute("INSERT INTO "+table_name+" (OID,date,val) VALUES ("+OID+","+date+","+val+")")
        self.conn.commit()

    def query_DB(self,query):
        self.cur.execute(query)
        a = self.cur.fetchall()
        return a

    def close_DB(self):
        self.conn.close()

print('loading dic...')
lon_lat_dic = np.load(this_root + '\\conf\\lon_lat_dic.npy').item()
print('done')
lon_lat_dic = dict(lon_lat_dic)
flag = 0
P = PostgreSQL()
for pix in lon_lat_dic:
    flag += 1.
    if flag % 100 == 0:
        print flag / len(lon_lat_dic) * 100, '%'
    # x = int(pix.split('.')[0])
    # y = int(pix.split('.')[1])
    table_name = str(lon_lat_dic[pix][0]) + '_' + str(lon_lat_dic[pix][1])
    P.mk_table(table_name)
P.close_DB()