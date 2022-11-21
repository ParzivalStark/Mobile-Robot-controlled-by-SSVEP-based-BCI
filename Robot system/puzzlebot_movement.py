#!/usr/bin/env python3

# Library for ROS
import rospy
# Type of message from velocity topic
from geometry_msgs.msg import Twist
# Libray to use UDP
import socket

# Publisher of velocity topic
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=100)
# Initialize node
rospy.init_node('basic_move', anonymous=True)
# Refresh rate for loop
rate = rospy.Rate(10)

# Clean message of velocity
vel = Twist()
vel.linear.x = 0
vel.linear.y = 0
vel.linear.z = 0
vel.angular.x = 0
vel.angular.y = 0
vel.angular.z = 0

# Flags to know type of move
forwardFlag = False
leftFlag = False
rightFlag = False

# Flag to ensure only one publication of the velocity
pubFlag = False

# IP and port from puzzlebot
ip = '192.168.0.25'
port = 4000
# Create socket to recieve data
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((ip, port))
# Disable wait time to get data
s.setblocking(0)

# Main code
while not rospy.is_shutdown():
    # Avoid exceptions when not recieving data
    try:
        data, addr = s.recvfrom(1024)
    except:
        data = ""
    
    # Check type of move, activate flag accordingly and get reference of current time
    if data in [b'Selection: up', b'Selection: up\n']:
        forwardFlag = True
        leftFlag = False
        rightFlag = False
        t0 = rospy.get_time()
    elif data in [b'Selection: turn_left', b'Selection: turn_left\n']:
        leftFlag = True
        forwardFlag = False
        rightFlag = False
        t0 = rospy.get_time()
    elif data in [b'Selection: turn_right', b'Selection: turn_right\n']:
        rightFlag = True
        forwardFlag = False
        leftFlag = False
        t0 = rospy.get_time()
    
    # Check flag and change velocity message accordingly
    if forwardFlag:
        # Front linear move
        vel.linear.x = 0.2
        # Publish message only one time
        if not pubFlag:
            pub.publish(vel)
            pubFlag = True
        # When time reaches 300 ms stop robot
        if rospy.get_time() - t0 >= 0.3:
            forwardFlag = False
            pubFlag = False
            vel.linear.x = 0
            pub.publish(vel)
    elif leftFlag:
        # Turn left move
        vel.angular.z = 0.05
        # Publish message only one time
        if not pubFlag:
            pub.publish(vel)
            pubFlag = True
        # When time reaches 300 ms stop robot
        if rospy.get_time() - t0 >= 0.3:
            leftFlag = False
            pubFlag = False
            vel.angular.z = 0
            pub.publish(vel)
    elif rightFlag:
        # Turn right move
        vel.angular.z = -0.05
        # Publish message only one time
        if not pubFlag:
            pub.publish(vel)
            pubFlag = True
        # When time reaches 300 ms stop robot
        if rospy.get_time() - t0 >= 0.03:
            rightFlag = False
            pubFlag = False
            vel.angular.z = 0
            pub.publish(vel)