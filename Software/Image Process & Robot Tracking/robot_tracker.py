'''
This code used for to dectect robot markers and from them extract
location and orientation of robots w.r.t. origin marker.
'''
import cv2
from cv2 import aruco
import numpy as np
import math

camera = cv2.VideoCapture(0 + cv2.CAP_DSHOW) # Enables camera 

def isRotationMatrix(R) : 
    #Checks for valid rotation matrix
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype = R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6

def rotationMatrixToEulerAngles(R) : 
    # Turns rotation matrix to radians.
    assert(isRotationMatrix(R))
    sy = math.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])
    singular = sy < 1e-6
    if  not singular :
        x = math.atan2(R[2,1] , R[2,2])
        y = math.atan2(-R[2,0], sy)
        z = math.atan2(R[1,0], R[0,0])
    else :
        x = math.atan2(-R[1,2], R[1,1])
        y = math.atan2(-R[2,0], sy)
        z = 0
    return np.array([x, y, z])

def orientation(rvec): 
    #Turns rotation vector to rotation matrix then turns it to radians.
    rod,_ = cv2.Rodrigues(rvec)
    ori = rotationMatrixToEulerAngles(rod)
    return ori[2]


def coordinate(o_x, o_y, x, y):
    # Gives coordinates of a marker w.r.t. marker at origin.
    f_x = (x - o_x)*1000
    f_y = (y - o_y)*1000
    return f_x, f_y

#Camera matrix found by calibration.
mtx = np.array([[736.84998156,   0.        , 348.02940053],
                [  0.        , 736.84998156, 269.56120894],
                [  0.        ,   0.        ,   1.        ]])

#Distortion coefficents of camera found by calibration.
dist = np.array([[-5.87090932e+01],
                 [ 8.58010534e+02],
                 [ 5.12005939e-05],
                 [ 2.27767059e-03],
                 [ 7.60525477e+02],
                 [-5.82126026e+01],
                 [ 8.28492084e+02],
                 [ 1.20930421e+03],
                 [ 0.00000000e+00],
                 [ 0.00000000e+00],
                 [ 0.00000000e+00],
                 [ 0.00000000e+00],
                 [ 0.00000000e+00],
                 [ 0.00000000e+00]])

NoneType=type(None)

while True:
    #Takes image from camera and converts it to gray image.
    return_value, img = camera.read()
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #Choosen aruco marker library.
    dictionary = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
    parameters = aruco.DetectorParameters_create()
    #Detection of markers.
    marker_corners, marker_IDs, rejected_canditates = aruco.detectMarkers(img, dictionary, parameters=parameters)
    #Getting rotation and translation vectors from detected markers.
    rvec, tvec, _ = aruco.estimatePoseSingleMarkers(marker_corners, 0.04, mtx, dist)

    datas = []
    
    if type(marker_IDs) != NoneType:
        if [76] in marker_IDs:
            #Marker with no 76 choosen as origin and its aspects found to create reference.
            pos_of_origin = marker_IDs.tolist().index([76])
            origin_x = tvec[pos_of_origin][0][0]
            origin_y = tvec[pos_of_origin][0][1]
            origin_orient = orientation(rvec[pos_of_origin])

            for i in range(len(marker_IDs)):
                data = []
                if marker_IDs[i] == [76]:
                    continue
                #Calculations of positon and orientation of detected robot markers w.r.t. origin.
                orient = orientation(rvec[i]) - origin_orient
                x_rev = tvec[i][0][0]
                y_rev = tvec[i][0][1]
                x, y = coordinate(origin_x, origin_y, x_rev, y_rev)
                data.extend((marker_IDs[i][0], x, y, orient))
                datas.append(data)
    
    if datas != []:
        #print(datas)
        f = open("t_r_of_robots.txt", mode='w')
        f.write("{}".format(datas))
        f.close()

    '''
    #Monitoring camera feed to debug.
    final = aruco.drawDetectedMarkers(img,marker_corners,marker_IDs)
    cv2.imshow("image", final)
    k = cv2.waitKey(1)
    if k%256 == 27:# ESC pressed
        break
    '''
