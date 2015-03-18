# To add a new process, copy/paste the following line and change the name of the Queue 
# process_Template = ProcessQueue(maxsize=0)



import Core.database

class Alert(object):

	def __init__(self, minAlert, maxAlert, hardwareConfigurationId, name, description):
		
		self.minAlert = minAlert
		self.maxAlert = maxAlert
		self.name = name
		self.description = description
		self.hardwareConfigurationId = hardwareConfigurationId


	def checkAndSendAlert(value):
		if(value > maxAlert):
			pass
		if(value < minAlert):
			pass
		
		

