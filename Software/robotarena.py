#!/usr/bin/env python3

'''
ME 462 TERM PROJECT - 2020 Spring

Created by Engineers with Attitude:
    
    Ege Uğur Aguş
    İsmail Melih Canbolat
    Koral Özbey 


This py file is created to provide the main classes used by the 
other Mini Robot Arena py files.   
'''

from abc import ABC, abstractmethod # We will use Abstract Base Classes for some of our classes.
import random #For random actuations 
import math  #For finding distance between robots 
import sys #Use sys module to convert strings to corresponding Classes
import numpy as np #Import Numpy for using matrices.

class Robot(ABC):
    """
    Robot is the base class for all robot types. Robot class include the 
    base properties of robots such as name, speed, depth of view and
    view angle of the robots.
    
    At the scenarios every event will affact the properties of the robots. Thus, 
    we will build proper interfaces at robots in order to easy use at events.
    """
    
    def __init__(self,name,speed,depth_of_view,view_angle,x_coor = "",y_coor = ""):
        """
        Specify the name, speed and the line of sight for the robots.
        """
        self.name = name
        self.speed = speed # That will the instantenous speed of the robot
        self.depth_of_view = depth_of_view # That will the instantenous depth of view of the robot
        self.view_angle = view_angle # That will the instantenous view angle of the robot
        self.type = "Robot"   #Specift the object type
        self.x = x_coor # store the position of the robot
        self.y = y_coor # store the position of the robot
        self.kind = name #Store its kind to give the GUI
        
    @abstractmethod  # Create an abstract method to prevent the creation of objects of ABC
    def abstract_method(self):
        pass

class Lion(Robot):
    """
    Lion is one of the robot types. It's name is Lion. Its base speed
    is 5, base depth of view is 5 and view angle is 40 degrees.
    """
    global lion_base_speed           #When a lion created save its default values as global
    global lion_base_depth_of_view
    global lion_base_view_angle
    
    lion_base_speed = 5              #Define default values of lion
    lion_base_depth_of_view = 5
    lion_base_view_angle = 40

    lion_number = 0
    
    def __init__(self,x_coor = '',y_coor =''):
        super().__init__("Lion",lion_base_speed,lion_base_depth_of_view,lion_base_view_angle,x_coor ,y_coor ) 
        # Create instantenous stats for lion
        self.base_speed = lion_base_speed # That will store the base speed of the lion
        self.base_depth_of_view = lion_base_depth_of_view # That will store the base depth of view
        self.base_view_angle = lion_base_view_angle # That will store the base view angle
        Lion.lion_number += 1
        self.name = "Lion{0}".format(self.lion_number)
        print("Total number of Lions is {0}.".format(Lion.lion_number))
        
    def __del__(self):
        Lion.lion_number -=1
        print("Total number of Lions is {0}.".format(Lion.lion_number))
        
    def abstract_method(self): # Override abstractmethod to provide creation of objects
        pass


class Deer(Robot):
    """
    Deer is one of the robot types. It's name is Deer. Its base speed
    is 5, depth of view is 4 and view angle is 60 degrees.
    """
    global deer_base_speed           #When a deer created save its base values as global
    global deer_base_depth_of_view
    global deer_base_view_angle
    
    deer_base_speed = 5              #Define base values of deer
    deer_base_depth_of_view = 4
    deer_base_view_angle = 60
    
    deer_number = 0
     
    def __init__(self,x_coor = '',y_coor =''):
        super().__init__("Deer",deer_base_speed,deer_base_depth_of_view,deer_base_view_angle, x_coor, y_coor ) 
        # Create instantenous stats of deer
        self.base_speed = deer_base_speed # That will store the instantenous speed of the Deer
        self.base_depth_of_view = deer_base_depth_of_view # That will store the instantenous depth of view
        self.base_view_angle = deer_base_view_angle # That will store the instantenous view angle        
        Deer.deer_number += 1
        self.name = "Deer{0}".format(Deer.deer_number)
        print("Total number of Deers is {0}.".format(Deer.deer_number))

    def abstract_method(self): # Override abstractmethod to provide creation of objects
        pass
     
    def __del__(self):
        Deer.deer_number -=1
        print("Total number of Deers is {0}.".format(Deer.deer_number))
        
class Grid(ABC):
    """
    Grid is the base class for all grid types. Grid class includes the main
    properties of grids. Grids only affect the specific robot types' speeds. 
    """ 
    def __init__(self,name,lion_speed = '' ,deer_speed = '', color = '' ): # One grid may not affect a certain type of robot. Thus
                                                               # Thus, we will remain optional variable for every robot at ABC class.                                 
        self.name = name
        self.lion_speed = lion_speed 
        self.deer_speed = deer_speed
        self.type = "Grid" # Specify the object type
        self.kind = name
        self.color = color
        self.speed_dictionary = {"Lion": lion_speed, "Deer" : deer_speed}
        
    @abstractmethod  # Create an abstract method to prevent the creation of objects of ABC
    def abstract_method(self):
        pass

class Obstacle(Grid):
    """
    Obstacle is a grid type.
    It represents the areas which robots can not pass.
    """
    def __init__(self):
        super().__init__("Obstacle",lion_speed = 0, deer_speed = 0, color = "gray")
    
    def abstract_method(self): # Override abstractmethod to provide creation of objects
        pass

class Forest(Grid):
    """
    Forest is a grid type.
    It is a good place to hide and run from the predators.
    """
    def __init__(self): 
        super().__init__("Forest",lion_speed = 3 ,deer_speed = 5, color = "green" )

    def abstract_method(self): # Override abstractmethod to provide creation of objects
        pass

class Savanna(Grid):
    """
    Savanna is a grid type.
    A good place to hunt for some predators.
    """
    def __init__(self):
        super().__init__("Savanna",lion_speed = 6, color = "yellow") # Savanna has no effect on deer speed
                                                       # Thus, it will return a string for deer_speed

    def abstract_method(self): # Override abstractmethod to provide creation of objects
        pass
    
# class RobotGrid(Grid):
#     """
#     The grid which shows the starting grid for the robot.
#     """
#     def __init__(self):
#         super().__init__("RobotGrid",color = "red") 

#     def abstract_method(self): # Override abstractmethod to provide creation of objects
#         pass
    
class Random_Actuation(ABC):
    
    """
    Random Actuion is the base class for all actuation types. 
    Actuations may affect the every properties of the Robots.
    They even may change the name of the robot. Actuations basicly depends on possbility if 
    the victim is lucky they shall pass.
    """
    def __init__(self,name,speed_multiplier = '',depth_of_view_multiplier = '', view_angle_multiplier = '' ):
        self.name = name
        self.speed_multiplier = speed_multiplier
        self.depth_of_view_multiplier = depth_of_view_multiplier
        self.view_angle_multiplier = view_angle_multiplier
        self.type = "Random Actuation"
        
    def myopic(actuation_name,robot,depth_of_view_multiplier,possibility):
        """
        For the actuations that will affect the depth of view.
        """
        goodluck = random.randint(0,100)
        
        if goodluck < possibility:
            robot.depth_of_view = robot.depth_of_view * depth_of_view_multiplier
            print("{0} is affected by {2}. Its depth of view multiplied by {1}!".format(robot.name,depth_of_view_multiplier,actuation_name))
            return robot
        else:
            print("{1} effect is not succesful on {0}!".format(robot.name,actuation_name))
            return robot
    
    def hobbler(actuation_name,robot,speed_multiplier,possibility): 
        """
        For the actuations that will affect the speed.
        """
        goodluck = random.randint(0,100)
        
        if goodluck < possibility:
            robot.speed = robot.speed * speed_multiplier
            print("{0} is affected by {2}. Its speed multiplied by {1}!".format(robot.name,speed_multiplier,actuation_name))
            return robot
        else:
            print("{1} effect is not succesful on {0}!".format(robot.name,actuation_name))
            return robot

    def surgery(actuation_name,exposed_robot,transform_robot,possibility):
        """
        For the actuations that will affact the name of the robot.
        A change in the name will also affect all other properties.
        """
        goodluck = random.randint(0,100)
        
        if goodluck < possibility: # Surgery will transform exposed_robot to transform_robot with base stats of transform_robot.
            old_name = exposed_robot.name #Store the old name of exposed_robot
            exposed_robot = transform_robot.__class__() 
            print("{0} is affected by {2}. It's name is now {1}!".format(old_name,exposed_robot.name,actuation_name))
            return exposed_robot
        else:
            print("{1} is not succesful on {0}!".format(exposed_robot.name,actuation_name))
            return exposed_robot
     
    @abstractmethod  # Create an abstract method to prevent the creation of objects of ABC
    def abstract_method(self):
        pass

class Random_Event(ABC):
    
    def __init__(self,name):
        self.name = name
        self.kind = name

    @abstractmethod  # Create an abstract method to prevent the creation of objects of ABC
    def abstract_method(self):
        pass

class Thunder1(Random_Event):

    def __init__(self):
        super().__init__(name = "Thunder")
    
    def abstract_method(self): # Override abstractmethod to provide creation of objects
        pass
    
class Transformer1(Random_Event):

    def __init__(self):
        super().__init__(name = "Transformer")
    
    def abstract_method(self): # Override abstractmethod to provide creation of objects
        pass

    
def Thunder(robot):
    """
    Basic Random Actuation method that affects the speed and the depth of view.
    
    Ex: 
        a = Deer()
        a = Thunder(a)
    """
    robot_return = Random_Actuation.myopic("Thunder",robot,0.5,20)  # with a %20 chance myopic will be triggered
    robot_return = Random_Actuation.hobbler("Thunder",robot,0.5,20) # with a %20 change hobbler will be triggered
    return robot_return

def Transformer(robot1,robot2):
    """
    Basic Random Actuation method that affects the name of the robot.
    
    Ex:
        a = Deer()
        b = Lion()
        a = Rainbow(a,b)
    """ 
    #with a 50% change surgery will be triggered
    return Random_Actuation.surgery("Transformer",robot1,robot2,50)
  
class Sensors(ABC):
    """
    This is the main class for the holding values that will be obtained from
    simulations.
    """
    def __init__(self,name):
        self.name = name
        self.type = "Sensor" # Specify the object type
        self.kind = name

    @abstractmethod  # Create an abstract method to prevent the creation of objects of ABC
    def abstract_method(self):
        pass

class Distance_Sensor(Sensors):
    """
    Distance sensor: This sensor will return the distance between robot and obstacles
    to the user.
    """
    def __init__(self):
        super().__init__("Distance Sensor")

    def GetValue(self):
        pass

    def abstract_method(self): # Override abstractmethod to provide creation of objects
        pass    

class Position_Sensor(Sensors):
    """
    Position sensor: This sensor will return the current positoin of the robot to the
    user.
    """
    def __init__(self):
        super().__init__("Position Sensor")

    def GetValue(self):
        pass

    def abstract_method(self): # Override abstractmethod to provide creation of objects
        pass    


class Scenario(ABC):
    """
    Main class for the scenarios
    """
    def __init__(self,name,threshold):
        self.name = name
        self.type = "Scenario" # Specify the object type
        self.threshold = threshold # Define specific threshold value for scenarios
        self.kind = name

    def win_condition(self, target, robot):
        dist = math.sqrt((target.position[0]-robot.position[0])**2
                         + (target.position[1]-robot.position[1])**2)
        
        # Calculate distance and compare it with specified threshold
        if dist < self.threshold:
            global Robot_win
            Robot_win = True #Define a flag to figure out if prey has won or not
            print("{0} has won!".format(robot.name))
        else:
            Robot_win = False #If flag still 'False' after specified time 
                                 #Prey will lost.
            
    @abstractmethod  # Create an abstract method to prevent the creation of objects of ABC
    def abstract_method(self):
        pass

class Prey_and_Predator(Scenario):
    """
    Prey & Predator game scenario.  If one of the Predator got its Prey then it wins the game.
    """        
    def __init__(self):
        super().__init__("Prey and Predator", threshold = "1")
        
    def abstract_method(self): # Override abstractmethod to provide creation of objects
        pass   

class Search_and_Rescue(Scenario):
    """
    Search & Rescue game scenario. All robots in the arena should find disabled robots
    in the arena. If one robot find a disabled robot, that disabled robot will join its team.
    At the end of the specified time. Largest group will win.
    """
    def __init__(self):
        super().__init__("Search and Rescue", threshold = "1")
        
    def abstract_method(self): # Override abstractmethod to provide creation of objects
        pass   

def Subclass_finder(cls):
    """
    This function is to define all subclasses of some classes in order to 
    define available subclasses to send to GUI
    """

    subclasses = [] # Create a list to deposit subclasses

    for subclass in cls.__subclasses__():
        subclasses.append(subclass)                     # Add founded subclass
        subclasses.extend(Subclass_finder(subclass))    # Check if there is a subclass
                                                        # of a subclass.

    Output_types = [] # Create a list to deposit final strings
    for i in range(len(subclasses)): 
        instance = subclasses[i]() # Create an instance for the 
        Output_types.append(instance.kind) # Add them to the output list
        
    return Output_types

def str_to_class(referance_name):
    """
    This functions returns the corresponding class with the referanced 
    parameter name.

    """
    return getattr(sys.modules[__name__], referance_name)
