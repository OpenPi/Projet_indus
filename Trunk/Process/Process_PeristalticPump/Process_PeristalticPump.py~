# To add a new process, follow instructions :
# Copy/Paste/rename Process_template folder
# Go to Trunk/Core/Queue_Global.py and follow instructions
# Go to Trunk/main.py and follow instructions
# Rename Process name in StartThread function


from Queue import Queue
from threading import Thread

import Core.Queue_Global as Queue_Global
from Core.QueueItem import QueueItem
from Core.actuator import PeristalticPump 
import Core.database as database

def process(Queue):

	while True:
		Item = Queue.get()
		state = Item.state
		data = Item.data
		if state == "Init":
			poolperistalticPumpConfig = database.databasePeristalticPump.getHardwareConfigurationByName("Peristaltic pump")
			peristalticPump = PeristalticPump(poolperistalticPumpConfig[0],poolperistalticPumpConfig[2], False)
		elif state == "Start":
			print("Start State")	

		elif state == "Process":
			pass
			
		elif state == "Stop":
			print("Stop State")

		elif state == "on":			
			peristalticPump.set_value(True)		

		elif state == "off":
			peristalticPump.set_value(False)
		#elif state == "auto":
		#	print("Peristaltic Auto State")
		#	peristalticPump.set_mode_auto()
		#	Queue_Global.PeristalticPump.enqueue('Process')
		#elif state == "setPumpDecision":
		#	peristalticPump.set_pump_decision(data)	
		#	Queue_Global.PeristalticPump.enqueue('Process')
		

		elif state == "Exit":

			break
		else:
			print("Programmation error : This state is not implemented : "+state)

		Queue.task_done() # Indicate that a formerly enqueued task is complete


def StartThread():
	ThreadProcess = Thread(target=process, args=(Queue_Global.process_PeristalticPump,))
	ThreadProcess.setDaemon(False)
	ThreadProcess.start()
