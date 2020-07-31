#!/usr/bin/env python3

# ME462 - Mobile Robot Arena - Robot GUI Controller
# This GUI provide wireless control the robots. (Performs better than the keyboard controller)
# Motion of the robot is controlled with arrow buttons.
# The speed of the robot can be set easily from given options.
# The battery information provided by the robot is also displayed on the GUI
#
# For the wireless communication, MQTT is used. A running MQTT broker is required.
# User only needs to set four MQTT parameters

from PyQt5 import QtCore, QtGui, QtWidgets  # https://pypi.org/project/PyQt5/
import paho.mqtt.client as mqtt  # https://pypi.org/project/paho-mqtt/
import time


# MQTT parameters - Set these according to your setup;
broker_IP = "192.168.1.107"                # Broker IP Address
client_name = "mqtt_gui_robot_controller"  # Client ID for this controller - Each mqtt client must have a unique ID
topic_pub = "me462_robot_1_control"        # Topic to publish to - for control output
topic_sub = "me462_robot_1_battery"        # Topic to subscribe to - for battery input

message = list("160160")  # Message to be sent to the robot - Must be mutable
motor_speed = 50  # Speed of the motors - 00 to 99 - Variable


def on_subscribe(client, userdata, mid, granted_qos):     # Runs on successful subscription to a topic
    print("Subscribed to the topic: " + topic_sub)


def on_message(client, userdata, msg):                    # Runs when a message is received
    # print("incoming message = " + str(msg.payload))
    value = int.from_bytes(msg.payload, byteorder="big")  # Convert incoming message(byte) to int
    ui.progressBar_battery.setProperty("value", value)    # Re-set progressBar according to battery info
                                                          # (May not be the best way?)


try:  # Try to connect to the MQTT broker
    client = mqtt.Client(client_name)  # Create a client instance
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.connect(broker_IP)
    client.subscribe(topic_sub)
except:
    print("Broker connection failure! \nPlease check MQTT parameters")
    time.sleep(2)
    exit()
client.loop_start()  # Starts a background thread for MQTT to function properly.


class Ui_MainWindow(object):  # GUI Setup
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        # MainWindow.resize(420, 320)
        MainWindow.setFixedSize(420,320)
        MainWindow.move(100,100)

        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        # MainWindow.setSizePolicy(sizePolicy)

        font = QtGui.QFont()
        font.setFamily("NanumGothicExtraBold")
        font.setPointSize(12)
        font.setWeight(50)
        MainWindow.setFont(font)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        font = QtGui.QFont()
        font.setFamily("NanumGothicExtraBold")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)

        self.forwardButton = QtWidgets.QPushButton(self.centralwidget)
        self.forwardButton.setGeometry(QtCore.QRect(120, 50, 70, 70))
        self.forwardButton.setFont(font)
        self.forwardButton.setObjectName("forwardButton")

        self.ccwButton = QtWidgets.QPushButton(self.centralwidget)
        self.ccwButton.setGeometry(QtCore.QRect(40, 100, 70, 70))
        self.ccwButton.setFont(font)
        self.ccwButton.setObjectName("ccwButton")

        self.cwButton = QtWidgets.QPushButton(self.centralwidget)
        self.cwButton.setGeometry(QtCore.QRect(200, 100, 70, 70))
        self.cwButton.setFont(font)
        self.cwButton.setObjectName("cwButton")

        self.backwardButton = QtWidgets.QPushButton(self.centralwidget)
        self.backwardButton.setGeometry(QtCore.QRect(120, 140, 70, 70))
        self.backwardButton.setFont(font)
        self.backwardButton.setObjectName("backwardButton")

        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)

        self.label1 = QtWidgets.QLabel(self.centralwidget)  # Speed
        self.label1.setGeometry(QtCore.QRect(320, 20, 61, 31))
        self.label1.setFont(font)
        self.label1.setObjectName("label1")

        self.label2 = QtWidgets.QLabel(self.centralwidget)  # Battery Status
        self.label2.setGeometry(QtCore.QRect(20, 260, 121, 21))
        self.label2.setFont(font)
        self.label2.setObjectName("label2")

        self.progressBar_battery = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar_battery.setGeometry(QtCore.QRect(150, 260, 251, 20))
        self.progressBar_battery.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.progressBar_battery.setProperty("value", 75)
        self.progressBar_battery.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar_battery.setObjectName("progressBar_battery")

        self.radioButton_1 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_1.setGeometry(QtCore.QRect(320, 60, 82, 17))
        self.radioButton_1.setObjectName("radioButton")

        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(320, 90, 82, 17))
        self.radioButton_2.setObjectName("radioButton_2")

        self.radioButton_3 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_3.setGeometry(QtCore.QRect(320, 120, 82, 17))
        self.radioButton_3.setObjectName("radioButton_3")

        self.radioButton_4 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_4.setGeometry(QtCore.QRect(320, 150, 81, 16))
        self.radioButton_4.setChecked(True)
        self.radioButton_4.setObjectName("radioButton_4")

        self.radioButton_5 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_5.setGeometry(QtCore.QRect(320, 180, 82, 17))
        self.radioButton_5.setObjectName("radioButton_5")

        self.radioButton_6 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_6.setGeometry(QtCore.QRect(320, 210, 82, 17))
        self.radioButton_6.setObjectName("radioButton_6")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        font = QtGui.QFont()
        font.setFamily("NanumGothicExtraBold")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.statusbar.setFont(font)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.forwardButton.pressed.connect(self.pressed_forward)  # When forwardButton is pressed, run pressed_forward
        self.forwardButton.released.connect(self.released_button)
        self.backwardButton.pressed.connect(self.pressed_backward)
        self.backwardButton.released.connect(self.released_button)
        self.ccwButton.pressed.connect(self.pressed_ccw)
        self.ccwButton.released.connect(self.released_button)
        self.cwButton.pressed.connect(self.pressed_cw)
        self.cwButton.released.connect(self.released_button)
        self.radioButton_1.pressed.connect(lambda: self.setSpeed("00"))
        self.radioButton_2.pressed.connect(lambda: self.setSpeed(20))
        self.radioButton_3.pressed.connect(lambda: self.setSpeed(40))
        self.radioButton_4.pressed.connect(lambda: self.setSpeed(60))
        self.radioButton_5.pressed.connect(lambda: self.setSpeed(80))
        self.radioButton_6.pressed.connect(lambda: self.setSpeed(99))


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate

        MainWindow.setWindowTitle(_translate("MainWindow", "Robot Controller"))
        self.forwardButton.setStatusTip(_translate("MainWindow", "Move Forward"))
        self.forwardButton.setText(_translate("MainWindow", "↑"))
        # self.forwardButton.setShortcut(_translate("MainWindow", "Up"))

        self.ccwButton.setStatusTip(_translate("MainWindow", "Turn CounterClockWise"))
        self.ccwButton.setText(_translate("MainWindow", "↺"))
        # self.ccwButton.setShortcut(_translate("MainWindow", "Left"))

        self.cwButton.setStatusTip(_translate("MainWindow", "Turn ClockWise"))
        self.cwButton.setText(_translate("MainWindow", "↻"))
        # self.cwButton.setShortcut(_translate("MainWindow", "Right"))

        self.backwardButton.setStatusTip(_translate("MainWindow", "Move Backward"))
        self.backwardButton.setText(_translate("MainWindow", "↓"))
        # self.backwardButton.setShortcut(_translate("MainWindow", "Down"))

        self.label1.setText(_translate("MainWindow", " Speed"))
        self.progressBar_battery.setStatusTip(_translate("MainWindow", "Remaining Battery Percentage"))
        self.label2.setText(_translate("MainWindow", "Battery Status"))
        self.radioButton_1.setText(_translate("MainWindow", "0%"))
        self.radioButton_1.setStatusTip("Set the speed to 0%")
        self.radioButton_2.setText(_translate("MainWindow", "20%"))
        self.radioButton_2.setStatusTip("Set the speed to 20%")
        self.radioButton_3.setText(_translate("MainWindow", "40%"))
        self.radioButton_3.setStatusTip("Set the speed to 40%")
        self.radioButton_4.setText(_translate("MainWindow", "60%"))
        self.radioButton_4.setStatusTip("Set the speed to 60%")
        self.radioButton_5.setText(_translate("MainWindow", "80%"))
        self.radioButton_5.setStatusTip("Set the speed to 80%")
        self.radioButton_6.setText(_translate("MainWindow", "100%"))
        self.radioButton_6.setStatusTip("Set the speed to 100%")

    def pressed_forward(self):
        message[0] = "1"  # Set the direction of the motor A
        message[3] = "1"  # Set the direction of the motor B
        client.publish(topic_pub, "".join(message))  # The message is converted to string and then published.
        print("Forward")


    def pressed_backward(self):
        message[0] = "0"
        message[3] = "0"
        client.publish(topic_pub, "".join(message))
        print("Backward")


    def pressed_ccw(self):
        message[0] = "0"
        message[3] = "1"
        client.publish(topic_pub, "".join(message))
        print("Turn left")


    def pressed_cw(self):
        message[0] = "1"
        message[3] = "0"
        client.publish(topic_pub, "".join(message))
        print("Turn right")

    def released_button(self):
        client.publish(topic_pub, "000000")  # Stop the robot when the button is released.
        print("Stop")

    def setSpeed(self,speed):
        message[1] = str(speed)[0]  # Assign speed values to the MQTT message
        message[2] = str(speed)[1]
        message[4] = str(speed)[0]
        message[5] = str(speed)[1]
        print(f"Speed is set to {speed}%")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
