import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O
import sys

DB_FILE="discobandit.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()

#basic function for searching for an item in a table and printing it out
def searchBlog(query):
    q = "SELECT average FROM stu_avg WHERE id =" + str(query) + ";"
    foo = c.execute(q)
    return str(foo.fetchall()[0])[1:-2]

#print(sys.argv[1])
#print(searchBlog(sys.argv[1]))

#basic function to check if password and username match
def checkCreds(user, passw):
    q = "SELECT password FROM users WHERE username ='" + str(user) + "';"
    foo = c.execute(q)
    return str(foo.fetchall()[0])[2:-3] == passw

# print(checkCreds('cchan00', 'oogabooga'))
# print(checkCreds('cchan00', 'oogaboogA'))
# print(checkCreds('cchan00', 'oogaboogaa'))
# print(checkCreds('cchan00', '1'))

#Print out the most recent blog post of a specific user
def displayPost(user):
    q = "SELECT postID, verID, content FROM posts WHERE username ='" + str(user) + "';"
    foo = c.execute(q)
    tuples = foo.fetchall()
    entries = []
    counter = 0
    for atuple in tuples:
        if atuple[0] < counter:
            entries[atuple[0]] = atuple[2]
        else:
            entries.append(atuple[2])
            counter += 1
    return entries

#print(displayPost('cchan00'))

#random comments for later
#need a timestamp for the post