# -*-coding:Latin-1 -*

# The recipe gives simple implementation of a Discrete Proportional-Integral-Derivative (PID) controller. 
# PID controller gives output value for error between desired reference input and measurement feedback to minimize error value.
#
# More information: http://en.wikipedia.org/wiki/PID_controller
#
# PlashBoard test PID


from time import sleep
import Core.database as database
import Core.Queue_Global as Queue_Global

class ThermocoupleRegulation(object):
	"""PID Thermocouple"""

	#------------------------------#
	# Definition of initialization #
	#------------------------------#
	def __init__(self, P=5.0, I=0.0, D=0.0, Derivator=0, Integrator=0, Integrator_max=500, Integrator_min=-500):
		self.Kp=P #Proportional gain, a tuning parameter
		self.Ki=I #Integral gain, a tuning parameter
		self.Kd=D #Derivative gain, a tuning parameter
		self.Derivator=Derivator #Derivator
		self.Integrator=Integrator #Integrator
		self.Integrator_max=Integrator_max #Integrator_max (a tag max)
		self.Integrator_min=Integrator_min #Integrator_min (a tag min)

		self.error=0.0 #asked error or previous error

		#Initialise some variables for the control loop
		self.pwr_coef=2 #conversion coefficient to obtain second
		self.coef_regul=1 #coefficient for duration of heaters

		#Initialise temperature rise time
		#self.desiredTemperature = self.set_point #desired temperature
		self.poolVolume = float(database.databaseThermocoupleRegulation.getUserConfiguration("pool_volume")) #volume of the pool (m3)
		self.powerHeatPump = float(database.databaseThermocoupleRegulation.getUserConfiguration("power_heat_pump")) #power of the heat pump (kW)

	
	#------------------------------#
	# Definition temperature value #
	#------------------------------#
	def BD_Temperature(self):
	  ### a lire dans la base de donnée
	    #temperature = float(input("saisissez une temperature °C : "))
	    temperature = database.databaseThermocoupleRegulation.getLastMeasureByName("Pool Temperature Sensor")
	    print("Temperature = {} ".format(temperature))
	    return temperature
	    
	
	#---------------------------#
	# Definition engine control #
	#---------------------------#	 
	def turn_on(self, numberOfSeconds):
	  ### taper dans le process marche moteur
	  print("turn on")
	  Queue_Global.process_Heater.enqueue('on', numberOfSeconds)
	 
	def turn_off(self):
	  ### taper dans le process arret moteur
	  print("turn off")
	  Queue_Global.process_Heater.enqueue('off')
	 
	
	
	
	#-------------------------#
	#  Definition of Updated  #
	#-------------------------#
	def Calulate_PID(self,current_value):
		"""
		Calculate PID output value for given reference input and feedback
		"""
		set_point = float(database.databaseThermocoupleRegulation.getUserConfiguration("temperature_setpoint")) #set_point is requested setpoint
		#error calculation
		self.error = set_point - current_value
	
		#PID calculation
		self.P_value = self.Kp * self.error
		self.D_value = self.Kd * ( self.error - self.Derivator)
		self.Derivator = self.error
	
		#Integrator calculation
		self.Integrator = self.Integrator + self.error
	
		# Control tag, if it is beyond the max or min
		if self.Integrator > self.Integrator_max:
			self.Integrator = self.Integrator_max
		elif self.Integrator < self.Integrator_min:
			self.Integrator = self.Integrator_min
	
		self.I_value = self.Integrator * self.Ki
	
		#calculation results PID
		PID = self.P_value + self.I_value + self.D_value
		print("PID = {}".format(PID))
	
		return PID


	def Regulate(self):
		# Turn on for initial ramp up
		state="off"
		self.turn_off()
		PID=self.Calulate_PID(self.BD_Temperature())

		#power = PID*self.pwr_coef
		#print("POWER = {} secondes soit {} minutes".format(power, power/60))

		#Temperature rise time
		initialTemperature = PID/2
		#temperatureDifference = self.desiredTemperature - initialTemperature
		#heatingTime = (self.poolVolume * temperatureDifference * 1.163) / self.powerHeatPump
		heatingTime = (self.poolVolume * initialTemperature * 1.163) / self.powerHeatPump
		print("heatingTime = {} minutes, {} heures, {} jours".format(heatingTime*60, heatingTime, heatingTime/24))
		
		self.turn_on(heatingTime*60*60) #return time heating operation


		#Long duration pulse width modulation
		"""for x in range (1, 100):
			if (power > x):
				if (state=="off"):
					state="on"
					self.turn_on()
					print("toto")
					sleep(power*self.coef_regul)
			else:
				if (state=="on"):
					state="off"
					self.turn_off()
					print("tata")"""
		#self.turn_on(power*self.coef_regul)
	

