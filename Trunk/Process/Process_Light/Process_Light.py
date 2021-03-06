# To add a new process, follow instructions :
# Copy/Paste/rename Process_template folder
# Go to Trunk/Core/Queue_Global.py and follow instructions
# Go to Trunk/main.py and follow instructions
# Rename Process name in StartThread function


from Queue import Queue
from threading import Thread
import time
import Core.Queue_Global as Queue_Global
from Core.QueueItem import QueueItem
from Core.actuator import *
import Core.database as database



def process(Queue):




	while True:
		Item = Queue.get()
		state = Item.state
		data = Item.data
		
		if state == "Init":
			poolLightConfig = database.databaseLight.getHardwareConfigurationByName("Pool Light")
			light = Light(poolLightConfig[0],poolLightConfig[2], False)



		elif state == "Start":
			print("Start State")	

		elif state == "Process":		
			Queue.enqueueIfEmpty(state, data, 1000)
			
		elif state == "Stop":
			print("Stop State")		

		elif state == "light":
			if(data == "on"):
				light.set_value(True)
			else:
				light.set_value(False)	



		elif state == "Exit":
			del database.databaseLight
			break
		else:
			print("Programmation error : This state is not implemented : "+state)

		Queue.task_done() # Indicate that a formerly enqueued task is complete


def StartThread():
	ThreadProcess = Thread(target=process, args=(Queue_Global.process_Light,))
	ThreadProcess.setDaemon(False)
	ThreadProcess.start()
