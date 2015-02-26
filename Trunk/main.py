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




# Process launch
Process_UserCommand.StartThread()


commande = ""


while commande != "Exit":
	commande = raw_input("commande : ")
	Queue_Global.process_UserCommand.enqueue(commande, 33)


