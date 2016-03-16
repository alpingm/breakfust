#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys

content = []

with open('init.txt') as my_file:
    content = my_file.read().splitlines()

ip = content[0]
login = content[1]
password = content[2]
database = content[3]

con = mdb.connect(ip, login, password, database);

with open(sys.argv[1],'r') as my_file:
    for line in my_file:
        temp = line.split(';')

        if len(temp) >= 12:
            sql =("INSERT INTO op1 VALUES(" + "'" + temp[0] + "','" + temp[1] + "','" + temp[2] + "','" + 
                                                 temp[3] + "','" + temp[4] + "','" + temp[5] + "','" + 
                                                 temp[6] + "','" + temp[7] + "','" + temp[8] + "','" + 
                                                 temp[9] + "','" + temp[10] + "')")

        try:

            cur = con.cursor()
            cur.execute(sql)
            
        except mdb.Error, e:
          
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)

con.commit()
cur.close()
con.close()