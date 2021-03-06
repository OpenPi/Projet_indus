# To add a new process, follow instructions :
# Copy/Paste/rename Process_template folder
# rename Process_Template.py
# Go to Trunk/Core/Queue_Global.py and follow instructions
# Go to Trunk/main.py and follow instructions
# Rename Process name in StartThread function (Queue_Global.YOUR_NEW_PROCESS)


from Queue import Queue
from threading import Thread

import Core.Queue_Global as Queue_Global
from Core.QueueItem import QueueItem

import Core.database as database

def process(Queue):

	while True:
		Item = Queue.get()
		state = Item.state
		data = Item.data
		if state == "Init":
			print("Init State")

		elif state == "Start":
			print("Start State")	

		elif state == "Process":
			userCommand = database.databaseUserCommand.getUserCommand()
			for row in userCommand :

				command(row[1], row[2], row[3], row[4])
				database.databaseUserCommand.userCommandDone(row[0])

			Queue.enqueueIfEmpty(state, data, 1000)

		elif state == "Stop":
			print("Stop State")		

		elif state == "Exit":
			del database.databaseUserCommand
			break
		else:
			print("Programmation error : This state is not implemented : "+state)

		Queue.task_done() # Indicate that a formerly enqueued task is complete


def StartThread():
	ThreadProcess = Thread(target=process, args=(Queue_Global.process_UserCommand,))
	ThreadProcess.setDaemon(False)
	ThreadProcess.start()

def command(type, command, targetName, value): # Handle the user command
	if(type == 'Actuators'):
		if(targetName == 'light'):
			Queue_Global.process_Light.enqueue(targetName, value)
		elif(targetName == 'pump'):
			Queue_Global.process_Pump.enqueue(value)
		elif(targetName == 'peristalticPump'):
			Queue_Global.process_PeristalticPump.enqueue(value)
	elif(type == 'UserConfiguration'):

		if(targetName == 'ph_setpoint'
		or targetName == 'temperature_setpoint'
		or targetName == 'temperature_setpoint'
		or targetName == 'temperature_alert_level' 
		or targetName == 'ph_alert_level' 
		or targetName == 'ph_offset'
		or targetName == 'pool_volume'
		or targetName == 'power_heat_pump'
		or targetName == 'water_level_alert'
		or targetName == 'peristaltic_pump_debit'
		or targetName == 'installation_tension'
		or targetName == 'temperature_offset'
		or targetName == 'pumping_hours'):
			
			database.databaseUserCommand.updateUserConfiguration(targetName, value)
		else:
			print('Database Error')
	else:
		print('Database Error')
