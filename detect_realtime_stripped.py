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

#initialize camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size = (640,480))


#main loop
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=False):
    image=frame.array
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    print(image)
    
   

    
    
    for i in range(0,1,1):
        for j in range(0,1,1):
            k = image[i,j]
   
    

    #write the filament diameter on the image
    cv2.putText(image, str(k), (100,100), font, 1, (255,255,255), 2, cv2.LINE_AA)
    
    
                  
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



