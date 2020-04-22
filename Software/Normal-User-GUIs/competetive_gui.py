#!/usr/bin/env python3

import robotarena as ra
import gui_selection_gui as gsg
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout, QLabel
from PyQt5.QtWidgets import QStatusBar, QToolBar, QRadioButton
from PyQt5.QtWidgets import QPushButton, QGroupBox

from functools import partial # Import partial to use functions with partials
import numpy as np #Import Numpy for using matrices.

text_to_show = 'Everything is Fine !'  #Initiate global variables
scenario_text = "No scenarios are selected by admin."
sensor_text = "No sensors are activated by admin."
actuation_text = "No random actuations are activated by admin."

class MainGui(QMainWindow):
    """
    Competetive GUI Set-up
    """
    def __init__(self):
        super().__init__()
        self.robot_types = ra.Subclass_finder(ra.Robot)
        self.group_name = input("Please Enter Your Group Name: ") 
        print("Welcome to the Robot Arena {0}".format(self.group_name))

        # Set some main window's properties
        self.setGeometry(550,200,400,400) # 3th parameter width, 4th is height
        self.setWindowTitle("Robot Arena Competetive Mode")

        self._createMenu()
        self._createToolBar()
        self._createStatusBar()

        # Set the central widget and general Layout
        self.generalLayout = QGridLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        # Add widgets to general Layout
        self.generalLayout.addWidget(self._createButton(),6,0)
        self.generalLayout.addWidget(self._mapInformation(), 4, 0)
        self.generalLayout.addWidget(self._createScenarioExplain(), 0, 0)
        self.generalLayout.addWidget(self._createRobotSelection(),1,0)
        self.generalLayout.addWidget(self._gridInformation(),3,0)
        self.generalLayout.addWidget(self._sensorInformation(),2,0,)
        self.generalLayout.addWidget(self._createDisplay(), 7, 0)
        self.generalLayout.addWidget(self._actuationInformation(),5,0)

    def _createMenu(self):
        '''
        Create basic menu bar with an exit option.
        '''
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction('&Exit', self.close)

    def _createToolBar(self):
        '''
        Create a tool bar with an exit option.
        '''
        tools = QToolBar()
        self.addToolBar(tools)
        tools.addAction('Exit', self.close)

    def _createStatusBar(self):
        '''
        Create a status bar with polite massages to the user.
        '''
        status = QStatusBar()
        status.showMessage("This is the Status Bar.")
        self.setStatusBar(status)      

    def _createDisplay(self):
        """
        This function creates the display screen at Gui in order to give some 
        information to the user.
        """
        global text_to_show

        self.text = QLabel(text_to_show)
        groupBox = QGroupBox('Display Screen')

        text_layout = QGridLayout()
        text_layout.addWidget(self.text,0,0)

        groupBox.setLayout(text_layout)

        return groupBox  

    def _createButton(self):
        """
        This function creates Join and Resign.
        """
        groupBox = QGroupBox('Join / Resign')                  #Create 'Start & Finish' group box
        start_button = QPushButton('Join', self)               #Create 'Start' and 'Finish' Push buttons
        finish_button = QPushButton('Resign', self)      

        start_button.clicked.connect(self._joinPressed)        #Define push buttons' click functions
        finish_button.clicked.connect(self._resignPressed)        

        buttonlayout = QGridLayout()                            #The instance of a QGridLayout is created
        buttonlayout.addWidget(start_button,0,0)                #Adding widget with position specified
        buttonlayout.addWidget(finish_button,0,1)               #Adding widget with position specified
        groupBox.setLayout(buttonlayout)                        #Setting layout specified
 
        return groupBox    

    def _joinPressed(self):
        print(gsg.group_name)

    def _resignPressed(self):
        pass

    def _sensorInformation(self):
        """
        This function creates the sensor explain screen at Gui in order to give some 
        information to the user about active sensors.
        """
        global sensor_text

        self.sensor_label = QLabel(sensor_text)
        groupBox = QGroupBox('Active Sensors')

        text_layout = QGridLayout()
        text_layout.addWidget(self.sensor_label,0,0)

        groupBox.setLayout(text_layout)

        return groupBox             
 
    def _actuationInformation(self):
        """
        This function creates the Actuation Infomration screen at Gui in order to give some 
        information to the user about active random actuations.
        """
        global actuation_text

        self.actuation_label = QLabel(actuation_text)
        groupBox = QGroupBox('Active Random Actuations')

        text_layout = QGridLayout()
        text_layout.addWidget(self.actuation_label,0,0)

        groupBox.setLayout(text_layout)

        return groupBox             

    def _gridInformation(self):
        """
        This function creates Grid Information button.
        """
        groupBox = QGroupBox("Grid Information")  #Create 'Game Map' group box
        buttonLayout = QGridLayout()               #The instance of a QGridLayout is created

        button1 = QPushButton("Press to Accsess to Grid Explanations")        
        # button1.clicked.connect(self.change_sand)
        buttonLayout.addWidget(button1,0,0)

        groupBox.setLayout(buttonLayout)             #Set the Layout of group box as radiolayout

        return groupBox        

    def _mapInformation(self):
        """
        This function creates Map Information button.
        """
        groupBox = QGroupBox("Game Map")  #Create 'Game Map' group box
        buttonLayout = QGridLayout()      #The instance of a QGridLayout is created

        button1 = QPushButton("Press to See Current Game Map")        
        # button1.clicked.connect(self.change_sand)
        buttonLayout.addWidget(button1,0,0)

        groupBox.setLayout(buttonLayout)             #Set the Layout of group box as radiolayout

        return groupBox        

    def _createScenarioExplain(self):
        """
        This function creates the scenario explain screen at Gui in order to give some 
        information to the user about selected scenario.
        """
        global scenario_text

        self.scenario_label = QLabel(scenario_text)
        groupBox = QGroupBox('Selected Competetive Scenario')

        text_layout = QGridLayout()
        text_layout.addWidget(self.scenario_label,0,0)

        groupBox.setLayout(text_layout)

        return groupBox   

    def _createRobotSelection(self):
        '''
        This function creates radio buttons for Robot Type selection.
        '''
        self.robot_list = {}                         #Create a list to create radio buttons
        groupBox = QGroupBox("Robot Type Selection")  #Create 'Robot Type Selection' group box
        radioLayout = QGridLayout()                   #The instance of a QGridLayout is created
        row = 0
        column = 0

        for Text in self.robot_types:
            self.robot_list[Text] = QRadioButton(Text) #Create Radio Buttons
            self.robot_list[Text].setChecked(False)    #Set initialy not checked
            self.robot_list[Text].toggled.connect(partial(self.RobotSelection,Text)) #Define functions
            radioLayout.addWidget(self.robot_list[Text],row,column) #Add buttons to the radio Layout
            column +=1 #Increase column number by 1 to set next buttons coordinates
            if column == 5: # If column number is reached 5 pass to the next row
                row += 1 
                column = 0

        groupBox.setLayout(radioLayout)             #Set the Layout of group box as radiolayout

        return groupBox

    def RobotSelection(self,Text):
        """
        Robot seleciton radio buttons function
        """
        self.robot_list[Text] = self.sender()       #We need to check if radio button is pressed or not
        if self.robot_list[Text].isChecked():       #Otherwise, it's sending 2 values one for itself and one for previous button
            global desired_robot
            desired_robot = Text
            print(desired_robot)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainGui()
    win.show()
    sys.exit(app.exec_())
