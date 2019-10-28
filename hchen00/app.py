from flask import Flask, render_template, request, session, redirect, url_for
import os
import sqlite3 
app = Flask(__name__)
DB_FILE="discobandit.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

app.secret_key = os.urandom(32)

db.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")

db.execute("CREATE TABLE IF NOT EXISTS posts (username TEXT, postID INTEGER ,verID INTEGER,title TEXT,content TEXT)")

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
    return True

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
                    return True
    return False

@app.route('/home')

def home():
    print(session)
    print('home')
    if "username" in session.keys():
        entries = []
        titles = []
        users = []
        number = 0
        for entry in c.execute("SELECT content FROM posts"):
            entries.append(''.join(entry))
            number+=1
        for title in c.execute("SELECT title FROM posts"):
            titles.append(''.join(title))
        for userns in c.execute("SELECT username FROM posts"):
            users.append(''.join(userns))
        entries.reverse()
        titles.reverse()
        users.reverse()
        print("Logged In: " + session['username'])
        return render_template("homepage.html",
                                                   user = session['username'],
                                                   usern = users,
                                                   title = titles,
                                                   entry = entries,
                                                   table = number)
    else:
        return redirect('/login')

@app.route('/profile')

def profile():
    print(session)
    print('profile')
    if "username" in session.keys():
        entries = []
        titles = []
        number = 0
        for entry in c.execute("SELECT content,username FROM posts"):
            if ''.join(entry[1]) == session['username']:
                entries.append(''.join(entry[0]))
                number+=1
        for title in c.execute("SELECT title,username FROM posts"):
            if ''.join(title[1]) == session['username']:
                titles.append(''.join(title[0]))
        entries.reverse()
        titles.reverse()
        print(entries)
        print(title)
        return render_template('profile.html', entry = entries, user = session['username'], title = titles, table = number)
    else:
        return redirect('/login')

def displayPost(user):
    q = "SELECT postID, verID, title, content FROM posts WHERE username ='" + str(user) + "';"
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
    final = "Welcome to " + user + """'s Blog!<br></br>"""
    for each in listofentries:
        final = final + each + """<br></br>"""
    return final

@app.route('/add')

def add():
    print(session)
    print('add')
    if 'username' in session.keys():
        return render_template('add.html', user = session['username'])

@app.route('/addE')

def createEntry():
    print(session)
    print('create entry')
    print(request.args['title'])
    print(request.args['entry'])
    if (addPost(session['username'], request.args['title'], request.args['entry'])):
        print("added post!")
        return redirect('/profile')
        
def addPost(username, title, content):
    foo = c.execute ("SELECT postID FROM posts;")
    counter = -1;
    for idx in foo:
        if idx[0] > counter:
            counter = idx[0]
    counter+=1
    c.execute("INSERT INTO posts VALUES ('" + username + "'," + str(counter) + ",1,'" + title + "','" + content + "');")
    db.commit()
    return True;

@app.route('/edit')
    return 

@app.route('/search')

def search():
    return render_template("results.html")

@app.route('/logout')

def logout():
    session.pop('username')
    session.pop('password')
    return redirect('/')

if __name__ == '__main__':
    app.debug = True
    DB_FILE="discobandit.db"
    db = sqlite3.connect('discobandit.db', check_same_thread=False)
    c = db.cursor() 
    app.run()
