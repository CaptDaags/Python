# Serial Spammer
# This sends the string defined in ser.write to the 
# serial port defined in the ser=serial.Serial
# over and over ever time.sleep seconds until ctrl + x is hit
#
# This is the basis of a little app to send a NMEA string to a serial
# port emulating a GPS receiver. This is going to be used to send a 
# dummy GPS location to a Icom 880H as you can't define a static 
# lat/long in that radio to send in the absence of a GPS.
#
# Prereqs: pyserial (pip install pyserial)

import serial
import time

while True:
	ser = serial.Serial('COM4')
	print(ser.portstr)
	ser.baudrate = 9600
	ser.write(b'yyyyyyyyyyyy \r\n')
	ser.close()
	time.sleep(10)
	
# --EOF--