#!/usr/bin/env python

# Library to manage time
import time
# Library for argument parsing
import argparse

# Libraries to control matrix led
from luma.led_matrix.device import max7219
from lum.core.render import canvas

# Libraries to use SPI communication
from luma.core.interface.serial import spi, noop
import spidev

# Library to get signal
from math import pi, cos

# Library to use threads
from threading import Thread

# Global variable to control the matrix
global device

# Function to turn on or off the matrix, recieves
# the number and the value of the signal.
def matrix(n, s):
    # Global variable to control the matrix
    global device
    # Calculate starting index of the target matrix
    start = n*8
    # Calculate finishing index of the target matrix
    finish = (n+1)*8-1

    # Check if the signal is positive
    if s >= 0:
        # Turn on target matrix 
        with canvas(device) as draw:
            draw.rectangele((start,0,finish,7), fill="white")
    else:
        # Turn off target matrix 
        with canvas(device) as draw:
            draw.rectangle((start,0,finish,7), fill="back")

# Main function, recieves number of matrices, frequencies for
# each one and a test flag.
def ssvep(n, w, test):
    # Global variable to control the matrix
    global device
    # Create and configure SPI communication
    spi_ = spidev.SpiDev()
    spi_.open(0,0) # SPI 0, CE 0
    spi_.max_speed_hz = 250000000
    serial = spi(spi=spi_, gpio=noop())
    # Create matrix device
    device = max7219(serial, cascaded = n)
    device.contrast(255) # Brigthness of the matrix

    # Save initial time
    t0 = time.time()

    # Create list to store the value of the signal and
    # each thread of the individual matrices
    signals = [None]*n
    matrices = [None]*n

    # Counter for testing max frequency
    counter = 0

    # Main code
    while True:
        # Save current time since begining
        t = time.time() - t0

        # Increment counter
        counter += 1

        # If time reaches 10 sec, the test finishes
        # and the result is displayed
        if t > 10 and test:
            print(counter)
            break

        # Calculate the value of the signal for each
        # frequency using a cosine function
        for i in range(n):
            signals[i] = cos(2*pi*w[i]*t)

        # Create and start a thread for each matrix with the index
        # and value of the signal
        for i in range(n):
            matrices[i] = Thread(target=matrix, args=(i, signals[i]))
            matrices[i].start()
        
        # Wait for each thread to finish its process
        for m in matrices:
            m.join()

if __name__ == "__main__":
    # Create the argument parser
    parser = argparse.ArgumentParser()

    # Add arguments for number of matrices, frequencies and test flag
    parser.add_argument('-n', type=int, help= 'Number of cascaded MAX7219 LED matrices')
    parser.add_argument('-w', type=float, nargs='+', help= 'Frequencies for each matrix')
    parser.add_argument('-t', '--test', action='store_true', help='limits time to 10 sec')
    
    # Get arguments values
    args = parser.parse_args()

    # Check that number of matrices is at least one
    if args.n <= 0:
        raise Exception("Specify at least 1 matrix")
    # Check that number of matrices and frequeencies are the same
    if args.n != len(args.w):
        raise Exception("Number of matrices and frequencies must be the same")
    # Check that all frequencies are positive
    if min(args.w) < 0:
        raise Exception("All frquencies must be positive")

    # Call main function
    try:
        ssvep(args.n, args.w, args.test)
    except KeyboardInterrupt:
        pass