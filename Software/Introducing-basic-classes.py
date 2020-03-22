from abc import ABC, abstractmethod # We will use Abstract Base Classes for some of our classes.
import random #For random actuations 

class Robot(ABC):
    """
    Robot is the base class for all robot types. Robot class include the 
    base properties of robots such as name, speed, depth of view and
    view angle of the robots.
    
    At the scenarios every event will affact the properties of the robots. Thus, 
    we will build proper interfaces at robots in order to easy use at events.
    """
    def __init__(self,name,speed,depth_of_view,view_angle):
        """
        Specify the name, speed and the line of sight for the robots.
        """
        self.name = name
        self.speed = speed # That will the instantenous speed of the robot
        self.depth_of_view = depth_of_view # That will the instantenous depth of view of the robot
        self.view_angle = view_angle # That will the instantenous view angle of the robot
        self.type = "Robot"   #Specift the object type

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
    
    def __init__(self):
        super().__init__("Lion",lion_base_speed,lion_base_depth_of_view,lion_base_view_angle) # Create instantenous stats for lion
        self.base_speed = lion_base_speed # That will store the base speed of the lion
        self.base_depth_of_view = lion_base_depth_of_view # That will store the base depth of view
        self.base_view_angle = lion_base_view_angle # That will store the base view angle
    
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
     
    def __init__(self):
        super().__init__("Deer",deer_base_speed,deer_base_depth_of_view,deer_base_view_angle) # Create instantenous stats of deer
        self.base_speed = deer_base_speed # That will store the instantenous speed of the Deer
        self.base_depth_of_view = deer_base_depth_of_view # That will store the instantenous depth of view
        self.base_view_angle = deer_base_view_angle # That will store the instantenous view angle        

    def abstract_method(self): # Override abstractmethod to provide creation of objects
        pass
        
class Grid(ABC):
    """
    Grid is the base class for all grid types. Grid class includes the main
    properties of grids. Grids only affect the specific robot types' speeds. 
    """ 
    def __init__(self,name,lion_speed = '' ,deer_speed = '' ): # One grid may not affect a certain type of robot. Thus
                                                               # Thus, we will remain optional variable for every robot at ABC class.                                 
        self.name = name
        self.lion_speed = lion_speed 
        self.deer_speed = deer_speed
        self.type = "Grid" # Specify the object type

    @abstractmethod  # Create an abstract method to prevent the creation of objects of ABC
    def abstract_method(self):
        pass
    
class Forest(Grid):
    """
    Forest is a grid type.
    It is a good place to hide and run from the predators.
    """
    def __init__(self): 
        super().__init__("Forest",lion_speed = 3 ,deer_speed = 5 )

    def abstract_method(self): # Override abstractmethod to provide creation of objects
        pass

class Savanna(Grid):
    """
    Savanna is a grid type.
    A good place to hunt for some predators.
    """
    def __init__(self):
        super().__init__("Savanna",lion_speed = 6) # Savanna has no effect on deer speed
                                                   # Thus, it will return a string for deer_speed

    def abstract_method(self): # Override abstractmethod to provide creation of objects
        pass

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
        
    def myopic(self,robot,depth_of_view_multiplier,possibility):
        """
        For the actuations that will affect the depth of view.
        """
        goodluck = random.randint(0,100)
        
        if goodluck < possibility:
            robot.depth_of_view = robot.depth_of_view * depth_of_view_multiplier
            print("You shall not pass!")
        else:
            print("You shall pass!")
            pass
    
    def hobbler(self,robot,speed,speed_multiplier,possibility): 
        """
        For the actuations that will affect the speed.
        """
        goodluck = random.randint(0,100)
        
        if goodluck < possibility:
            robot.speed = robot.speed * speed_multiplier
            print("You shall not pass!")
        else:
            print("You shall pass!")
            pass

    def surgery(self,a,b,possibility):
        """
        For the actuations that will affact the name of the robot.
        A change in the name will also affect all other properties.
        """
        goodluck = random.randint(0,100)
        
        if goodluck < possibility: # Surgery will transform a to b with base stats of b.
            a.name = b.name
            a.speed = b.base_speed
            a.view_angle = b.base_view_angle
            a.depth_of_view = b.base_depth_of_view
            print("You shall not pass!")
        else:
            print("You shall pass!")
            pass
     
    @abstractmethod  # Create an abstract method to prevent the creation of objects of ABC
    def abstract_method(self):
        pass
    
class Thunder(Random_Actuation):
    """
    Zeus is that you ?
    """
    def __init__(self,robot):
        super().__init__("Thunder")
        self.myopic(robot,0.5,20) # with a %20 chance myopic will be triggered
        self.hobbler(robot,0.5,20) # with a %20 change hobbler will be triggered
     
    def abstract_method(self): # Override abstractmethod to provide creation of objects
        pass

class Rainbow(Random_Actuation):
    """
    Maybe you can see Freddie.
    """
    def __init__(self,robot1,robot2):
        super().__init__("Rainbow")
        self.surgery(robot1,robot2,20)  #with a %20 change surgery will be triggered
     
    def abstract_method(self): # Override abstractmethod to provide creation of objects
        pass
  
class Sensors(ABC):
    """
    This is the main class for the holding values that will be obtained from
    simulations.
    """
    def __init__(self,name):
        self.name = name

    @abstractmethod  # Create an abstract method to prevent the creation of objects of ABC
    def abstract_method(self):
        pass

class Distance_sensor(Sensors):
    """
    Distance sensor.
    """
    def _init(self):
        super().__init__("DistanceSensor")

    def GetValue(self):
        pass

    def abstract_method(self): # Override abstractmethod to provide creation of objects
        pass    

class Scenario(ABC):
    """
    Main class for the scenarios
    """
    def __init__(self,name):
        self.name = name

    @abstractmethod  # Create an abstract method to prevent the creation of objects of ABC
    def abstract_method(self):
        pass

class Prey_Predator(Scenario):
    """
    Prey & Predator game scenario.  This game can be played with 2 types of 
    robots. Prey is the Deer and the Predator is the Lion.
    """        
    def __init__(self):
        super().__init__("Prey&Predator")
        
    def abstract_method(self): # Override abstractmethod to provide creation of objects
        pass   
