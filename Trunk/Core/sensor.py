#!/usr/bin/python

from Lib.IO_Ana import get_input_ana
from Lib.IO_Ana import set_refVolt_adc
from Lib.IO_Num import get_input_num
from Lib.IO_Num import set_pullUp
from Lib.IO_Num import set_input_direction

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
	def __init__(self, hardwareId, channel):
		"""
		Sensor class
		
		hardwareId: Id to hardware equipment
		channel: Physical position sensor on Expender PI
		"""
		self.hardwareId = hardwareId
		self.channel = channel
	
class AnalogSensor(Sensor):
	"""
	Mother class analog sensors
	Inherit to Sensor class
	"""
	
	# Builder class
	def __init__(self, hardwareId, channel, refVolt):
		"""
		Analog sensor class
		
		hardwareId: Unique Id to hardware
		channel: Physical position sensor on Expender PI
		refVolt: Reference voltage of Expender PI
		"""
		# Exchange channel position by pair
		channelChanged = channel%2
		if channelChanged == 0:
			channelChanged = channelChanged+channel-1
		else:
			channelChanged = channelChanged+channel
		
		Sensor.__init__(self, hardwareId, channelChanged)
		self.refVolt = refVolt
		
		set_refVolt_adc(self.refVolt)	# Call set value reference voltage
		
	# Get and return physical value of analog sensor 
	def get_value_sensor(self):
		"""
		Return value to analog sensor		
		"""
		valueSensor = get_input_ana(self.channel)	# get_input_ana return -1 if ERROR
		
		return valueSensor
	
class NumericSensor(Sensor):
	"""
	Mother class numeric sensors
	Inherit to Sensor class
	"""
	
	# Builder class
	def __init__(self, hardwareId, pin, pullup):
		"""
		Numeric sensor class
		
		hardwareId: Unique Id to hardware
		pin: Physical position sensor on Expender PI
		"""
		Sensor.__init__(self, hardwareId, pin)
		self.pullup = pullup
		
		set_input_direction(self.channel)		# Set pin to input
		set_pullUp(self.channel, self.pullup)	# Set pull type
	
	# Get and return physical value of numeric sensor
	def get_value_sensor(self):
		"""
		Return value to digital sensor		
		"""
		valueSensor = get_input_num(self.channel)	# get_input_num return -1 if ERROR
		
		return valueSensor		
	

	
class Thermocouple(AnalogSensor):
	"""
	Class for thermocouple sensor
	Inherit to AnalogSensor class
	"""
	
	# Builder class
	def __init__(self, hardwareId, channel, refVolt):
		"""
		Thermocouple sensor class
		
		hardwareId: Unique Id to hardware
		channel: Physical position sensor on Expender PI
		refVolt: Reference voltage of Expender PI
		"""
		AnalogSensor.__init__(self, hardwareId, channel, refVolt)
	
	# convert physical value to temperature value
	def conversion(self, voltValue):
		"""
		Convert physical value to temperature value

		voltValue: Value to convert
		
		Return Temperature value
		"""
		
		# c0 = 0
		# c1 = 25.08355
		# c2 = 0.07860106
		# c3 = -0.2503131
		# c4 = 0.08315270
		# c5 = -1.228034E-02
		# c6 = 9.804036E-04
		# c7 = -4.413030E-05
		# c8 = 1.057734E-06
		# c9 = -1.052755E-08

		# x =voltValue

		# temp = c0+(x*(c1+(x*(c2+(x*(c3+(x*(c4+(x*(c5+(x*(c6+(x*(c7+(x*(c8+(x*c9)))))))))))))))))
		
		temp = (voltValue - 1.25)/0.005
		
		return float(temp)		
	
	# Return temperature
	def get_value(self):
		"""
		Return temperature value
		"""
		
		voltValue = self.get_value_sensor()
		
		# If get_value_sensor work return Temperature else Error
		if voltValue == -1:
			print("ERROR: get value thermocouple sensor\n")
			return -1
		else:
			return self.conversion(voltValue)
			
class PhMeter(AnalogSensor):
	"""
	Class for ph sensor
	Inherit to AnalogSensor class
	"""
	
	# Builder class
	def __init__(self, hardwareId, channel, refVolt):
		"""
		Ph meter class
		
		hardwareId: Unique Id to hardware
		channel: Physical position sensor on Expender PI
		refVolt: Reference voltage of Expender PI
		"""
		AnalogSensor.__init__(self, hardwareId, channel, refVolt)
	
	# convert physical value to ph value
	def conversion(self, value):
		"""
		Convert physical value to ph value

		value: Value to convert
		
		Return ph value
		"""
		phValue = value*5.0/1024/6
		return phValue

	# Return ph
	def get_value(self):
		"""
		Return ph value
		"""
	
		voltValue = self.get_value_sensor()
		
		# If get_value_sensor work return ph else Error
		if voltValue == -1:
			print("ERROR: get value ph sensor\n")
			return -1
		else:
			return self.conversion(voltValue)
			
class AmpereMeter(AnalogSensor):
	"""
	Class for ampere sensor
	Inherit to AnalogSensor class
	"""
	
	# Builder class
	def __init__(self, hardwareId, channel, refVolt):
		"""
		Ampere meter class
		
		hardwareId: Unique Id to hardware
		channel: Physical position sensor on Expender PI
		refVolt: Reference voltage of Expender PI
		"""
		AnalogSensor.__init__(self, hardwareId, channel, refVolt)
	
	# convert physical value to ampere value
	def conversion(self, value):
		"""
		Convert physical value to ampere value

		value: Value to convert
		
		Return current value
		"""
		
		ampereValue = value*30
		return ampereValue

	# Return ampere
	def get_value(self):
		"""
		Return current value
		"""
		
		voltValue = self.get_value_sensor()
		
		# If get_value_sensor work return current else Error
		if voltValue == -1:
			print("ERROR: get value ph sensor\n")
			return -1
		else:
			return self.conversion(voltValue)