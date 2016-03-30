import pymongo
import sys
import os
import time
import json
import datetime

#### Initialization ####
#Location and tool identification numbers
loc_id = "1"
dev_id = "1"

#Dictionary for sensor data
mongodict = {}

#Files contained on the Raspberry Pi that Z-Wave components log to.
file_w1 = "SensorValueLoggingZWayVDevzway7049415-b653d2b49b58cce3de2551a19baf6c9a.json"
file_d = "SensorValueLoggingZWayVDevzway9048114-afd4edf97cd3c8497ea7f13f4e0cbde1.json"
files = [file_w1]

#Array for correct order of timestamps
timestamps = []


#Loads init file containing: ip, port, login, password and database
with open('init_mongo.txt') as my_file:
    content = my_file.read().splitlines()

host = content[0]
port = int(content[1])
login = content[2]
password = content[3]
database = content[4]

#### Datastructures ####
#Constructs a data point
class Data_point:
    w1 = 0
    w2 = 0
    kwh = 0
    d = ""

    def __str__(self):
        return "w1: " + str(self.w1) + ', w2: ' + str(self.w2) + ', kwh:' + str(self.kwh) + ', door: ' + str(self.d)


while(1):
#### Parsing of input files ####
    #Reads the log files and creates an entry in the mongodict for every second.
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
                    if int(data['time']) not in mongodict:
                        point = Data_point()
                        if arg == file_w1:
                            point.w1 = data['value']
                        elif arg == file_d:
                            point.d = data['value']

                        mongodict[int(data['time'])] = point
                        timestamps.append(int(data['time']))
                        
                    # Otherwise
                    else:
                        temppoint = mongodict[int(data['time'])]     

                        if arg == file_w1:
                            temppoint.w1 = data['value'] 
                        elif arg == file_d:
                            temppoint.d = data['value']

                        mongodict[int(data['time'])] = temppoint
            # Truncate the file just read
            open(arg, 'w').close()

#### Database communication ####
    #Open connection to database
    client = pymongo.MongoClient(host, port)
    db = client.energy
    db.authenticate(login, password, source='admin')

    #for key in mongodict:
    for key in timestamps:
        point = mongodict[key]

        #print point
        milliseconds = int(str(key)[-3:])
        realtime = datetime.datetime.fromtimestamp(float(str(key)[0:-3])).strftime('%Y-%m-%d %H:%M:%S')

        #Creating hourly input

        #sql = "INSERT IGNORE INTO Omegapoint VALUES (" + "'" + str(realtime) + ":" + str(milliseconds) + "','" +  str(point.w1)  + "','" + str(point.d) + "')"

        try:

            doc_sensordata = {"locationId":loc_id, "deviceId":dev_id, "time":str(realtime) + ":" + str(milliseconds), "value_w":str(point.w1), "door":str(point.d)}
            #db.energyData.insert(doc_sensordata)
            print doc_sensordata


        except pymongo.errors.ServerSelectionTimeoutError as err:
            # do whatever you need
            print(err)
 
    
    print "Done with uploading, going again in 5 minutes" 
    
    timestamps = []
    mongodict = {}

    time.sleep(300)