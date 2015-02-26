import MySQLdb

# print all the first cell of all the rows
    #for row in cur.fetchall() :
    #    print row[0]

#db = MySQLdb.connect("localhost", "root", "", "PlashBoard")

class Database:

    def __init__(self, server, username, password, database):
        self.db = MySQLdb.connect(server, username, password, database)
        self.cur = self.db.cursor()

    def __del__(self):
        self.db.close()
        self.cur.close()

    def insertMeasure(self, hardwareConfigurationId, value):
        # Use all the SQL you like$
        try:
            for i in range(1,50) :
                self.cur.execute("INSERT INTO measure (hardwareConfigurationId, value, timestamp) VALUES (%s, %s, NOW())", (str(hardwareConfigurationId), str(value)))
            self.db.commit()
        except:
            self.db.rollback()

    def getUserCommand(self):


        self.cur.execute("SELECT * FROM userCommand WHERE done=0")
        result = self.cur.fetchall()
        self.db.commit()
        return result

    def userCommandDone(self, id):


        try:
            self.cur.execute("UPDATE userCommand SET done = 1 WHERE id="+str(id))
            self.db.commit()
        except:
            self.db.rollback()

    def updateUserConfiguration(self, id):


        try:
            self.cur.execute("UPDATE userCommand SET done = 1 WHERE id="+str(id))
            self.db.commit()
        except:
            self.db.rollback()


database = Database("localhost", "root", "", "PlashBoard")
