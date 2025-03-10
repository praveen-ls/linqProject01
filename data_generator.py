from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import random
import time

server= "localhost:9092"
dataGenerator = KafkaProducer(
    bootstrap_servers=[server],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

def sendMessage(topic, message):
    dataGenerator.send(topic,message)
    dataGenerator.flush()

colors = ["red", "blue", "green", "yellow","white","black","gray"]
try:
    for i in range(0,10000):
        colorSelection = colors[random.randint(0,6)]
        jsonMessage={"color": colorSelection,"value": random.randint(1,100)}
        sendMessage("workerDataTest",jsonMessage)
        time.sleep(1)
except KafkaError as e:
    print(f"DEBUG:: Error occured: {e}")
finally:
    dataGenerator.close()
