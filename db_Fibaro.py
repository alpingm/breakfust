import MySQLdb as mdb
import sys
import time
import json
import os
import datetime

sqldict = {}
loc_id = "1"
tool_id = "1"

#file_w1 = "SensorValueLoggingZWayVDevzway7050214-0296b831126ab6556d80579af60c9194.json"
file_w1 = "SensorValueLoggingZWayVDevzway7049414-9b38b91de0dead60c6830a8ed9a3ab51.json"
#file_w2 = "SensorValueLoggingZWayVDevzway7050216-50a0f88e1a973d908a265ec0282dc48b.json"
file_d = "SensorValueLoggingZWayVDevzway9048115-4d71598f17715df5c371ab443e33ff5c.json"
#file_kwh = "SensorValueLoggingZWayVDevzway7050217-b70ddde05f49467d22116300e81c47e9.json"

#files = [file_w1, file_w2, file_kwh, file_d]
#files = [file_w1, file_d]
files = [file_w1]
timestamps = []

with open('init.txt') as my_file:
    content = my_file.read().splitlines()

ip = content[0]
login = content[1]
password = content[2]
database = content[3]

class Data_point:
    w1 = 0
    w2 = 0
    kwh = 0
    d = ""

    def __str__(self):
        return "w1: " + str(self.w1) + ', w2: ' + str(self.w2) + ', kwh:' + str(self.kwh) + ', door: ' + str(self.d)


while(1):
        # For each file
    for arg in files:
        print "Processing New file: " + arg
        # Check if they have content, otherwise print error and break for loop
        if os.stat(arg).st_size > 0:
            with open(arg,'r+') as my_file:
                datas = json.load(my_file)
                # Iterate through the sensorData part of json object
                for data in datas["sensorData"]:
                    # If the timestamp has not been entered previously to dict
                    if int(data['time']) not in sqldict:
                       # print "Creating new data point and adding to timestamp: " + str(data['time'])
                        point = Data_point()
                        if arg == file_w1:
                            point.w1 = data['value']
                        #elif arg == file_w2:
                         #   point.w2 = data['value']
                        #elif arg == file_kwh:
                         #   point.kwh = data['value']
                        elif arg == file_d:
                           # print "Logging file was door, creating new"
                            point.d = data['value']

                        sqldict[int(data['time'])] = point
                        timestamps.append(int(data['time']))
                        
                    # Otherwise
                    else:
                       # print "Adding new value to point: " +  str(data['time'])   
                        temppoint = sqldict[int(data['time'])]     

                        if arg == file_w1:
                            temppoint.w1 = data['value'] 
                        #elif arg == file_w2:
                         #   temppoint.w2 = data['value']
                        #elif arg == file_kwh:
                         #   temppoint.kwh = data['value']
                        elif arg == file_d:
                            print "Logging file was door, appending"
                            temppoint.d = data['value']

                        sqldict[int(data['time'])] = temppoint
            # Truncate the file just read
            open(arg, 'w').close()

        #else:
           # print "Error: one of files are empty, trying again next run"
            # Break the for loop and wait 120 seconds before next run.
            #break


    con = mdb.connect(ip, login, password, database);
    #for key in sqldict:
    for key in timestamps:
        point = sqldict[key]

        #print point
        milliseconds = int(str(key)[-3:])
        realtime = datetime.datetime.fromtimestamp(float(str(key)[0:-3])).strftime('%Y-%m-%d %H:%M:%S')

        #sql =("INSERT INTO Config_1 VALUES ("+ loc_id + ",'" + tool_id + "', " + key + ",'value_w','value_v','value_a','value_kwh')")
        sql = "INSERT IGNORE INTO Omegapoint VALUES (" + "'" + str(realtime) + ":" + str(milliseconds) + "','" +  str(point.w1)  + "','" + str(point.d) + "')"
       # print "Key: " + str(key)
        #print "Milliseconds: " + str(milliseconds)
        #if str(point.d) == "on":
        print sql

        try:
            cur = con.cursor()
            cur.execute(sql)
        except mdb.Error, e:
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)
    
    print "Done with uploading, going again in 5 minutes" 
    
    timestamps = []
    sqldict = {}	
    con.commit()
    cur.close()
    con.close()

    time.sleep(300)
