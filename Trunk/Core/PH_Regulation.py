# The recipe gives simple implementation of a Discrete Proportional-Integral-Derivative (PID) controller. 
# PID controller gives output value for error between desired reference input and measurement feedback to minimize error value.
#
# More information: http://en.wikipedia.org/wiki/PID_controller
#			 		http://www.phidgets.com/docs/1130_User_Guide
#					http://clement.storck.me/blog/2014/08/controle-et-supervision-de-la-piscine/
#
# PlashBoard test PID


from time import sleep

class PH_Regulation(object):
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

		self.set_point=7.3 #set_point is requested setpoint
		self.error=0.0 #asked error or previous error

		#Initialise some variables for the control loop
		self.pwr_coef=-2 #conversion coefficient to obtain second
		self.coef_regul=1 #coefficient for duration of heaters

		self.initialization = False

		#Preset value for the conversion scale
		self.correctingBasicPh = 160 #ml (milliliter)
		self.lowerPh = 0.1 #unit ph
		self.poolVolume = 10 #m3 (cubic meter)	

		#Rate of flow
		self.valueLiter = 0.4 #unit liter
		self.valueHours = 1 #unit hours



	
	#------------------------------#
	# Definition PH initialization #
	#------------------------------#
	def PH_init(self):
		print("Etalonnage de la sonde PH 10")
		# inizialisation PH 10 
		nextEtape = 0
		while nextEtape != 1 :
			nextEtape = float (input ("taper 1 pour continuer : "))
		
		print("Tremper la sonde dans solution PH 10")
		while nextEtape != 2 :
			nextEtape = float (input ("taper 2 quand la sonde est immergé : "))	
			
		print("Etalonnage PH 10 en cours ..")
		PH = self.BD_PH()
		#sleep(10)
		print ("Etalonnage PH 10 terminer")
		print(PH)
		if PH >= 9.0 and PH <= 11.0 :
			print("Sonde OK")
		else: 
			print("Sonde HS")

		# inizialisation PH 7
		print("Etalonnage de la sonde PH 7")
		while nextEtape != 3 :
			nextEtape = float (input ("taper 3 pour continuer : "))
		
		print("Tremper la sonde dans solution PH 7")
		while nextEtape != 4 :
			nextEtape = float (input ("taper 4 quand la sonde est immergé : "))	
			
		print("Etalonnage PH 7 en cours ..")
		PH = self.BD_PH()
		#sleep(10)
		print ("Etalonnage PH 7 terminer")
		print(PH)
		if PH >= 6.0 and PH <= 8.0 :
			print("Sonde OK")
		else: 
			print("Sonde HS")
		
		return 0


	#------------------------------#
	# Definition PH value #
	#------------------------------#
	def BD_PH(self):
	  ### a lire dans la base de donnée
	    SensorValuePH = float(input("saisissez un ph : "))
	    return SensorValuePH

	#------------------------------#
	# Definition temperature value #
	#------------------------------#
	def BD_Temperature(self):
	  ### a lire dans la base de donnée
	    temperature = float(input("saisissez une temperature °C : "))
	    return temperature
	
	#---------------------------#
	# Definition engine control #
	#---------------------------#	 
	def turn_on(self):
	  ### taper dans le process marche moteur
	  print("turn on")
	 
	def turn_off(self):
	  ### taper dans le process arret moteur
	  print("turn off")
	 
	
	
	
	#-------------------------#
	#  Definition of Updated  #
	#-------------------------#
	def Calulate_PH(self,current_value_temp, current_value_ph):
		"""
		Depending on the temperature of the solution and on the actual pH level, 
		the SensorValue can change dramatically. To incorporate temperature (in degrees Celsius) for added accuracy, 
		the following formula can be used: 
		"""

		firstEquation = 2.5 - ( current_value_ph / 200 )
		secondEquation = 0.257179 + 0.000941468 * current_value_temp
		PH = 7 - ( firstEquation / secondEquation )

		return PH


	def Calculate_Volume_Produced_LessPh(self, current_value_ph, set_point_ph):
		"""
		An average of 160 mL of less liquid pH corrector lower the pH of 0.1 units of 10 m3 of water.
		Example: 4 liters less liquid pH corrector lower the pH from 7.8 to 7.3 for a volume of 50 m3 of water.
		"""

		#Variable
		varPoolVolume = self.poolVolume / 10
		phCorrector = (current_value_ph - set_point_ph) / self.lowerPh

		#Calculation
		correctionDose = self.correctingBasicPh * phCorrector * varPoolVolume

		#Conversion milliliter to liter
		milliliter = correctionDose
		liter = milliliter / 1000

		#print("Dosage ph- = {} milliliter whether {} liter".format(milliliter, liter))

		return milliliter


	def Calculate_Time_Produced_LessPh(self, current_milliliter):
		"""
		Parameter of the peristaltic pump
		"""
		#print("valueLiter = {} ".format(self.valueLiter))
		#print("valueHours = {} ".format(self.valueHours))
		

		#pump conversion parameter
		valueMilliliter = self.valueLiter * 1000
		valueMinutes = ( self.valueHours * 60 ) 

		#print("valueMilliliter = {} ".format(valueMilliliter))
		#print("valueMinutes = {} ".format(valueMinutes))

		timeProduced = ( current_milliliter * valueMinutes ) / valueMilliliter

		#print("timeProduced = {} ".format(timeProduced))
		#print("timeProduced = {} secondes soit {} minutes".format(timeProduced*60, timeProduced))

		return timeProduced #minutes


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
		PID = PID * 10
		print("PID = {}".format(PID))
	
		return PID


	def Regulate(self):
		#Initialise some variables for the control loop
		if self.initialization == False:
			#self.PH_init()
			self.initialization = True 

		#test seb
		calculatePhLess = self.Calculate_Volume_Produced_LessPh(self.BD_PH(), self.set_point)
		print("calculatePhLess ml = {}".format(calculatePhLess))

		timeProduced = self.Calculate_Time_Produced_LessPh(calculatePhLess)
		print("timeProduced = {} secondes soit {} minutes".format(timeProduced*60, timeProduced))

		# Turn on for initial ramp up
		state="off"
		self.turn_off()
		#PID=self.Calulate_PID(self.BD_PH())

		#power = PID*self.pwr_coef
		#power = calculatePhLess/10

		#print("POWER = {} secondes soit {} minutes".format(power, power/60))

		#Long duration pulse width modulation
		if (calculatePhLess > self.set_point):
			if (state=="off"):
				state="on"
				self.turn_on()
				print("toto")
				sleep(timeProduced*60)
		else:
			if (state=="on"):
				state="off"
				self.turn_off()
				print("tata")
				#print(power*self.coef_regul)

#		#Long duration pulse width modulation
#		for x in range (1, 100):
#			if (power > x):
#				if (state=="off"):
#					state="on"
#					self.turn_on()
#					print("toto")
#					#sleep(power*self.coef_regul)
#			else:
#				if (state=="on"):
#					state="off"
#					self.turn_off()
#					print("tata")
#					#print(power*self.coef_regul)

	

if __name__ == '__main__':
    
   	#PH_init()
	PH = PH_Regulation()
	while True:
		PH.Regulate()
		 