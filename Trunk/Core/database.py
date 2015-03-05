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
        cur.execute("SELECT * FROM userCommand WHERE done=0")
        result = cur.fetchall()
	cur.close()
        return result

    def userCommandDone(self, id):


        try:

	    cur = self.db.cursor()
            cur.execute("UPDATE userCommand SET done = 1 WHERE id="+str(id))
            self.db.commit()
	    cur.close()
        except:
            self.db.rollback()

    def updateUserConfiguration(self, id):


        try:

	    cur = self.db.cursor()
            cur.execute("UPDATE userCommand SET done = 1 WHERE id="+str(id))
            self.db.commit()
	    cur.close()
        except:
            self.db.rollback()

    def getHardwareConfigurationByName(self, name):

	cur = self.db.cursor()
	try:
        	cur.execute("SELECT * FROM hardwareConfiguration WHERE name='"+name+"' LIMIT 1")
        	result = cur.fetchone()
		cur.close()
		return result
	except:
   	    print "Error: unable to fecth data"
	    return 0	


	



        

    def getLastMeasureByName(self, name):
	print("getLastMeasureByName")
	cur = self.db.cursor()
        cur.execute("SELECT measure.value, hardwareConfiguration.name FROM measure INNER JOIN hardwareConfiguration ON measure.hardwareConfigurationId = hardwareConfiguration.Id WHERE name = '"+ name +"' LIMIT 1")
        result = cur.fetchone()
	cur.close()

        return result[0]

databaseSensorsRead = Database("localhost", "root", "root", "PlashBoard")
databaseActuators = Database("localhost", "root", "root", "PlashBoard")
databaseUserCommand = Database("localhost", "root", "root", "PlashBoard")
databaseThermocoupleRegulation = Database("localhost", "root", "root", "PlashBoard")
