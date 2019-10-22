
import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O



def addUser(username,password):
    foo = c.execute ("SELECT username FROM users;")
    for uName in foo:
        if uName[0] == username:
            return False;
    c.execute("INSERT INTO users VALUES ('" + username + "','" + password + "')")
    return True;

def addPost(username,content):
    foo = c.execute ("SELECT posID FROM posts;")
    counter = -1;
    for idx in foo:
        if idx[0] > counter:
            counter = idx[0]
    counter+=1
    c.execute("INSERT INTO posts VALUES ('" + username + "'," + str(counter) + ",0,'" + content + "');")
    return True;
    
def editPost(username,postID,content):
    foo = c.execute ("SELECT verID from posts WHERE posID = " + str(postID) + ";")
    counter = -1;
    for idx in foo:
        if idx[0] > counter:
            counter = idx[0]
    if counter == -1:
        return addPost(username,content)
    counter+=1;
    c.execute("INSERT INTO posts VALUES ('" + username + "'," + str(postID) + "," + str(counter) + ",'" + content + "');")
    return True
    

def userValid(username,password):
    foo = c.execute ("SELECT username FROM users;")
    for uName in foo:
        if uName[0] == username:
            boo = c.execute("SELECT password FROM users WHERE username = '" + username + "';")
            for passW in boo:
                if (passW[0] == password):
                    return True;
    return False;



DB_FILE="discobandit.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops


print (userValid("cchan00","K"))


db.commit() #save changes
db.close()  #close database










