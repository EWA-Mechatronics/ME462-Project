#!/usr/bin/env python3

'''
ME 462 TERM PROJECT - 2020 Spring

Created by Engineers with Attitude:
    
    Ege Uğur Aguş
    İsmail Melih Canbolat
    Koral Özbey 


This is Game Manager.    
'''

import robotarena as ra
import numpy as np
import math 
import sys

from os import listdir
from os.path import isfile, join


class GeneralGameMenager():
    '''
    General game manager class. It involves methods that will be used by all possible scenarios.
    '''

    def __init__(self,user_path, simulation_path , robot_type, game_map, sensor_list, random_actuation_list):
        """
        Specify the name, speed and the line of sight for the robots.
        """

        self.user_path = user_path #The path that user will send txt files.
        self.simulation_path = simulation_path #The path that simulation will send txt files.
        self.robot = eval('ra.'+ robot_type +'()') #Initiate the specified robot.
        self.target_coor = [] # Initiate target coordinates
        self.robot_initial_coor  = [] # Initiate target coordinates
        
        for i in range(len(game_map)):  # To find Target Coordinates
            for j in range(len(game_map)):
                if game_map[i][j] == 'T':
                    self.target_coor.append(i)
                    self.target_coor.append(j)
                    break
                else:
                    pass
                
        for i in range(len(game_map)):  # To find Robot Coordinates
            for j in range(len(game_map)):
                if game_map[i][j] == 'R':
                    self.robot_initial_coor.append(i)
                    self.robot_initial_coor.append(j)
                    break
                else:
                    pass        

    def text_reader(self, target_path):
        '''
        This function will find the txt files in specified path and read the desired target positions for the robot.
        User have to create new txt files at specified directory to make their robot move. If there is no new text file,
        robot will just try to reach last updated coordinates.Name of the txt files in the 'fileX.txt' and X value have to
        be increased for every update. Text file should only contains desired x and y coordinates of the main cells. They should 
        be aparted with single space ' '. User can not give coordinates of grids that are not the neighboor of the current grid 
        of the robot.
        '''
    
        txt_files = [file for file in listdir(target_path) if isfile(join(target_path, file))] #Create a list for all txt files
        f = open(join(target_path, txt_files[-1]), "r") #Open the last updated txt file on only read mode
        coordinates = list(map(int,f.readline().split())) #Read the 1st line of the file and create a list of integers with founded values.
        
        return coordinates

    def punishment(self):
        '''
        This function is for the making robots currently on a obstacle stop and rotate.
        '''
        linear_vel = 0
        angular_vel = 1 
        #Make robot go in the webots here. With specified linear_vel and angular_vel.

    def check_robot_grid(self,robot,game_map):
        '''
        This function will return the type of the grid that robot currently on.
        '''
        return(game_map[robot.x][robot.y])

    def distance_finder_robot_to_robot(self,prey,predator):
        '''
        This function will return the distance between prey and predator.
        '''
        return (math.sqrt((prey.x-predator.x)**2 + (prey.y-predator.y)**2))
    
    def distance_finder_robot_target(self,robot,target_coor):
        '''
        This function will return the distance between robot and target grid.
        '''
        return (math.sqrt((robot.x-target_coor[0])**2 + (robot.y-target_coor[1])**2))

    def robot_move(self,robot):
        '''
        This function will make the robot, at the simulation, move.Read coordinates, and find needed angular velociy and
        allowed linear velocity for robot. Then make robot move. 
        '''
        
        user_coordinates = self.text_reader(self.user_path)
        simulation_coordinates = self.text_reader(self.simulation_path) #Simulation coordinates will store the current robot x and y values. Also needed angular position
        
        angular_position = math.atan2(user_coordinates[1]-simulation_coordinates[1], user_coordinates[0]-simulation_coordinates[0] ) # Find needed angular position 
        
        if abs(angular_position - simulation_coordinates[2]) >= 0.02: # Define a radian threashold to make robot only rotate. Maybe PID control.
            linear_vel = 0
            angular_vel = 1 # Find the angular velocity range, needed value etc. Also define a way to decide the angular vel
            
        else:
            linear_vel = robot.speed
        
        #Make robot go in the webots here. With specified linear_vel and angular_vel.
     
        
class game_manager_Prey_Predator_SB(GeneralGameMenager):
    
    '''
    Game manager for prey and predator game scenario of Sandbox Mode. 
    '''

    def __init__(self,user_path, simulation_path , robot_type, game_map, sensor_list, random_actuation_list):
        super().__init__(user_path, simulation_path , robot_type, game_map, sensor_list, random_actuation_list)
        self._loop() #Main loop which will make the all calculations after initiated.
    
    def _loop(self):
        
        while self.distance_finder_robot_target(self.robot,self.target_coor) >= 1: #Robot did not reach the target.
        
            robot_currenet_coords = self.text_reader(self.simulation_path)    # Read the current robot coordinates from simulation
            self.robot.x = robot_currenet_coords[0]                           # 1st index of the list is the x coordinates
            self.robot.y = robot_currenet_coords[1]                           # 2nd index of the list is the x coordinates
            
            if self.check_robot_grid(self.robot,self.game_map) == 'O':        # Check the robot on an obstacle or not
                self.punishment() # Robot hit the obstacle apply punishment
            else:
                #Check the grid and evaluate the robots current maximum speed.
                self.robot.speed = eval("ra."+self.check_robot_grid(self.robot,self.game_map)+"().speed_dictionary['{0}']".format(self.robot.kind))
                
                self.robot_move(self.robot) # Take user path and simulation path from user.

    
def main(arg1,arg2,arg3,arg4,arg5,arg6):
    
        if arg6 == 'SB_Prey_Predator':
            game_manager_Prey_Predator_SB() # Take inputs in order.




if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])

