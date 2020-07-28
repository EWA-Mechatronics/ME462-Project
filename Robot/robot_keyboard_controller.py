#!/usr/bin/env python3

from pynput import keyboard
import paho.mqtt.client as mqtt
import time


# Adjust these according to your setup;
broker_IP = "192.168.1.107"            # Broker IP Address
client_name = "mqtt_robot_controller"  # Client ID for this controller
topic_pub = "me462_robot_1_control"    # Topic to publish to

message = list("150150")  # Message to be sent to the robot - Must be mutable
motor_speed = 50  # Speed of the motors - 00 to 99 - Variable

client = mqtt.Client(client_name)  # Create a client instance

try:  # Try to connect to the MQTT broker
    client.connect(broker_IP)
    print("Broker connection is established. Press ESC to terminate the controller")
except:
    print("Broker connection failure! \nPlease check MQTT parameters")
    time.sleep(2)
    exit()


def forward():
    message[0] = "1"  # Set the direction of the motor A
    message[3] = "1"  # Set the direction of the motor B
    client.publish(topic_pub, "".join(message))  # The message is converted to string and then published.
    print("Forward")


def backward():
    message[0] = "0"  # Set the direction of the motor A
    message[3] = "0"  # Set the direction of the motor B
    client.publish(topic_pub, "".join(message))  # The message is converted to string and then published.
    print("Backward")


def turn_left():
    message[0] = "0"  # Set the direction of the motor A
    message[3] = "1"  # Set the direction of the motor B
    client.publish(topic_pub, "".join(message))  # The message is converted to string and then published.
    print("Turn left")


def turn_right():
    message[0] = "1"  # Set the direction of the motor A
    message[3] = "0"  # Set the direction of the motor B
    client.publish(topic_pub, "".join(message))  # The message is converted to string and then published.
    print("Turn right")


def speed_up():
    global motor_speed
    if motor_speed == 90:
        print("Max Speed is Reached")
        return
    motor_speed += 10  # Increase the speed pwm by 10 percent
    print(f"The speed is increased to {motor_speed}")
    message[1] = str(motor_speed)[0]  # Assign speed values to the MQTT message
    message[2] = str(motor_speed)[1]
    message[4] = str(motor_speed)[0]
    message[5] = str(motor_speed)[1]


def slow_down():
    global motor_speed
    if motor_speed == 10:
        print("Min Speed is Reached")
        return
    motor_speed -= 10  # Increase the speed pwm by 10 percent
    print(f"The speed is decreased to {motor_speed}")
    message[1] = str(motor_speed)[0]  # Assign speed values to the MQTT message
    message[2] = str(motor_speed)[1]
    message[4] = str(motor_speed)[0]
    message[5] = str(motor_speed)[1]


robot_functions = {
    keyboard.Key.up: forward,
    keyboard.Key.down: backward,
    keyboard.Key.left: turn_left,
    keyboard.Key.right: turn_right,
    keyboard.Key.page_up: speed_up,
    keyboard.Key.page_down: slow_down
}


def on_press(key):  # The function that runs when a key is pressed
    if key == keyboard.Key.esc:  # Stop listener if ESC is pressed
        print("---EXIT---")
        time.sleep(1)
        return False
    try:
        robot_functions[key]()  # Run the specific function according to the pressed key
    except:
        print("INVALID KEY")
        pass
    print("message: "+"".join(message)+"\n")


def on_release(key):  # The function that runs when a key is released
    client.publish(topic_pub, "000000")  # Stop the robot when the key is released.
    # pass


# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()
