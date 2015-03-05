#!/usr/bin/python

from Core.actuator import Light
from time import sleep

pin = 1

light = Light(pin)

value = True

light.override = True
print("Test override: {}".format(light.override))
light.override = 22
print("Test override: {}".format(light.override))
light.override = False
print("Test override: {}".format(light.override))

i = 0
while i < 10:

	if value:
		value = False
	else:
		value = True
		
	light.set_value(value)
	print("light value: {}".format(value))
	
	i += 1
	sleep(5)