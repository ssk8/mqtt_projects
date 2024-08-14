import paho.mqtt.client as mqtt
from datetime import datetime, timedelta

global last_write_time
last_write_time = dict() 

def on_connect(client, userdata, flags, reason_code, properties):
    global last_write_time
    print(f"Connected with result code {reason_code}")
    for topic in ("+/temp","+/temperature","+/pressure", "+/humidity"):
        client.subscribe(topic)
    client.subscribe("test")

def on_message(client, userdata, msg):
    global last_write_time
    if msg.topic.startswith("pi"):
        message = f"{datetime.now()}, {msg.topic}, {float(msg.payload)}"
    else: 
        message = f"{msg.topic}: {str(msg.payload)[2:-1]}"
    if (last_write_time.get(msg.topic, datetime.now()-timedelta(minutes=31)) +timedelta(minutes=30)) < datetime.now():
        with open("log.csv","a") as log:
            log.write(message+"\n")
            if msg.topic.startswith("pi"):
                last_write_time[msg.topic] = datetime.now()
    print(message)
    

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("tbox", 1883, 60)


mqttc.loop_forever()

