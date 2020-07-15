'''
Simple example code for competitors those who need to get arena top image.
'''

import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("EWA_arenacam")

def on_message(client, userdata, msg):
    print(type(msg.payload))
    f = open("arena_top_image.png","wb")
    f.write(msg.payload)
    f.close()
    print("Image Recieved")

client = mqtt.Client("reciever")
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.1.7", 1883)
client.loop_forever()
