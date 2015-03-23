from ABE.ABE_ExpanderPi import RTC
from ABE.ABE_helpers import ABEHelpers
from datetime import datetime
import urllib2 as url

"""
================================================
RTC (Real Time Clock) management

Version 1.0 Created 12/03/2015

================================================
"""

def _getOSDate():
	"""
	After test Return OS clock
	"""
	req = url.Request('http://www.google.com')		# Create request of connection
	
	# Control state connection
	try:
		url.urlopen(req)
	except IOError:
		print("ERROR: Connection impossible. Initialization time impossible")
		return -1
	else:
		return datetime.now()		# Return OS clock

def _initRtc():
	"""
	Intialization clock to RTC Expander Pi
	"""
	t = _getOSDate()
	# Test if error _getOSDate()
	if t = -1:
		return -1
	
	# Convert OS clock format to rtc Expander Pi format
	rtcDate = str(t.year)+"-"+str(t.month)+"-"+str(t.day)+"T"+str(t.hour)+":"+str(t.minute)+":"+str(t.second)

	rtc.set_date(rtcDate)	# Save initialization clock
	
	
# Public function

def getDate():
	"""
	Return date and time to RTC Expander Pi
	"""
	return rtc.read_date()	# Return date and time

def getTime():
	"""
	Return time to RTC Expander Pi
	"""
	j = 0
	t = str(getDate())	# Save date and time
	# Loop to scan date/Time 
	for i in t:
		j += 1	# Save loop's position
		if i == 'T':	# In str t, the date and time is separate by 'T'
			n=0
			time=''
			while n<5:
				time = time+t[j+n]
				n += 1
			return time	# Return time

def reguleTime():
	"""
	Control if clock expander Pi value is correct
	"""
	t = _getOSDate()
	# Test if error _getOSDate())
	if t = -1:
		return -1
		
	osTime = str(t.hour)+":"+str(t.minute)	# Get and convert OS time
	rtcTime = getTime()						# Get Expander Pi time

	# Control if OS time == Expander Pi time
	if osTime <> rtcTime:
		_initRtc()		# Initialize Expander Pi Time

# Instantiate Expander Pi time
i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()
rtc = RTC(bus)