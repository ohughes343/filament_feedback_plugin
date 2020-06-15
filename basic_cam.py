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

#remove out.txt if it exists
if os.path.exists('out.txt'):
    os.remove('out.txt')

   
#file to write diameter values to
f=open('out.txt','w')

#initialize camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size = (640,480))

#array of previous values for data smoothing
previous_width=[]
for p in range(0,100):
    previous_width.append(110)

#main loop
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image=frame.array
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    
    
    boundary = [(0, 10, 10), (80, 240, 255)] #*this requires a clean white background
    lower = boundary[0]
    upper = boundary[1]

    mask = cv2.inRange(hsv,lower, upper)

    result = cv2.bitwise_and(image,image,mask=mask)
    
    
    #width of current frame
    width = []
   
    rows,cols,_ = result.shape
    
    array=[]
    
    
    #points defining the rectangle to be scanned
    pt1=(int((cols/5)),int(239*(rows/480)))
    pt2=(int(4*(cols/5)),int(241*(rows/480)))
    
    #give width array enough elements for all the rows
    for r in range(pt2[0]-pt1[0]):
        array.append(0)
    
    
        
    for i in range(pt1[1],pt2[1],1):
        #array.append(0)
        for j in range(pt1[0],pt2[0],1):
            k = result[i,j]
            if k.all()!=0: array[i]+=1
    
    
            
    filament_width_px = int(100*round((sum(array) / len(array)),2))
    #width=(filament_width_px + previous_width)/2
    #previous_width=filament_width_px
    
    #shift values in array left and add newest value
    for p in range(0,len(previous_width)-1):
        previous_width[p] = previous_width[p+1]
        
    previous_width[9]=filament_width_px
    width = sum(previous_width) / len(previous_width)
    
    #output diameter to file
    with open('out.txt','a') as f:
        print(str(width), file=f)
    
    
    #write the filament diameter on the image
    cv2.putText(image, str(width), (100,100), font, 1, (255,255,255), 2, cv2.LINE_AA)
    
    #draw rectangle around scanned area
    cv2.rectangle(image,pt1,pt2,(255,0,0),1)
    
    #draw frame
    cv2.imshow("frame", image)
    
    #print(array)
    #print(filament_width_px)
    
    
    key = cv2.waitKey(1)
    rawCapture.truncate(0)
    if key==27:
        break


cv2.destroyAllWindows()



