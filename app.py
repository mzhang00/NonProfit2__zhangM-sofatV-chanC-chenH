from flask import Flask, render_template, request, session, redirect, url_for, flash
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
    if (enteredU == ""):
        return redirect(url_for("error", msge = "please enter a non-empty username"))
    if (enteredP == ""):
        return redirect(url_for("error", msge = "please enter a non-empty password"))
    if (addUser(enteredU,enteredP)):
        print("add user: " + enteredU + " , " + enteredP)
        return redirect(url_for('loginE', msge = "Signed up succesfully!"))
    else:
        return redirect(url_for("error", msge = "username in use"))

def addUser(username,password):
    foo = c.execute ("SELECT username FROM users;")
    for uName in foo:
        if uName[0] == username:
            return False
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
        flash('You were successfully logged in!')
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
        foo = c.execute("SELECT postID FROM posts")
        for li in foo:
            if li[0] + 1 > number:
                number = li[0] + 1
        for i in range(0,number):
            line = getMostRecent(c, i)
            print(line)
            if (line != -1):
                entries.append(line[4])
                titles.append(line[3])
        entries.reverse()
        titles.reverse()
        print(entries)
        print(titles)
        return render_template('profile.html', entry = entries, user = session['username'], title = titles, table = number)
    else:
        return redirect('/login')

def getMostRecent(c, postID):
    temp = c.execute("SELECT * FROM posts WHERE postID = " + str(postID) + ";")
    ID = -1
    for li in temp:
        if li[2] > ID:
            ID = li[2]
    temp2 = c.execute("SELECT * FROM posts WHERE postID = " + str(postID) + ";")
    for mi in temp2:
        if mi[2] == ID:
            return li
    return -1


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
    counter = -1
    for idx in foo:
        if idx[0] > counter:
            counter = idx[0]
    counter+=1
    c.execute("INSERT INTO posts VALUES ('" + username + "'," + str(counter) + ",1,'" + title + "','" + content + "');")
    db.commit()
    return True

@app.route('/edit')

def edit():
    idx = int(request.args['numPosts']) - int(request.args['idx']) - 1
    print("edit init")
    print("old values : " +  request.args['oldTitle'] +" ," + request.args['oldContent'])
    return render_template('edit.html', postID = idx, oldTitle = request.args['oldTitle'], oldContent = request.args['oldContent'])

@app.route('/editE')

def editEntry():
    print(session)
    print("edit entry")
    if "username" in session.keys():
        if (editPost(session["username"], request.args['postID'], request.args['title'], request.args['entry'])):
            print("edited post!")
    return redirect('/profile')

def editPost(username,postID,title,content):
    foo = c.execute ("SELECT verID from posts WHERE postID = " + str(postID) + ";")
    counter = -1
    for idx in foo:
        if idx[0] > counter:
            counter = idx[0]
    if counter == -1:
        return addPost(username,title,content)
    counter+=1
    c.execute("INSERT INTO posts VALUES ('" + username + "'," + str(postID) + "," + str(counter) + ",'" + title + "','" + content + "');")
    db.commit()
    return True


@app.route('/search')

def search():
    query = request.args['search']
    searchType = request.args['type']
    print("Search")
    print(request.args)
    entries = []
    titles = []
    users = []
    ents = []
    tits = []
    uses = []
    number = 0
    msg = ''
    for entry in c.execute("SELECT content FROM posts"):
        entries.append(''.join(entry))
    for title in c.execute("SELECT title FROM posts"):
        titles.append(''.join(title))
    for userns in c.execute("SELECT username FROM posts"):
        users.append(''.join(userns))
    entries.reverse()
    titles.reverse()
    users.reverse()
    length = len(users)
    if searchType == 'userSearch':
        for x in range(length):
            if query in users[x]:
                uses.append(users[x])
                tits.append(titles[x])
                ents.append(entries[x])
                number+=1
    if searchType == 'titleSearch':
        for x in range(length):
            if query in titles[x]:
                uses.append(users[x])
                tits.append(titles[x])
                ents.append(entries[x])
                number+=1
    if searchType == 'entrySearch':
        for x in range(length):
            if query in entries[x]:
                uses.append(users[x])
                tits.append(titles[x])
                ents.append(entries[x])
                number+=1
    if number == 0:
        msg = 'No results for "' + query + '"'
    return render_template("results.html",
                           usern=uses,
                           title = tits,
                           entry = ents,
                           table = number,
                           msge = msg)

@app.route('/logout')

def logout():
    print("logging out: ")
    session.pop('username')
    session.pop('password')
    flash('You were successfully logged out!')
    return redirect('/')

if __name__ == '__main__':
    app.debug = True
    DB_FILE="discobandit.db"
    db = sqlite3.connect('discobandit.db', check_same_thread=False)
    c = db.cursor()
    app.run()
