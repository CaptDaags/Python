# Serial NMEA Spammer 4
# This sends the string defined in ser.write to the 
# serial port defined in the ser=serial.Serial
# over and over ever time.sleep seconds until ctrl + x is hit
#
# This is the basis of a little app to send a GGA NMEA string to a serial
# port emulating a GPS receiver. This is going to be used to send a 
# dummy GPS location to a Icom 880H as you can't define a static 
# lat/long in that radio to send in the absence of a GPS.
#
# Prereqs: pyserial (pip install pyserial)
#
# Version 1.30
#
# NOTES:
#  - Probably do not need the \r\n when sending to the radio itself.
#  - Need to add current GMT so that its not timed out in APRS.FI or anywhere else
#    if you used a dummy time.
#  - The USB to RS232 sits on COM4
#  - The Icom data cable sits on COM3
#
# NMEA - GLL String Format Example
# GLL - Geographic Latitude and Longitude is a holdover from Loran data and some old units may 
# not send the time and data active information if they are emulating Loran data. 
# If a gps is emulating Loran data they may use the LC Loran prefix instead of GP.
#
#  $GPGLL,4916.46,N,12311.12,W,225444,A,*1D
#
# Where:
#     GLL          Geographic position, Latitude and Longitude
#     4916.46,N    Latitude 49 deg. 16.45 min. North
#     12311.12,W   Longitude 123 deg. 11.12 min. West
#     225444       Fix taken at 22:54:44 UTC
#     A            Data Active or V (void)
#     *iD          checksum data
#
#
# Learnings
#	- Icom ID-880H DOES check for the checksum, if not correct GPS indicator flashes but
#	still uploads the position to APRS.Fi Flashing indicator means GPS data but not a valid fix.
#	- To get the altitude, need the GGA, RMC and the sat sentences GSA and GSV. Go figure.
#	- Dont need the second wait between individual sentences, just blast it out.
#	- The ID-880H sets the data port to 9600 by default. Need to go in menu
#	SET>FUNC>SPEED to set to 4800 if you want 4800.
#	- Need to work out how to pass UTC and DDATE into the same string.
#	- The alpha chars in the checksum need to be uppercase.

import serial
import time
import re
from datetime import datetime

while True:
	#
	# INITIALISE THE SERIAL PORT
	#
	ser = serial.Serial('COM3')
	# Send the port to the console for the monkey to see
	print("Sending To COM Port", ser.portstr)
	ser.baudrate = 4800
	
	#
	# GENERATE THE UTC TIME STAMP
	#

	UTC = datetime.utcnow().strftime("%H%M%S")
	
	#
	# GENERATE A CLEAN GGA STRING WITH CURRENT UTC
	#

	# Generate a clean GGA string with no $ or * chars that are not included in the
	# checksum calculation. Note this is the old format, probably need to convert
	# to the new {} format usage at some point.
	# Also note that the 14.6 is the alt and you may want to change
	GGA = ("GPGGA,%s,3756.53,S,14500.06,E,1,13,0.9,14.6,M,40.1,M,,") %UTC

	#
	# CALCULATE THE CHECKSUM
	#

	# Write the clean GGA to a variable for calculation purposes
	chksumdata = GGA
	
	# Initialise the first XOR value
	csum = 0

	# XOR'ing value of csum against the next char in line
	# and storing the new XOR value in csum
	for c in chksumdata:
		csum ^= ord(c)
			
	# This is the calculated checksum
	calccsum = hex(csum)
	
	#
	# CHECKSUM FORMAT MANIPULATION
	#

	# Get the last two characters of the checksum dropping the 0x
	calccsum = calccsum[-2:]
	# Now convert any chars in the checksum to upper as needed by the ID-880H
	calccsum = calccsum.upper()
	
	# Now put the string to be transmitted together with the calculated checksum
	GPGGA = ("$") + GGA + ("*") + calccsum + ("\r\n")
	
	# Drop the string to be transmitted to the console for the monkey to see
	print ("GPGAA=", GPGGA)

	#
	# SERIAL TRANSMISSION
	#

	# Now write the formated NMEA string out to the serial port
	ser.write(bytes(GPGGA,'utf-8'))

	# Close the port and have a little sleep before doing it all again
	ser.close()
	time.sleep(1)
	
# --EOF--