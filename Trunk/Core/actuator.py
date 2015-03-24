#!/usr/bin/python

from Lib.IO_Ana import set_output_ana
from Lib.IO_Num import set_output_num
from Lib.IO_Num import set_output_direction

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
	def __init__(self, hardwareId, channel, initValue):
		"""
		Actuator class
		
		hardwareId: Id to hardware equipment
		channel: Physical position actuator on Expender PI
		initValue: Inital value to actuator
		"""
		self.hardwareId = hardwareId
		self.channel = channel
		self.initValue = initValue
	
class AnalogActuator(Actuator):
	"""
	Mother class analog actuator
	Inherit to Actuator class
	"""
	
	# Builder class
	def __init__(self, hardwareId, channel, voltage, initValue):
		"""
		Analog actuator class
		
		hardwareId: Unique Id to hardware
		channel: Physical position actuator on Expander PI
		voltage: Type of value
		initValue: Inital value to actuator
		"""
		Actuator.__init__(self, hardwareId, channel, initValue)
		self.voltage = voltage
		
		self.set_value(self.initValue)	# Initialize actuator
		
	# Destructor class
	def __del__(self):
		self.set_value(self.initValue)	# Initialize actuator
	
	# Set value activator
	def set_value(self, value):
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
	def __init__(self, hardwareId, pin, initValue):
		"""
		Numeric actuator class
		
		hardwareId: Unique Id to hardware
		pin: Physical position actuator on Expender PI
		"""
		Actuator.__init__(self, hardwareId, pin, initValue)
		self._lock = False
		self.state = ''
		
		set_output_direction(self.channel)		# Set pin to output
		
		self.set_value(self.initValue)	# Initialize actuator
	
	# Destructor class
	def __del__(self):
		print("Delete class ID: {} -- initValue: {}".format(self.hardwareId, self.initValue))
		self.set_value(self.initValue)	# Initialize actuator
	
	# Set value activator to on and lock
	def set_on(self):
		"""
		Lock authorization change value actuator and Set True the actuator
		"""
		self._lock = True
		value = True
		if self.state <> value:
			set_output_num(self.channel, not value)  #active low relay
			self.state = value
	
	# Set value activator to off and lock
	def set_off(self):
		"""
		Lock authorization change value actuator and Set False the actuator
		"""
		self._lock = True
		value = False
		if self.state <> value:
			set_output_num(self.channel, not value)  #active low relay
			self.state = value
		
	# Reset lock
	def set_mode_auto(self):
		"""
		Unlock authorization change value actuator for automatic mode
		"""
		self._lock = False
		
	# Set value activator
	def set_value(self, value):
		if (self.state <> value) and not self._lock:
			set_output_num(self.channel, not value)  #active low relay
			self.state = value
		
	# Get value actuator
	def get_value(self):
		return self.state

		
class Pump(NumericActuator):
	"""
	Class for pump actuator
	Inherit to NumericActuator class
	"""
	
	# Builder class
	def __init__(self, hardwareId, pin, initValue=False): 
		"""
		Pump actuator class
		
		hardwareId: Unique Id to hardware
		pin: Physical position actuator on Expender PI
		initValue: Inital value to actuator
		"""
		NumericActuator.__init__(self, hardwareId, pin, initValue)	
	
class Light(NumericActuator):
	"""
	Class for Light actuator
	Inherit to NumericActuator class
	"""
	
	# Builder class
	def __init__(self, hardwareId, pin, initValue=False): 
		"""
		Light actuator class
		
		hardwareId: Unique Id to hardware
		pin: Physical position actuator on Expender PI
		initValue: Inital value to actuator
		"""
		NumericActuator.__init__(self, hardwareId, pin, initValue)	
		
class Heater(NumericActuator):
	"""
	Class for heater actuator
	Inherit to NumericActuator class
	"""
	
	# Builder class
	def __init__(self, hardwareId, pin, initValue=False):
		"""
		Heater actuator class
		
		hardwareId: Unique Id to hardware
		pin: Physical position actuator on Expender PI
		initValue: Inital value to actuator	
		"""
		NumericActuator.__init__(self, hardwareId, pin, initValue)
		
class peristalticPump(NumericActuator):
	"""
	Class for peristaltic pump actuator
	Inherit to NumericActuator class
	"""
	
	# Builder class
	def __init__(self, hardwareId, pin, initValue=False): 
		"""
		Peristaltic pump actuator class
		
		hardwareId: Unique Id to hardware
		pin: Physical position actuator on Expender PI
		initValue: Inital value to actuator
		"""
		NumericActuator.__init__(self, hardwareId, pin, initValue)

# Template class
class NewAnalogActuator(AnalogActuator):
	"""
	Class description
	Inherit to AnalogActuator class
	"""
	
	# Builder class
	def __init__(self, hardwareId, channel, voltage, initValue=0.0):
		"""
		Analog actuator description
		
		hardwareId: Unique Id to hardware
		channel: Physical position actuator on Expander PI
		voltage: Type of value
		initValue: Inital value to actuator
		"""
		AnalogActuator.__init__(self, hardwareId, channel, voltage, initValue)
		
class NewNumericActuator(NumericActuator):
	"""
	Class description
	Inherit to NumericActuator class
	"""
	
	# Builder class
	def __init__(self, hardwareId, pin, initValue=False): 
		"""
		Digital actuator description
		
		hardwareId: Unique Id to hardware
		pin: Physical position actuator on Expender PI
		initValue: Inital value to actuator
		"""
		NumericActuator.__init__(self, hardwareId, pin, initValue)
		
