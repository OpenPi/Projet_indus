import MySQLdb



class Database:

    def __init__(self, server, username, password, database):
        self.db = MySQLdb.connect(server, username, password, database)

    def __del__(self):
        self.db.close()

    def insertMeasure(self, hardwareConfigurationId, value):
        # Use all the SQL you like$
        try:

	    cur = self.db.cursor()
            cur.execute("INSERT INTO measure (hardwareConfigurationId, value, timestamp) VALUES (%s, %s, NOW())", (str(hardwareConfigurationId), str(value)))
            self.db.commit()
	    cur.close()
        except:
            self.db.rollback()

    def getUserCommand(self):
	
	cur = self.db.cursor()
        cur.execute("SELECT * FROM usercommand WHERE done=0")
        result = cur.fetchall()
	self.db.commit()
	cur.close()
        return result

    def userCommandDone(self, id):


        try:

	    cur = self.db.cursor()
            cur.execute("UPDATE usercommand SET done = 1 WHERE id="+str(id))
            self.db.commit()
	    cur.close()
        except:
            self.db.rollback()

    def updateUserConfiguration(self, name, value):

        try:
	    cur = self.db.cursor()
            cur.execute("UPDATE userconfiguration SET value = '" + str(value) + "' WHERE name='"+str(name)+"'")
            self.db.commit()
	    cur.close()
        except:
            self.db.rollback()

    def getUserConfiguration(self, name):

	cur = self.db.cursor()
	try:
        	cur.execute("SELECT * FROM userconfiguration WHERE name='"+name+"' LIMIT 1")
        	result = cur.fetchone()
		self.db.commit()
		cur.close()
		return result[4]
	except:
   	    print "Error: unable to fecth data"
	    return 0	


    def getHardwareConfigurationByName(self, name):

	cur = self.db.cursor()
	try:
        	cur.execute("SELECT * FROM hardwareconfiguration WHERE name='"+name+"' LIMIT 1")
        	result = cur.fetchone()
		self.db.commit()
		cur.close()
		return result
	except:
   	    print "Error: unable to fecth data"
	    return 0	


    def getLastMeasureByName(self, name):

	cur = self.db.cursor()
        cur.execute("SELECT measure.value, hardwareconfiguration.name FROM measure INNER JOIN hardwareconfiguration ON measure.hardwareConfigurationId = hardwareconfiguration.Id WHERE name = '"+ name +"' ORDER BY timestamp DESC")
        result = cur.fetchone()


	self.db.commit()
	cur.close()

        return result[0]

databaseSensorsRead = Database("localhost", "root", "root", "plashboard")
databaseActuators = Database("localhost", "root", "root", "plashboard")
databaseUserCommand = Database("localhost", "root", "root", "plashboard")
databaseThermocoupleRegulation = Database("localhost", "root", "root", "plashboard")
databaseHeater = Database("localhost", "root", "root", "plashboard")
databasePump = Database("localhost", "root", "root", "plashboard")
databaseAlert = Database("localhost", "root", "root", "plashboard")
