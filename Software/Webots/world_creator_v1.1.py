'''
Future Update Notes:
1) Non-supervisor mode is not coded.
2) robot_creator function takes too much arguments and more argument
   necessary for options like robot tags, data transfer between real
   robot and player, etc. New structure might be necessary.
3) Codes modified for admin-permissions in Windows, in Linux they should
   be arranged.
4) Robot tag creation not included.
5) Collaboration of game manager and world creator is still not 
   considered.
6) Controller paths should be arranged according to Linux system and
   webots configuration.

Updates
1) All controllers updated for mqtt.
2) Arena top camera contoller added.
'''

import numpy as np
from decimal import Decimal
import math
from pathlib import Path
import ctypes, sys #for Windows only

def is_admin():# Windows Admin Permissions
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def grid_material(no):
	'''
	New texture may be added easily with location of texture file(should
	be in jpg format) only corresponding number will assigned to texture
	in the function.
	'''
	if no == 0:
		return 0
	if no == 1:
		return 'textures/earth_texture.jpg'
	if no == 2:
		return 'textures/water_texture.jpg'
	if no == 3:
		return 'textures/desert_texture.jpg'
	if no == 4:
		return 'textures/cell_texture.jpg'

def floor_text(x,z,i,grid_length,material,world_text):
	'''
	Creates script of every floor element of floor matrix.
	'''
	world_text.append('Floor {\n')
	world_text.append('  translation {0} 0 {1}\n'.format(x,z))
	world_text.append('  name "floor({0})"\n'.format(i))
	world_text.append('  size {0} {0}\n'.format(grid_length))
	world_text.append('  tileSize {0} {0}\n'.format(grid_length))
	world_text.append('  appearance Appearance {\n')
	world_text.append('    texture ImageTexture {\n')
	world_text.append('      url [\n')
	world_text.append('        "{}"\n'.format(material))
	world_text.append('      ]\n')
	world_text.append('      filtering 0\n')
	world_text.append('    }}}\n')

def arena_creator(floor_matrix, grid_length,world_text):
	'''
	floor_matrix is a matrix and it decides shape of the arena, number 
	of grids, grid colors. Each matrix element is a grid texture. 
	Corresponding element number will be defined. Value of grid_length
	in meters.
	For example:
	A = [1 3]	Element value: 0 = box obstacle, 1 = earth, 2 = water, 
	    [3 4]				   3 = sand, 4 = cell
	'''
	i = 0
	for ix,iz in np.ndindex(floor_matrix.shape):
		x = (grid_length / 2) + (iz * grid_length)
		z = (grid_length / 2) + (ix * grid_length)
		material = grid_material(floor_matrix[ix,iz])
		if material != 0:
			floor_text(x,z,i,grid_length,material,world_text)
		if material == 0:
			obstacle(x,z,i,grid_length,world_text)
		i += 1

		

def distance_sensor(r_no,s_no,x,z,r,cov,res,s,body,world_text,main,loop):
	'''
	x, z and r are x-coordinate, z-coordinate and direction(rotation
	around	y axis), repectively. Values of x, z, r should calculated
	w.r.t. robot body. cov(Coverage) is range of the sensor and 
	res(resolution) tells smallest change in distance a sensor can 
	detect. x, z, r and coverage in meters. Body is imaginary body of
	sensor device and value of body can be True or False. r_no and s_no
	are id of the robot that carries sensor and id of sensor(there might
	be multiple sensor on a robot, they must identified distinctly), 
	repectively. Imaginary body is black as default. r is in degrees.
	s is for supervisor mode of the robot(True or False). main and loop
	are main and loop part of the controller.
	'''
	pi_5f = float("{:.5f}".format(math.pi))
	r = r / 180 * pi_5f
	world_text.append('    DistanceSensor {\n')
	world_text.append('      translation {0} 0 {1}\n'.format(x,z))
	world_text.append('      rotation 0 1 0 {}\n'.format(r))
	if body == True:
		world_text.append('      children [\n')
		world_text.append('        Shape {\n')
		world_text.append('          appearance PBRAppearance {\n')
		world_text.append('            baseColor 0 0 0\n')
		world_text.append('            roughness 1\n')
		world_text.append('            metalness 0\n')
		world_text.append('          }\n')
		world_text.append('          geometry Box {\n')
		world_text.append('            size 0.001 0.001 0.001\n')
		world_text.append('          }}]\n')
	world_text.append('      name "ds_{0}_{1}"\n'.format(r_no,s_no))
	world_text.append('      lookupTable [\n')
	world_text.append('        0 0 0\n')
	world_text.append('        {0} {1} 0\n'.format(cov,res))
	world_text.append('      ]}\n')
	#Controller Part
	if s == True:
		main.append('ds_1 = supervisor.getDistanceSensor("ds_{0}_{1}")\n'.format(r_no,s_no))
		main.append('ds_1.enable(timeStep)\n')
		main.append('ds.append(ds_1)\n')
		
	#if s == False:


def robot_controller(r_no,supervisor,main,loop):
	'''
	r_no is robot no. main and loop are part of controller scripts which
	necessary for devices and sensors.
	'''
	robot_controller_main = [] # main function of robot controller
	robot_controller_loop = [] # loop function of robot controller
	robot_controller_main.append('import json\n')
	robot_controller_main.append('from pathlib import Path\n')
	robot_controller_main.append('from controller import *\n')
	robot_controller_main.append('import paho.mqtt.publish as mqtt\n')
	robot_controller_main.append('\n')
	robot_controller_main.append('timeStep = 32\n')#Default
	robot_controller_main.append('ds = []\n')
	robot_controller_main.append('file_to_open = Path("C:/Users/Korcan/Desktop/ME462/l_r_of_Robot_1.txt")\n') #EDIT THISSS

	if supervisor == True:
		robot_controller_main.append('supervisor = Supervisor()\n')
		robot_controller_main.append('robot_node = supervisor.getFromDef("Robot_{}")\n'.format(r_no))
		robot_controller_main.append('trans_field = robot_node.getField("translation")\n')
		robot_controller_main.append('rot_field = robot_node.getField("rotation")\n')
		robot_controller_main.append('\n')
		
		robot_controller_loop.append('while supervisor.step(timeStep) != -1:\n')
		robot_controller_loop.append('    val_translation = trans_field.getSFVec3f()\n')
		robot_controller_loop.append('    val_rotation = rot_field.getSFRotation()\n')
		robot_controller_loop.append("    f = open(file_to_open, mode='r')\n")
		robot_controller_loop.append('    data_as_string = f.readlines()\n')
		robot_controller_loop.append('    f.close()\n')
		robot_controller_loop.append('    try:\n')
		robot_controller_loop.append('        if len(data_as_string[{}]) != 0:\n'.format(r_no-1))
		robot_controller_loop.append('            data = json.loads(data_as_string[{}])\n'.format(r_no-1))
		robot_controller_loop.append('            trans_field.setSFVec3f(data[0])\n')
		robot_controller_loop.append('            rot_field.setSFRotation(data[1])\n')
		robot_controller_loop.append('    except IndexError:\n')
		robot_controller_loop.append('        pass\n')
		robot_controller_loop.append('\n')
	
	loop.append('    sen_vals = []\n')
	loop.append('    for e in ds:\n')
	loop.append('        sen_vals.append(e.getValue())\n')
	loop.append('\n')
	loop.append('    sen_vals = json.dumps(sen_vals)\n')
	loop.append('    mqtt.single("EWA_robot_{}",sen_vals ,hostname="192.168.1.7")\n'.format(r_no)) #Hostname should be broker adress
	
	#if super == False:
		
	robot_controller_main = robot_controller_main + main
	robot_controller_loop = robot_controller_loop + loop
	final_controller = robot_controller_main + robot_controller_loop
	
	location = "C:/Program Files/Webots/projects/default/controllers/Robot_{}".format(r_no)# EDIT THIS for proper path in Linux
	if is_admin():#Windows admin permissions inside of this if part of the program
		Path(location).mkdir(parents=False, exist_ok=True)
		[f.unlink() for f in Path(location).glob("*") if f.is_file()]
		f = open(location + "/Robot_{}.py".format(r_no), "w")
		f.writelines(final_controller)
		f.close()
	else:
    # Re-run the program with admin rights
		ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
		
	
def robot_creator(x,z,r_no,supervisor,world_text):
	'''
	Value of supervisor can be True or False. If value is False than
	motors are enabled. r_no is id of the robot. x and z are start
	coordinates of robot. r_no should not be 0, 0 is used for Arena
	Top Camera.
	'''
	main = []
	loop = []

	world_text.append('DEF Robot_{} Robot '.format(r_no))
	world_text.append('{\n')
	world_text.append('  translation {0} 0.03 {1}\n'.format(x,z))
	world_text.append('  children [\n')
	#Below lines for robot body
	world_text.append('    DEF robot_{}_body Shape '.format(r_no))
	world_text.append('{\n')
	world_text.append('      appearance PBRAppearance {\n')
	world_text.append('        baseColor 0.917647 0.145098 0.145098\n')
	world_text.append('        roughness 1\n')
	world_text.append('        metalness 0\n')
	world_text.append('      }\n')
	world_text.append('      geometry Box {\n')
	world_text.append('        size 0.09 0.06 0.07\n')
	world_text.append('      }}\n')
	#Below lines for sensor
	distance_sensor(r_no,1,0.045,0,0,0.1,100,supervisor,False,world_text,main,loop)
	distance_sensor(r_no,2,-0.045,0,180,0.1,100,supervisor,False,world_text,main,loop)
	distance_sensor(r_no,3,0,0.035,-90,0.1,100,supervisor,False,world_text,main,loop)
	distance_sensor(r_no,4,0,-0.035,90,0.1,100,supervisor,False,world_text,main,loop)
	#Below lines for motor when no real robots exist
	if supervisor == False:
		motor()
	world_text.append('  ]\n')
	#end of the children of robot
	world_text.append('  name "robot_{}"\n'.format(r_no))
	world_text.append('  boundingObject USE robot_{}_body\n'.format(r_no))
	world_text.append('  controller "Robot_{}"\n'.format(r_no))
	if supervisor == True:
		world_text.append('  supervisor TRUE\n')
	world_text.append('}\n')
	
	#controller of robot
	robot_controller(r_no,supervisor,main,loop)
	
def motor(x,z):
	'''
	x, y are coordinates are w.r.t the robot body and x, y values are
	in meters.
	'''

def obstacle(x,z,i,a,world_text):
	'''
	Cubic obstacle with side size a in meters. x, y are coordinate
	values of obstacle w.r.t general coordinate axis. Base color is
	the color of the obstacle and it made black as default.
	'''
	world_text.append('Solid {\n')
	world_text.append('  translation {0} {1} {2}\n'.format(x,a/2,z))
	world_text.append('  children [\n')
	world_text.append('    DEF obstacle_{0} Shape '.format(i))
	world_text.append('{\n')
	world_text.append('      appearance PBRAppearance {\n')
	world_text.append('        baseColor 0 0 0\n')
	world_text.append('        roughness 1\n')
	world_text.append('        metalness 0\n')
	world_text.append('      }\n')
	world_text.append('      geometry Box {\n')
	world_text.append('        size {0} {0} {0}\n'.format(a))
	world_text.append('      }}]\n')
	world_text.append('  name "obstacle_{}"\n'.format(i))
	world_text.append('  boundingObject USE obstacle_{}\n'.format(i))
	world_text.append('}\n')
	

def arena_top_cam(a,grid_length,y,width,height,quality,world_text):
	'''
	x, z coordinates of middle point of the arena and can be found by 
	arena matrix(a) with grid_length. Value of y should be proper
	perpendicular distance from the floor and y value in meters. Values
	of width and height are resolution of camera and values are in
	pixels. Also quality is added to decrease quality of the images for
	size issues in the mqtt performance. Quality is between 0-100 and
	100 is best quality.
	'''
	x = a.shape[0]
	x = x / 2 * grid_length
	z = a.shape[1]
	z = z / 2 * grid_length
	y = y * (width / height) #Assumed width > height
	
	world_text.append('DEF Arena_Cam Robot {\n')
	world_text.append('  translation {0} {1} {2}\n'.format(x,y,z))
	world_text.append('  rotation -1 0 0 1.5708\n')
	world_text.append('  children [\n')
	world_text.append('    Camera {\n')
	world_text.append('      name "Arena_Top_Cam"\n')
	world_text.append('      width {}\n'.format(width))
	world_text.append('      height {}\n'.format(height))
	world_text.append('    }]\n')
	world_text.append('  name "robot_0"\n')
	world_text.append('  controller "arena_top_cam"\n')
	world_text.append('  supervisor TRUE\n')
	world_text.append('}\n')
	
	#Controller of the arena top camera
	arenatopcam_controller = []
	
	arenatopcam_controller.append('from controller import *\n')
	arenatopcam_controller.append('import paho.mqtt.publish as mqtt\n')
	arenatopcam_controller.append('import io\n')
	arenatopcam_controller.append('from PIL import Image\n')
	arenatopcam_controller.append('\n')
	arenatopcam_controller.append('timeStep = 128\n') #Arena camera takes image every 128ms
	arenatopcam_controller.append('supervisor = Supervisor()\n')
	arenatopcam_controller.append('arena_cam = supervisor.getCamera("Arena_Top_Cam")\n')
	arenatopcam_controller.append('arena_cam.enable(timeStep)\n')
	arenatopcam_controller.append('\n')
	arenatopcam_controller.append('while supervisor.step(timeStep) != -1:\n')
	arenatopcam_controller.append('    image = arena_cam.getImage()\n')
	arenatopcam_controller.append('    image_new = Image.frombytes("RGBA", ({0},{1}), image, "raw")\n'.format(width ,height))
	arenatopcam_controller.append('    image_new = image_new.convert("RGB")\n')
	arenatopcam_controller.append('    b, g, r = image_new.split()\n')
	arenatopcam_controller.append('    image_new = Image.merge("RGB", (r, g, b))\n')
	arenatopcam_controller.append('    imgByteArr = io.BytesIO()\n')
	arenatopcam_controller.append('    image_new.save(imgByteArr, format="jpeg",optimize=True,quality={})\n'.format(quality))
	arenatopcam_controller.append('    imgByteArr = imgByteArr.getvalue()\n')
	arenatopcam_controller.append('    mqtt.single("EWA_arenacam", imgByteArr ,hostname="192.168.1.7")\n') #Use hostname of the broker
	
	location = "C:/Program Files/Webots/projects/default/controllers/arena_top_cam" # EDIT THIS for proper path in Linux
	if is_admin():#Windows admin permissions inside of this if part of the program
		Path(location).mkdir(parents=False, exist_ok=True)
		[f.unlink() for f in Path(location).glob("*") if f.is_file()]
		f = open(location + "/arena_top_cam.py", "w")
		f.writelines(arenatopcam_controller)
		f.close()
	else:
    # Re-run the program with admin rights
		ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

def world_creator(floor_matrix,grid_length,basic_time_step):
	'''
	floor_matrix is a matrix and it decides shape of the arena, number 
	of grids, grid colors. Each matrix element is a grid texture. 
	Corresponding element number will be defined. Value of grid_length
	in meters. basic_time_step is the time step increament used by 
	Webots and expressed in milliseconds. Default value of basic time
	step in Webots is 32ms.
	'''
	contents = []
	a = floor_matrix.shape
	m = a[0]
	n = a[1]
	x = m / 2 * grid_length
	z = n / 2 * grid_length
	max_length = max(m,n) * grid_length
	y = max_length / 0.748 #Field of view calculations
	
	#Main contents of world
	contents.append('#VRML_SIM R2020a utf8\n')
	contents.append('WorldInfo {\n')
	contents.append('  basicTimeStep {}\n'.format(basic_time_step))
	contents.append('}\n')
	contents.append('Viewpoint {\n')
	contents.append('  orientation -1 0 0 1.5708\n')
	contents.append('  position {0} {1} {2}\n'.format(x,2*y,z))
	contents.append('}\n')
	contents.append('TexturedBackground {\n')
	contents.append('}\n')
	contents.append('TexturedBackgroundLight {\n')
	contents.append('}\n')
	
	#Element of world: Arena, Robots, Top Camera
	arena_creator(floor_matrix, grid_length,contents)
	robot_creator(-grid_length,grid_length,1,True,contents)
	robot_creator(-grid_length,3*grid_length,2,True,contents)
	arena_top_cam(floor_matrix,grid_length,y,1600,1200,70,contents)
		
	f = open("sample_world.wbt", "w")
	f.writelines(contents)
	f.close()
	

a = np.random.randint(0,5,size=(10,10))
print(a)
print(a.shape)
world_creator(a, 0.15, 32)
