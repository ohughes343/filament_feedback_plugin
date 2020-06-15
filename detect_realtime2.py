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
GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)   # Set pin 8 to be an output pin and set initial value to low (off)

font = cv2.FONT_HERSHEY_SIMPLEX

#constants
mm_to_px_ratio = .0125

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

GPIO.output(8, GPIO.HIGH) # Turn on laser

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
    
    #5-value array to make running average
    x=[0,0,0,0,0]
    
    
    for i in range(pt1[1],pt2[1],1):
        #width.append(0)
        for j in range(pt1[0],pt2[0],1):
            k = result[i,j]
        if k.all() != 0:width[i]+=1
                
    filament_width_px = sum(width) / len(width)
    filament_width_mm = filament_width_px * mm_to_px_ratio
    try:
        percentage =   1.75**2 / filament_width_mm**2
    except ZeroDivisionError:
        percentage = 0
    
    #print ("Image width = " + str(image.shape[1]) + "px")
    #print ("Image height = " + str(image.shape[0]) + "px")
    #print ("Average filament width = " + str(filament_width_px) + "px")
    #print ("Average filament width = " + str(filament_width_mm) + "mm")
    #print ("gcode command: M221 S" + str(round(percentage,4)))
    
    #output diameter to file
    with open('out.txt','a') as f:
        print(str(filament_width_px), file=f)

    #write the filament diameter on the image
    cv2.putText(image, str(filament_width_px), (100,100), font, 1, (255,255,255), 2, cv2.LINE_AA)
    
    #draw rectangle around scanned area
    cv2.rectangle(image,pt1,pt2,(255,0,0),1)
                  
    #original
    cv2.imshow("frame", image)
    
    #black and white
    #cv2.imshow("mask", mask)
    
    #color
    #cv2.imshow("result", result)

    key = cv2.waitKey(1)
    rawCapture.truncate(0)
    if key==27:
        break

cv2.destroyAllWindows()


