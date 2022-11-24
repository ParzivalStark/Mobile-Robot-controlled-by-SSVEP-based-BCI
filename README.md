# Active navigation of a mobile robot controlled by an SSVEP based BCI

This project seeks to use the BCI "BrainTec" bassed on SSVEP to control a mobile robot "Puzzlebot" in a navigation task on a real environment. This repository has the documentation of the code implemented to achieve this.

## Integration
The system consist of two main parts that are described in the following sections.

### [SSVEP system](SSVEP%20system)

### [Robot system](Robot%20system)

The diagram of the different parts is shown in the following figure, where the idea is that the person receives the stimuli of the leds, along with the camera from the robot, the person has electrods connected to be able to get their EEG signals, which are proccessed by the BCI to get the intention of the person, this is passed as a movement to the robot which has the camera attached to it, therefore moving the image in the person's screen who has to act accordingly to finish the navigation task.

<p align="center">
  <img src="../Reference%20images/calibration_board.png" width="512" height="750"/>
</p>