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
import Process.Process_Light.Process_Light as Process_Light
import Process.Process_Heater.Process_Heater as Process_Heater
import Process.Process_Pump.Process_Pump as Process_Pump
import Process.Process_Alert.Process_Alert as Process_Alert
import Process.Process_PeristalticPump.Process_PeristalticPump as Process_PeristalticPump
import Process.Process_PhRegulation.Process_PhRegulation as Process_PhRegulation
import Process.Process_RTC.Process_RTC as Process_RTC

# Process launch
Process_UserCommand.StartThread()
Process_SensorsRead.StartThread()
Process_Light.StartThread()
Process_TemperatureRegulation.StartThread()
Process_Heater.StartThread()
Process_Pump.StartThread()
Process_Alert.StartThread()
Process_PeristalticPump.StartThread()
Process_RTC.StartThread()
Process_PhRegulation.StartThread()

commande = ""

#Init
Queue_Global.process_UserCommand.enqueue('Process')
Queue_Global.process_SensorsRead.enqueue('Init')
Queue_Global.process_SensorsRead.enqueue('Process')
Queue_Global.process_Light.enqueue('Init')
Queue_Global.process_Heater.enqueue('Init')
Queue_Global.process_Pump.enqueue('Init') #this process call Ph Regulation
Queue_Global.process_Alert.enqueue('Init')
Queue_Global.process_Alert.enqueue('Process')
Queue_Global.process_PeristalticPump.enqueue('Init')
Queue_Global.process_RTC.enqueue('Init')

print("PlashBoard........................Init")

while commande != "Exit":
    commande = raw_input("")
    if commande == "Exit":
        Queue_Global.process_UserCommand.enqueue('Exit')
        Queue_Global.process_SensorsRead.enqueue('Exit')
        Queue_Global.process_Light.enqueue('Exit')
        Queue_Global.process_TemperatureRegulation.enqueue('Exit')
	Queue_Global.process_Heater.enqueue('Exit')
	Queue_Global.process_Pump.enqueue('Exit')
	Queue_Global.process_Alert.enqueue('Exit')
	Queue_Global.process_PeristalticPump.enqueue('Exit')
	Queue_Global.process_RTC.enqueue('Exit')
	Queue_Global.process_PhRegulation.enqueue('Exit')

