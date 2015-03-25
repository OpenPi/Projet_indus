# To add a new process, follow instructions :
# Copy/Paste/rename Process_template folder
# Go to Trunk/Core/Queue_Global.py and follow instructions
# Go to Trunk/main.py and follow instructions
# Rename Process name in StartThread function


from Queue import Queue
from threading import Thread

import Core.Queue_Global as Queue_Global
from Core.QueueItem import QueueItem
import Core.PhRegulation as PhRegulation

def process(Queue):
	phRegulation = PhRegulation.PhRegulation()
	while True:
		Item = Queue.get()
		state = Item.state
		data = Item.data
		if state == "Init":
			print("Init State")

		elif state == "Start":
			print("Start State")	

		elif state == "Process":
			#print("Process State")		

			#Calculate time to find index to check

			indexProcess = (date.now().hour*60 + date.now().minute)/PhRegulation.precision

			#Check decision and start or stop pump
			if(phRegulation.pumpDecision[indexProcess] == 1):
				Queue_Global.PeristalticPump.enqueue('on')
					
			else:
				Queue_Global.PeristalticPump.enqueue('off')

			Queue.enqueueIfEmpty(state, data, 1000)
			#print(pumpDecision[indexProcess])
			#indexProcess += 1

			
			#Test without time
			
		elif state == "Stop":
			print("Stop State")		

		elif state == "Exit":

			break
		else:
			print("Programmation error : This state is not implemented : "+state)

		Queue.task_done() # Indicate that a formerly enqueued task is complete


def StartThread():
	ThreadProcess = Thread(target=process, args=(Queue_Global.process_Template,))
	ThreadProcess.setDaemon(False)
	ThreadProcess.start()
