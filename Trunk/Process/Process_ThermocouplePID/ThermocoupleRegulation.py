# The recipe gives simple implementation of a Discrete Proportional-Integral-Derivative (PID) controller. 
# PID controller gives output value for error between desired reference input and measurement feedback to minimize error value.
#
# More information: http://en.wikipedia.org/wiki/PID_controller
#
# PlashBoard test PID


from time import sleep

class TemperatureRegulation(object):
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

		self.set_point=0.0 #set_point is requested setpoint
		self.error=0.0 #asked error or previous error

	
	#------------------------------#
	# Definition temperature value #
	#------------------------------#
	def BD_Temperature():
	  ### a lire dans la base de donnée
	
	#---------------------------#
	# Definition engine control #
	#---------------------------#	 
	def turn_on():
	  ### taper dans le process marche moteur
	 
	def turn_off():
	  ### taper dans le process arret moteur
	 
	
	
	
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
	
		return PID


	def Regulate(self):
		#Initialise some variables for the control loop
		pwr_cnt=1
		pwr_tot=0

		# Turn on for initial ramp up
		state="on"
		turn_on()
		PID=Calulate_PID(BD_Temperature())

		while True:
		    power = PID/100
		    if (power > 0):
		        pwr_tot = pwr_tot + power
		    pwr_ave = pwr_tot / pwr_cnt
		    pwr_cnt = pwr_cnt + 1

		    # Long duration pulse width modulation
		    for x in range (1, 100):
		        if (power > x):
		            if (state=="off"):
		                state="on"
		                turn_on()
		        else:
		            if (state=="on"):
		                state="off"
		                turn_off()
		        sleep(1)
	


