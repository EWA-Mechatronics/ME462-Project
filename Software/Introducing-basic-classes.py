from abc import ABC, abstractmethod # We will use Abstract Base Classes for some of our classes.

class Robot(ABC):
    """
    Robot is the base class for all robot types. Robot class include the 
    base properties of robots such as name, speed, depth of view and
    view angle of the robots.
    """
    def __init__(self,name,speed,depth_of_view,view_angle):
        """
        Specify the name, speed and the line of sight for the robots.
        """
        self.name = name
        self.speed = speed
        self.depth_of_view = depth_of_view
        self.view_angle = view_angle
        self.type = "Robot"

    @abstractmethod  # Create an abstract method to prevent the creation of objects of ABC
    def abstract_method(self):
        pass


class Lion(Robot):
    """
    Leo is one of the robot types. It's name is Leo. Its base speed
    is 5, base depth of view is 5 and view angle is 40 degrees.
    """
    def __init__(self):
        super().__init__("Lion",5,5,40)
    
    def abstract_method(self): # Override abstractmethod to provide creation of objects
        pass

class Deer(Robot):
    """
    Deer is one of the robot types. It's name is Deer. Its base speed
    is 5, depth of view is 4 and view angle is 60 degrees.
    """
    def __init__(self):
        super().__init__("Deer",5,4,60)

    def abstract_method(self): # Override abstractmethod to provide creation of objects
        pass
        
class Grid(ABC):
    """
    Grid is the base class for all grid types. Grid class includes the main
    properties of grids and speed changer for robot types.
    """ 
    def __init__(self,name):
        self.name = name
        
    def speed_changer(self,name,constant):
        """
        This function states how a grid affects the specified robot. name specifies
        the robot type and constant stores the effect of the grid to the robot speed.
        
        Ex: a = speed_changer("Lion",0.5) 
            a = ["Lion",0.5]
            
        We will store this list to remember that grid multiplies Lion's speed with
        0.5 . 
        """
        return  [name,constant]

    @abstractmethod  # Create an abstract method to prevent the creation of objects of ABC
    def abstract_method(self):
        pass
    
class Forest(Grid):
    """
    A good place to hide and run from the predators.
    """
    def __init__(self):
        super().__init__("Forest")
        self.lion = self.speed_changer("Lion",0.5)
        self.deer = self.speed_changer("Deer",1.5)

    def abstract_method(self): # Override abstractmethod to provide creation of objects
        pass

class Savanna(Grid):
    """
    A good place to hunt for some predators.
    """
    def __init__(self):
        super().__init__("Savanna")
        self.lion = self.speed_changer("Lion",2)
        self.deer = self.speed_changer("Deer",1)

    def abstract_method(self): # Override abstractmethod to provide creation of objects
        pass

class Random_Actuation(ABC):
    """
    Random Actuion is the base class for all actuation types. 
    """
    def __init__(self,name):
        self.name = name
        
    def myopic(self,depth_of_view,constant):
        """
        For the actuations that will affect the depth of view.
        """
        return [depth_of_view, constant]
    
    def hobbler(self,speed,constant):
        """
        For the actuations that will affect the speed.
        """
        return [speed,constant]

    @abstractmethod  # Create an abstract method to prevent the creation of objects of ABC
    def abstract_method(self):
        pass
    
class Thunder(Random_Actuation):
    """
    Zeus is that you ?
    """
    def __init__(self):
        super().__init__("Thunder")
        self.view_effect = self.myopic("depth_of_view",0.4)
        self.speed_effect = self.hobbler("speed",0.4)
        
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
    Prey & Predator game scenario.
    """        
    def __init__(self):
        super().__init__("Prey&Predator")
        
    def abstract_method(self): # Override abstractmethod to provide creation of objects
        pass   
