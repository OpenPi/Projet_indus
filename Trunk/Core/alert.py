# To add a new process, copy/paste the following line and change the name of the Queue 
# process_Template = ProcessQueue(maxsize=0)



import Core.database as database
from datetime import datetime, date, time, timedelta

class Alert(object):

	def __init__(self, userConfigurationName, name, description):
		
		self.userConfigurationName = userConfigurationName
		self.name = name
		self.description = description



	def checkAndSendAlert(self):
		try:
			minMaxConfiguration = database.databaseAlert.getUserConfiguration(self.userConfigurationName)
			minMax = minMaxConfiguration[4].split(':', 1 )
			minAlert = float(minMax[0])
			maxAlert = float(minMax[1])
			lastMeasure = database.databaseAlert.getLastMeasureByHardwareConfigurationId(minMaxConfiguration[2])
			timestamp = str(lastMeasure[2])
			value = lastMeasure[0]
			dateLastMeasure = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
			if(dateLastMeasure > datetime.now() + timedelta(days=-1)):	
				if(value > maxAlert):
				    database.databaseAlert.addAlertIfNotExist(self.name, self.description + ' too high', minMaxConfiguration[2])
			
				elif(value < minAlert):
				    database.databaseAlert.addAlertIfNotExist(self.name, self.description + ' too low', minMaxConfiguration[2])

		except:
			print("Last measure is too old to show alert")

