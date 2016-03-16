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

drop   = ("DROP DATABASE " + database + ";")
create = ("CREATE DATABASE " + database + ";")

try:

    cur = con.cursor()
    cur.execute(drop)
    cur.execute(create)
               
except mdb.Error, e:
          
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)

con.commit()
cur.close()
con.close()