#!/usr/bin/env python3

'''
ME 462 TERM PROJECT - 2020 Spring

Created by Engineers with Attitude:
    
    Ege Uğur Aguş
    İsmail Melih Canbolat
    Koral Özbey 


This is the Sandbox GUI. Created to provide personal study of Mini Robot Arena.    
'''

import robotarena as ra
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtWidgets import QGridLayout, QCheckBox, QLabel
from PyQt5.QtWidgets import QStatusBar, QToolBar, QRadioButton
from PyQt5.QtWidgets import QPushButton, QGroupBox
from functools import partial # Import partial to use functions with partials
import numpy as np #Import Numpy for using matrices.
from PyQt5.QtCore import pyqtSignal
import subprocess as sp

text_to_show = 'This is the Sandbox GUI Display'  #Initiate global variables
sensor_window_text = "This is the Sensor Information Window."
grid_window_text = "This is the Grid Information Window."
scenario_window_text = "This is the Scenario Selection Window."
robot_window_text = "This is the Robot Selection Window."
actuation_window_text = "This is the Random Actuation Selection Window."

desired_sensor_list = []
desired_scenario = []
desired_actuation_list = []
desired_robot = 0
global_game_map = np.zeros(shape=(8,8),dtype = str) 
game_map_colors = np.zeros(shape=(8,8),dtype = object) 
externalProcess = 0 #Start manager as an external process
simulation_started = False # Flag for simulation

refresh_flag = True #Flag for the checking if game map is generating for the for time or not.
button_list = {}

class MainGui(QMainWindow):
    """
    SandBox GUI Set-up
    """
    open_grid_info = pyqtSignal() #Define signals to open selected windows
    open_sensor_info = pyqtSignal() 
    open_map_generator = pyqtSignal()
    open_scenario_selector = pyqtSignal()
    open_robot_selector = pyqtSignal()
    open_actuation_selector = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.group_name = input("Please Enter Your Group Name: ")
        print("Welcome to the Robot Arena {0}".format(self.group_name))
        
        self.robot_types = ra.Subclass_finder(ra.Robot)
        self.grid_types = ra.Subclass_finder(ra.Grid)
        self.scenario_types = ra.Subclass_finder(ra.Scenario)
        self.sensor_types = ra.Subclass_finder(ra.Sensors)
        self.game_map_actual = np.zeros(shape=(8,8),dtype = str) # Matrix of game map
        self.game_map = np.zeros(shape=(8,8),dtype = str) # Matrix of game map
        
        # Set some main window's properties
        self.setGeometry(550,200,350,300) # 3th parameter width, 4th is height
        self.setWindowTitle("Robot Arena SandBox Mode")
        
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
        self.generalLayout.addWidget(self._createMap(), 5, 0)
        self.generalLayout.addWidget(self._createScenarioSelection(), 0, 0)
        self.generalLayout.addWidget(self._createRobotSelection(),1,0)
        self.generalLayout.addWidget(self._createGridType(),4,0)
        self.generalLayout.addWidget(self._createSensorSelection(),2,0,)
        self.generalLayout.addWidget(self._createDisplay(), 7, 0)
        self.generalLayout.addWidget(self._createRandomActuaiton(),3,0)

    def closeEvent(self,event):
        
        '''
        This function will prevent the missclicks on the exit button by asking for a second time.
        Also this function will be sure that the Game Manager will be terminated when the GUI is closed.
        '''
        
        global simulation_started
        
        reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to exit the Mini Robot Arena ?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            
            if simulation_started == False: #Simulation did not start. Thus just quit.
            
                event.accept()
                
            else: #Simulation started. Thus first terminate the Game Manager
            
                sp.Popen.terminate(externalProcess) # closes the process
                event.accept()
        else:
            event.ignore()        


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
        status.showMessage("ME462-Term Project Mini Robot Arena !")
        self.setStatusBar(status)      
        
    def _createDisplay(self):
        """
        This function creates the display screen at Gui in order to give some 
        information to the user.
        """
        global text_to_show
        
        self.text = QLabel(text_to_show)
        groupBox5 = QGroupBox('Display Screen')

        text_layout = QGridLayout()
        text_layout.addWidget(self.text,0,0)
        
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
        '''
            This fucntion will initiate GameManager.py with given inputs.

        '''
            
        global desired_sensor_list 
        global desired_scenario 
        global desired_actuation_list 
        global desired_robot 
        global global_game_map
        global externalProcess
        global simulation_started
        
        if desired_robot != 0: # Check wheter the robot type is selected or not.
            
            if len(desired_scenario) != 0: # Check wheter the scenario type is selected or not.
                 
                simulation_started = True # Simulation is started. Set the flag.
                args = [desired_sensor_list,desired_scenario,desired_actuation_list,desired_robot,"GAME_MAP","SB_Prey_Predator"]
                i = 0                
                for arg in args: # If parameter is a list convert it to a string splitted with ',' to be able to read at manager
                    if type(arg) == list:
                        string = ",".join(arg)
                        args[i] = string
                    i += 1
                
                externalProcess = sp.Popen(['python','denemepy.py', args[0],args[1],args[2],args[3],args[4],args[5] ]) # Runs specified py script
                
                self.statusBar().showMessage('Simulation is Started !')      
                
            else:
                self.statusBar().showMessage('Scenario did not selected !')
        else:
            self.statusBar().showMessage('Robot did not selected !')
        
    def _finishPressed(self):
        '''
            This fucntion will terminate GameManager.py to prevent working loops at the background.

        '''
        
        global externalProcess
        global simulation_started
        
        if simulation_started == True: #Check wheter simulation is started or not.
        
            sp.Popen.terminate(externalProcess) # closes the process
            
            simulation_started = False # Simulation is finished. Set the flag.
            
            self.statusBar().showMessage('Simulation is Stoped !')
        
        else:
            
            self.statusBar().showMessage('Simulation did not started at the first place !')

    def _createRandomActuaiton(self):
        """
        This function creates Select Random Actuation Window groupbox and returns that.
        """
        groupBox = QGroupBox('Select Random Actuation')        #Create 'Select Random Actuation' group box
        start_button = QPushButton('Random Actuations', self)  #Create 'Random Actuations' Push button
        
        start_button.clicked.connect(self._openActuationInfo)      #Define push button's click functions   

        buttonlayout = QGridLayout()                            #The instance of a QGridLayout is created
        buttonlayout.addWidget(start_button,0,0)                #Adding widget with position specified
        groupBox.setLayout(buttonlayout)                        #Setting layout specified
 
        return groupBox    
    
    def _openActuationInfo(self):
        """
        This is the random actuation selection push button function. This emits a signal to Controller()
        to open specified window.
        """ 
        
        global simulation_started
        
        if simulation_started == True:
            self.statusBar().showMessage('Simulation is Running ! Stop the Simulation First !')
        else:
            self.open_actuation_selector.emit()  # Emit signal          

    def _createSensorSelection(self):
        """
        This function creates Select Available Sensors Window groupbox and returns that.
        """
        groupBox = QGroupBox('Select Available Sensors')        #Create 'Select Available Sensors' group box
        start_button = QPushButton('Sensors', self)             #Create 'Sensors' Push button
        
        start_button.clicked.connect(self._openSensorInfo)      #Define push button's click functions   

        buttonlayout = QGridLayout()                            #The instance of a QGridLayout is created
        buttonlayout.addWidget(start_button,0,0)                #Adding widget with position specified
        groupBox.setLayout(buttonlayout)                        #Setting layout specified
 
        return groupBox    
    
    def _openSensorInfo(self):
        """
        This sensor selection push button function. This emits a signal to Controller()
        to open specified window.
        """    
        
        global simulation_started
        
        if simulation_started == True:
            self.statusBar().showMessage('Simulation is Running ! Stop the Simulation First!')
        else:        
            self.open_sensor_info.emit()  # Emit signal          

    def _createGridType(self):
        """
        This function creates Show Available Grid Types Window groupbox and returns that.
        """
        groupBox = QGroupBox('Show Available Grid Types')     #Create 'Show Available Grid Types' group box
        start_button = QPushButton('Grids', self)             #Create 'Grids' Push buttons
        
        start_button.clicked.connect(self._openGridInfo)      #Define push button's click function    

        buttonlayout = QGridLayout()                          #The instance of a QGridLayout is created
        buttonlayout.addWidget(start_button,0,0)              #Adding widget with position specified
        groupBox.setLayout(buttonlayout)                      #Setting layout specified
 
        return groupBox           

    def _openGridInfo(self):
        """
        This grid information push button function. This emits a signal to Controller()
        to open specified window.
        """        
        
        global simulation_started
        
        if simulation_started == True:
            self.statusBar().showMessage('Simulation is Running ! Stop the Simulation First!')
        else:          
            self.open_grid_info.emit()   # Emit signal


    def _createMap(self):
        """
        This function creates Arrange Game Map Window groupbox and returns that.
        """
        groupBox = QGroupBox('Arrange Game Map')        #Create 'Arrange Game Map' group box
        start_button = QPushButton('Game Map', self)    #Create 'Game Map' Push button
        
        start_button.clicked.connect(self._openMapGenerator)  #Define push button's click function   

        buttonlayout = QGridLayout()                     #The instance of a QGridLayout is created
        buttonlayout.addWidget(start_button,0,0)         #Adding widget with position specified
        groupBox.setLayout(buttonlayout)                 #Setting layout specified
 
        return groupBox
              
    def _openMapGenerator(self):
        """
        This map generator push button function. This emits a signal to Controller()
        to open specified window.
        """    
        
        global simulation_started
        
        if simulation_started == True:
            self.statusBar().showMessage('Simulation is Running ! Stop the Simulation First!')
        else:  
            self.open_map_generator.emit() # Emit signal

    def _createScenarioSelection(self):
        """
        This function creates Scenario Selection Window groupbox and returns that.
        """
        groupBox = QGroupBox('Scenario Selection Window')       #Create 'Select Available Sensors' group box
        start_button = QPushButton('Scenarios', self)           #Create 'Scenarios' Push button
        
        start_button.clicked.connect(self._openScenarioSelection) #Define push button's click function   

        buttonlayout = QGridLayout()                            #The instance of a QGridLayout is created
        buttonlayout.addWidget(start_button,0,0)                #Adding widget with position specified
        groupBox.setLayout(buttonlayout)                        #Setting layout specified        

        return groupBox

    def _openScenarioSelection(self):
        """
        This scenario selection push button function. This emits a signal to Controller()
        to open specified window.
        """
 
        global simulation_started
        
        if simulation_started == True:
            self.statusBar().showMessage('Simulation is Running ! Stop the Simulation First!')
        else:      
            self.open_scenario_selector.emit()  # Emit signal
    
    
    def _createRobotSelection(self):
        """
        This function creates Robot Selection Window groupbox and returns that.
        """
        groupBox = QGroupBox('Robot Selection Window')       #Create 'Robot Selection Window' group box
        start_button = QPushButton('Robots', self)           #Create 'Robots' Push button
        
        start_button.clicked.connect(self._openRobotSelection)  #Define push buttons' click functions    

        buttonlayout = QGridLayout()                            #The instance of a QGridLayout is created
        buttonlayout.addWidget(start_button,0,0)                #Adding widget with position specified
        groupBox.setLayout(buttonlayout)                        #Setting layout specified        

        return groupBox      
    
    def _openRobotSelection(self):
        """
        This robot selection push button function. This emits a signal to Controller()
        to open specified window.
        """
        
        global simulation_started
        
        if simulation_started == True:
            self.statusBar().showMessage('Simulation is Running ! Stop the Simulation First!')
        else:      
            self.open_robot_selector.emit()  # Emit signal

class SensorInfo(QMainWindow):
    """
    This is the Sensor Information Window Set-up.
    """
    def __init__(self):
        super().__init__()
        
        self.sensor_types = ra.Subclass_finder(ra.Sensors)
        
        # Set some main window's properties
        self.setWindowTitle("Sensor Information Window")
        
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()
                
        # Set the central widget and general Layout
        self.generalLayout = QGridLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        
        # Add widgets to general Layout
        self.generalLayout.addWidget(self._createSensorSelection(),0,0,)
        self.generalLayout.addWidget(self._createDisplay(), 1, 0)

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
        status.showMessage("Select the Sensors that You Want to Activate !")
        self.setStatusBar(status)    

    def _createSensorSelection(self):
        '''
        This function creates radio buttons for sensor selection.
        '''
        self.sensor_box= {}                      #Create a list to create radio buttons
        groupBox = QGroupBox("Sensor Selection")  #Create 'Scenario Selection' group box
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
        print __doc__ of the corresponding Sensor subclass.
        """
        global sensor_window_text
        
        if self.sensor_box[Text].isChecked() == True: #If the box is checked print to the display
            Text_editted = Text.replace(" ", "_")
            sensor_window_text = ra.str_to_class(Text_editted).__doc__
            self.text.setText(sensor_window_text+"Now Activated.")
        
        else: #If the box is not checked print to the display
            self.text.setText(sensor_window_text + "Now Deactivated.")

    def _createDisplay(self):
        """
        This function creates the display screen at Sensor Information 
        Window in order to give some information to the user.
        """
        global sensor_window_text
        
        self.text = QLabel(sensor_window_text)
        groupBox = QGroupBox('Display Screen')

        text_layout = QGridLayout()
        text_layout.addWidget(self.text,0,0)
        
        groupBox.setLayout(text_layout)
        
        return groupBox 
    
class GridInfo(QMainWindow):
    """
    This is the Sensor Information Window Set-up.
    """
    def __init__(self):
        super().__init__()
        
        self.grid_types = ra.Subclass_finder(ra.Grid)
        
        # Set some main window's properties
        self.setWindowTitle("Grid Information Window")
        
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()           
        # Set the central widget and general Layout
        self.generalLayout = QGridLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        # Add widgets to general Layout
        self.generalLayout.addWidget(self._createGridInformation(),0,0,)
        self.generalLayout.addWidget(self._createDisplay(), 1, 0)

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
        status.showMessage("Select the Grid type to see It's information !")
        self.setStatusBar(status)    

    def _createGridInformation(self):
        """
        This function creates grid type buttons at GUI to give user
        some information about grids.
        """
        self.grids_type_grid = {}                     #Create a list to create push buttons
        groupBox = QGroupBox("Available Grid Types")  #Create 'Available Grid Types' group box
        buttonLayout = QGridLayout()                  #The instance of a QGridLayout is created
        row = 0
        column = 0
        
        for Text in self.grid_types:
            self.grids_type_grid[Text] = QPushButton(Text) #Create Push Buttons
            self.grids_type_grid[Text].clicked.connect(partial(self.grid_explainer,Text)) #distinguish every button's funciton
            color = ra.str_to_class(Text)().color #Find the specific color of grid
            self.grids_type_grid[Text].setStyleSheet("background-color: {0}".format(color)) #Arrange the color of the button
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
        self.text.setText(ra.str_to_class(Text).__doc__)

    def _createDisplay(self):
        """
        This function creates the display screen at Grid Information 
        Window in order to give some information to the user.
        """
        global grid_window_text
        
        self.text = QLabel(grid_window_text)
        groupBox = QGroupBox('Display Screen')

        text_layout = QGridLayout()
        text_layout.addWidget(self.text,0,0)
        
        groupBox.setLayout(text_layout)
        
        return groupBox 

class MapGenerator(QMainWindow):
    """
    This is the Map Generator Window Set-up.
    """
    def __init__(self):
        super().__init__()
        
        global global_game_map
        global Robot_Grid # Flags for the specifying Robot or Target Grid
        global Target_Grid
        global refresh_flag
        
        Robot_Grid = False
        Target_Grid = False
        
        self.game_map = global_game_map # Matrix of game map
        self.grid_types = ra.Subclass_finder(ra.Grid)
        
        # Button text | position on the QGridLayout
        self.pre_grids = {'[0,0]': (0, 0),
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
         
        # Set some main window's properties
        self.setWindowTitle("Game Map Generation Window")
        
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()
                
        # Set the central widget and general Layout
        self.generalLayout = QGridLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        
        # Add widgets to general Layout
        if refresh_flag == True:
            self.generalLayout.addWidget(self._createMapGenerator(),2,0,)
        else:
            self.generalLayout.addWidget(self._refreshMapGenerator(),2,0)
        self.generalLayout.addWidget(self._setAllGrids(), 0, 0)
        self.generalLayout.addWidget(self._setRobotandTargetGrids(),1,0)

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
        status.showMessage("Create the Game Map ! Do not Forget to Place the Robot and the Target !")
        self.setStatusBar(status)    

    def _createMapGenerator(self):
       '''
       This function creates Push Buttons For Defining Map at Map Generation Window.
       '''
       groupBox = QGroupBox('Map Grids')      #Create 'Map Grids' group box
       self.grids = {}                        #Crate a list to create buttons
       MapLayout = QGridLayout()              #Create layout as a grid layout  

       # Create the buttons and add them to the grid layout
       for Text, position in self.pre_grids.items():
           self.grids[Text] = QPushButton(Text) #Create Push Buttons
           self.grids[Text].setFixedSize(40, 40) #Fix the size of the buttons
           self.grids[Text].clicked.connect(partial(self.map_changer,Text)) #Define functions
           MapLayout.addWidget(self.grids[Text], position[0], position[1]) #Add buttons to the layout
           
       groupBox.setLayout(MapLayout) #Setting specified layout

       global refresh_flag
       refresh_flag = False

       global button_list
       button_list = self.grids

       return groupBox          

    def _refreshMapGenerator(self):
       '''
       This function creates Push Buttons For Defining Map at Map Generation Window.
       '''
       groupBox = QGroupBox('Map Grids')      #Create 'Map Grids' group box
       self.grids = {}                        #Crate a list to create buttons
       MapLayout = QGridLayout()              #Create layout as a grid layout  
       
       global global_game_map
       global game_map_colors
       
       # Create the buttons and add them to the grid layout
       for Text, position in self.pre_grids.items():
           str_to_list = Text.strip('][').split(',')
           self.grids[Text] = QPushButton(global_game_map[position[0]][position[1]]) #Create Push Buttons
           self.grids[Text].setFixedSize(40, 40) #Fix the size of the buttons
           self.grids[Text].clicked.connect(partial(self.map_changer,Text)) #Define functions
           self.grids[Text].setStyleSheet("background-color: {0}".format(game_map_colors[int(str_to_list[0])][int(str_to_list[1])])) #Arrange the color of the button
           MapLayout.addWidget(self.grids[Text], position[0], position[1]) #Add buttons to the layout
           
       groupBox.setLayout(MapLayout) #Setting specified layout

       return groupBox          
         
    def map_changer(self,Text):
        """
        This function let user the arrange the game map from GUI.
        
        """
        str_to_list = Text.strip('][').split(',') # Convert string to list 

        global Robot_Grid # Flags for the specifying Robot or Target Grid
        global Target_Grid
        
        global global_game_map
        global game_map_colors

        if Robot_Grid == True:
            self.grids[Text].setText("R")
            self.grids[Text].setStyleSheet("background-color: {0}".format('silver')) #Arrange the color of the button
            self.game_map[int(str_to_list[0])][int(str_to_list[1])] = 'R'
            Robot_Grid = False
            color = 'silver'
            
        elif Target_Grid == True:
            self.grids[Text].setText("T")
            self.grids[Text].setStyleSheet("background-color: {0}".format('silver')) #Arrange the color of the button            
            self.game_map[int(str_to_list[0])][int(str_to_list[1])] = 'T'
            Target_Grid = False
            color = 'silver'
            
        else:
    
            if len(self.grids[Text].text()) > 2 or len(self.grids[Text].text()) < 1 or self.grids[Text].text() == 'R' or  self.grids[Text].text() == 'T' : 
                #Changing the name of the for the 1st time. Ex: [0][0] to 'O'.
                self.grids[Text].setText("{0}".format(self.grid_types[0][0]))            
                self.game_map[int(str_to_list[0])][int(str_to_list[1])] = self.grid_types[0][0]
                color = ra.str_to_class(self.grid_types[0])().color #Find the specific color of grid
                self.grids[Text].setStyleSheet("background-color: {0}".format(color)) #Arrange the color of the button
    
            else:
                for i in range(len(self.grid_types)):
                    if self.grids[Text].text() == self.grid_types[i][0]:
                        if i == len(self.grid_types)-1:
                            self.grids[Text].setText("{0}".format(self.grid_types[0][0]))
                            self.game_map[int(str_to_list[0])][int(str_to_list[1])] = self.grid_types[0][0]
                            color = ra.str_to_class(self.grid_types[0])().color #Find the specific color of grid
                            self.grids[Text].setStyleSheet("background-color: {0}".format(color)) #Arrange the color of the button
                            break
                        else:
                            self.grids[Text].setText("{0}".format(self.grid_types[i+1][0]))
                            self.game_map[int(str_to_list[0])][int(str_to_list[1])] = self.grid_types[i+1][0]
                            color = ra.str_to_class(self.grid_types[i+1])().color #Find the specific color of grid
                            self.grids[Text].setStyleSheet("background-color: {0}".format(color)) #Arrange the color of the button
                            break
            
             
        game_map_colors[int(str_to_list[0])][int(str_to_list[1])] = color 
        global_game_map = self.game_map 
        

    def _setAllGrids(self):
        """
            This function creates buttons to set all grids of the map as a specified
            grid type.
        """
        self.grids_type_grid = {}                     #Create a list to create radio buttons
        groupBox = QGroupBox("Set All Grids")         #Create 'Set All Grip Types' group box
        buttonLayout = QGridLayout()                  #The instance of a QGridLayout is created
        row = 0
        column = 0
        
        for Text in self.grid_types:
            self.grids_type_grid[Text] = QPushButton(Text) #Create Push Buttons
            self.grids_type_grid[Text].clicked.connect(partial(self._setSpecified,Text)) #distinguish every button's funciton
            color = ra.str_to_class(Text)().color #Find the specific color of grid
            self.grids_type_grid[Text].setStyleSheet("background-color: {0}".format(color)) #Arrange the color of the button
            buttonLayout.addWidget(self.grids_type_grid[Text],row,column) #Add buttons to the radio Layout
            column +=1 #Increase column number by 1 to set next buttons coordinates
            if column == 5: # If column number is reached 5 pass to the next row
                row += 1 
                column = 0

        groupBox.setLayout(buttonLayout)             #Set the Layout of group box as radiolayout
    
        return groupBox    

    def _setRobotandTargetGrids(self):
        """
            This function creates buttons to set robot and the target of the map as a specified
            grid type.
        """
        self.grids_type_grid = {}                       #Create a list to create radio buttons
        groupBox = QGroupBox("Robot And Target Grids")  #Create 'Robot And Target Grids' group box
        buttonLayout = QGridLayout()                    #The instance of a QGridLayout is created

        
        robot_grid = QPushButton('Robot') #Create Push Buttons
        robot_grid.clicked.connect(partial(self._setRobotorTarget,'Robot')) #distinguish every button's funciton
        robot_grid.setStyleSheet("background-color: {0}".format('silver')) #Arrange the color of the button
        buttonLayout.addWidget(robot_grid,0,0) #Add buttons to the radio Layout
  
        target_grid = QPushButton('Target') #Create Push Buttons
        target_grid.clicked.connect(partial(self._setRobotorTarget,'Target')) #distinguish every button's funciton
        target_grid.setStyleSheet("background-color: {0}".format('silver')) #Arrange the color of the button
        buttonLayout.addWidget(target_grid,0,1) #Add buttons to the radio Layout        

        groupBox.setLayout(buttonLayout)             #Set the Layout of group box as radiolayout
    
        return groupBox  

        
    def _setRobotorTarget(self,Text):
        
        global Robot_Grid # Flags for the specifying Robot or Target Grid
        global Target_Grid
        
        if Text == 'Robot':
            Robot_Grid = True
        elif Text == 'Target':
            Target_Grid = True
        else:
            pass
            

    def _setSpecified(self,Kind):
        """
        This function will set the all of the grid buttons' names and colors to the 
        specified grid type.
        """
        global game_map_colors
        color = ra.str_to_class(Kind)().color #Find the specific color of grid

        self.game_map.fill(Kind[0]) # Set new game_map        

        for Text in self.grids: #Create a loop for all the grid push buttons
             str_to_list = Text.strip('][').split(',') # Convert string to list
             game_map_colors[int(str_to_list[0])][int(str_to_list[1])] = color
             self.grids[Text].setText(Kind[0]) # Arrange the Text of the button
             self.grids[Text].setStyleSheet("background-color: {0}".format(color)) #Arrange the color of the button

        global global_game_map
        
        global_game_map = self.game_map  
        
        
class ScenarioSelector(QMainWindow):
    """
    This is the Scenario Selection Window Set-up.
    """
    def __init__(self):
        super().__init__()
        self.scenario_types = ra.Subclass_finder(ra.Scenario) # Find available Scenarios
        
        # Set some main window's properties
        self.setWindowTitle("Scenario Selection Window")
        
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()
                
        # Set the central widget and general Layout
        self.generalLayout = QGridLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        
        # Add widgets to general Layout
        self.generalLayout.addWidget(self._createScenarioButtons(),0,0,)
        self.generalLayout.addWidget(self._createDisplay(), 1, 0)

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
        status.showMessage("Select the Scenario !")
        self.setStatusBar(status)    

    def _createScenarioButtons(self):
        """
        This function creates scenario radio buttons at the Scenario selection window.
        """
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
            global scenario_window_text
            
            Text_editted = Text.replace(" ", "_")
            scenario_window_text = ra.str_to_class(Text_editted).__doc__
            self.text.setText(scenario_window_text+ Text +" is selecteed as scenario !")
            desired_scenario.append(Text_editted)
            if len(desired_scenario) == 2:
                desired_scenario.pop(0)
            print("Desired Scenario: ")
            print(desired_scenario)

    def _createDisplay(self):
        """
        This function creates the display screen at Scenario Selection 
        Window in order to give some information to the user.
        """
        global scenario_window_text
        
        self.text = QLabel(scenario_window_text)
        groupBox = QGroupBox('Display Screen')

        text_layout = QGridLayout()
        text_layout.addWidget(self.text,0,0)
        
        groupBox.setLayout(text_layout)
        
        return groupBox 

class RobotSelector(QMainWindow):
    """
    This is the Robot Selection Window Set-up.
    """ 
    def __init__(self):
        super().__init__()
        self.robot_types = ra.Subclass_finder(ra.Robot) # Find available Robots
        
        # Set some main window's properties
        self.setWindowTitle("Robot Selection Window")
        
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()
                
        # Set the central widget and general Layout
        self.generalLayout = QGridLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        
        # Add widgets to general Layout
        self.generalLayout.addWidget(self._createRobotSelection(),0,0,)
        self.generalLayout.addWidget(self._createDisplay(), 1, 0)

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
        status.showMessage("Select the Robot Type !")
        self.setStatusBar(status)    
      
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
            global robot_window_text
            desired_robot = Text
            print(desired_robot)

            robot_window_text = ra.str_to_class(Text).__doc__
            self.text.setText(robot_window_text+ Text +" is selecteed as robot !")        
            
    def _createDisplay(self):
       """
       This function creates the display screen at Robot Selection 
       Window in order to give some information to the user.
       """
       global robot_window_text
       
       self.text = QLabel(robot_window_text)
       groupBox = QGroupBox('Display Screen')

       text_layout = QGridLayout()
       text_layout.addWidget(self.text,0,0)
       
       groupBox.setLayout(text_layout)
       
       return groupBox 

class RandomActuationSelector(QMainWindow):
    """
    This is the Random Actuation Selection Window Set-up.
    """ 
    def __init__(self):
        super().__init__()
        self.actuation_types = ra.Subclass_finder(ra.Random_Event) # Find available Robots
        
        
        # Set some main window's properties
        self.setWindowTitle("Random Actuation Selection Window")
        
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()
                
        # Set the central widget and general Layout
        self.generalLayout = QGridLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        
        # Add widgets to general Layout
        self.generalLayout.addWidget(self._createActuationSelection(),0,0,)
        self.generalLayout.addWidget(self._createDisplay(), 1, 0)

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
        status.showMessage("Select the Active Random Actuations !")
        self.setStatusBar(status)    

    def _createActuationSelection(self):
        '''
        This function creates radio buttons for Random Actuation selection.
        '''
        self.actuation_box= {}                                 #Create a list to create radio buttons
        groupBox = QGroupBox("Random Actuation Selection")  #Create 'Scenario Selection' group box
        radioLayout = QGridLayout()                          #The instance of a QGridLayout is created
        row = 0
        column = 0
        
        for Text in self.actuation_types:
            self.actuation_box[Text] = QCheckBox(Text)    #Create Radio Buttons
            self.actuation_box[Text].setChecked(False)    #Set initialy not checked
            self.actuation_box[Text].stateChanged.connect(partial(self._selectedActuations,Text)) #Define functions
            self.actuation_box[Text].stateChanged.connect(partial(self._actuationExplainer,Text)) #Define functions            
            radioLayout.addWidget(self.actuation_box[Text],row,column) #Add buttons to the radio Layout
            column +=1 #Increase column number by 1 to set next buttons coordinates
            if column == 5: # If column number is reached 5 pass to the next row
                row += 1 
                column = 0

        groupBox.setLayout(radioLayout)             #Set the Layout of group box as radiolayout
    
        return groupBox

    def _selectedActuations(self,Text, state):
        """
        Returns the selected Random Actuations to the manager.
        """
        global desired_actuation_list
        Text_editted = Text.replace(" ", "_")       
        
        if self.actuation_box[Text].isChecked() == True: #If the box is checked add Actuation to the desired list
            desired_actuation_list.append(Text_editted)
        else: #If the box is not checked remove Actuation from the desired list
            desired_actuation_list.remove(Text_editted)

        print("Active Actuations: ")
        print(desired_actuation_list)        

    def _actuationExplainer(self,Text):

        """
        When user pressed one of the grid buttons. This function will
        print __doc__ of the corresponding Actuation subclass.
        """
        global actuation_window_text
        
        if self.actuation_box[Text].isChecked() == True: #If the box is checked print to the display
            Text_editted = Text.replace(" ", "_")
            actuation_window_text = ra.str_to_class(Text_editted).__doc__
            self.text.setText(actuation_window_text+"Now Activated.")
        
        else: #If the box is not checked print to the display
            self.text.setText(actuation_window_text + "Now Deactivated.")

    def _createDisplay(self):
       """
       This function creates the display screen at Random Actuation Selection 
       Window in order to give some information to the user.
       """
       global actuation_window_text
       
       self.text = QLabel(actuation_window_text)
       groupBox = QGroupBox('Display Screen')

       text_layout = QGridLayout()
       text_layout.addWidget(self.text,0,0)
       
       groupBox.setLayout(text_layout)
       
       return groupBox 
    
class sandController:
    """
        This class is to control the switching between windows.
    """
    def __init__(self):
        pass

    def show_MainGui(self):
        self.show_selection = MainGui()
        self.show_selection.open_grid_info.connect(self._openGridInfo)
        self.show_selection.open_sensor_info.connect(self._openSensorInfo)
        self.show_selection.open_map_generator.connect(self._openMapGenerator)
        self.show_selection.open_scenario_selector.connect(self._openScenarioSelector)
        self.show_selection.open_robot_selector.connect(self._openRobotSelector)
        self.show_selection.open_actuation_selector.connect(self._openRandomActuationSelector)
        self.show_selection.show()

    def _openGridInfo(self):
        self.window = GridInfo()
        self.window.show()

    def _openSensorInfo(self):
        self.window = SensorInfo()
        self.window.show()

    def _openMapGenerator(self):
        self.window = MapGenerator()
        self.window.show()

    def _openScenarioSelector(self):
        self.window = ScenarioSelector()
        self.window.show()

    def _openRobotSelector(self):
        self.window = RobotSelector()
        self.window.show()

    def _openRandomActuationSelector(self):
        self.window = RandomActuationSelector()
        self.window.show()
        
def main():
    app = QApplication(sys.argv)
    controller = sandController()
    controller.show_MainGui()
    sys.exit(app.exec_())
    
    

if __name__ == '__main__':
    main()
    sp.Popen.terminate(externalProcess) # closes the process
