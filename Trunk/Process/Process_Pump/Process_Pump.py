# To add a new process, follow instructions :
# Copy/Paste/rename Process_template folder
# Go to Trunk/Core/Queue_Global.py and follow instructions
# Go to Trunk/main.py and follow instructions
# Rename Process name in StartThread function


from Queue import Queue
from threading import Thread

import Core.Queue_Global as Queue_Global
from Core.QueueItem import QueueItem
from datetime import datetime
import Core.database as database
from Core.actuator import Pump

def process(Queue):
	poolPumpConfig = database.databasePump.getHardwareConfigurationByName("Pool Pump")

	pump = Pump(poolPumpConfig[0],poolPumpConfig[2])
	#pump = Pump(5,2)

	while True:
		Item = Queue.get()
		state = Item.state
		data = Item.data
		if state == "Init":
			print("Init State")

			precision = 30 #minute
			poolTemperature = 12.0
			preferedHours = [1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1] # use the same precision 
			pumpDecision  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] # use the same precision 

			pumpingTime = (poolTemperature / 3) * 60 # 1 hour of pumping every 3 degrees
			pumpingInterval = pumpingTime / precision # Number of block to place in pumpDecision
			
			if pumpingInterval > 48 :
				pumpingInterval = 48

			pumpingInterval = 30

			#Calculate position of max occurence 1
			numberOfIntervale = 1
			value = preferedHours[0]
			index = 0
			consecutive = 0
			interConsecutive = 0
			i = 0
			for block in preferedHours:
				if block != value :
					numberOfIntervale += 1
					value = block
					if interConsecutive > consecutive :
						consecutive = interConsecutive
						index = i-1
					interConsecutive = 0
				if block == 0 :
					interConsecutive += 1
				i += 1

			#Its a circle array so extrem bound was the same
			if preferedHours[0] == preferedHours[len(preferedHours)-1] :
				numberOfIntervale -= 1

			blockApply = 0
			for i in range(index, 0, -1) :
				if preferedHours[i] == 1 and blockApply < pumpingInterval/2 :
					pumpDecision[i] = 1
					blockApply += 1

			for i in range(index, len(preferedHours)) :
				if preferedHours[i] == 1 and blockApply < pumpingInterval :
					pumpDecision[i] = 1
					blockApply += 1

			#After that if block not assigned complete pumpDecision with preferedHours
			i = 0
			while blockApply < pumpingInterval :
				if preferedHours.count(1) < pumpDecision.count(1) or i == len(preferedHours):
					break
				if preferedHours[i] == 1 and pumpDecision[i] == 0:
					pumpDecision[i] = 1
					blockApply += 1
				i += 1

			#After that if block not assigned we have to start pump over preferedHours
			while blockApply < pumpingInterval :
				numberOfIntervale = 1
				value = preferedHours[0]
				index = 0
				consecutive = 0
				interConsecutive = 0
				previousConsecutive = 0
				interPreviousConsecutive = 0
				nextConsecutive = 0
				i = 0
				for block in pumpDecision:
					if block != value :
						numberOfIntervale += 1
						value = block
						if interConsecutive > consecutive :
							consecutive = interConsecutive
							previousConsecutive = interPreviousConsecutive
							interPreviousConsecutive = 0
							index = i-1
						else :
							nextConsecutive = interPreviousConsecutive
						interConsecutive = 0
					if block == 0 :
						interConsecutive += 1
					else :
						interPreviousConsecutive += 1
					i += 1

				#Its a circle array so extrem bound was the same
				if preferedHours[0] == preferedHours[len(preferedHours)-1] :
					nextConsecutive = interPreviousConsecutive
					numberOfIntervale -= 1

				if(numberOfIntervale == 2) :
					pumpDecision[index-consecutive/2] = 1
					blockApply += 1
				elif previousConsecutive < nextConsecutive :
					pumpDecision[index-consecutive+1] = 1
					blockApply += 1
				else :
					pumpDecision[index] = 1
					blockApply += 1



			print(pumpingInterval)
			print(blockApply)
			print(preferedHours)
			print(pumpDecision)
			

			#now = datetime.now()
			#hoursLeft = 23 - now.hour
			#minutesLeft = 59 - now.minute + 1
		#
			#numberOfPrecisionFormattedTimeLeft = HourToPrecisionFormatted(hoursLeft, minutesLeft, precision) + 1
#
			#startTimeInNumberOfPrecisionFormattedTime = HourToPrecisionFormatted(now.hour, now.minute, precision)
#
			#pumpingTPrecisionFormattedTimeList = [0] * numberOfPrecisionFormattedTimeLeft
#
			#if(preferedHours[startTimeInNumberOfPrecisionFormattedTime:].count(1) > pumpingTime):
			#	print("All in prefered hours but we have to adapt time in bloc time")
			#	# Choose when to pump during prefered hours
#
			#elif(preferedHours[startTimeInNumberOfPrecisionFormattedTime:].count(1) < pumpingTime):
			#	print("Not all in prefered hours")
			#	# Pump during all prefered hours and choose when pumping all hours left
			#else:
			#	print("All in prefered hour")
			#	# Go to process
#
#
			#print(str(preferedHours[startTimeInNumberOfPrecisionFormattedTime:].count(1)) + " | " + str(numberOfPrecisionFormattedTimeLeft) + " | " + str(startTimeInNumberOfPrecisionFormattedTime) + " | " + str(pumpingTime)) 
			#print(preferedHours[startTimeInNumberOfPrecisionFormattedTime:])
			#print("Left till midnight "+ str(hoursLeft) +"h"+ str(minutesLeft)) 
		elif state == "Start":
			print("Start State")	

		elif state == "Process":
			print("Process State")		
			Queue.enqueueIfEmpty(state, data, 1000)
			
		elif state == "on":
			
			pump.set_on()		

		elif state == "off":
			pump.set_off()	

		elif state == "auto":
			pump.set_mode_auto()	
			#Launch process

		elif state == "Stop":
			print("Stop State")	

		elif state == "Exit":

			break
		else:
			print("Programmation error : This state is not implemented : "+state)

		Queue.task_done() # Indicate that a formerly enqueued task is complete


def StartThread():
	ThreadProcess = Thread(target=process, args=(Queue_Global.process_Pump,))
	ThreadProcess.setDaemon(False)
	ThreadProcess.start()

def HourToPrecisionFormatted(hour, minute, precision):
	hourInMinutes = hour * 60 + minute
	hourToPrecisionFormatted = hourInMinutes / precision
	return hourToPrecisionFormatted

#class preferedHour(object):

#	def __init__(self, ):
		
