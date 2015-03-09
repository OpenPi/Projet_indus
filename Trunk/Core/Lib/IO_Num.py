#!/usr/bin/python

from ABE.ABE_helpers import ABEHelpers
from ABE.ABE_ExpanderPi import IO

"""
================================================
Write or Read the value of numeric output to Expender Pi

Version 1.0 Created 19/02/2015

================================================
"""

def set_output_num(pin, value, pullup):
	
	"""
	Set value of numeric output
	
	pin : Number of output pin
	value : If True the logic pull is up
	
	Return -1 if ERROR
	"""	
	
	# Control value of parameters
	# Control if the number pin is a Integer
	try:
		int == type(pin)
	except ValueError:
		print("ERROR: The value of pin is not number")
		return -1
	
	# Control if the value is a boolean
	try:
		bool == type(value)
	except ValueError:
		print("ERROR: The value is not boolean")
		return -1
		
	# Control if the number pin is in the band
	if ((pin < 1) or (pin > 16)):
		print("ERROR: The pin's number is incorrect")
		return -1

	i2c_helper = ABEHelpers()
	bus = i2c_helper.get_smbus()

	io = IO(bus)  # create an instance of the IO class
	
	io.set_pin_direction(pin, 0)		# Define as output pin
	
	# Define home position "up or down"
	if pullup:
		io.set_pin_pullup(pin, 0xFF)
	else:
		io.set_pin_pullup(pin, 0x00)
	
	io.write_pin(pin, value)
	
def get_input_num(pin, pullup):
	
	"""
	Get value of numeric input
	
	pin : Number of input pin
	pullup : If True the logic pull is up
	
	Return the state of numeric input OR -1 if ERROR
	"""	
	
	# Control value of parameters
	# Control if the number pin is a Integer
	try:
		int == type(pin)
	except ValueError:
		print("ERROR: The value of pin is not number")
		return -1
	
	# Control if the pullup is a boolean
	try:
		bool == type(pullup)
	except ValueError:
		print("ERROR: The pull resistor is not boolean")
		return -1
		
	# Control if the number pin is in the band
	if ((pin < 1) or (pin > 16)):
		print("ERROR: The pin's number is incorrect")
		return -1

	i2c_helper = ABEHelpers()
	bus = i2c_helper.get_smbus()

	io = IO(bus)  # create an instance of the IO class
	
	io.set_pin_direction(pin, 1)		# Define as input pin
	
	# Define home position "up or down"
	if pullup:
		io.set_pin_pullup(pin, 0xFF)
	else:
		io.set_pin_pullup(pin, 0x00)
		
	return io.read_pin(pin)