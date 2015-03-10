#!/usr/bin/python

#from ABE_helpers import ABEHelpers
from ABE.ABE_ExpanderPi import DAC
from ABE.ABE_ExpanderPi import ADC

"""
================================================
Write or Read the value of analog output to Expender Pi

Version 1.0 Created 18/02/2015

================================================
"""

def set_refVolt_adc(refVolt):
	"""
	Initializes the reference voltage to Expander Pi
	
	refVolt: Reference voltage to Expander Pi
	
	Return -1 if ERROR
	"""

	# Control if the reference voltage is a number	
	try:
		(int == type(refVolt)) or (float == type(refVolt))
	except ValueError:
		print("ERROR: The value of reference voltage is not number\n")
		return -1

	adc.set_adc_refvoltage(refVolt)		# Initializes the reference voltage

def set_output_ana(channel, value, voltage=False):
	"""
	Set value of analog output
	
	channel : Number of output channel
	value : Value to send of analog output
	voltage : If voltage == True -> 0> value < 2.048 Else 0> value <4095
	
	return -1 if ERROR
	"""	
	
	# Control value of parameters
	# Control if the channel parameter is a Integer
	try:
		int == type(channel)
	except ValueError:
		print("ERROR: The value of channel is not number.")
		return -1

	# Control if the channel parameter is in the band
	try:
		((channel > 0) and (channel < 3))
	except ValueError:
		print("ERROR: The channel's number is incorrect")
		return -1
	
	# Control if the voltage parameter command is a boolean
	try: 
		bool == type(voltage)
	except ValueError:
		print("ERROR: The parameter voltage is not boolean")
		return -1
	
	if voltage:
		# Control if the voltage command is a number	
		try:
			(int == type(value)) or (float == type(value))
		except ValueError:
			print("ERROR: The value of command is not number")
			return -1
		
		# Control if the value parameter is in the band
		if ((value < 0) or (value > 2.048)):
			print("ERROR: The value's number is incorrect")
			return -1
		
		dac.set_dac_voltage(channel, value)  # set the voltage on channel "channel" to "value" V
		
	else:
		# Control if the voltage command is a number	
		try:
			int == type(value)
		except ValueError:
			print("ERROR: The value of command is not integer")
			return -1
			
		# Control if the value parameter is in the band
		if ((value < 0) or (value > 4095)):
			print("ERROR: The value's number is incorrect")
			return -1
			
		dac.set_dac_raw(channel, value)		# set value on channel "channel" to "value" (12 bits)
		
def get_input_ana(channel):
	"""
	Get value of analog input
	
	channel : Number of input channel
	
	Return the value of analog input in voltage OR -1 if ERROR
	"""	
	
	# Control value of parameters
	# Control if the channel is a Integer
	try:
		int == type(channel)
	except ValueError:
		print("ERROR: The value of channel is not number\n")
		return -1
		
	# Control if the channel is in the band
	try:
		((channel > 0) and (channel < 9))
	except ValueError:
		print("ERROR: The channel's number is incorrect\n")
		return -1
	
	voltage = float(adc.read_adc_voltage(channel))	# Read the value of the input
	
	return voltage		# Return value to analog input
	
adc = ADC()  	# create an instance of the ADC class (Input analog)
dac = DAC()  	# create an instance of the DAC class (Output analog)