# Description of the SSVEP system
In order to create the stimuli for the SSVEP phenomena, some led matrices were used that were controlled with a
Raspberry Pi 3B+, the communication was done via SPI protocol.  

## Raspberry Pi configuration
In order to use the SPI protocol on the Raspberry Pi, it is necesary to first activate it, since it is turned off
by default. It can be done either using the graphical interface or the terminal.  
To do it with the GUI, the configuration is located in the Pi Start Menu > Preferences > Raspberry Pi Configuration.
A window will appear and in te interface tab the SPI needs to be enabled.  
To do it via terminal, run the command "sudo raspi-config", a menu will pop up, move with the arrows and select 
Interacing Options, look for SPI and select yes to enable it.  
It is recommended to reboot the system to ensure the changes were applied correctly.  

## Matrix leds
The Matrices had the MAX7219 driver and were controlled with the Luma LED Matrix library, the installation instructions
can be found at https://luma-led-matrix.readthedocs.io/en/latest/install.html  

The matrix has five input pins which are connected as it is indicated in the following image.  
<p align="center">
  <img src="../Reference%20images/MatrixConnection.png"/>
</p>  

The board has two set of pins to enable daisy-chaning, just connecting the output pins to the input ones in the next matrix. Any number of matrices can be chained, as long as the right amount of current is supplied.

## Program
To get the desired frequencies in each matrix a cosine function was used, whenever the value of this signal was positive
the matrix was turned on, otherwise it was turned off. Since all matrices were chained and taken as only one by the program it was necessary to calculate the starting and finishing index of each individual matrix. Threads were also used to ensure that the process was done more precisely.

## Usage
Arguments were added to allow a different number of stimuli and frequencies according to the needs. For the number of matrices "-n" is used along with the number, then the frequencies "-w" is used with the frequencies separated by spaces, one last argument was added "-t", this is a flag that makes the program stop after 10 seconds and displays a counter to be able to determine the maximum frequency.  
Finally, it is necesarry to use sudo permissions to acces the SPI interface.  
For example if 4 stimuli with frequencies 10, 12, 15 and 17 with no test flag the following command will be used **sudo python3 [SSVEP.py](SSVEP.py) -n 4 -w 10 12 15 17**
