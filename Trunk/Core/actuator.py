#!/usr/bin/python

from Lib.IO_Ana import set_output_ana
from Lib.IO_Num import set_output_num

"""
================================================
Actuator class

Version 1.0 Created 23/02/2015

================================================
"""

class Actuator(object):
	"""
	Mother class of actuator
	"""
	
	# Builder class
	def __init__(self, hardwareId, channel):
		"""
		Actuator class
		
		hardwareId: Id to hardware equipment
		channel: Physical position actuator on Expender PI
		"""
		self.hardwareId = hardwareId
		self.channel = channel
	
class AnalogActuator(Actuator):
	"""
	Mother class analog actuator
	Inherit to Actuator class
	"""
	
	# Builder class
	def __init__(self, hardwareId, channel, voltage=False):
		"""
		Analog actuator class
		
		channel: Physical position actuator on Expender PI
		voltage: Type of value
		"""
		Actuator.__init__(self, hardwareId, channel)
		self.voltage = voltage
	
	# Set value activator
	def set_value_activator(self, value):
		set_output_ana(self.channel, value, self.voltage)
	
class NumericActuator(Actuator):
	"""
	Mother class numeric actuator
	Inherit to Actuator class
	"""
	
	# Builder class
	def __init__(self, hardwareId, pin):
		"""
		Numeric actuator class
		
		pin: Physical position actuator on Expender PI
		"""
		Actuator.__init__(self, hardwareId, pin)
		self._override = False
		
	def getOverride(self):
		return self._override
		
	def setOverride(self, value):
		if bool == type(value):
			self._override = value
		else:
			print("ERROR: override is boolean")
		
	override = property(getOverride, setOverride)
		
	# Set value activator
	def set_value(self, value):
		if self._override:
			set_output_num(self.channel, value)
		
class Pump(NumericActuator):
	"""
	Class for pump actuator
	Inherit to NumericActuator class
	"""
	
	# Builder class
	def __init__(self, hardwareId, pin): 
		"""
		Pump actuator class
		
		pin: Physical position actuator on Expender PI
		"""
		NumericActuator.__init__(self, hardwareId, pin)	
	


class Light(NumericActuator):
	"""
	Class for Light actuator
	Inherit to NumericActuator class
	"""
	
	# Builder class
	def __init__(self, hardwareId, pin): 
		"""
		Light actuator class
		
		pin: Physical position actuator on Expander PI
		"""
		NumericActuator.__init__(self, hardwareId, pin)	
	
		
class Heater(NumericActuator):
	"""
	Class for heater actuator
	Inherit to NumericActuator class
	"""
	
	# Builder class
	def __init__(self, hardwareId, pin):
		"""
		Heater actuator class
		
		pin: Physical position actuator on Expander PI		
		"""
		NumericActuator.__init__(self, hardwareId, pin)	


class actuatorTestAnalog(AnalogActuator):

	def __init__(self, hardwareId, channel,	voltage):
		AnalogActuator.__init__(self, hardwareId, channel, voltage=False)
