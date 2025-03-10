from kafka import KafkaConsumer
from kafka.errors import KafkaError
import json
import psycopg2
import time
from datetime import datetime

server="localhost:9092"
workersSubMessage = KafkaConsumer('workerDataTest', bootstrap_servers=[server], auto_offset_reset='earliest', enable_auto_commit=True,value_deserializer=lambda x: x.decode('utf-8') if x else None
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
def aggregatedMessageToDB(timest,color,avg,sumof):
    connection = psycopg2.connect(**DBCONFIG)
    #print("DEBUG::connected")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO message (time, color, sum, average) VALUES (%s, %s, %s, %s);",
        (timest, color, sumof, average))
    connection.commit()
    #print("DEBUG::commited")
    cursor.close()
    connection.close()

timeWindowData = {}
window = 15
startTime = time.time()
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
        timestamp = datetime.now(datetime.UTC)
        
        for color, values in timeWindowData.items():
            #print("DEBUG::values")
            #print(values)
            sumof = sum(values)
            average = sumof/len(values)
            #print("DEBUG:: sum {sumof}")
            #print("DEBUG:: average {average}")
            aggregatedMessageToDB(timestamp, color, sumof, average)

        timeWindowData = {}
        startTime = time.time()
