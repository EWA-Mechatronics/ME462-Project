#!/usr/bin/env python3

import Introducing-basic-classes as ra
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout, QCheckBox, QLabel
from PyQt5.QtWidgets import QStatusBar, QToolBar, QRadioButton
from PyQt5.QtWidgets import QPushButton, QGroupBox
import time, threading
from functools import partial # Import partial to use functions with partials
import numpy as np #Import Numpy for using matrices.
from PyQt5.QtCore import Qt

text_to_show = 'Everything is Fine !'  #Initiate global variables
desired_sensor_list = []
desired_scenario = []

class MainGui(QMainWindow):
    """
    Main Gui Set-up
    """
    def __init__(self):
        super().__init__(),
        
        self.robot_types = ra.Subclass_finder(ra.Robot)
        self.grid_types = ra.Subclass_finder(ra.Grid)
        self.scenario_types = ra.Subclass_finder(ra.Scenario)
        self.sensor_types = ra.Subclass_finder(ra.Sensors)
        self.game_map = np.zeros(shape=(8,8),dtype = str) # Matrix of game map
        
        # Set some main window's properties
        self.setGeometry(550,200,750,750) # 3th parameter width, 4th is height
        self.setWindowTitle("Robot Arena GUI")
        
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()
                
        # Set the central widget and general Layout
        self.generalLayout = QGridLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        
        #Create Led Pins, Pot-Bar & Button Pins
        self.generalLayout.addWidget(self._createButton(),5,0)
        self.generalLayout.addWidget(self._createMap(), 4, 0)
        self.generalLayout.addWidget(self._createScenarioSelection(), 0, 0)
        self.generalLayout.addWidget(self._createRobotSelection(),1,0)
        self.generalLayout.addWidget(self._createGridType(),3,0)
        self.generalLayout.addWidget(self._createSensorSelection(),2,0,)
        self.generalLayout.addWidget(self._createDisplay(), 6, 0)
        
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
        
        # self.text_arduino_output = QLabel('The Data Coming From Arduino')
        # self.pot_value = QLabel("Pot Value")
        self.text = QLabel(text_to_show)
        groupBox5 = QGroupBox('Display Screen')

        text_layout = QGridLayout()
        text_layout.addWidget(self.text,0,0)
        # text_layout.addWidget(self.text_arduino_output, 1, 0)
        # text_layout.addWidget(self.pot_value,2,0)
        
        groupBox5.setLayout(text_layout)
        
        return groupBox5    
        
        
    def _createButton(self):
        """
        This function creates start and finish buttons at GUI.
        """

        groupBox = QGroupBox('Start & Finish')                  #Create 'Start & Finish' group box
        start_button = QPushButton('Start', self)               #Create 'Start' and 'Finish' Push buttons
        finish_button = QPushButton('Finish', self)      
        
        start_button.clicked.connect(self._startPressed)        #Define push buttons' click functions
        finish_button.clicked.connect(self._finishPressed)        

        buttonlayout = QGridLayout()                            #The instance of a QGridLayout is created
        buttonlayout.addWidget(start_button,0,0)                #Adding widget with position specified
        buttonlayout.addWidget(finish_button,0,1)               #Adding widget with position specified
        groupBox.setLayout(buttonlayout)                        #Setting layout specified
 
        return groupBox    

    def _startPressed(self):
        pass
    
    def _finishPressed(self):
        pass
    
    def _createSensorSelection(self):
        '''
        This function creates radio buttons for scenario selection.
        '''
        self.sensor_box= {}                      #Create a list to create radio buttons
        groupBox = QGroupBox("Scenario Selection")  #Create 'Scenario Selection' group box
        radioLayout = QGridLayout()                 #The instance of a QGridLayout is created
        row = 0
        column = 0
        
        for Text in self.sensor_types:
            self.sensor_box[Text] = QCheckBox(Text) #Create Radio Buttons
            self.sensor_box[Text].setChecked(False)    #Set initialy not checked
            self.sensor_box[Text].stateChanged.connect(partial(self._selectedSensors,Text)) #Define functions
            self.sensor_box[Text].stateChanged.connect(partial(self._sensorExplainer,Text)) #Define functions            
            radioLayout.addWidget(self.sensor_box[Text],row,column) #Add buttons to the radio Layout
            column +=1 #Increase column number by 1 to set next buttons coordinates
            if column == 5: # If column number is reached 5 pass to the next row
                row += 1 
                column = 0

        groupBox.setLayout(radioLayout)             #Set the Layout of group box as radiolayout
    
        return groupBox
    
    def _selectedSensors(self,Text, state):
        """
        Returns the selected sensors to the manager.
        
        """
        global desired_sensor_list
        Text_editted = Text.replace(" ", "_")       
        
        if self.sensor_box[Text].isChecked() == True: #If the box is checked add sensor to the desired list
            desired_sensor_list.append(Text_editted)
        else: #If the box is not checked remove sensor from the desired list
            desired_sensor_list.remove(Text_editted)

        print("Active Sensors: ")
        print(desired_sensor_list)        

    def _sensorExplainer(self,Text):

        """
        When user pressed one of the grid buttons. This function will
        print __doc__ of the corresponding Grid subclass.
        """
        global text_to_show
        
        if self.sensor_box[Text].isChecked() == True: #If the box is checked print to the display
            Text_editted = Text.replace(" ", "_")
            text_to_show = ra.str_to_class(Text_editted).__doc__
            self.text.setText(text_to_show+"Now Activated.")
        
        else: #If the box is not checked print to the display
            self.text.setText(Text + ". Now Deactivated.")           
            
    def _createGridType(self):
        """
        This function creates grid type buttons at GUI to give user
        some information about grids.
        """
        self.grids_type_grid = {}                     #Create a list to create radio buttons
        groupBox = QGroupBox("Available Grid Types")  #Create 'Available Grid Types' group box
        buttonLayout = QGridLayout()                  #The instance of a QGridLayout is created
        row = 0
        column = 0
        
        for Text in self.grid_types:
            self.grids_type_grid[Text] = QPushButton(Text) #Create Push Buttons
            self.grids_type_grid[Text].clicked.connect(partial(self.grid_explainer,Text)) #distinguish every button's funciton
            buttonLayout.addWidget(self.grids_type_grid[Text],row,column) #Add buttons to the radio Layout
            column +=1 #Increase column number by 1 to set next buttons coordinates
            if column == 5: # If column number is reached 5 pass to the next row
                row += 1 
                column = 0

        groupBox.setLayout(buttonLayout)             #Set the Layout of group box as radiolayout
    
        return groupBox    
    
    def grid_explainer(self,Text):
        """
            When user pressed one of the grid buttons. This function will
            print __doc__ of the corresponding Grid subclass.
        """
        print(ra.str_to_class(Text).__doc__)
            
                      
    def _createMap(self):
        '''
        This function creates Push Buttons For Defining Map at GUI
        '''
        groupBox = QGroupBox('Map Grids')      #Create 'Start & Finish' group box
        self.grids = {}                        #Crate a list to create buttons
        MapLayout = QGridLayout()              #Create layout as a grid layout  
        
        # Button text | position on the QGridLayout
        grids = {'[0,0]': (0, 0),
                   '[0,1]': (0, 1),
                   '[0,2]': (0, 2),
                   '[0,3]': (0, 3),
                   '[0,4]': (0, 4),
                   '[0,5]': (0, 5),
                   '[0,6]': (0, 6),
                   '[0,7]': (0, 7),
                   '[1,0]': (1, 0),
                   '[1,1]': (1, 1),
                   '[1,2]': (1, 2),
                   '[1,3]': (1, 3),
                   '[1,4]': (1, 4),
                   '[1,5]': (1, 5),
                   '[1,6]': (1, 6),
                   '[1,7]': (1, 7),
                   '[2,0]': (2, 0),
                   '[2,1]': (2, 1),
                   '[2,2]': (2, 2),
                   '[2,3]': (2, 3),
                   '[2,4]': (2, 4),
                   '[2,5]': (2, 5),
                   '[2,6]': (2, 6),
                   '[2,7]': (2, 7),
                   '[3,0]': (3, 0),
                   '[3,1]': (3, 1),
                   '[3,2]': (3, 2),
                   '[3,3]': (3, 3),
                   '[3,4]': (3, 4),
                   '[3,5]': (3, 5),
                   '[3,6]': (3, 6),
                   '[3,7]': (3, 7),
                   '[4,0]': (4, 0),
                   '[4,1]': (4, 1),
                   '[4,2]': (4, 2),
                   '[4,3]': (4, 3),
                   '[4,4]': (4, 4),
                   '[4,5]': (4, 5),
                   '[4,6]': (4, 6),
                   '[4,7]': (4, 7),                 
                   '[5,0]': (5, 0),
                   '[5,1]': (5, 1),
                   '[5,2]': (5, 2),
                   '[5,3]': (5, 3),
                   '[5,4]': (5, 4),
                   '[5,5]': (5, 5),
                   '[5,6]': (5, 6),
                   '[5,7]': (5, 7),                   
                   '[6,0]': (6, 0),
                   '[6,1]': (6, 1),
                   '[6,2]': (6, 2),
                   '[6,3]': (6, 3),
                   '[6,4]': (6, 4),
                   '[6,5]': (6, 5),
                   '[6,6]': (6, 6),
                   '[6,7]': (6, 7),                                                                            
                   '[7,0]': (7, 0),
                   '[7,1]': (7, 1),
                   '[7,2]': (7, 2),
                   '[7,3]': (7, 3),
                   '[7,4]': (7, 4),
                   '[7,5]': (7, 5),
                   '[7,6]': (7, 6),
                   '[7,7]': (7, 7),
                   }
        # Create the buttons and add them to the grid layout
        for Text, position in grids.items():
            self.grids[Text] = QPushButton(Text) #Create Push Buttons
            self.grids[Text].setFixedSize(40, 40) #Fix the size of the buttons
            self.grids[Text].clicked.connect(partial(self.map_changer,Text)) #Define functions
            MapLayout.addWidget(self.grids[Text], position[0], position[1]) #Add buttons to the layout
            
        groupBox.setLayout(MapLayout) #Setting specified layout
 
        return groupBox   
    
    def _createScenarioSelection(self):
        '''
        This function creates radio buttons for scenario selection.
        '''
        self.scenario_grids = {}                    #Create a list to create radio buttons
        groupBox = QGroupBox("Scenario Selection")  #Create 'Scenario Selection' group box
        radioLayout = QGridLayout()                 #The instance of a QGridLayout is created
        row = 0
        column = 0
        
        for Text in self.scenario_types:
            self.scenario_grids[Text] = QRadioButton(Text) #Create Radio Buttons
            self.scenario_grids[Text].setChecked(False)    #Set initialy not checked
            self.scenario_grids[Text].toggled.connect(partial(self.ScenarioSelection,Text)) #Define functions
            radioLayout.addWidget(self.scenario_grids[Text],row,column) #Add buttons to the radio Layout
            column +=1 #Increase column number by 1 to set next buttons coordinates
            if column == 5: # If column number is reached 5 pass to the next row
                row += 1 
                column = 0

        groupBox.setLayout(radioLayout)             #Set the Layout of group box as radiolayout
    
        return groupBox

    def ScenarioSelection(self,Text):
        """
        Scenario radio buttons function.

        """
        self.scenario_grids[Text] = self.sender()    #We need to check if radio button is pressed or not
        if  self.scenario_grids[Text].isChecked():   #Otherwise, it's sending 2 values one for itself and one for previous button
            global desired_scenario
            global text_to_show
            
            Text_editted = Text.replace(" ", "_")
            text_to_show = ra.str_to_class(Text_editted).__doc__
            self.text.setText(text_to_show+ Text +" is selecteed as scenario !")
            desired_scenario.append(Text_editted)
            if len(desired_scenario) == 2:
                desired_scenario.pop(0)
            print("Desired Scenario: ")
            print(desired_scenario)
            
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
        
    def map_changer(self,Text):
        """
        This function let user the arrange the game map from GUI.
        
        """
        str_to_list = Text.strip('][').split(',') # Convert string to list

        if self.grids[Text].text() == "O":
            self.grids[Text].setText("F") #Change the GUI Button Text
            self.game_map[int(str_to_list[0])][int(str_to_list[1])] = "F" #Modify the game map matrix
        elif self.grids[Text].text() == "F":
            self.grids[Text].setText("S")  #Change the GUI Button Text
            self.game_map[int(str_to_list[0])][int(str_to_list[1])] = "S" #Modify the game map matrix            
        elif self.grids[Text].text() == "S":
            self.grids[Text].setText("O")  #Change the GUI Button Text
            self.game_map[int(str_to_list[0])][int(str_to_list[1])] = "O" #Modify the game map matrix            
        else:
            self.grids[Text].setText("O")  #Change the GUI Button Text
            self.game_map[int(str_to_list[0])][int(str_to_list[1])] = "O" #Modify the game map matrix
        
        print("Game MAP :")
        print(self.game_map)
        

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
    
