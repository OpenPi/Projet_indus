#!/usr/bin/python

from Lib.IO_Ana import set_output_ana
from Lib.IO_Num import set_output_num
from Lib.IO_Num import set_output_direction
from Lib.IO_Num import set_pullUp

"""
================================================
Actuator class

Version 1.0 Created 23/02/2015

================================================
"""

class Actuator:
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
	def __init__(self, hardwareId, channel, voltage):
		"""
		Analog actuator class
		
		hardwareId: Unique Id to hardware
		channel: Physical position actuator on Expander PI
		voltage: Type of value
		"""
		Actuator.__init__(self, hardwareId, channel)
		self.voltage = voltage
	
	# Set value activator
	def set_value_activator(self, value):
		"""
		Set value to analog actuator		
		"""
		set_output_ana(self.channel, value, self.voltage)
	
class NumericActuator(Actuator):
	"""
	Mother class numeric actuator
	Inherit to Actuator class
	"""
	
	# Builder class
	def __init__(self, hardwareId, pin, pullup):
		"""
		Numeric actuator class
		
		hardwareId: Unique Id to hardware
		pin: Physical position actuator on Expender PI
		"""
		Actuator.__init__(self, hardwareId, pin)
		self._lock = False
		self.pullup = pullup
		
		set_output_direction(self.channel)		# Set pin to output
		set_pullUp(self.channel, self.pullup)	# Set pull type
	
	# Set value activator to on and lock
	def set_on(self):
		"""
		Lock authorization change value actuator and Set True the actuator
		"""
		self._lock = True
		value = True
		set_output_num(self.channel, not value)  #active low relay
	
	# Set value activator to off and lock
	def set_off(self):
		"""
		Lock authorization change value actuator and Set False the actuator
		"""
		self._lock = True
		value = False
		set_output_num(self.channel, not value)  #active low relay
		
	# Reset lock
	def set_mode_auto(self):
		"""
		Unlock authorization change value actuator for automatic mode
		"""
		self._lock = False
		
	# Set value activator
	def set_value(self, value):
		if not self._lock:
			set_output_num(self.channel, not value)  #active low relay
		

		
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