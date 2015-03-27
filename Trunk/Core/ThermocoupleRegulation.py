# PlashBoard 
#
# The recipe gives simple implementation of a Discrete Proportional-Integral-Derivative (PID) controller. 
# PID controller gives output value for error between desired reference input and measurement feedback to minimize error value.
#
# More information: http://en.wikipedia.org/wiki/PID_controller
#
#Explanation of the pool temperature control program:
#A set temperature is recovered in the lower data. This instruction corresponds to the target value given by the operator. The basic setpoint is 25 degrees.
#The actual temperature of the pool is retrieved from the database. The actual temperature corresponds to the value of the temperature sensor.
#Several constraints come into play:
#	- The volume of the pool (it is adjustable by the user)
#	- Heating heating power (heat pump) (it is adjustable by the user)
#To improve the heating time, using a PID.
#At each temperature acquisition, it recalculates the PID. This PID can reduce the heating time. Indeed no one approaches the setpoint at the PID therefore reduces the heating time decreases. The further away from the target, the higher the heating time increases.
#The program works:
#	- If the actual temperature is higher than the temperature recorded so we do nothing.
#	- If the actual temperature is below the setpoint temperature, then the heating is activated. For this the program returns a duration of heating time.
#The calling program temperature control will use the heating time to activate the heating with the requested time.



from time import sleep
import Core.database as database
import Core.Queue_Global as Queue_Global

class ThermocoupleRegulation(object):
	"""PID Thermocouple"""

	#------------------------------#
	# Definition of initialization #
	#------------------------------#
	def __init__(self, P=1.81, I=0.00158, D=0.0, Derivator=0, Integrator=0, Integrator_max=10, Integrator_min=-10):
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
		self.poolVolume = float(database.databaseThermocoupleRegulation.getUserConfigurationValue("pool_volume")) #volume of the pool (m3)
		self.powerHeatPump = float(database.databaseThermocoupleRegulation.getUserConfigurationValue("power_heat_pump")) #power of the heat pump (kW)
		

	
	#------------------------------#
	# Definition temperature value #
	#------------------------------#
	def BD_Temperature(self):
		"""
		Recovery of the temperature in the database
		"""
		temperature = database.databaseThermocoupleRegulation.getLastMeasureByName("Pool Temperature Sensor")[0]
		#print("Temperature = {} ".format(temperature))
		return temperature
	    
	
	#---------------------------#
	# Definition engine control #
	#---------------------------#	 
	def turn_on(self, numberOfSeconds):
		"""
		Request of pump operation
		"""
		#print("turn on heating")
		Queue_Global.process_Heater.enqueue('on', numberOfSeconds)
	 
	def turn_off(self):
		"""
		Request the pump stop
		"""
		#print("turn off heating")
		Queue_Global.process_Heater.enqueue('off')
	 
	
	
	
	#-------------------------#
	#  Definition of Updated  #
	#-------------------------#
	def Calulate_PID(self,current_value):
		"""
		Calculate PID output value for given reference input and feedback
		"""
		set_point = float(database.databaseThermocoupleRegulation.getUserConfigurationValue("temperature_setpoint")) #set_point is requested setpoint
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
		#print("PID = {}".format(PID))
	
		return PID


	def Regulate(self):
		"""
		Operation control
		"""

		PID=self.Calulate_PID(self.BD_Temperature())

		#Temperature rise time
		initialTemperature = PID/2

		heatingTime = (self.poolVolume * initialTemperature * 1.163) / self.powerHeatPump
		#print("heatingTime = {} minutes, {} heures, {} jours".format(heatingTime*60, heatingTime, heatingTime/24))
		
		self.turn_on(heatingTime*60*60) #return time heating operation



	

