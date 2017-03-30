import os
import math
import cv2
import numpy as np
import serial
import RPi.GPIO as GPIO
import time

print cv2.__version__
centerThresh = 200                      #the center threshold
lidRadius = 445                         #actual lid radius in pixels
success = "#"                           #success character
failure = "?"                           #failure character
reCenter = "*"                          #recentering character

GPIO.setmode(GPIO.BOARD)                #set mode of gpio to use board numbers
GPIO.setup(32, GPIO.IN, GPIO.PUD_DOWN)  #set mode of pin 32 to an input pin

#initialize output pins for the 7-segment display.
GPIO.setup(29, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(40, GPIO.OUT)

#initialize the serial port communication
port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=5.0)

print "waiting to read lid..."
cherryPop = 1
lidstate = False

while True:
    lidState = GPIO.input(32)

    if lidState:
        GPIO.output(29, 0)
        GPIO.output(31, 0)
        GPIO.output(33, 0)
        GPIO.output(35, 0)
        GPIO.output(37, 0)
        GPIO.output(38, 0)
        GPIO.output(40, 1)
        try:
            if cherryPop == 1:
                port.write(success) #success we recieved the start signal
                cherryPop = 0

            os.system("fswebcam -S 150 -r 800x600 --no-banner testimage.jpg")
            img = cv2.imread('testimage.jpg', 0)
            img = cv2.resize(img, (1280, 960))
            height, width = img.shape
            print width, height

            #image's center coordinates
            xCntr = width/2
            yCntr = height/2

            img = cv2.medianBlur(img, 5)
            cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

            circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 50,
                                       param1=50, param2=30, minRadius=400, maxRadius=450)


            circles = np.uint16(np.around(circles))

            closerCirc = 1000
            closerCircRadius = 0
            print circles

            #find the radius of the detected circle that is closest to our lid's radius
            for j in circles[0, :]:
                if abs(j[2] - lidRadius) < closerCirc:
                    closerCirc = abs(j[2] - lidRadius)
                    closerCircRadius = j[2]

            #make the parameters of all but the closest circle 0. i.e null them
            for k in circles[0, :]:
                if k[2] == closerCircRadius:
                    continue
                else:
                    k[0] = 0
                    k[1] = 0
                    k[2] = 0

            print circles

            #find that closest circle and get our x and y distances
            for l in circles[0, :]:
                if l[0] != 0:
                    x_dist = l[0] - xCntr
                    y_dist = l[1] - yCntr

            #grab the absolute distance between the cirlce centroid and the center of the image
            distance = round(math.sqrt((pow(x_dist, 2)) + (pow(y_dist, 2))))

            print "abs distance:", distance
            #terminate lid reading if we are within our threshold
            if distance <= centerThresh:
                break

            print "x-Dist:", x_dist
            print "y-Dist:", y_dist

            #send the distances to the arduino
            port.write(reCenter)
            port.write(str(int(x_dist)))
            port.write("\r\n")
            port.write(str(int(y_dist)))

            for j in circles[0, :]:
                if j[0] != 0:
                    if j[0]-xCntr < 0:
                        print 'left'
                    else:
                        print 'right'
                    if j[1]-yCntr < 0:
                        print 'up'
                    else:
                        print 'down'

        except AttributeError:
            print "No cirles detected"
            lidstate = False
            port.write(failure)

port.write(success) #we successfully centered over the cache lid

a = 29
b = 31
c = 33
d = 35
e = 37
f = 38
g = 40

print "waiting to read die..."

while True:
    diestate = GPIO.input(32)

    if diestate:

        try:
            os.system("fswebcam -S 150 -r 800x600 --no-banner testimagePip.jpg")
            img = cv2.imread('testimagePip.jpg', 0)
            img = cv2.resize(img, (1280, 960))
            img = cv2.medianBlur(img, 5)
            cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

            circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 10,
                                       param1=50, param2=30, minRadius=15, maxRadius=30)


            circles = np.uint16(np.around(circles))

            #method of filtering false positives
            an = circles[0][0][0] + 140
            bn = circles[0][0][0] - 140
            cn = circles[0][0][1] + 140
            dn = circles[0][0][1] - 140

            print circles

            #if the detected circles are not within these ranges they are false positives
            #  hence filtered
            for i in circles[0, :]:
                if i[0] >= bn and i[0] <= an and i[1] >= dn and i[1] <= cn:
                    continue
                else:
                    i[0] = 0
                    i[1] = 0
                    i[2] = 0
            count = 0

            #count the number of pips
            for j in circles[0, :]:
                if j[0] != 0:
                    count += 1

            print circles
            print count, "pips"

            #print the appropriate count number to the 7-segment display
            if count == 1:
                GPIO.output(a, 1)
                GPIO.output(b, 0)
                GPIO.output(c, 0)
                GPIO.output(d, 1)
                GPIO.output(e, 1)
                GPIO.output(f, 1)
                GPIO.output(g, 1)

            elif count == 2:
                GPIO.output(a, 0)
                GPIO.output(b, 0)
                GPIO.output(c, 1)
                GPIO.output(d, 0)
                GPIO.output(e, 0)
                GPIO.output(f, 1)
                GPIO.output(g, 0)

            elif count == 3:
                GPIO.output(a, 0)
                GPIO.output(b, 0)
                GPIO.output(c, 0)
                GPIO.output(d, 0)
                GPIO.output(e, 1)
                GPIO.output(f, 1)
                GPIO.output(g, 0)

            elif count == 4:
                GPIO.output(a, 1)
                GPIO.output(b, 0)
                GPIO.output(c, 0)
                GPIO.output(d, 1)
                GPIO.output(e, 1)
                GPIO.output(f, 0)
                GPIO.output(g, 0)

            elif count == 5:
                GPIO.output(a, 0)
                GPIO.output(b, 1)
                GPIO.output(c, 0)
                GPIO.output(d, 0)
                GPIO.output(e, 1)
                GPIO.output(f, 0)
                GPIO.output(g, 0)

            elif count == 6:
                GPIO.output(a, 1)
                GPIO.output(b, 1)
                GPIO.output(c, 0)
                GPIO.output(d, 0)
                GPIO.output(e, 0)
                GPIO.output(f, 0)
                GPIO.output(g, 0)

            else:
                GPIO.output(a, 0)
                GPIO.output(b, 0)
                GPIO.output(c, 0)
                GPIO.output(d, 0)
                GPIO.output(e, 0)
                GPIO.output(f, 0)
                GPIO.output(g, 1)

            port.write(success) #success we read the die
            break

        except AttributeError:
            print "No cirles detected"
            diestate = False
            port.write(failure) #failure we didn't read the die
