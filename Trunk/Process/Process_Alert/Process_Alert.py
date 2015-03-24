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
import Core.alert as alert

def process(Queue):

	while True:
		Item = Queue.get()
		state = Item.state
		data = Item.data
		
		if state == "Init":
			temperatureAlert = alert.Alert('temperature_alert_level', 'Temperature alert', 'The water\'s temperature is')
			phAlert = alert.Alert('ph_alert_level', 'Ph alert', 'The water\'s ph is')
			waterLevelAlert = alert.Alert('water_level_alert', 'Water\'s level  alert', 'The water\'s level is')

		elif state == "Start":
			print("Start State")	

		elif state == "Process":
	
			temperatureAlert.checkAndSendAlert()
			phAlert.checkAndSendAlert()
			waterLevelAlert.checkAndSendAlert()
			Queue.enqueueIfEmpty(state, data, 1000)
			
		elif state == "Stop":
			print("Stop State")		

		elif state == "Exit":

			break
		else:
			print("Programmation error : This state is not implemented : "+state)

		Queue.task_done() # Indicate that a formerly enqueued task is complete


def StartThread():
	ThreadProcess = Thread(target=process, args=(Queue_Global.process_Alert,))
	ThreadProcess.setDaemon(False)
	ThreadProcess.start()
