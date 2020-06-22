import time 
import serial

ser=serial.Serial('/dev/ttyACM0',250000)
while 1:
	x=ser.read()
	print x
