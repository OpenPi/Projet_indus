#!/usr/bin/python

from Lib.IO_Ana import get_input_ana
from Lib.IO_Num import get_input_num

"""
================================================
Sensors class

Version 1.0 Created 23/02/2015

================================================
"""

class Sensor:
	"""
	Mother class of sensors
	"""
	
	# Builder class
	def __init__(self, channel):
		"""
		Sensor class
		
		channel: Physical position sensor on Expender PI
		"""
		self.channel = channel
	
class AnalogSensor(Sensor):
	"""
	Mother class analog sensors
	Inherit to Sensor class
	"""
	
	# Builder class
	def __init__(self, channel, refVolt):
		"""
		Analog sensor class
		
		channel: Physical position sensor on Expender PI
		refVolt: Reference voltage of Expender PI
		"""
		Sensor.__init__(self, channel)
		self.refVolt = refVolt
		
	# Get and return physical value of analog sensor 
	def get_value_sensor(self):
		valueSensor = get_input_ana(self.channel, self.refVolt)
		
		return valueSensor
	
class NumericSensor(Sensor):
	"""
	Mother class numeric sensors
	Inherit to Sensor class
	"""
	
	# Builder class
	def __init__(self, pin, pullup=True):
		"""
		Numeric sensor class
		
		pin: Physical position sensor on Expender PI
		pullup: If True the logic pull is up
		"""
		Sensor.__init__(self, pin)
		self.pullup = pullup
	
	# Get and return physical value of numeric sensor
	def get_value_sensor(self):
		valueSensor = get_input_num(self.channel, self.pullup)	# get_input_ana return -1 if ERROR
		
		return valueSensor		
		
class Thermocouple(AnalogSensor):
	"""
	Class for thermocouple sensor
	Inherit to AnalogSensor class
	"""
	
	# Builder class
	def __init__(self, channel, refVolt):
		"""
		Thermocouple sensor class
		
		channel: Physical position sensor on Expender PI
		refVolt: Reference voltage of Expender PI
		"""
		AnalogSensor.__init__(self, channel, refVolt)
	
	# convert physical value to temperature value
	def conversion(self, voltValue):
		c0 = 0
		c1 = 25.08355
		c2 = 0.07860106
		c3 = -0.2503131
		c4 = 0.08315270
		c5 = -1.228034E-02
		c6 = 9.804036E-04
		c7 = -4.413030E-05
		c8 = 1.057734E-06
		c9 = -1.052755E-08

		x =voltValue

		temp = c0+(x*(c1+(x*(c2+(x*(c3+(x*(c4+(x*(c5+(x*(c6+(x*(c7+(x*(c8+(x*c9)))))))))))))))))
		return float(temp*100)		
	
	# Return temperature
	def get_value(self):
		voltValue = self.get_value_sensor()
		
		if voltValue == -1:
			print("ERROR: get value thermocouple sensor\n")
			return -1
		else:
			return self.conversion(voltValue)
			
class PhMeter(AnalogSensor):

	# Builder class
	def __init__(self, channel, refVolt):
		"""
		Ph meter class
		
		channel: Physical position sensor on Expender PI
		refVolt: Reference voltage of Expender PI
		"""
		AnalogSensor.__init__(self, channel, refVolt)
	
	# convert physical value to ph value
	def conversion(self, value):
		phValue = value*5.0/1024/6
		return phValue

	# Return ph
	def get_value(self):
		voltValue = self.get_value_sensor()
		
		if voltValue == -1:
			print("ERROR: get value ph sensor\n")
			return -1
		else:
			return self.conversion(voltValue)
			
class AmpereMeter(AnalogSensor):

	# Builder class
	def __init__(self, channel, refVolt):
		"""
		Ampere meter class
		
		channel: Physical position sensor on Expender PI
		refVolt: Reference voltage of Expender PI
		"""
		AnalogSensor.__init__(self, channel, refVolt)
	
	# convert physical value to ampere value
	def conversion(self, value):
		ampereValue = value*30
		return ampereValue

	# Return ampere
	def get_value(self):
		voltValue = self.get_value_sensor()
		
		if voltValue == -1:
			print("ERROR: get value ph sensor\n")
			return -1
		else:
			return self.conversion(voltValue)
			
class sensorTestNumeric(NumericSensor):

	def __init__(self, pin, pullup=True):
		NumericSensor.__init__(self, pin, pullup)
	
	def get_value(self):
		return self.get_value_sensor()