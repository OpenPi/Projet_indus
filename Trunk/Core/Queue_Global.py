# To add a new process, copy/paste the following line and change the name of the Queue 
# process_Template = ProcessQueue(maxsize=0)


from Queue import Queue
from Core.QueueItem import QueueItem
import time
import Core.database
class ProcessQueue(Queue, object):

	def __init__(self, maxsize = 0):
		super(ProcessQueue, self).__init__()
        
	def enqueue(self, state, data):
		self.put(QueueItem(state, data))

	def enqueueIfEmpty(self, state, data,timeoutMs):
		time.sleep(timeoutMs/1000)
		if(self.empty()):
			self.enqueue(state,data)

process_UserCommand = ProcessQueue(maxsize=0)
