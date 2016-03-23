import pymongo
import sys
import time
import json
import os
import datetime

with open('init_mongo.txt') as my_file:
    content = my_file.read().splitlines()

host = content[0]
port = int(content[1])
login = content[2]
password = content[3]
database = content[4]
log_file = "SensorValueLoggingZWayVDevzway7049415-b653d2b49b58cce3de2551a19baf6c9a.json"


client = pymongo.MongoClient(host, port)
db = client.test
db.authenticate(login, password, source='admin')



with open(log_file) as my_file:
    datas = json.load(my_file)

#FUNKAR INTE
#original_id = ObjectId()

try:

    doc0 = {"deviceId":datas['deviceId'],"deviceName":datas['deviceName']}
    db.loactionData.insert(doc0)

    print "Inserted: " + str(doc0)

    for data in datas["sensorData"]:
        
        doc1 = {"sensorID":datas['deviceId'],"time":data['time'], "value_w":data['value']}

        db.energyData.insert(doc1)
        print "Inserted: " + str(doc1)


except pymongo.errors.ServerSelectionTimeoutError as err:
    # do whatever you need
    print(err)


