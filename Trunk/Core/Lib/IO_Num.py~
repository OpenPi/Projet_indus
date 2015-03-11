#!/usr/bin/python

from ABE.ABE_helpers import ABEHelpers
from ABE.ABE_ExpanderPi import IO

"""
================================================
Write or Read the value of numeric output to Expander Pi

Version 1.0 Created 19/02/2015

================================================
"""

def set_output_direction(pin):
	"""
	Define pin setting, to output
	
	pin: Number of output pin
	
	Return -1 if ERROR
	"""
	
	# Control value of parameters
	# Control if the number pin is a Integer
	try:
		int == type(pin)
	except ValueError:
		print("ERROR: The value of pin is not number")
		return -1
		
	# Control if the number pin is in the band
	try:
		((pin > 0) and (pin < 17))
	except ValueError:
		print("ERROR: The pin's number is incorrect")
		return -1
	
	io.set_pin_direction(pin, 0)		# Define as output pin
	
def set_input_direction(pin):
	"""
	Define pin setting, to input
	
	pin: Number of input pin
	
	Return -1 if ERROR
	"""
	
	# Control value of parameters
	# Control if the number pin is a Integer
	try:
		int == type(pin)
	except ValueError:
		print("ERROR: The value of pin is not number")
		return -1
	
	# Control if the number pin is in the band
	try:
		((pin > 0) and (pin < 17))
	except ValueError:
		print("ERROR: The pin's number is incorrect")
		return -1
	
	io.set_pin_direction(pin, 1)		# Define as input pin

def set_pullUp(pin, value=True):
	"""
	Define pull type to pin
	
	pin: Number of input pin
	value: Value to pull up - True = PullUp / False = PullDown
	
	Return -1 if ERROR
	"""
	
	# Control value of parameters
	# Control if the number pin is a Integer
	try:
		bool == type(value)
	except ValueError:
		print("ERROR: The value of polarity is not boolean")
		return -1
		
	# If value = True pull type is pullUp else is pullDown
	if value:
		io.set_pin_pullup(pin, 0xFF)	# Set pin to pullUP
	else:
		io.set_pin_pullup(pin, 0x00)	# Set pin to pullDown
	
def set_output_num(pin, value):
	"""
	Set value of numeric output
	
	pin : Number of output pin
	value : Value to write in output
	
	Return -1 if ERROR
	"""	
	
	# Control value of parameters	
	# Control if the value is a boolean
	try:
		bool == type(value)
	except ValueError:
		print("ERROR: The value is not boolean")
		return -1

	io.write_pin(pin, value)	# Write value to Pin
	
def get_input_num(pin):
	"""
	Get value of numeric input
	
	pin : Number of input pin
	
	Return the state of numeric input OR -1 if ERROR
	"""	
		
	return io.read_pin(pin)		# Read state of pin
	
i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()	# Create i2c instance
io = IO(bus)  # create an instance of the IO class