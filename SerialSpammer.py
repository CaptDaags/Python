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
#
# Version 1.00
#
# NOTES:
#  - Probably do not need the \r\n when sending to the radio itself.
#  - Need to add current GMT so that its not timed out in APRS.FI or anywhere else
#    if you used a dummy time.
#
# NMEA - GLL String Format Example
# GLL - Geographic Latitude and Longitude is a holdover from Loran data and some old units may not send the time and data active information if they are emulating Loran data. If a gps is emulating Loran data they may use the LC Loran prefix instead of GP.
#
#  $GPGLL,3756.50,S,14500.06,E,225444,A,*1D
#
# Where:
#     GLL          Geographic position, Latitude and Longitude
#     4916.46,N    Latitude 49 deg. 16.45 min. North
#     12311.12,W   Longitude 123 deg. 11.12 min. West
#     225444       Fix taken at 22:54:44 UTC
#     A            Data Active or V (void)
#     *iD          checksum data

import serial
import time
from datetime import datetime
while True:
	ser = serial.Serial('COM4')
	print(ser.portstr)
	ser.baudrate = 9600
	UTC = datetime.utcnow().strftime("%H%M%S")
	print (UTC)
	GLL = ("$GPGLL,3756.50,S,14500.06,E,%s,A,*1D\r\n") % UTC
	ser.write(bytes(GLL,'utf-8'))
	ser.close()
	time.sleep(10)
	
# --EOF--