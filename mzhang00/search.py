import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O
import sys

DB_FILE="discobandit.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()

def searchBlog(query):
    q = "SELECT average FROM stu_avg WHERE id =" + str(query) + ";"
    foo = c.execute(q)
    return str(foo.fetchall()[0])[1:-2]

#print(sys.argv[1])
print(searchBlog(sys.argv[1]))

#def searchBlogArgs():
#    return searchBlog(sys.argv[1])

#print(searchBlogArgs)
