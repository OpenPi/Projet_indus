from ABE.ABE_ExpanderPi import RTC
from ABE.ABE_helpers import ABEHelpers
from datetime import datetime
import urllib2 as url

def initRtc():
	req = url.Request('http://www.google.com')
	try:
		url.urlopen(req)
	except IOError:
		print("ERROR: Connection impossible. Initialization time impossible")
		return -1

	t = datetime.now()

	rtcDate = str(t.year)+"-"+str(t.month)+"-"+str(t.day)+"T"+str(t.hour)+":"+str(t.minute)+":"+str(t.second)

	rtc.set_date(rtcDate)

def getDate():
	return rtc.read_date()

def getTime():
	j = 0
	t = str(getDate())
	for i in t:
		j += 1
		if i == 'T':
			n=0
			time=''
			while n<5:
				time = time+t[j+n]
				n += 1
			return time

def reguleTime():
	t = datetime.now()
	osTime = str(t.hour)+":"+str(t.minute)
	rtcTime = getTime()

	if osTime <> rtcTime:
		initRtc()

i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()
rtc = RTC(bus)
