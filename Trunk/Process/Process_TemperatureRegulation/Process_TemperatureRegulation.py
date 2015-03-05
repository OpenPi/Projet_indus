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
import Core.ThermocoupleRegulation as ThermocoupleRegulation

def process(Queue):
	thermocoupleRegulation = ThermocoupleRegulation.ThermocoupleRegulation()
	while True:
		Item = Queue.get()
		state = Item.state
		data = Item.data
		if state == "Init":
			print("Init State")

		elif state == "Start":
			print("Start State")	

		elif state == "Process":

			thermocoupleRegulation.Regulate()
			
			Queue.enqueueIfEmpty(state, data, 60000)
			
		elif state == "Stop":
			print("Stop State")		

		elif state == "Exit":
			del database.databaseThermocoupleRegulation
			break
		else:
			print("Programmation error : This state is not implemented : "+state)

		Queue.task_done() # Indicate that a formerly enqueued task is complete


def StartThread():
	ThreadProcess = Thread(target=process, args=(Queue_Global.process_TemperatureRegulation,))
	ThreadProcess.setDaemon(False)
	ThreadProcess.start()