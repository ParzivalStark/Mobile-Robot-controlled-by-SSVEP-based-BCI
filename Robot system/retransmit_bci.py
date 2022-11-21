# Library to use UDP
import socket

# IP and port from BCI
UDP_IP = "127.0.0.1"
UDP_PORT = 2000

# Create socket to recieve data
sock_bci = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_bci.bind((UDP_IP, UDP_PORT))
# Disable wait time to get data
sock_bci.setblocking(0)

# Create socket to send data
s_jetson=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s_jetson.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10000000)
# IP and port from Puzzlebot
serverip="192.168.0.25"
serverport=4000

# Main code
while True:
    # Avoid exceptions when not recieving data
    try:
        # Recieve data from BCI
        data, addr = sock_bci.recvfrom(1024)
        print(data)
        # Send data to Puzzlebot
        s_jetson.sendto(data,(serverip , serverport))
    except:
        print("error sending")