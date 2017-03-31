# Dice-Reading

Reads the face of a white die with black pips.

Initializes the Pi's GPIO pins, takes a picture from the webcam attached to the usb port of the Pi, processes the Image, to obtain the number of pips, and prints out the value.

If there is a seven segment display attached to the Pi's GPIO pin in the manner displayed below, then the correct number should be displayed.

# Usage:

the masterCamera.py script contains both the lid centering algorithm to center over the lid and to read the die after the lid has been lifted. It contains all the necessary initializations for RPi - Arduino serial communication. The script is run at startup via crontab and is not suppressed as a background process.

lidDetect.py and readPips.py are separted and older versions of the masterCamera.py script which combines both and has recent changes.

get_null_vals.py returns an array of baseband values that the Xethru sees at it's current position.

xethruDetect.py tries to detect dead ends vs regular cells.

