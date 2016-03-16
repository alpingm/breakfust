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
#CREATE TABLES
		
location = ("CREATE TABLE Location ("      +
            "name            VARCHAR(50)," +
            "location_id     VARCHAR(50)," +
		    "appliance 	     VARCHAR(50)," +
		    "appliance_model VARCHAR(50)," +
		    "tool_model 	 VARCHAR(50)," +
		    "logging_speed   VARCHAR(50));")

try:

    cur = con.cursor()
    cur.execute(location)

except mdb.Error, e:
		  
	print "Error %d: %s" % (e.args[0],e.args[1])
	sys.exit(1)

con.commit()
cur.close()
con.close()