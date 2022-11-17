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

The matrix has five pins which are connected as it is indicated in the following image.  
![Matrix connection with Raspberry](../Reference%20images/MatrixConnection.png)

Any number of matrices can be chained, as long as the right amount of current is supplied.

## Program

## Usage