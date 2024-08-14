#!/usr/bin/python

import paho.mqtt.publish as publish
from time import sleep
from smbus2 import SMBus
from bmp280 import BMP280

def get_temp():
    probe_adress = "/sys/bus/w1/devices/28-0000067040a8/w1_slave"

    with open(probe_adress, 'r') as file:
            raw_reading = file.read()

            temp = int(raw_reading[~5:])/1000
            return temp

def loop():
    while 1:
        measurements = dict()
        measurements['temp'] = get_temp()
        measurements['temperature'] = round(bmp280.get_temperature(), 2)
        measurements['pressure'] = round(bmp280.get_pressure(), 2)
        msgs= list()
        for topic, payload in measurements.items():
            msgs.append({"topic":f'piz/{topic}', "payload":payload})
        publish.multiple(msgs, hostname="192.168.1.106")
        for msg in msgs:
            print(f"published {msg['topic']}: {msg['payload']}")
        sleep(30)

if __name__ == "__main__":
    bus = SMBus(1)
    bmp280 = BMP280(i2c_dev=bus)
    loop()
