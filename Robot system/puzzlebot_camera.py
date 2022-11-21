import cv2
import socket
import pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--ip', type=str)
args = parser.parse_args()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10000000)
serverip = args.ip or '192.168.0.50'
serverport = 4000

cap = cv2.VideoCapture('nvarguscamerasrc ! video/x-raw(memory:NVMM), width=1280, height=720, format=NV12, framerate=60/1 ! nvvidconv flip-method=0 ! video/x-raw, width=640, height=360, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink')

while True:
    ret, frame = cap.read()
    ret, buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
    x_as_bytes = pickle.dumps(buffer)

    #cv2.imshow('frame', frame)

    try:
        s.sendto(x_as_bytes, (serverip, serverport))
    except:
        print("Error sending image")

    if cv2.waitKey(10) == 13:
        break

cv2.destroyAllWindows()
cap.release()