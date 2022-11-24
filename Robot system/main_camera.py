# Library for computer vision
import cv2 as cv
# Library to use ArUco markers
from cv2 import aruco
# Library to do calculations
import numpy as np
# Library to use UDP
import socket
# Library to decompress image
import pickle
# Library to measure time
from time import time

# IP and port of the receiving computer
ip='192.168.0.50'
port=4000
# Create socket to get the camera images from the puzzlebot
s=socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
s.bind((ip,port))

# Size of images to be displayed
IM_SIZE = 75
# Minimum distance to show arrows
DIST_LIM = 80
# Minimum distance to show goal
DIST_LIM_2 = 50
# ArUco ids of the arrows and goal
ID_LEFT = 5
ID_RIGHT = 3
ID_GOAL = 1
# Real size of markers
MARKER_SIZE = 15  # centimeters
# Time start image was displayed
TIME2START = 0.5
# Time arrows were displayed
TIME2TURN = 2

# Flags to know if the image should be displayed
startFlag = False
turnLeftFlag = False
turnRightFlag = False
goalFlag = False

# Define dictonary to use
marker_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)

# Create markers detector
param_markers = aruco.DetectorParameters_create()

# Get and resize images to be displayed
left = cv.imread('data/izquierda.png')
left = cv.resize(left, (IM_SIZE,IM_SIZE))
forward = cv.imread('data/adelante.jpg')
forward = cv.resize(forward, (IM_SIZE,IM_SIZE))
right = cv.imread('data/derecha.jpg')
right = cv.resize(right, (IM_SIZE,IM_SIZE))
goal = cv.imread('data/goal.png')
goal = cv.resize(goal, (IM_SIZE*2,IM_SIZE*2))
start = cv.imread('data/start.jpg')
start = cv.resize(start, (IM_SIZE*2,IM_SIZE*2))

# Calibration data path for the camera
calib_data_path = "calib_data/MultiMatrix2.npz"
# Load calibration data
calib_data = np.load(calib_data_path)
# Decompress calibration data
cam_mat = calib_data["camMatrix"]
dist_coef = calib_data["distCoef"]
r_vectors = calib_data["rVector"]
t_vectors = calib_data["tVector"]

# Main code
while True:
    # Recieve image from puzzlebot
    x=s.recvfrom(1000000)
    # Get only image
    data=x[0]
    # Decompress image
    data=pickle.loads(data)
    # Decode image
    frame = cv.imdecode(data, cv.IMREAD_COLOR)
    
    # Convert frame to grayscale
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Get markers from frame
    marker_corners, marker_IDs, reject = aruco.detectMarkers(gray_frame, marker_dict, parameters=param_markers)
    
    # Check if markers were detected
    if len(marker_corners) > 0:
        # Get ids from the markers
        ids = marker_IDs.flatten()
        # Iterate through each marker
        for (marker_corner, marker_id) in zip(marker_corners, ids):
            # Check if the id is of interest
            if marker_id in [ID_LEFT, ID_GOAL, ID_RIGHT]:
                # Estimate pose
                rVec, tVec, _ = aruco.estimatePoseSingleMarkers(marker_corner, MARKER_SIZE, cam_mat, dist_coef)
                # Calculate distance
                distance = np.sqrt(tVec[0][0][2] ** 2 + tVec[0][0][0] ** 2 + tVec[0][0][1] ** 2)
                
                # Get time and enable the appropiate flag if the code is close enough
                if distance <= DIST_LIM and marker_id == ID_LEFT:
                    turn_time = time()
                    turnLeftFlag = True
                elif distance <= DIST_LIM and marker_id == ID_RIGHT:
                    turn_time = time()
                    turnRightFlag = True
                elif distance <= DIST_LIM_2 and marker_id == ID_GOAL:
                    goalFlag = True

    # Check flags and overlap corresponding image
    # Check time to turn off flag
    if turnLeftFlag:
        frame[int(frame.shape[0]/2-IM_SIZE/2):int(frame.shape[0]/2+IM_SIZE/2),
                int(frame.shape[1]/2-IM_SIZE/2):int(frame.shape[1]/2+IM_SIZE/2)] = left
        if time() - turn_time >= TIME2TURN:
            turnLeftFlag = False

    elif turnRightFlag:
        frame[int(frame.shape[0]/2-IM_SIZE/2):int(frame.shape[0]/2+IM_SIZE/2),
                int(frame.shape[1]/2-IM_SIZE/2):int(frame.shape[1]/2+IM_SIZE/2)] = right
        if time() - turn_time >= TIME2TURN:
            turnRightFlag = False

    elif goalFlag:
        frame[int(frame.shape[0]/2-IM_SIZE):int(frame.shape[0]/2+IM_SIZE),
                int(frame.shape[1]/2-IM_SIZE):int(frame.shape[1]/2+IM_SIZE)] = goal

    # Get pressed key
    key = cv.waitKey(1)
    # Finish program with 'q'
    if key == ord("q"):
        break
    # Enable start flag with 'Enter'
    elif key == 13 and not startFlag:
        startFlag = True
        start_time = time()

    # Check start flag to overlap its image
    if startFlag:    
        frame[int(frame.shape[0]/2-IM_SIZE):int(frame.shape[0]/2+IM_SIZE),
                    int(frame.shape[1]/2-IM_SIZE):int(frame.shape[1]/2+IM_SIZE)] = start
        # Disable flag when time is over
        if time() - start_time >= TIME2START:
            startFlag = False

    # Display image
    cv.imshow("ROBOT CAMERA", frame)    
    
# Close socket and windows
s.close()
cv.destroyAllWindows()
