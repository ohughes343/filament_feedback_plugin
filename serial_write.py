import serial 
import time

ser=serial.Serial('/dev/ttyACM0', 250000)

time.sleep(2)
ser.write("G0 X10\r\n")
time.sleep(1)
ser.close()
