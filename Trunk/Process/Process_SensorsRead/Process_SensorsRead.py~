# templateSensorConfig = database.databaseSensorsRead.getHardwareConfigurationByName("Template sensor name")	
# templateSensor = TemplateSensor(templateSensorConfig[0],templateSensorConfig[2], 4.14, 60, 2)

from Queue import Queue
from threading import Thread

import Core.Queue_Global as Queue_Global
from Core.QueueItem import QueueItem
import Core.database as database
from Core.sensor import *

def process(Queue):

	while True:
		Item = Queue.get()
		state = Item.state
		data = Item.data
		if state == "Init":
			numberOfSecond = 59
			
			# get the hardware configurations
			poolThermocoupleConfig = database.databaseSensorsRead.getHardwareConfigurationByName("Pool Temperature Sensor")			
			pumpAmpereMeterConfig = database.databaseSensorsRead.getHardwareConfigurationByName("Pump Ampere Meter")
			poolPhConfig = database.databaseSensorsRead.getHardwareConfigurationByName("Pool Ph Meter")			
			waterLevelConfig = database.databaseSensorsRead.getHardwareConfigurationByName("Water Level Sensor")

			#Instance the sensors
			poolThermocouple = Thermocouple(poolThermocoupleConfig[0],poolThermocoupleConfig[2], 4.14, 60, 2, float(database.databaseSensorsRead.getUserConfigurationValue("temperature_offset")))
			pumpAmpereMeter = AmpereMeter(pumpAmpereMeterConfig[0],pumpAmpereMeterConfig[2], 4.14, 60, 2, float(database.databaseSensorsRead.getUserConfigurationValue("installation_tension")))
			poolPhMeter = PhMeter(poolPhConfig[0],poolPhConfig[2], 4.14, 60, 2, float(database.databaseSensorsRead.getUserConfigurationValue("ph_offset")))
			waterLevelMeter = WaterLevelMeter(waterLevelConfig[0],waterLevelConfig[2], 4.14, 60, 2)


		elif state == "Start":
			print("Start State")	

		elif state == "Process":

			if(numberOfSecond > 1):
				
				poolThermocouple.read_save(numberOfSecond)# Read and save the sensor value
				pumpAmpereMeter.read_save(numberOfSecond)
				poolPhMeter.read_save(numberOfSecond)
				waterLevelMeter.read_save(numberOfSecond)
				numberOfSecond = numberOfSecond - 1
				
			else:
				numberOfSecond = 60
			
			Queue.enqueueIfEmpty(state, data, 1000)
			
		elif state == "Stop":
			print("Stop State")		

		elif state == "Exit":
			del poolThermocouple
			del pumpAmpereMeter
			del poolPhMeter
			del database.databaseSensorsRead
			break
		else:
			print("Programmation error : This state is not implemented : "+state)

		Queue.task_done() # Indicate that a formerly enqueued task is complete


def StartThread():
	ThreadProcess = Thread(target=process, args=(Queue_Global.process_SensorsRead,))
	ThreadProcess.setDaemon(False)
	ThreadProcess.start()
