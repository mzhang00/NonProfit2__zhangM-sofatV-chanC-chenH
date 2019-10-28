from flask import Flask, render_template, request, session, redirect, url_for
import os
import sqlite3 
app = Flask(__name__)
DB_FILE="discobandit.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

app.secret_key = os.urandom(32)

db.execute("CREATE TABLE IF NOT EXISTS users (username,password)")

db.execute("CREATE TABLE IF NOT EXISTS posts (username,postID,verID,title,content)")

##@app.route('/')
##def root():
##    if "username" in session.keys():
##        print("Logged In: " + session['username'])
##        return render_template("welcome.html", user = session['username'])
##    else:
##        return render_template("login.html", msg = "")
##
##@app.route('/auth')
##def auth():
##    enteredU = request.args['username']
##    enteredP = request.args['password']
##    if (userValid(enteredU,enteredP)):
##        session['username'] = enteredU
##        session['password'] = enteredP
##        return render_template("welcome.html", user = session['username'])
##    else:
##        return render_template("loginFailed.html")
##
##@app.route('/signup')
##def signUp():
##    return render_template("signup.html")
##
##@app.route('/signupCheck')
##def signupCheck():
##    enteredU = request.args['username']
##    enteredP = request.args['password']
##    if (addUser(enteredU,enteredP)):
##        print("add user: " + enteredU + " , " + enteredP)
##        return render_template("login.html", msg = "Signed up succesfully!")
##    
##    else:
##        return render_template("signup.html", msg = "username in use")
##
##@app.route('/signedUp')
##def signedUp():
##    #addUser(request.args[username],request.args[password])
##    return render_template("signedUp.html")
##
##def addUser(username,password):
##    foo = c.execute ("SELECT username FROM users;")
##    for uName in foo:
##        if uName[0] == username:
##            return False;
##    c.execute("INSERT INTO users VALUES ('" + username + "','" + password + "')")
##    print("insert into users")
##    db.commit()
##    return True;
##
##def addPost(username,content):
##    foo = c.execute ("SELECT postID FROM posts;")
##    counter = -1;
##    for idx in foo:
##        if idx[0] > counter:
##            counter = idx[0]
##            counter+=1
##            c.execute("INSERT INTO posts VALUES ('" + username + "'," + str(counter) + ",0,'" + content + "');")
##            db.commit()
##    return True;
##
##def editPost(username,postID,content):
##    foo = c.execute ("SELECT verID from posts WHERE postID = " + str(postID) + ";")
##    counter = -1;
##    for idx in foo:
##        if idx[0] > counter:
##            counter = idx[0]
##    if counter == -1:
##        return addPost(username,content)
##    counter+=1;
##    c.execute("INSERT INTO posts VALUES ('" + username + "'," + str(postID) + "," + str(counter) + ",'" + content + "');")
##    db.commit()
##    return True
##
##
##def userValid(username,password):
##    foo = c.execute ("SELECT username FROM users;")
##    for uName in foo:
##        if uName[0] == username:
##            boo = c.execute("SELECT password FROM users WHERE username = '" + username + "';")
##            for passW in boo:
##                if (passW[0] == password):
##                    return True;
##    return False;

@app.route('/')

def root():
    return render_template('welcome.html')

@app.route('/login')

def login():
     return render_template("auth.html", msg = '')

@app.route('/login/<string:msge>')

def loginE(msge = ''):
    return render_template("auth.html", msg = msge)

@app.route('/error/<string:msge>')

def error(msge = ''):
    return render_template("error.html", msg = msge)

@app.route('/signup')

def signup():
    return render_template("create.html")

@app.route('/create')

def create():
    enteredU = request.args['username']
    enteredP = request.args['password']
    if (addUser(enteredU,enteredP)):
        print("add user: " + enteredU + " , " + enteredP)
        return redirect(url_for('loginE', msge = "Signed up succesfully!"))
    else:
        return redirect(url_for("error", msge = "username in use"))
    
def addUser(username,password):
    foo = c.execute ("SELECT username FROM users;")
    for uName in foo:
        if uName[0] == username:
            return False;
    c.execute("INSERT INTO users VALUES ('" + username + "','" + password + "')")
    print("insert into users")
    db.commit()
    return True;

@app.route('/auth')

def auth():
    enteredU = request.args['username']
    enteredP = request.args['password']
    if (userValid(enteredU,enteredP)):
        session['username'] = enteredU
        session['password'] = enteredP
        return redirect('/home')
    else:
        return redirect(url_for('error', msge = "login failed"))

def userValid(username,password):
    foo = c.execute ("SELECT username FROM users;")
    for uName in foo:
        if uName[0] == username:
            boo = c.execute("SELECT password FROM users WHERE username = '" + username + "';")
            for passW in boo:
                if (passW[0] == password):
                    return True;
    return False;

@app.route('/home')

def home():
    if "username" in session.keys():
        print("Logged In: " + session['username'])
        return render_template("homepage.html", user = session['username'])
    else:
        return redirect('/login')

@app.route('/profile')

def profile():
    if "username" in session.keys():
        e = renderPosts(displayPost(session['username']), session['username'])
        return render_template('profile.html', entry = e)
    else:
        return redirect('/login')

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
    entries.reverse()
    return entries

def renderPosts(listofentries, user):
    final = "Welcome to " + user + """'s Blog!<br><br>"""
    for each in listofentries:
        final = final + each + """<br><br>"""
    return final

@app.route('/add')

def add():
    return render_template('add.html')

@app.route('/addE')

def create():
    if (addPost(session['username'], request.args['title'], request.args['entry'])):
        return redirect('/profile')
        
def addPost(username, title, content):
    foo = c.execute ("SELECT postID FROM posts;")
    counter = -1;
    for idx in foo:
        if idx[0] > counter:
            counter = idx[0]
            counter+=1
            c.execute("INSERT INTO posts VALUES ('" + username + "'," + str(counter) + ",0,'" + title +  content + "');")
            db.commit()
    return True;

@app.route('/search')

def search():
    return render_template("results.html")

@app.route('/logout')

def logout():
    session.pop('username')
    return redirect('/')

if __name__ == '__main__':
    app.debug = True
    DB_FILE="discobandit.db"
    db = sqlite3.connect('discobandit.db', check_same_thread=False)
    c = db.cursor() 
    app.run()
