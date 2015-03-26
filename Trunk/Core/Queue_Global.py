# To add a new process, copy/paste the following line and change the name of the Queue 
# process_Template = ProcessQueue(maxsize=0)


from Queue import Queue
from Core.QueueItem import QueueItem
import time
import Core.database
class ProcessQueue(Queue, object):

	def __init__(self, maxsize = 0):
		super(ProcessQueue, self).__init__()
        
	def enqueue(self, state, data= False):#Enqueue an element
		self.put(QueueItem(state, data))

	def enqueueIfEmpty(self, state, data = False, timeoutMs = 1000): #Enqueue the element if the queue is empty.

		numberOfSeconds = timeoutMs/1000 # Number Of seconds to wait before timeout
		while(numberOfSeconds > 0 and self.empty()):
			if(numberOfSeconds >= 1):
				time.sleep(1)
			else:
				time.sleep(numberOfSeconds)
				
			numberOfSeconds = numberOfSeconds - 1
		if(self.empty()):
			self.enqueue(state,data)

#Declare The Process Queues
process_UserCommand = ProcessQueue(maxsize=0)
process_SensorsRead = ProcessQueue(maxsize=0)
process_Light = ProcessQueue(maxsize=0)
process_TemperatureRegulation = ProcessQueue(maxsize=0)
process_Heater = ProcessQueue(maxsize=0)
process_Pump = ProcessQueue(maxsize=0)
process_Alert = ProcessQueue(maxsize=0)
process_PeristalticPump = ProcessQueue(maxsize=0)
process_PhRegulation = ProcessQueue(maxsize=0)
process_RTC = ProcessQueue(maxsize=0)
