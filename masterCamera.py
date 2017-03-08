import cv2
import numpy as np
import os
import serial
import RPi.GPIO as GPIO
import time

print cv2.__version__

GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.IN, GPIO.PUD_DOWN)

GPIO.setup(11, GPIO.OUT) #undefined / ready pin
GPIO.setup(13, GPIO.OUT) #success pin
GPIO.setup(15, GPIO.OUT) #failure pin

GPIO.setup(29, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(40, GPIO.OUT)

while True:
    lidState = GPIO.input(32)

    if lidState:

        try:

	    print "reading lid..."
            port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=5.0)
            os.system("fswebcam -S 150 -r 800x600 --no-banner testimage.jpg")
            img = cv2.imread('testimage.jpg', 0)
            img = cv2.resize(img, (1280, 960))
            height, width = img.shape
            print width, height

            xCntr = width/2
            yCntr = height/2

            #445 = actual pixel radius
            img = cv2.medianBlur(img, 5)
            cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

            circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT, 1,50,
                                        param1=50, param2=30, minRadius=400, maxRadius=450)


            circles = np.uint16(np.around(circles))

            closerCirc = 1000
            closerCircRadius = 0
            print circles   
            for j in circles[0,:]:
                if abs(j[2] - 445) < closerCirc :
                    closerCirc = abs(j[2] - 445)
                    closerCircRadius = j[2]
            for k in circles[0,:]:
                if k[2] == closerCircRadius:
                    continue
                else:
                    k[0] = 0
                    k[1] = 0
                    k[2] = 0

            print circles
            for l in circles[0,:]:
                if l[0] != 0:
                    x_dist = l[0] - xCntr
                    y_dist = l[1] - yCntr

            print "x-Dist:", x_dist
            print "y-Dist:", y_dist

            port.write(str(int(x_dist)))
            port.write(str(int(y_dist)))

            for j in circles[0,:]:
                if j[0] != 0:
                    if j[0]-xCntr < 0:
                        print 'left'
                    else:
                        print 'right'
                    if j[1]-yCntr < 0:
                        print 'up'
                    else:
                        print 'down'

            GPIO.output(13,1) #success
            time.sleep(3)
            GPIO.output(13,0)
            break

        except AttributeError:
            print "No cirles detected"
            lidstate = False
            GPIO.output(15,1)   #failure
            time.sleep(6)
            GPIO.output(15,0)


a = 29
b = 31
c = 33
d = 35
e = 37
f = 38
g = 40


while True:
    diestate = GPIO.input(32)

    if diestate:

        try:
	    print "reading die..."
            os.system("fswebcam -S 150 -r 800x600 --no-banner testimage.jpg")
            img = cv2.imread('testimage.jpg',0)
            img = cv2.resize(img, (1280, 960))
            img = cv2.medianBlur(img,5)
            cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

            circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,10,
                                        param1=50,param2=30,minRadius=15,maxRadius=20)


            circles = np.uint16(np.around(circles))

            an=circles[0][0][0] + 140
            bn=circles[0][0][0] - 140
            cn=circles[0][0][1] + 140
            dn=circles[0][0][1] - 140

	    print circles
            for i in circles[0,:]:
                if i[0] >= bn and i[0] <= an and i[1] >= dn and i[1] <= cn :
                    continue
                else:
                    i[0] = 0
                    i[1] = 0
                    i[2] = 0
            count = 0
            for j in circles[0,:]:
                if j[0] != 0:
                    count += 1

	    print circles
	    print count, "pips"	
            if count == 1:
                GPIO.output(a,1)
                GPIO.output(b,0)
                GPIO.output(c,0)
                GPIO.output(d,1)
                GPIO.output(e,1)
                GPIO.output(f,1)
                GPIO.output(g,1)

            elif count == 2:
                GPIO.output(a,0)
                GPIO.output(b,0)
                GPIO.output(c,1)
                GPIO.output(d,0)
                GPIO.output(e,0)
                GPIO.output(f,1)
                GPIO.output(g,0)

            elif count == 3:
                GPIO.output(a,0)
                GPIO.output(b,0)
                GPIO.output(c,0)
                GPIO.output(d,0)
                GPIO.output(e,1)
                GPIO.output(f,1)
                GPIO.output(g,0)

            elif count == 4:
                GPIO.output(a,1)
                GPIO.output(b,0)
                GPIO.output(c,0)
                GPIO.output(d,1)
                GPIO.output(e,1)
                GPIO.output(f,0)
                GPIO.output(g,0)

            elif count == 5:
                GPIO.output(a,0)
                GPIO.output(b,1)
                GPIO.output(c,0)
                GPIO.output(d,0)
                GPIO.output(e,1)
                GPIO.output(f,0)
                GPIO.output(g,0)

            elif count == 6:
                GPIO.output(a,1)
                GPIO.output(b,1)
                GPIO.output(c,0)
                GPIO.output(d,0)
                GPIO.output(e,0)
                GPIO.output(f,0)
                GPIO.output(g,0)

            else:
                GPIO.output(a,0)
                GPIO.output(b,0)
                GPIO.output(c,0)
                GPIO.output(d,0)
                GPIO.output(e,0)
                GPIO.output(f,0)
                GPIO.output(g,1)

            GPIO.output(13,1) #success
            time.sleep(3)
            GPIO.output(13,0)
            break
        
        except AttributeError:
            print "No cirles detected"
            diestate = False
            GPIO.output(15,1)   #failure
            time.sleep(6)
            GPIO.output(15,0)
