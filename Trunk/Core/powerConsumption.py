#!/usr/bin/python

import database

totalCunsumption = 0.0
voltage = 230

def currentPower():
	global voltage

	print("get database ampere meter value to 1min")
	currenPower = currentCurrent * voltage
	print("Set the current cunsumtption to database")

def calculCunsumption():
	global totalCunsumption

	print("Get the current cunsumtption to database")
	totalCunsumption += (currenPower/60)
	print("Set the total cunsumtption to database")
	
def resetCunsumption():
	global totalCunsumption

	totalCunsumption = 0.0