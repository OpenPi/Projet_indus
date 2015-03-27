# To add a new process, follow instructions :
# Copy/Paste/rename Process_template folder
# Go to Trunk/Core/Queue_Global.py and follow instructions
# Go to Trunk/main.py and follow instructions
# Rename Process name in StartThread function


from Queue import Queue
from threading import Thread

import Core.Queue_Global as Queue_Global
from Core.QueueItem import QueueItem
import Core.database as database
from Core.actuator import Heater


def process(Queue):

	while True:
		Item = Queue.get()
		state = Item.state
		data = Item.data
		if state == "Init":
			poolHeaterConfig = database.databaseHeater.getHardwareConfigurationByName("Pool Heater")
			heater = Heater(poolHeaterConfig[0],poolHeaterConfig[2], False)			
			Queue_Global.process_TemperatureRegulation.enqueue('Process')
		elif state == "Start":
			print("Start State")	

		elif state == "on":
			#print("Heater : On State")
			numberOfSecond = data
			heater.set_value(True)
			Queue_Global.process_Heater.enqueue('Process')
		elif state == "off":
			#print("Heater : Off State")	
			heater.set_value(False)

		elif state == "Process":
			#print("Number of second left : " + str(numberOfSecond))
			numberOfSecond = numberOfSecond - 1
			if(numberOfSecond <= 0):
				Queue_Global.process_Heater.enqueue('off')
			else:			
				Queue.enqueueIfEmpty(state, data, 1000)
			
		elif state == "Stop":
			print("Stop State")		

		elif state == "Exit":

			break
		else:
			print("Programmation error : This state is not implemented : "+state)

		Queue.task_done() # Indicate that a formerly enqueued task is complete


def StartThread():
	ThreadProcess = Thread(target=process, args=(Queue_Global.process_Heater,))
	ThreadProcess.setDaemon(False)
	ThreadProcess.start()
