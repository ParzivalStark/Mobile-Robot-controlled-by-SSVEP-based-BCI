# Description of the robot system

## Puzzlebot
Puzzlebot is a mobile robot developed by Manchester Robotics, it uses a diferental drive controlled by a special board based on an ESP32 to control the motors and recieved the information from the encoders. It communicates via ROS serial with a Jetson Nano 2GB to enable complex algorithms to control the robot using ROS. It also has a camera module v2 from Raspberry to use computer vision algorithms.

### Movement with ROS
The robot received the movements via UDP, and depending on the move the velocities were change accordingly by passing them to the corresponding topic. Each move lasted 300 ms, this timer was reseted each time the same move was recieved to ensure a continous movement. [Code](puzzlebot_movement.py)  

### Conection
The movements detected by the BCI were transmited via UDP to the same computer that was running it, so in order to pass them to the robot an additional script was needed to collect the data and retransmit it to the puzzlebot via UPD as well. [Code](retransmit_bci.py)  

## Camera
The camera used is a PIS-1685 camera module for Raspberry Pi Camera Board V2, the normal camera of the module was change in order to get a better perspective when navigating through the route.  

### Connection
The raw image was transmitted via UDP, in order to do it the image it was first encoded, compressed into a pickle, sent and then the process was reverted when recieved in the main computer to apply some algorithms to use ArUco codes to measure distance. [Code](puzzlebot_camera.py)

### Calibration
To be able to measure distance the camera needed to be calibated, this [code](capture_calibration_images.py) was used to take images of a calibration board, that can be seen in the following image, after taking and saving the pictures, another [script](camera_calibration.py) was used to get the parameters of the calibration. The full procces can be seen on this [video](https://www.youtube.com/watch?v=JHeNger8B2E)  ![Calibration board](../Reference%20images/calibration_board.png)  

### ARUCO codes


#### Generation

#### Distance

#### Signals