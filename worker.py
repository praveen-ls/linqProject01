from kafka import KafkaConsumer
from kafka.errors import KafkaError
import json
import psycopg2
import time
from datetime import datetime

server="localhost:9092"
workersSubMessage = KafkaConsumer('workerData', bootstrap_servers=[server], auto_offset_reset='earliest', enable_auto_commit=True,value_deserializer=lambda x: x.decode('utf-8') if x else None
    )

#for message in workersSubMessage:
#    print(message.value)
DBCONFIG = {
    "dbname": "tsdb",
    "user": "tsdbadmin",
    "password": "rs0b9u57afc1f344",
    "host": "t4h6sqbzyc.xq0dr8321m.tsdb.cloud.timescale.com",
    "port": "35046"
}
def getAggregatedData():
    connection = psycopg2.connect(**DBCONFIG)
    #print("DEBUG::connected")
    cursor = connection.cursor()
    cursor.execute("SELECT color,count,valueSum,average FROM aggregate;")
    data=cursor.fetchall()
    #print("DEBUG::retrieved")
    cursor.close()
    connection.close()
    colorData = {} 
    if data:
        for color,count,valueSum,average in data:
            colorData[color] = {"count":count,"valueSum":valueSum}
    return colorData


def aggregatedMessageToDB(timest,color,avg,sumof,colorData):
    connection = psycopg2.connect(**DBCONFIG)
    #print("DEBUG::connected")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO message (time, color, sum, average) VALUES (%s, %s, %s, %s);",
        (timest, color, sumof, average))
    cursor.execute("INSERT INTO aggregate (time, color, count,valueSum,average) VALUES (%s, %s, %s,%s,%s) ",
                   (timest,color,colorData["count"],colorData["valueSum"],colorData["average"]))
    connection.commit()
    #print("DEBUG::commited")
    cursor.close()
    connection.close()

timeWindowData = {}
window = 15
startTime = time.time()
colorData = getAggregatedData()
for message in workersSubMessage:
    data = json.loads(message.value)  
    color = data.get("color")
    value = int(data.get("value"))
    if color not in timeWindowData:
        timeWindowData[color] = []
    timeWindowData[color].append(value)
    #print("fDEBUG:: {time.time() -startTime}")
    if time.time() - startTime >= window:
        #print(timeWindowData)
        timestamp = datetime.utcnow()
        
        for color, values in timeWindowData.items():
            #print("DEBUG::values")
            #print(values)
            sumof = sum(values)
            average = sumof/len(values)
            #print("DEBUG:: sum {sumof}")
            #print("DEBUG:: average {average}")
            if color not in colorData:
                colorData[color]={"count":len(values),"valueSum":sumof,"average":average}
            else:
                ccount=colorData[color]["count"]+len(values)
                cvalue=colorData[color]["valueSum"]+sumof
                colorData[color]={"count":ccount,"valueSum":cvalue,"average":cvalue/ccount}
            
            aggregatedMessageToDB(timestamp, color, sumof, average,colorData[color])

        timeWindowData = {}
        startTime = time.time()
