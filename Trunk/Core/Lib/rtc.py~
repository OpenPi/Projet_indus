from ABE.ABE_ExpanderPi import RTC
from ABE.ABE_helpers import ABEHelpers
from datetime import datetime
import urllib2 as url
import os
"""
================================================
RTC (Real Time Clock) management

Version 1.0 Created 12/03/2015

================================================
"""

def initRtc():
	"""
	After test Return OS clock
	"""
	req = url.Request('http://www.google.com')		# Create request of connection
	print(rtc.read_date())
	# Control state connection
	try:
		url.urlopen(req)
	except IOError:
		print("ERROR: Connection impossible. Initialization time impossible")

		date = rtc.read_date()
	 	dateHour = date.split('T', 1 )
		YearMonthDay = dateHour[0].split('-',2) 
		HourMinuteSecond = dateHour[1].split(':',2) 
  		os.system("sudo date "+YearMonthDay[1]+YearMonthDay[2]+HourMinuteSecond[0]+HourMinuteSecond[1]+YearMonthDay[0]+"."+HourMinuteSecond[2]) #Change OS hour

		

def reguleTime():
	"""
	Control if clock expander Pi value is correct
	"""
	t = datetime.now()
	rtcDate = str(t.year)+"-"+str(t.month)+"-"+str(t.day)+"T"+str(t.hour)+":"+str(t.minute)+":"+str(t.second)
	if rtcDate <> rtc.read_date():
		
	
		# Convert OS clock format to rtc Expander Pi format
		

		rtc.set_date(rtcDate)	# Save initialization clock"""


# Instantiate Expander Pi time
i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()
rtc = RTC(bus)




