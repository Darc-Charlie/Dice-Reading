
import cv2
import numpy as np
import os
import RPi.GPIO as GPIO

print cv2.__version__

GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.IN)
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
        os.system("fswebcam -S 80 --no-banner testimage.jpg")
        GPIO.output(36,0)
        img = cv2.imread("testimage.jpg")
        img = cv2.resize(img, (340, 340))

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        edge = cv2.Canny(gray, 4000, 5000, apertureSize=5)
        vis = img.copy()
        vis = np.uint8(vis/2.)
        vis[edge != 0] = (0, 255, 0)
        #cv2.imshow('edge', vis)
        #cv2.imshow('edgevar', edge)

        #invert
        ##############################
        edge_inv = cv2.bitwise_not(edge)
        ####################################

        #floodfill
        ##################################################
        # Copy the thresholded image.
        im_floodfill = edge_inv.copy()

        # Mask used to flood filling.
        # Notice the size needs to be 2 pixels than the image.
        h, w = edge_inv.shape[:2]
        mask = np.zeros((h+2, w+2), np.uint8)

        # Floodfill from point (0, 0)
        cv2.floodFill(im_floodfill, mask, (0,0), 0)
        ####################################################

        #cv2.imshow('pips', im_floodfill)
        ff2 = im_floodfill.copy()
        h2, w2 = ff2.shape[:2]
        mask2 = np.zeros((h2+2, w2+2), np.uint8)
        cv2.floodFill(ff2, mask2, (0,0), 255)
        im_floodfill_inv = cv2.bitwise_not(ff2)
        im_out = im_floodfill | im_floodfill_inv


        ##########################################################
        pyramids = cv2.distanceTransform(im_out, 2, 3)
        cv2.normalize(pyramids, pyramids, 0, 1.2, cv2.NORM_MINMAX)


        # obtain markers for the watershed algorithm by thresholding
        markers = cv2.threshold(pyramids, 0.8, 1, 0)[1] 


        # dilate the dice markers with a DICE_SIZE px element to capture all pips in the contours
        #newImg = cv2.dilate(markers, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(DICE_SIZE, DICE_SIZE)))

        # convert the numpy matrix from float [0..1] to int [0..255]
        bwImg = cv2.convertScaleAbs(markers * 255)

        # capture those contours!
        _, pyramids, hierarchy = cv2.findContours(bwImg.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        pipsNum = str(len(pyramids)) + " pips"
        ##########################################################

        print pipsNum

        '''bcd = "{0:b}".format(len(pyramids))
        misinZeros = 4 - len(bcd)    
        for x in range (misinZeros):
            bcd = '0' + bcd
        print bcd

        num = 2
        for y in range (4):
            GPIO.output(29+num, int(bcd[y]))
            num += 2 '''

        if len(pyramids) is 1:
            a(1)
            b(0)
            c(0)
            d(1)
            e(1)
            f(1)
            g(1)

        elif len(pyramids) is 2:
            a(0)
            b(0)
            c(1)
            d(0)
            e(0)
            f(1)
            g(0)

        elif len(pyramids) is 3:
            a(0)
            b(0)
            c(0)
            d(0)
            e(1)
            f(1)
            g(0)

        elif len(pyramids) is 4:
            a(1)
            b(0)
            c(0)
            d(1)
            e(1)
            f(0)
            g(0)

        elif len(pyramids) is 5:
            a(0)
            b(1)
            c(0)
            d(0)
            e(1)
            f(0)
            g(0)

        elif len(pyramids) is 6:
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
