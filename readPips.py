import cv2
import numpy as np
import os
import RPi.GPIO as GPIO

print cv2.__version__

GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(40, GPIO.OUT)


a = 29
b = 31
c = 33
d = 35
e = 37
f = 38
g = 40

    
    
while True:
    state = GPIO.input(32)
    
    if state:
        GPIO.output(36,1)
        os.system("fswebcam -S 150 -r 800x600 --fps 12 --no-banner testimage.jpg")
        GPIO.output(36,0)
        img = cv2.imread('testimage.jpg',0)
        img = cv2.resize(img, (1280, 960))
        img = cv2.medianBlur(img,5)
        cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

        circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,50,
                                    param1=50,param2=30,minRadius=15,maxRadius=35)


        circles = np.uint16(np.around(circles))

        an=circles[0][0][0] + 140
        bn=circles[0][0][0] - 140
        cn=circles[0][0][1] + 140
        dn=circles[0][0][1] - 140

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

        state = False
        break
