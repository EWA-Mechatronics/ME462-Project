import json
from pathlib import Path
from controller import *
import paho.mqtt.publish as mqtt

timeStep = 32
ds = []
file_to_open = Path("C:/Users/Korcan/Desktop/ME462/t_r_of_robots.txt")
supervisor = Supervisor()
robot_node = supervisor.getFromDef("Robot_EWA")
trans_field = robot_node.getField("translation")
rot_field = robot_node.getField("rotation")

robot_marker = 95
ds_1 = supervisor.getDistanceSensor("ds_EWA_1")
ds_1.enable(timeStep)
ds.append(ds_1)
ds_1 = supervisor.getDistanceSensor("ds_EWA_2")
ds_1.enable(timeStep)
ds.append(ds_1)
ds_1 = supervisor.getDistanceSensor("ds_EWA_3")
ds_1.enable(timeStep)
ds.append(ds_1)
ds_1 = supervisor.getDistanceSensor("ds_EWA_4")
ds_1.enable(timeStep)
ds.append(ds_1)
while supervisor.step(timeStep) != -1:
    val_translation = trans_field.getSFVec3f()
    val_rotation = rot_field.getSFRotation()
    f = open(file_to_open, mode='r')
    data_as_string = f.read()
    f.close()
    data = json.loads(data_as_string)
    for d in data:
        if robot_marker in d:
            translation = [d[1]/1000, 0.03, d[2]/1000]
            rotation = [0, 1, 0, -d[3]]
            trans_field.setSFVec3f(translation)
            rot_field.setSFRotation(rotation)

    sen_vals = []
    for e in ds:
        sen_vals.append(e.getValue())
    robot_infos = []
    robot_infos.extend((sen_vals,val_translation,val_rotation))
    robot_infos = json.dumps(robot_infos)
    mqtt.single("W2M_EWA",robot_infos ,hostname="192.168.1.7")
