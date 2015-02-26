# To add a new process, Copy/Paste/Rename the following line :
# import Process.Process_Template.Process_Template as Process_Template
# And start the new process by Copy/Paste/Rename : 
# Process_Template.StartThread()



import MySQLdb
from Queue import Queue
from threading import Thread


from Core.pref import preferences

import Core.Queue_Global as Queue_Global
from Core.QueueItem import QueueItem
import Process.Process_UserCommand.Process_UserCommand as Process_UserCommand
import Process.Process_SensorsRead.Process_SensorsRead as Process_SensorsRead




# Process launch
Process_UserCommand.StartThread()
Process_SensorsRead.StartThread()

commande = ""

Queue_Global.process_UserCommand.enqueue('Process')
Queue_Global.process_SensorsRead.enqueue('Process')

while commande != "Exit":
    commande = raw_input("commande : ")
    if commande == "Exit":
        Queue_Global.process_UserCommand.enqueue('Exit')
        Queue_Global.process_SensorsRead.enqueue('Exit')


