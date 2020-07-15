'''
Simple example code for competitors those who need to get sensor values.
'''

import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("EWA_robot_1")

def on_message(client, userdata, msg):
    data = msg.payload
    data = json.loads(data)
    print(data)
    
client = mqtt.Client("reciever")
# Client name is "reciever" and it should be unique for each script on same broker.
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.1.7", 1883)
# "192.168.1.7" is local broker IP.
client.loop_forever()
