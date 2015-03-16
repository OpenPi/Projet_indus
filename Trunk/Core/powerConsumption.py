#!/usr/bin/python

import database

"""
================================================
Calcul consumption

Version 1.0 Created 12/03/2015

================================================
"""

totalConsumption = 0.0
voltage = 230	# Replace by reference file

def currentPower():
	"""
	Save to database the power consumption
	"""
	global voltage	# Replace by preference

	currentCurrent = 1  # Replace by get value database
	print("get database ampere meter value to 1min")	# Get ampere meter value
	currenPower = currentCurrent * voltage	# calcul power
	print("Set the current cunsumtption to database")	# Set power consumption value

def calculConsumption():
	"""
	Calcul total consumption
	Need to call all minute
	"""
	global totalConsumption

	currenPower = 1  # Replace by get value database
	print("Get the current cunsumtption to database")	# Get power consumption value
	totalConsumption += (currenPower/60)
	print("Set the total cunsumtption to database")		# Set total cunsumption
	
def resetConsumption():
	"""
	Reset counter to consumption
	"""
	global totalConsumption

	totalConsumption = 0.0