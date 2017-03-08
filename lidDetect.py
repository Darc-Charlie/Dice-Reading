import cv2
import os
import numpy as np
import serial

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
  
except AttributeError:
    print "No cirles detected"
        
