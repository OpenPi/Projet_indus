# To add a new process, Copy/Paste/Rename the following line :
# import Process.Process_Template.Process_Template as Process_Template
# And start the new process by Copy/Paste/Rename : 
# Process_Template.StartThread()



import MySQLdb
from Queue import Queue
from threading import Thread



import Core.Queue_Global as Queue_Global
from Core.QueueItem import QueueItem
import Process.Process_UserCommand.Process_UserCommand as Process_UserCommand
import Process.Process_SensorsRead.Process_SensorsRead as Process_SensorsRead
import Process.Process_TemperatureRegulation.Process_TemperatureRegulation as Process_TemperatureRegulation
import Process.Process_Actuators.Process_Actuators as Process_Actuators
import Process.Process_Heater.Process_Heater as Process_Heater
import Process.Process_Pump.Process_Pump as Process_Pump
import Process.Process_Alert.Process_Alert as Process_Alert


# Process launch
Process_UserCommand.StartThread()
Process_SensorsRead.StartThread()
Process_Actuators.StartThread()
Process_TemperatureRegulation.StartThread()
Process_Heater.StartThread()
Process_Pump.StartThread()
Process_Alert.StartThread()

commande = ""

Queue_Global.process_UserCommand.enqueue('Process')
Queue_Global.process_SensorsRead.enqueue('Init')
Queue_Global.process_SensorsRead.enqueue('Process')
Queue_Global.process_Actuators.enqueue('Init')
Queue_Global.process_Heater.enqueue('Init')
Queue_Global.process_Pump.enqueue('Init')
Queue_Global.process_Alert.enqueue('Init')
Queue_Global.process_Alert.enqueue('Process')



while commande != "Exit":
    commande = raw_input("commande : ")
    if commande == "Exit":
        Queue_Global.process_UserCommand.enqueue('Exit')
        Queue_Global.process_SensorsRead.enqueue('Exit')
        Queue_Global.process_Actuators.enqueue('Exit')
        Queue_Global.process_TemperatureRegulation.enqueue('Exit')
	Queue_Global.process_Heater.enqueue('Exit')
	Queue_Global.process_Pump.enqueue('Exit')
	Queue_Global.process_Alert.enqueue('Exit')

