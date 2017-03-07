import cv2
import math
import os
import numpy as np
import serial
import struct

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

try:
    circles = np.uint16(np.around(circles))
    print circles   
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

    cv2.circle(cimg,(xCntr,yCntr),2,(181,38,213),3)
    distance = round(math.sqrt((pow(circles[0][0][0] - xCntr,2)) + (pow(circles[0][0][1] - yCntr,2))))
    print distance
    port.write(str(int(distance)))

    for j in circles[0,:]:
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
        
