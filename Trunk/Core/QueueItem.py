class QueueItem:
	""" Define Items that will be send in Queues by :
			- A State
			- A Data
	"""
	def __init__(self, state, data):
		self.state = state
		self.data = data