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
To be able to measure distance the camera needed to be calibated, this [code](capture_calibration_images.py) was used to take images of a calibration board, that can be seen in the following image, after taking and saving the pictures, another [script](camera_calibration.py) was used to get the parameters of the calibration. The full procces can be seen on this [video](https://youtu.be/JHeNger8B2E).  
<p align="center">
  <img src="../Reference%20images/calibration_board.png"/>
</p>

### ArUco markers
To give indications durign the navigation task, AruCo markers were used, this codes are binary square markers that enable augmented reality and can be used for pose estimation. Using this we calculate distance between the robot and the code to put arrows in the camera when the person needed to turn to continue with the route.  
<p align="center">
  <img src="../Reference%20images/aruco4.png"/>
</p>

#### Generation
The OpenCV library has a function to generate ArUco markers, using the dictionay, id and size of the marker it's possible to generate and save markers ready to be used. This [code](https://github.com/bioruben/data_live_2022/blob/main/generate_aruco.py) generates markers with de original dictonary passing the id as an argument.  

#### Distance
To measure the distance between the robot and the markers, there's a function that can estimate the pose of the code using the corners of the detected marker, the real size of the marker and the calibration parameters. The [code](distance_aruco.py) used to measure the distance is based on this [video](https://youtu.be/mn-M6Qzx6SE).  

#### Arrows
By calculating the distance it was possible to give indications to the persons in the same camera, when they were to close, an arrow appeared on the center of the image to indicate that a turn was neccesary to avoid a collision. Also at the end of the route a "Good job" message appeared to indicate the succesful completition of the task.
