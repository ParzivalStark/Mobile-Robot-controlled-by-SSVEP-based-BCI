# Library to use camera
import cv2
# Library to use UDP
import socket
# Library to compress image
import pickle
# Library to use arguments
import argparse

# Create argument parser
parser = argparse.ArgumentParser()
# Add ip argument to use to transmit camera
parser.add_argument('--ip', type=str)
# Get arguments
args = parser.parse_args()

# Create socket to transmit image
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10000000)
# IP and port of the reciving computer
serverip = args.ip or '192.168.0.50' # Use default ip if no arguments were passed
serverport = 4000

# Initialize video from the camera using a pipeline to get the right format
cap = cv2.VideoCapture('nvarguscamerasrc ! video/x-raw(memory:NVMM), width=1280, height=720, format=NV12, framerate=60/1 ! nvvidconv flip-method=0 ! video/x-raw, width=640, height=360, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink')

# Main code
while True:
    # Get image from camera
    ret, frame = cap.read()
    # Encode image
    ret, buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
    # Compress image
    x_as_bytes = pickle.dumps(buffer)

    #cv2.imshow('frame', frame)

    # Avoid exceptions when not sending data
    try:
        s.sendto(x_as_bytes, (serverip, serverport))
    except:
        print("Error sending image")

    if cv2.waitKey(10) == 13:
        break

# Close windows and release camera
cv2.destroyAllWindows()
cap.release()