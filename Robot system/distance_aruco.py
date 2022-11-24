# Library for computer vision
import cv2 as cv
# Library to use ArUco markers
from cv2 import aruco
# Library to do calculations
import numpy as np

# Calibration data path for the camera
calib_data_path = "../calib_data/MultiMatrix.npz"
# Load calibration data
calib_data = np.load(calib_data_path)
# Decompress calibration data
cam_mat = calib_data["camMatrix"]
dist_coef = calib_data["distCoef"]
r_vectors = calib_data["rVector"]
t_vectors = calib_data["tVector"]

# Real size of the marker
MARKER_SIZE = 5.9  # centimeters

# Select dictonary
marker_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)

# Create markers detector
param_markers = aruco.DetectorParameters_create()

# Object to capture video from the camera
cap = cv.VideoCapture(0)

# Main code
while True:
    # Get frame from camera
    ret, frame = cap.read()
    
    # Convert frame to gray scale
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Get markers from frame
    marker_corners, marker_IDs, reject = aruco.detectMarkers(gray_frame, marker_dict, parameters=param_markers)

    # Check if any markers were detected
    if marker_corners:
        # Get rotation and transfomation vectors of the marker in relation to the camera
        rVec, tVec, _ = aruco.estimatePoseSingleMarkers(marker_corners, MARKER_SIZE, cam_mat, dist_coef)
        # Get number of markers
        total_markers = range(0, marker_IDs.size)
        # Iterate through every marker
        for ids, corners, i in zip(marker_IDs, marker_corners, total_markers):
            # Draw the outline of the marker
            cv.polylines(frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA)

            # Decompress the corners
            corners = corners.reshape(4, 2)
            corners = corners.astype(int)
            top_right = corners[0].ravel()
            top_left = corners[1].ravel()
            bottom_right = corners[2].ravel()
            bottom_left = corners[3].ravel()

            # Calculate the distance
            distance = np.sqrt(tVec[i][0][2] ** 2 + tVec[i][0][0] ** 2 + tVec[i][0][1] ** 2)

            # Draw the pose of the marker
            point = cv.drawFrameAxes(frame, cam_mat, dist_coef, rVec[i], tVec[i], 4, 4)

            # Display the distance
            cv.putText(
                frame,
                f"id: {ids[0]} Dist: {round(distance, 2)}",
                top_right,
                cv.FONT_HERSHEY_PLAIN,
                1.3,
                (0, 0, 255),
                2,
                cv.LINE_AA,
            )
            # Display the coordinates
            cv.putText(
                frame,
                f"x:{round(tVec[i][0][0],1)} y: {round(tVec[i][0][1],1)} ",
                bottom_right,
                cv.FONT_HERSHEY_PLAIN,
                1.0,
                (0, 0, 255),
                2,
                cv.LINE_AA,
            )
    # Show image
    cv.imshow("frame", frame)
    # Exit code pressin 'q'
    key = cv.waitKey(1)
    if key == ord("q"):
        break

# Close windows and camera
cap.release()
cv.destroyAllWindows()