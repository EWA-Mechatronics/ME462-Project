'''
This code used for camera calibartion to get camera matrix and distortion
coefficients which are used in getting translation and rotaion vector of
the aruco markers. estimatePoseSingleMarkers function of open cv need
camera matrix and distortion coefficients. 10 pre taken images used for
calibration. Most of the code taken from;
https://mecaruco2.readthedocs.io/en/latest/notebooks_rst/Aruco/sandbox/ludovic/aruco_calibration_rotation.html
'''

import cv2
from cv2 import aruco
import numpy as np

allCorners = []
allIds = []
decimator = 0
# SUB PIXEL CORNER DETECTION CRITERION
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.00001)
dictionary = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
board = aruco.CharucoBoard_create(7, 5, 1, .8, dictionary)

for i in range(0,10):
    
    frame = cv2.imread("calibration_{}.png".format(i))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, dictionary)

    if len(corners)>0:
        # SUB PIXEL DETECTION
        for corner in corners:
            cv2.cornerSubPix(gray, corner,winSize = (3,3),zeroZone = (-1,-1),criteria = criteria)
        res2 = aruco.interpolateCornersCharuco(corners,ids,gray,board)
        if res2[1] is not None and res2[2] is not None and len(res2[1])>3 and decimator%1==0:
            allCorners.append(res2[1])
            allIds.append(res2[2])

    decimator+=1

imsize = gray.shape

cameraMatrixInit = np.array([[ 1000.,    0., imsize[0]/2.],
                             [    0., 1000., imsize[1]/2.],
                             [    0.,    0.,           1.]])

distCoeffsInit = np.zeros((5,1))
flags = (cv2.CALIB_USE_INTRINSIC_GUESS + cv2.CALIB_RATIONAL_MODEL + cv2.CALIB_FIX_ASPECT_RATIO)

(ret, camera_matrix, distortion_coefficients0,
 rotation_vectors, translation_vectors,
 stdDeviationsIntrinsics, stdDeviationsExtrinsics,
 perViewErrors) = aruco.calibrateCameraCharucoExtended(
                  charucoCorners=allCorners,
                  charucoIds=allIds,
                  board=board,
                  imageSize=imsize,
                  cameraMatrix=cameraMatrixInit,
                  distCoeffs=distCoeffsInit,
                  flags=flags,
                  criteria=(cv2.TERM_CRITERIA_EPS & cv2.TERM_CRITERIA_COUNT, 10000, 1e-9))
                  
print(camera_matrix)
print(distortion_coefficients0)
