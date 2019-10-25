from flask import Flask, render_template, request, session
import os
import sqlite3 
app = Flask(__name__)

app.secret_key = os.urandom(32)

@app.route('/')
def root():
    if "username" in session.keys():
        print("Logged In: " + session['username'])
        return render_template("welcome.html", user = session['username'])
    else:
        return render_template("login.html", msg = "")


@app.route('/auth')
def auth():
    enteredU = request.args['username']
    enteredP = request.args['password']
    if (userValid(enteredU,enteredP)):
        session['username'] = enteredU
        session['password'] = enteredP
        return render_template("welcome.html", user = session['username'])
    else:
        return render_template("loginFailed.html")

@app.route('/signup')
def signUp():
    return render_template("signup.html")

    
@app.route('/signupCheck')
def signupCheck():
    enteredU = request.args['username']
    enteredP = request.args['password']
    if (addUser(enteredU,enteredP)):
        print("add user: " + enteredU + " , " + enteredP)
        return render_template("login.html", msg = "Signed up succesfully!")
    
    else:
        return render_template("signup.html", msg = "username in use")

    


@app.route('/signedUp')
def signedUp():
    #addUser(request.args[username],request.args[password])
    return render_template("signedUp.html")



def addUser(username,password):
    foo = c.execute ("SELECT username FROM users;")
    for uName in foo:
        if uName[0] == username:
            return False;
    c.execute("INSERT INTO users VALUES ('" + username + "','" + password + "')")
    print("insert into users")
    db.commit()
    return True;

def addPost(username,content):
    foo = c.execute ("SELECT postID FROM posts;")
    counter = -1;
    for idx in foo:
        if idx[0] > counter:
            counter = idx[0]
            counter+=1
            c.execute("INSERT INTO posts VALUES ('" + username + "'," + str(counter) + ",0,'" + content + "');")
            db.commit()
    return True;

def editPost(username,postID,content):
    foo = c.execute ("SELECT verID from posts WHERE postID = " + str(postID) + ";")
    counter = -1;
    for idx in foo:
        if idx[0] > counter:
            counter = idx[0]
    if counter == -1:
        return addPost(username,content)
    counter+=1;
    c.execute("INSERT INTO posts VALUES ('" + username + "'," + str(postID) + "," + str(counter) + ",'" + content + "');")
    db.commit()
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




if __name__ == '__main__':
    app.debug = True
    DB_FILE="discobandit.db"
    db = sqlite3.connect('discobandit.db', check_same_thread=False)
    c = db.cursor() 
    app.run()
