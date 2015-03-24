# PlashBoard
#
# More information: http://www.phidgets.com/docs/1130_User_Guide
#			 		
#



from time import sleep
import Core.database as database
import Core.Queue_Global as Queue_Global

class PH_Regulation(object):
	"""PID Thermocouple"""

	#------------------------------#
	# Definition of initialization #
	#------------------------------#
	def __init__(self):

		#pH setpoint given by the user
		self.set_point=7.3 #set_point is requested setpoint ###########################################

		#Preset value for the conversion scale
		self.correctingBasicPh = 160 #ml (milliliter)
		self.lowerPh = 0.1 #unit ph
		self.poolVolume = float(database.databaseThermocoupleRegulation.getUserConfiguration("pool_volume")) #volume of the pool (m3) #####################

		#Rate of flow, parameter of the peristaltic pump
		self.valueLiter = 0.4 #unit liter ##############################################
		self.valueHours = 1 #unit hours   ##############################################



	#------------------------------#
	# Definition PH value #
	#------------------------------#
	def BD_PH(self):
	    SensorValuePH = float(input("saisissez un ph : ")) ###########################################
	    return SensorValuePH
	
	
	#-------------------------#
	#  Definition of Updated  #
	#-------------------------#
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

		# Control tag, if it is beyond the max or min
		dosage = milliliter
		dosage_min = 0
		dosage_max = ( self.poolVolume *100 ) / 10 # 100ml --> 10m3

		if dosage > dosage_max:
			dosage = dosage_max
		elif dosage < dosage_min:
			 dosage = dosage_min

		return dosage


	def Calculate_Time_Produced_LessPh(self, current_milliliter):
		"""
		Parameter of the peristaltic pump
		"""
		#pump conversion parameter
		valueMilliliter = self.valueLiter * 1000
		valueMinutes = ( self.valueHours * 60 ) 

		timeProduced = ( current_milliliter * valueMinutes ) / valueMilliliter

		return timeProduced #minutes


	def Calculate_Number_Injection(self, poolVolume):
		"""
		Calculating the number of product injection days
		"""
		if self.poolVolume <= 50:
			NumberInjection = 3
		if self.poolVolume > 50 and self.poolVolume <= 70:
			NumberInjection = 5
		if self.poolVolume > 70 and self.poolVolume <= 90:
			NumberInjection = 6
		if self.poolVolume > 90 and self.poolVolume <= 130:
			NumberInjection = 11
		if self.poolVolume > 130 and self.poolVolume <= 260:
			NumberInjection = 20

		return NumberInjection


	def Regulate(self):

		#calculating the volume of product injection
		calculatePhLess = self.Calculate_Volume_Produced_LessPh(self.BD_PH(), self.set_point)
		print("calculatePhLess ml = {} and L = {}".format(calculatePhLess, calculatePhLess/1000))

		#calculating the number of product injection
		timeProduced = self.Calculate_Time_Produced_LessPh(calculatePhLess)
		print("timeProduced = {} secondes soit {} minutes".format(timeProduced*60, timeProduced))

		#calculating the number of product injection days
		NumberInjection = self.Calculate_Number_Injection(self.poolVolume)
		print("NumberInjection = {}".format(NumberInjection))

		#calculating operation hours of injection with respect to the hours of operation of the pump of the swimming pool.
		precision = 30 #precision
		precisionInjection = 0 #precision d'injection
		injectionPrevious = 0 #injection Number Previous
		inject = 0 #injected
		value = 0 #value
		forecast = 4 #forecast
		#pumpDecision = recovery of pump operation hours of the pool
		pumpDecision = [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0] #schedule of pump operation hours
		#peristalticPumpDecision = initializing the operating hours of the dosing pump
		peristalticPumpDecision = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #schedule of peristaltic pump operation hours
		#timeInjectionBlock = dosing time injection block
		timeInjectionBlock = timeProduced / NumberInjection

		for i in range(0, len(pumpDecision)):
			if ( pumpDecision[i] == 1  ) and ( value == 0 ) and ( inject < NumberInjection ) and ( forecast >= 4):
				value = 1
				forecast = 0
				injectionPrevious += 1
				inject += 1
				if timeInjectionBlock > 30:
					peristalticPumpDecision[i] = 30
					injectionPrevious += 30
				else:
					peristalticPumpDecision[i] = int(timeInjectionBlock)
					injectionPrevious += int(timeInjectionBlock)


			elif pumpDecision[i] == 0:
				value = 0
				injectionPrevious = 0
				forecast += 1

			elif ( pumpDecision[i] == 1 ) and ( value == 1 ):
				if injectionPrevious < timeInjectionBlock :
					if timeInjectionBlock - injectionPrevious > 30:
						peristalticPumpDecision[i] = 30
						injectionPrevious += 30
					else:
						peristalticPumpDecision[i] = int(timeInjectionBlock - injectionPrevious)
						injectionPrevious += int(timeInjectionBlock - injectionPrevious)
			else :
				forecast += 1

		print("timeInjectionBlock = {}".format(timeInjectionBlock))
		print("pumpDecision = {}".format(pumpDecision))
		print("peristalticPumpDecision = {}".format(peristalticPumpDecision))

		return peristalticPumpDecision

		 