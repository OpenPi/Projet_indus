#!/usr/bin/python

from Core.sensor import Thermocouple
from Core.sensor import PhMeter
from Core.sensor import AmpereMeter
from time import sleep

chlTh = 1
chlPh = 2
chlAmp = 3
refVolt = 4.140

tempSensor = Thermocouple(chlTh, refVolt)
phSensor = PhMeter(chlPh, refVolt)
ampereSensor = AmpereMeter(chlAmp, refVolt)

i = 0
while i < 120:
	print("Temperature: {}C -- {}V".format(tempSensor.get_value(), tempSensor.get_value_sensor() ))
	print("Ph: {}".format(phSensor.get_value()))
	print("Ampere: {}".format(ampereSensor.get_value()))
	print("\n")
	i += 1
	sleep(0.5)
	
