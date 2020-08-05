'''
Future Update Notes:
1) All topic names are hardcoded those should be changed in a way game
   manager sends.
1) Battery status will be taken from robot and will be sent to desired
   destination. This feature is not coded.

Notes:
1) Nomenclator;
   W2M: Webots to Manager (ex: Simulation sensor values)
   M2T: Manager to Team   (ex: Manipulated sensor values)
   T2M: Team to Manager   (ex: Desired robot motor speeds)
   M2R: Manager to Robot  (ex: Manipulated motor speeds)

2) Manager variable is a dictionary that manipulates values.
   Ex:
   manager = {"robot_1":{"sensor_type": [0,1], "sensor_power" : 75,  "speed" : 1  },
              "robot_2":{"sensor_type": [1,0], "sensor_power" : 100, "speed" : 0.5}}

3) Sensor type used for on/off different sensor. First element for 
   distance sensors and second element for position/orientation sensor.
   Number of sensor can be increased and controlled with adding new 
   sensor to sensor type variable in manager dictionary.
'''

import paho.mqtt.client as mqtt
import json
import datetime

log_datas = []

def webots2team(robot, manager_data, message, target):
    #Manipulates data coming from Webots.
    data = json.loads(message)
    sensor_types = manager_data[robot]["sensor_type"]
    if sensor_types[0] == True:
        sensor_power = manager_data[robot]["sensor_power"]
        sensor_values = data[0]
        for p in sensor_values:
            if p > sensor_power:
                sensor_values[sensor_values.index(p)] = sensor_power
        sensor_values = json.dumps(sensor_values)
        client.publish(target,sensor_values)
    if sensor_types[1] == True:
        data.pop(0)
        data = json.dumps(data)
        client.publish(target,data)
        

def team2robot(robot, manager_data, message, target):
    #Robot motor speed manipulations.
    speed = manager_data[robot]["speed"]
    data = json.loads(message)
    data = str(data)
    m_1 = round(int(data[1] + data[2]) * speed)
    m_2 = round(int(data[4] + data[5]) * speed)
    data = data[0] + str(m_1) + data[3] + str(m_2)
    client.publish(target,data)

    
def on_publish(client,userdata,result):
    pass

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe([("W2M_EWA",0),("W2M_2",0),("W2M_3",0),("W2M_4",0)]) #Example Topics for W2M
    client.subscribe([("T2M_EWA",0),("T2M_2",0),("T2M_3",0),("T2M_4",0)]) #Example Topics for T2M

def on_message(client, userdata, msg):
    topic = msg.topic
    message = msg.payload
    
    #Taking log datas
    log_datas.append('topic:{0}, message:{1}, time:{2}\n'.format(topic,json.loads(message),datetime.datetime.now().time()))
    
    #Get game manager commands as dictionary
    f = open("manager_datas.txt", mode='r')
    data_as_string = f.read()
    f.close()
    manager = json.loads(data_as_string)

    #Example for a webots to team communication.
    if topic == "W2M_EWA":
        webots2team("robot_1", manager, message, "M2T_EWA")
    #Few more examples for many team scenario.
    if topic == "W2M_2":
        webots2team("robot_2", manager, message, "M2T_2")        
    if topic == "W2M_3":
        webots2team("robot_3", manager, message, "M2T_3")        
    if topic == "W2M_4":
        webots2team("robot_4", manager, message, "M2T_4")
    
    #Example for a team to robot communication.
    if topic == "T2M_EWA":
        team2robot("robot_1", manager, message, "M2R_EWA")
    #Few more examples for many team scenario.
    if topic == "T2M_2":
        team2robot("robot_2", manager, message, "M2R_2")
    if topic == "T2M_3":
        team2robot("robot_3", manager, message, "M2R_3")
    if topic == "T2M_4":
        team2robot("robot_4", manager, message, "M2R_4")       
 
    # Saves log datas    
    f = open("log_datas.txt", "w")
    f.writelines(log_datas)
    f.close()


client = mqtt.Client("mqtt_manager") #Client name, must be unique.
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.connect("192.168.1.7", 1883) #192.168.1.7 is local broker.
client.loop_forever()
