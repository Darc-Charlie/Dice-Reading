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

def a(x):
    GPIO.output(29,x)
def b(x):
    GPIO.output(31,x)
def c(x):
    GPIO.output(33,x)
def d(x):
    GPIO.output(35,x)
def e(x):
    GPIO.output(37,x)
def f(x):
    GPIO.output(38,x)
def g(x):
    GPIO.output(40,x)
    
    
while True:
    state = GPIO.input(32)
    
    if state:
        GPIO.output(36,1)
        os.system("fswebcam -S 120 -r 800x600 --no-banner testimage.jpg")
        GPIO.output(36,0)
        img = cv2.imread('testimage.jpg',0)
        img = cv2.resize(img, (1280, 960))
        img = cv2.medianBlur(img,5)
        cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

        circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,50,
                                    param1=50,param2=30,minRadius=15,maxRadius=35)


        circles = np.uint16(np.around(circles))

        a=circles[0][0][0] + 140
        b=circles[0][0][0] - 140
        c=circles[0][0][1] + 140
        d=circles[0][0][1] - 140

        for i in circles[0,:]:
            if i[0] >= b and i[0] <= a and i[1] >= d and i[1] <= c :
                continue
            else:
                i[0] = 0
                i[1] = 0
                i[2] = 0
        count = 0
        for j in circles[0,:]:
            if j[0] != 0:
                count += 1

        if count is 1:
            a(1)
            b(0)
            c(0)
            d(1)
            e(1)
            f(1)
            g(1)

        elif count is 2:
            a(0)
            b(0)
            c(1)
            d(0)
            e(0)
            f(1)
            g(0)

        elif count is 3:
            a(0)
            b(0)
            c(0)
            d(0)
            e(1)
            f(1)
            g(0)

        elif count is 4:
            a(1)
            b(0)
            c(0)
            d(1)
            e(1)
            f(0)
            g(0)

        elif count is 5:
            a(0)
            b(1)
            c(0)
            d(0)
            e(1)
            f(0)
            g(0)

        elif count is 6:
            a(1)
            b(1)
            c(0)
            d(0)
            e(0)
            f(0)
            g(0)

        else:
            a(0)
            b(0)
            c(0)
            d(0)
            e(0)
            f(0)
            g(1)

        state = False
        break
