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

#EMPTY DATABASE

sql1 =("INSERT INTO Location VALUES ('1', 'OP', 'Wine-frigde', '?', '1', 'Z-Wave Aoen Labs Socket', '3')")
sql1 =("INSERT INTO Location VALUES ('1', 'OP', 'Wine-frigde', '?', '1', 'Z-Wave Aoen Labs Socket', '3')")
	
try:

    cur = con.cursor()
    cur.execute(sql1)
    
               
except mdb.Error, e:
          
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)

con.commit()
cur.close()
con.close()
