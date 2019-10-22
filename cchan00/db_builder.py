
import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O


DB_FILE="discobandit.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

db.execute("CREATE TABLE IF NOT EXISTS users (username,password)")

db.execute("CREATE TABLE IF NOT EXISTS posts (username,posID,verID,content)")



db.commit() #save changes
db.close()  #close database
