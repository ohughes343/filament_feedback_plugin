import cv2
import numpy as np 
from picamera.array import PiRGBArray
from picamera import PiCamera 

def nothing(x):
    pass
 
cv2.namedWindow("Trackbars")
 
cv2.createTrackbar("B", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("G", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("R", "Trackbars", 0, 255, nothing)

camera = PiCamera()
camera.resolution = (1280, 960)
#camera.resolution = (128, 96)
camera.framerate = 10

rawCapture = PiRGBArray(camera, size=(1280, 960))

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    B = cv2.getTrackbarPos("B", "Trackbars")
    G = cv2.getTrackbarPos("G", "Trackbars")
    R = cv2.getTrackbarPos("R", "Trackbars")

    green = np.uint8([[[B, G, R]]])
    hsvGreen = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
    
    #BGR limits
    boundary = [(0, 10, 11), (100, 240, 255)] #*this requires a clean white background
    lower = boundary[0]
    upper = boundary[1]
    #lowerLimit = np.uint8([hsvGreen[0][0][0]-10,100,100])
    lowerLimit = np.uint8(0)
    #upperLimit = np.uint8([hsvGreen[0][0][0]+10,255,255])
    upperLimit = np.uint8(255)

    mask = cv2.inRange(hsv, lower, upper)

    result = cv2.bitwise_and(image  , image , mask=mask)

    cv2.imshow("frame", image)
    cv2.imshow("mask", mask)
    cv2.imshow("result", result)

    key = cv2.waitKey(1)
    rawCapture.truncate(0)
    if key == 27:
        break

cv2.destroyAllWindows()