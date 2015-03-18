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
	pump = Pump(poolPumpConfig[0],poolPumpConfig[2], False)
	
	while True:
		Item = Queue.get()
		state = Item.state
		data = Item.data
		if state == "Init":

			indexProcess = 0

			date = datetime

			precision = 30 #minute
			poolTemperature = database.databasePump.getLastMeasureByName("Pool Temperature Sensor")
			pumpingHoursConfig = database.databasePump.getUserConfiguration("pumping_hours")
			

			#Create preference hours with data in database
			preferedHours = []
			for value in pumpingHoursConfig:
				if value == ',':
					pass
				elif value == '1':
					preferedHours.append(1)
				else:
					preferedHours.append(0)
			
			pumpDecision  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] # use the same precision 

			pumpingTime = (poolTemperature / 3) * 60 # 1 hour of pumping every 3 degrees
			pumpingInterval = pumpingTime / precision # Number of block to place in pumpDecision
			
			if pumpingInterval > 48 :
				pumpingInterval = 48

			#pumpingInterval = 30

			#Calculate position of max occurence of 0 in preferedHours
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

			#Apply half of pumping time to the left of max occurency of 0
			blockApply = 0
			for i in range(index, 0, -1) :
				if preferedHours[i] == 1 and blockApply < pumpingInterval/2 :
					pumpDecision[i] = 1
					blockApply += 1
			#Try to place all of pumping time to the right
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

			#After that if block not assigned we have to start pump over preferedHours, calculate max occurrence of 0
			#and number of element (1) next and previous of the max occurence of 0 
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
				#If only two block (one with 1 and one with 0) create a new block of pumping in the bigger block of 0
				if(numberOfIntervale == 2) :
					pumpDecision[index-consecutive/2] = 1
					blockApply += 1
				#Else add pumping to the tinner block of 1
				elif previousConsecutive < nextConsecutive :
					pumpDecision[index-consecutive+1] = 1
					blockApply += 1
				else :
					pumpDecision[index] = 1
					blockApply += 1
			#print(pumpingHoursConfig)
			#print(pumpingInterval)
			#print(blockApply)
			#print(preferedHours)
			print(pumpDecision)
			dateIndex = date.now()
			Queue_Global.process_Pump.enqueue('Start')
			
		elif state == "Start":
			print("Start State")
			Queue_Global.process_Pump.enqueue('auto')	

		elif state == "Process":
			#print("Process State")		

			#Calculate time to find index to check
			#Test without time
			if(date.now().day > dateIndex.day):
				Queue_Global.process_Pump.enqueue('Init')
			else:
				indexProcess = (date.now().hour*60 + date.now().minute)/precision

				#Check decision and start or stop pump
				if(pumpDecision[indexProcess] == 1):
					pump.set_value(True)
					
				else:
					pump.set_value(False)
				Queue.enqueueIfEmpty(state, data, 1000)
			#print(pumpDecision[indexProcess])
			#indexProcess += 1

			
			#Test without time
			
			
		elif state == "on":	
			print("On State")		
			pump.set_on()		

		elif state == "off":
			print("Off State")
			pump.set_off()	

		elif state == "auto":
			print("Auto State")
			pump.set_mode_auto()
			Queue_Global.process_Pump.enqueue('Process')	

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
		
