# Test the regex and checksum builder for the NMEA spammer project
# Most of this goodness came from http://doschman.blogspot.com.au/2013/01/calculating-nmea-sentence-checksums.html

# Import the regeular expression (re) device that is used to strip $ * and CR LF:
import re
# This is the string that we'll be testing:
sentence = "$GPGLL,3756.50,S,14500.06,E,221155,A,*1D\r\n"
# Take a peak at it in all its glory:
print (sentence)
#chsum = sentence[le0n(sentence) - 2:]
#print ("chsum=", chsum)


# - Regex Out The Nasty Stuff We Dont Want
chksumdata = re.sub("(\n|\r\n)","", sentence[sentence.find("$")+1:sentence.find("*")])
print ("chksumdata=", chksumdata)

# Initialise the first XOR value
csum = 0

# XOR'ing value of csum against the next char in line
# and storing the new XOR value in csum
for c in chksumdata:
	csum ^= ord(c)

# Print stuff. The correct checksum for this example is 1F
print ("Checksum", csum)
calccsum = hex(csum)
print ("calccsum=", calccsum)
