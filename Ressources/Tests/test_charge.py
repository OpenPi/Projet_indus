import MySQLdb
import time

db = MySQLdb.connect("localhost", "root", "", "PlashBoard")

cur = db.cursor() 


debut = time.time()

# Use all the SQL you like$
try:
    for i in range(1,50) :
        cur.execute("INSERT INTO measure (hardwareConfigurationId, value, timestamp) VALUES (%s, %s, NOW())", ("3","2.4"))
    db.commit()
except:
    db.rollback()


# Use all the SQL you like
#cur.execute("SELECT * FROM measure ")

# print all the first cell of all the rows
#for row in cur.fetchall() :
#    print row[0]

fin = time.time()

print "%f secondes" % (fin-debut, )

db.close()