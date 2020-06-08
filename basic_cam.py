# import the necessary packages
import sys
import numpy as np
import argparse
import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import io
import os
import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
from time import sleep     # Import the sleep function from the time module

font = cv2.FONT_HERSHEY_SIMPLEX


#initialize camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size = (640,480))


#main loop
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image=frame.array
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    
    
    boundary = [(0, 15, 17), (40, 240, 255)] #*this requires a clean white background
    lower = boundary[0]
    upper = boundary[1]

    mask = cv2.inRange(hsv,lower, upper)

    result = cv2.bitwise_and(image,image,mask=mask)
    
    
    #width of current frame
    width = []
   
    rows,cols,_ = result.shape
    
    #give width array enough elements for all the rows
    for r in range(rows):
        width.append(0)
    
    #points defining the rectangle to be scanned
    pt1=(int(cols/5),int(230*(rows/480)))
    pt2=(int(4*(cols/5)),int(250*(rows/480)))
    
    
    
    array=[]
    for i in range(0,1,1):
        array.append(0)
        for j in range(0,1,1):
            k = result[i,j]
        if k.all()!=0: array[i]+=1
    
    cv2.imshow("frame", image)
    print(array)
    
    
    key = cv2.waitKey(1)
    rawCapture.truncate(0)
    if key==27:
        break


cv2.destroyAllWindows()



