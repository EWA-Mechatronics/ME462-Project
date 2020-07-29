#!/usr/bin/env python3

'''
ME 462 TERM PROJECT - 2020 Spring

Created by Engineers with Attitude:

    Ege Uğur Aguş
    İsmail Melih Canbolat
    Koral Özbey 

This is the Real Robot Case GUI. Created to provide co-op study of Mini Robot Arena, with the admission of a instructor.   
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

text_to_show = 'This is the Real Time GUI Display'  #Initiate global variables
sensor_window_text = "This is the Sensor Information Window."
grid_window_text = "This is the Grid Information Window."
robot_window_text ="This is the Robot Information Window."
scenario_window_text = "This is the Scenario Selection Window."
actuation_window_text = "This is the Random Actuation Selection Window."

desired_scenario = []
desired_actuation_list = []
group_names = {}
global_game_map = np.zeros(shape=(8,8),dtype = str) 
game_map_colors = np.zeros(shape=(8,8),dtype = object) 
externalProcess = 0 #Start manager as an external process
simulation_started = False # Flag for simulation
any_window_opened = False

refresh_flag = True #Flag for the checking if game map is generating for the for time or not.
refresh_flag_scenario = True #Flag for the checking if sensors are generating for the for time or not.
refresh_flag_actuation = True #Flag for the checking if actuations are generating for the for time or not.
robot_is_generated_flag = False #Flag for checking if any robots are defined
button_list = {}

game_map_row_number = 7 #Assumed dimensions for game map
game_map_column_number = 7 

class MainGui(QMainWindow):
    """
    Robot Arena Real Arena Mode GUI Set-up
    """
    open_grid_info = pyqtSignal() #Define signals to open selected windows
    open_robot_info = pyqtSignal() 
    open_sensor_info = pyqtSignal() 
    open_map_generator = pyqtSignal()
    open_scenario_selector = pyqtSignal()
    open_robot_selector = pyqtSignal()
    open_robot_deletor = pyqtSignal()
    open_robot_show = pyqtSignal()
    open_actuation_selector = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        self.robot_types = ra.Subclass_finder(ra.Robot)
        self.grid_types = ra.Subclass_finder(ra.Grid)
        self.scenario_types = ra.Subclass_finder(ra.Scenario)
        self.sensor_types = ra.Subclass_finder(ra.Sensors)
        self.game_map_actual = np.zeros(shape=(8,8),dtype = str) # Matrix of game map
        self.game_map = np.zeros(shape=(8,8),dtype = str) # Matrix of game map
        
        # Set some main window's properties
        self.setGeometry(550,200,350,300) # 3th parameter width, 4th is height
        self.setWindowTitle("Robot Arena Real Arena Mode")
        
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()
                
        # Set the central widget and general Layout
        self.generalLayout = QGridLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        
        # Add widgets to general Layout
        self.generalLayout.addWidget(self._createButton(),7,0)
        self.generalLayout.addWidget(self._createMap(), 6, 0)
        self.generalLayout.addWidget(self._createScenarioSelection(), 0, 0)
        self.generalLayout.addWidget(self._createRobotSelection(),3,0)
        self.generalLayout.addWidget(self._createRobotType(),1,0)
        self.generalLayout.addWidget(self._createGridType(),5,0)
        self.generalLayout.addWidget(self._createSensorSelection(),2,0,)
        self.generalLayout.addWidget(self._createDisplay(), 8, 0)
        self.generalLayout.addWidget(self._createRandomActuaiton(),4,0)

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
            
        global desired_scenario 
        global desired_actuation_list 
        global group_names 
        global global_game_map
        global externalProcess
        global simulation_started
        global game_map_row_number
        global game_map_column_number
        
        game_flag = True
        
        for i in range(int(game_map_row_number)):
            for k in range(int(game_map_column_number)):
                if global_game_map[i][k] == "":
                   game_flag = False
                   break
               
                else:
                    pass
        if game_flag == True: 
            if len(group_names) >= 1: # Check wheter the robot type is selected or not.
                
                if len(desired_scenario) != 0: # Check wheter the scenario type is selected or not.
                     
                    simulation_started = True # Simulation is started. Set the flag.
                    game_map = global_game_map.tolist()
                    args = [desired_scenario,group_names,game_map,"real_time_play"]
                    i = 0
                    for arg in args: # If parameter is a list convert it to a string splitted with ',' to be able to read at manager
                        if type(arg) == list:
                            string = ','.join(map(str, arg))
                            args[i] = string
                            i += 1
                        else:
                            i += 1
                    
                    externalProcess = sp.Popen(['python','denemepy.py', args[0],args[1],args[2],args[3]]) # Runs specified py script
                    
                    self.statusBar().showMessage('Simulation is Started !')
                    print('Simulation is Started !')
                    
                else:
                    self.statusBar().showMessage('Scenario did not selected !')
                    print('Scenario did not selected !')
            else:
                self.statusBar().showMessage('No robot added !')
                print('No robot added !')
        else:
            self.statusBar().showMessage('Set the Game MAP !')
            print('Set the Game MAP !')
        
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
            print('Simulation is Stoped !')
        
        else:
            
            self.statusBar().showMessage('Simulation did not started at the first place !')
            print('Simulation did not started at the first place !')

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
        start_button = QPushButton('Sensor Types', self)             #Create 'Sensors' Push button
        
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
        start_button = QPushButton('Grid Types', self)             #Create 'Grids' Push buttons
        
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

    def _createRobotType(self):
        """
        This function creates Show Available Robot Types Window groupbox and returns that.
        """
        groupBox = QGroupBox('Show Available Robot Types')     #Create 'Show Available Grid Types' group box
        start_button = QPushButton('Robot Types', self)             #Create 'Grids' Push buttons
        
        start_button.clicked.connect(self._openRobotInfo)      #Define push button's click function    

        buttonlayout = QGridLayout()                          #The instance of a QGridLayout is created
        buttonlayout.addWidget(start_button,0,0)              #Adding widget with position specified
        groupBox.setLayout(buttonlayout)                      #Setting layout specified
 
        return groupBox    

    def _openRobotInfo(self):
        """
        This robot information push button function. This emits a signal to Controller()
        to open specified window.
        """        
        
        global simulation_started
        
        if simulation_started == True:
            self.statusBar().showMessage('Simulation is Running ! Stop the Simulation First!')
        else:          
            self.open_robot_info.emit()   # Emit signal

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
        
        groupBox = QGroupBox('Robot Window')       #Create 'Robot Selection Window' group box
        add_button = QPushButton('Add Robot', self)           #Create 'Robots' Push button
        delete_button = QPushButton('Delete Robot',self)
        show_button = QPushButton('Show Robots',self)
        
        add_button.clicked.connect(self._openRobotSelection)  #Define push buttons' click functions    
        delete_button.clicked.connect(self._openRobotDeletion)
        show_button.clicked.connect(self._openRobotShow)

        buttonlayout = QGridLayout()                            #The instance of a QGridLayout is created
        buttonlayout.addWidget(show_button,0,0)                #Adding widget with position specified
        buttonlayout.addWidget(add_button,0,1)                #Adding widget with position specified
        buttonlayout.addWidget(delete_button,0,2)                #Adding widget with position specified
        groupBox.setLayout(buttonlayout)                        #Setting layout specified        

        return groupBox        
    
    def _openRobotDeletion(self):
        """
        This robot deletion push button function. This emits a signal to Controller()
        to open specified window.
        """
        
        global simulation_started
        
        if simulation_started == True:
            self.statusBar().showMessage('Simulation is Running ! Stop the Simulation First!')
        else:      
            self.open_robot_deletor.emit()  # Emit signal
    
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

    def _openRobotShow(self):
        """
        This robot show push button function. This emits a signal to Controller()
        to open specified window.
        """
        
        global simulation_started
        
        if simulation_started == True:
            self.statusBar().showMessage('Simulation is Running ! Stop the Simulation First!')
        else:      
            self.open_robot_show.emit()  # Emit signal

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
        self.generalLayout.addWidget(self._createSensorInformation(),0,0,)
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
        status.showMessage("Select the Sensor type to see Its information !")
        self.setStatusBar(status)    

    def closeEvent(self,event):
        
        global any_window_opened
        
        any_window_opened = False
        event.accept()

    def _createSensorInformation(self):
        """
        This function creates grid type buttons at GUI to give user
        some information about grids.
        """
        self.sensor_type_deposit = {}                     #Create a list to create push buttons
        groupBox = QGroupBox("Available Sensor Types")  #Create 'Available Grid Types' group box
        buttonLayout = QGridLayout()                  #The instance of a QGridLayout is created
        row = 0
        column = 0
        
        for Text in self.sensor_types:
            self.sensor_type_deposit[Text] = QPushButton(Text) #Create Push Buttons
            self.sensor_type_deposit[Text].clicked.connect(partial(self.sensor_explainer,Text)) #distinguish every button's funciton
            buttonLayout.addWidget(self.sensor_type_deposit[Text],row,column) #Add buttons to the radio Layout
            column +=1 #Increase column number by 1 to set next buttons coordinates
            if column == 5: # If column number is reached 5 pass to the next row
                row += 1 
                column = 0

        groupBox.setLayout(buttonLayout)             #Set the Layout of group box as radiolayout
    
        return groupBox    
    
    def sensor_explainer(self,Text):
        """
            When user pressed one of the grid buttons. This function will
            print __doc__ of the corresponding Grid subclass.
        """
        Text = Text.replace(" ", "_")
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
    
class GridInfo(QMainWindow):
    """
    This is the Grid Information Window Set-up.
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
        status.showMessage("Select the Grid type to see Its information !")
        self.setStatusBar(status)    

    def closeEvent(self,event):
        
        global any_window_opened
        
        any_window_opened = False
        event.accept()

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

class RobotInfo(QMainWindow):
    """
    This is the Robot Information Window Set-up.
    """
    def __init__(self):
        super().__init__()
        
        self.grid_types = ra.Subclass_finder(ra.Robot)
        
        # Set some main window's properties
        self.setWindowTitle("Robot Information Window")
        
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()           
        # Set the central widget and general Layout
        self.generalLayout = QGridLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        # Add widgets to general Layout
        self.generalLayout.addWidget(self._createRobotInformation(),0,0,)
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
        status.showMessage("Select the Robot type to see Its information !")
        self.setStatusBar(status)    

    def closeEvent(self,event):
        
        global any_window_opened
        
        any_window_opened = False
        event.accept()

    def _createRobotInformation(self):
        """
        This function creates grid type buttons at GUI to give user
        some information about grids.
        """
        self.grids_type_grid = {}                     #Create a list to create push buttons
        groupBox = QGroupBox("Available Robot Types")  #Create 'Available Grid Types' group box
        buttonLayout = QGridLayout()                  #The instance of a QGridLayout is created
        row = 0
        column = 0
        
        for Text in self.grid_types:
            self.grids_type_grid[Text] = QPushButton(Text) #Create Push Buttons
            self.grids_type_grid[Text].clicked.connect(partial(self.robot_explainer,Text)) #distinguish every button's funciton
            color = ra.str_to_class(Text)().color #Find the specific color of grid
            self.grids_type_grid[Text].setStyleSheet("background-color: {0}".format(color)) #Arrange the color of the button
            buttonLayout.addWidget(self.grids_type_grid[Text],row,column) #Add buttons to the radio Layout
            column +=1 #Increase column number by 1 to set next buttons coordinates
            if column == 5: # If column number is reached 5 pass to the next row
                row += 1 
                column = 0

        groupBox.setLayout(buttonLayout)             #Set the Layout of group box as radiolayout
    
        return groupBox    
    
    def robot_explainer(self,Text):
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
        global robot_window_text
        
        self.text = QLabel(robot_window_text)
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
        global game_map_row_number
        global game_map_column_number
        
        Robot_Grid = False
        Target_Grid = False
        
        self.game_map = global_game_map # Matrix of game map
        self.grid_types = ra.Subclass_finder(ra.Grid)
        self.pre_grids = {}
        
        # Button text | position on the QGridLayout
        
        for i in range(int(game_map_row_number)): # Assume that arena length and width are 7
            for j in range(int(game_map_column_number)):
                self.pre_grids["[{0},{1}]".format(i,j)] = tuple([i,j])        
         
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
            self.generalLayout.addWidget(self._createMapGenerator(),3,0,)
        else:
            self.generalLayout.addWidget(self._refreshMapGenerator(),3,0)
        self.generalLayout.addWidget(self._setAllGrids(), 1, 0)
        self.generalLayout.addWidget(self._setMapSize(),0,0)
        # self.generalLayout.addWidget(self._setRobotandTargetGrids(),1,0)

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
        status.showMessage("Create the Game Map ! ")
        self.setStatusBar(status)    

    def closeEvent(self,event):
        
        global any_window_opened
        
        any_window_opened = False
        event.accept()

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
        
        global global_game_map
        global game_map_colors

    # if Robot_Grid == True:
    #     self.grids[Text].setText("R")
    #     self.grids[Text].setStyleSheet("background-color: {0}".format('silver')) #Arrange the color of the button
    #     self.game_map[int(str_to_list[0])][int(str_to_list[1])] = 'R'
    #     Robot_Grid = False
    #     color = 'silver'
        
    # elif Target_Grid == True:
    #     self.grids[Text].setText("T")
    #     self.grids[Text].setStyleSheet("background-color: {0}".format('silver')) #Arrange the color of the button            
    #     self.game_map[int(str_to_list[0])][int(str_to_list[1])] = 'T'
    #     Target_Grid = False
    #     color = 'silver'
        
    # else:

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

    def _setMapSize(self): 
        """
        This creates the group box to set game map size.
        """
        
        groupBox = QGroupBox("Set Game Map Size")
        buttonLayout = QGridLayout()
        
        self.map_size_button = QPushButton("Set Size")
        self.map_size_button.clicked.connect(self._setMapSizeChanger)
        
        buttonLayout.addWidget(self.map_size_button,0,0)
        
        groupBox.setLayout(buttonLayout)
        
        return groupBox

    def _setMapSizeChanger(self):
        """
        This function resize the game map. 
        """
        
        global game_map_row_number
        global game_map_column_number
        global global_game_map
        global game_map_colors
        
        desired_row_number = input("Please enter the row number of the map: ")
        
        try:
            if int(desired_row_number) <= 50:
                print("Row number of the map is fixed to {0}".format(int(desired_row_number)))
                game_map_row_number = desired_row_number
            else:
                raise Exception
        except:
            print("Invalid type of input. Please try an integer value up to 50.")
        
        desired_column_number = input("Please enter the column number of the map: ")
        
        try:
            if int(desired_column_number) <= 50:
                print("Column number of the map is fixed to {0}".format(int(desired_column_number)))
                game_map_column_number = desired_column_number
            else:
                raise Exception
        except:
            print("Invalid type of input. Please try an integer value up to 50.")       
        
        global_game_map = np.zeros(shape=(int(game_map_row_number),int(game_map_column_number)),dtype = str) 
        game_map_colors = np.zeros(shape=(int(game_map_row_number),int(game_map_column_number)),dtype = object) 
        
        refresh_flag = True #Recreate the map, do not refresh it.
        self.close()

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
        
        global refresh_flag_scenario
        
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
        self.generalLayout.addWidget(self._createDisplay(), 1, 0)
        if refresh_flag_scenario == True:
            self.generalLayout.addWidget(self._createScenarioButtons(),0,0,)
        else:
            self.generalLayout.addWidget(self._refreshScenarioButtons(),0,0)


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

    def closeEvent(self,event):
        
        global any_window_opened
        
        any_window_opened = False
        event.accept()

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

    def _refreshScenarioButtons(self):
        """
        This function refresh scenario radio buttons at the Scenario selection window.
        """
        
        global desired_scenario
        
        self.scenario_grids = {}                    #Create a list to create radio buttons
        groupBox = QGroupBox("Scenario Selection")  #Create 'Scenario Selection' group box
        radioLayout = QGridLayout()                 #The instance of a QGridLayout is created
        row = 0
        column = 0
        
        for Text in self.scenario_types:
            self.scenario_grids[Text] = QRadioButton(Text) #Create Radio Buttons
            if Text == desired_scenario[0].replace("_", " "):
                self.scenario_grids[Text].setChecked(True) #Set initialy checked
            else:
                print(Text)
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
        global refresh_flag_scenario
        
        refresh_flag_scenario = False 
        
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

    def closeEvent(self,event):
        
        global any_window_opened
        
        any_window_opened = False
        event.accept()        

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
            self.robot_list[Text] = QPushButton(Text) #Create Radio Buttons
            
            self.robot_list[Text].clicked.connect(partial(self.RobotAddition,Text)) #Define functions
            radioLayout.addWidget(self.robot_list[Text],row,column) #Add buttons to the radio Layout
            column +=1 #Increase column number by 1 to set next buttons coordinates
            if column == 5: # If column number is reached 5 pass to the next row
                row += 1 
                column = 0

        groupBox.setLayout(radioLayout)             #Set the Layout of group box as radiolayout
        
        return groupBox      

    def RobotAddition(self,Text):
        """
        Add the name of the group_names dictionary and describe their robot type and real robot's QR number
        """
        
        global group_names        

        group_name = input("Please enter the name of the Group NAME: ")
        real_qr_no = input("Please enter the QR no of the real robot: ")
        sensor_row = []
        sensor_types = ra.Subclass_finder(ra.Sensors)
        allowed_values_for_sensor = [0,1]
        
        for a in sensor_types:
            given_input = input("Is {0} available for this robot, 0 or 1: ".format(a))
            
            try:
                if int(given_input) in allowed_values_for_sensor:
                    sensor_row.append(given_input)
                else:
                    raise Exception
            except :
                print("Invalid value for sensor availability. It's set to '0'. Please only enter 0 or 1.")
                sensor_row.append(0)
                    
        group_names[group_name] = [Text,real_qr_no,sensor_row]
        self.close()

class RobotDeletor(QMainWindow):
    """
    This is the Robot Deletion Window Set-up.
    """ 
    def __init__(self):
        
        global group_names
        
        super().__init__()
        self.defined_names = [] #Create a list to store defined names of the groups
        for x in group_names:
          self.defined_names.append(x)
        
        # Set some main window's properties
        self.setWindowTitle("Robot Delation Window")
        
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()
                
        # Set the central widget and general Layout
        self.generalLayout = QGridLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        
        # Add widgets to general Layout
        self.generalLayout.addWidget(self._createRobotDelation(),0,0,)

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
        status.showMessage("Select the Robot that will be deleted.")
        self.setStatusBar(status)    

    def closeEvent(self,event):
        
        global any_window_opened
        
        any_window_opened = False
        event.accept()        

    def _createRobotDelation(self):
        '''
        This function creates radio buttons for Robot Type selection.
        '''
        
        self.robot_list = {}                         #Create a list to create radio buttons
        groupBox = QGroupBox("Robot Deletion")       #Create 'Robot Deletion' group box
        radioLayout = QGridLayout()                  #The instance of a QGridLayout is created
        row = 0
        column = 0
        
        for Text in self.defined_names:
            self.robot_list[Text] = QPushButton(Text) #Create Radio Buttons
            
            self.robot_list[Text].clicked.connect(partial(self.RobotDelation,Text)) #Define functions
            radioLayout.addWidget(self.robot_list[Text],row,column) #Add buttons to the radio Layout
            column +=1 #Increase column number by 1 to set next buttons coordinates
            if column == 5: # If column number is reached 5 pass to the next row
                row += 1 
                column = 0

        groupBox.setLayout(radioLayout)             #Set the Layout of group box as radiolayout
        
        return groupBox      

    def RobotDelation(self,Text):
        """
        Delete the name of the group_names dictionary and describe their robot type and real robot's QR number
        """
        
        global group_names        

        for x in group_names:
            if x == Text:
                group_names.pop(x)
                print("{0} is deleted.".format(x))
                break
        
        print(group_names)
        self.close()
       
class RobotShower(QMainWindow):
    """
    This is the Robot Shower Window Set-up.
    """ 
    def __init__(self):
        
        global group_names
        
        super().__init__()
        self.defined_names = [] #Create a list to store defined names of the groups
        for x in group_names:
          self.defined_names.append(x)
        
        
        # Set some main window's properties
        self.setWindowTitle("Robot Information Window")
        
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()
                
        # Set the central widget and general Layout
        self.generalLayout = QGridLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        
        # Add widgets to general Layout
        self.generalLayout.addWidget(self._createRobotShowing(),0,0,)
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
        status.showMessage("Select the Robot to see Its Information !")
        self.setStatusBar(status)    

    def closeEvent(self,event):
        
        global any_window_opened
        
        any_window_opened = False
        event.accept()        

    def _createRobotShowing(self):
        '''
        This function creates radio buttons for Robot Type selection.
        '''
        
        self.robot_list = {}                         #Create a list to create radio buttons
        groupBox = QGroupBox("Robot Information")    #Create 'Robot Information' group box
        radioLayout = QGridLayout()                  #The instance of a QGridLayout is created
        row = 0
        column = 0
        
        for Text in self.defined_names:
            self.robot_list[Text] = QPushButton(Text) #Create Radio Buttons
            
            self.robot_list[Text].clicked.connect(partial(self.RobotShow,Text)) #Define functions
            radioLayout.addWidget(self.robot_list[Text],row,column) #Add buttons to the radio Layout
            column +=1 #Increase column number by 1 to set next buttons coordinates
            if column == 5: # If column number is reached 5 pass to the next row
                row += 1 
                column = 0

        groupBox.setLayout(radioLayout)             #Set the Layout of group box as radiolayout
        
        return groupBox      

    def RobotShow(self,Text):
        """
        Delete the name of the group_names dictionary and describe their robot type and real robot's QR number
        """        
        
        self.text.setText("{0}".format(group_names[Text]))
            
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
        global refresh_flag_actuation
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
        self.generalLayout.addWidget(self._createDisplay(), 1, 0)
        self.generalLayout.addWidget(self._createActuationSelection(),0,0,)


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
        
    def closeEvent(self,event):
        
        global any_window_opened
        
        any_window_opened = False
        event.accept()

    def _createActuationSelection(self):
        '''
        This function creates radio buttons for Random Actuation selection.
        '''
        global desired_actuation_list
        
        actuation_tuple = tuple(desired_actuation_list)
        self.actuation_box= {}                                 #Create a list to create radio buttons
        groupBox = QGroupBox("Random Actuation Selection")  #Create 'Scenario Selection' group box
        radioLayout = QGridLayout()                          #The instance of a QGridLayout is created
        row = 0
        column = 0
        
        for Text in self.actuation_types:
            self.actuation_box[Text] = QCheckBox(Text)    #Create Radio Buttons
            for i in actuation_tuple:
                if i == Text:
                    self.actuation_box[Text].setChecked(True) #Set initialy  checked
                    break
                else:
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
        
        global any_window_opened 
        
        any_window_opened = False
        self.show_selection = MainGui()
        self.show_selection.open_grid_info.connect(self._openGridInfo)
        self.show_selection.open_robot_info.connect(self._openRobotInfo)
        self.show_selection.open_sensor_info.connect(self._openSensorInfo)
        self.show_selection.open_map_generator.connect(self._openMapGenerator)
        self.show_selection.open_scenario_selector.connect(self._openScenarioSelector)
        self.show_selection.open_robot_selector.connect(self._openRobotSelector)
        self.show_selection.open_robot_deletor.connect(self._openRobotDeletor)
        self.show_selection.open_robot_show.connect(self._openRobotShower)
        self.show_selection.open_actuation_selector.connect(self._openRandomActuationSelector)
        self.show_selection.show()

    def _openGridInfo(self):
        
        global any_window_opened 
        if any_window_opened == False:
            self.window = GridInfo()
            any_window_opened = True
            self.window.show() 
        else:
            pass

    def _openRobotInfo(self):
        
        global any_window_opened
        if any_window_opened == False:
            self.window = RobotInfo()
            any_window_opened = True
            self.window.show()
        else:
            pass
        
    def _openSensorInfo(self):
        
        global any_window_opened
        if any_window_opened == False:
            self.window = SensorInfo()
            any_window_opened = True
            self.window.show()
        else:
            pass
        
    def _openMapGenerator(self):
        
        global any_window_opened
        if any_window_opened == False:
            self.window = MapGenerator()
            any_window_opened = True
            self.window.show()
        else:
            pass

    def _openScenarioSelector(self):
        
        global any_window_opened
        if any_window_opened == False:
            self.window = ScenarioSelector()
            any_window_opened = True
            self.window.show()
        else:
            pass

    def _openRobotSelector(self):
        
        global any_window_opened
        if any_window_opened == False:
            self.window = RobotSelector()
            any_window_opened = True
            self.window.show()
        else:
            pass

    def _openRobotShower(self):
        
        global any_window_opened
        if any_window_opened == False:
            self.window = RobotShower()
            any_window_opened = True
            self.window.show()
        else:
            pass

    def _openRobotDeletor(self):
        
        global any_window_opened
        if any_window_opened == False:
            self.window = RobotDeletor()
            any_window_opened = True
            self.window.show()
        else:
            pass

    def _openRandomActuationSelector(self):
        
        global any_window_opened
        if any_window_opened == False:
            self.window = RandomActuationSelector()
            any_window_opened = True
            self.window.show()
        else:
            pass
        
def main():
    app = QApplication(sys.argv)
    controller = sandController()
    controller.show_MainGui()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
    sp.Popen.terminate(externalProcess) # closes the process
