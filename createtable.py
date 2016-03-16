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

loc = (raw_input('Location name (Can not contain spaces): '))
loc_id = (raw_input('Location ID: '))
app = (raw_input('Type of appliance: '))
app_model = (raw_input('Appliance model: '))
config = (raw_input('Tool: '))
logspeed = (raw_input('Loggin speed (s): '))

#INSERT LOCATION
location = ("INSERT INTO Location VALUES (" + "'" + loc + "', '" + loc_id + "', '" + app +  "', '" + app_model + "', '" + config + "','" + logspeed + "');")

#CREATE TABLE
table = ("CREATE TABLE " + loc + "("   +
          "time          VARCHAR(50)," +
          "value_w0      VARCHAR(50)," +
          "value_w1      VARCHAR(50)," +
          "value_kwh     VARCHAR(50)," +
          "openclose     VARCHAR(50)," +
          "PRIMARY KEY (time))")

try:

    cur = con.cursor()
    #INSERT LOCATION
    cur.execute(location)
    #CREATE TABLE
    cur.execute(table)

except mdb.Error, e:
		  
	print "Error %d: %s" % (e.args[0],e.args[1])
	sys.exit(1)

con.commit()
cur.close()
con.close()