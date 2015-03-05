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
	def __init__(self, P=2.0, I=0.0, D=1.0, Derivator=0, Integrator=0, Integrator_max=500, Integrator_min=-500):
		self.Kp=P #Proportional gain, a tuning parameter
		self.Ki=I #Integral gain, a tuning parameter
		self.Kd=D #Derivative gain, a tuning parameter
		self.Derivator=Derivator #Derivator
		self.Integrator=Integrator #Integrator
		self.Integrator_max=Integrator_max #Integrator_max (a tag max)
		self.Integrator_min=Integrator_min #Integrator_min (a tag min)

		self.set_point=30.0 #set_point is requested setpoint
		self.error=0.0 #asked error or previous error

		#Initialise some variables for the control loop
		#self.pwr_cnt=1
		#self.pwr_tot=0
		self.pwr_coef=2 #conversion coefficient to obtain second
		self.coef_regul=1 #coefficient for duration of heaters

	
	#------------------------------#
	# Definition temperature value #
	#------------------------------#
	def BD_Temperature(self):
	  ### a lire dans la base de donnée
	    #temperature = float(input("saisissez une temperature °C : "))
	    temperature = database.databaseThermocoupleRegulation.getLastMeasureByName("Pool Temperature Sensor")
	    return temperature
	    print("Temperature = {} ".format(temperature))
	
	#---------------------------#
	# Definition engine control #
	#---------------------------#	 
	def turn_on(self):
	  ### taper dans le process marche moteur
	  print("turn on")
	  Queue_Global.process_Actuators.enqueue('heater', 'on')
	 
	def turn_off(self):
	  ### taper dans le process arret moteur
	  print("turn off")
	  Queue_Global.process_Actuators.enqueue('heater', 'off')
	 
	
	
	
	#-------------------------#
	#  Definition of Updated  #
	#-------------------------#
	def Calulate_PID(self,current_value):
		"""
		Calculate PID output value for given reference input and feedback
		"""
	
		#error calculation
		self.error = self.set_point - current_value
	
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
		#Initialise some variables for the control loop
		#pwr_cnt=1
		#pwr_tot=0

		# Turn on for initial ramp up
		#state="on"
		#self.turn_on()
		state="off"
		self.turn_off()
		PID=self.Calulate_PID(self.BD_Temperature())

		power = PID*self.pwr_coef

		print("POWER = {} secondes soit {} minutes".format(power, power/60))
		#if (power > 0):
		#	self.pwr_tot = self.pwr_tot + power
		#	print("pwr_tot = {}".format(self.pwr_tot))
#		#self.pwr_ave = self.pwr_tot / self.pwr_cnt
#		print("pwr_ave = {}".format(self.pwr_ave))
#		self.pwr_cnt = self.pwr_cnt + 1
#		print("pwr_cnt = {}".format(self.pwr_cnt))

		#Long duration pulse width modulation
		for x in range (1, 100):
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
					print("tata")
	

