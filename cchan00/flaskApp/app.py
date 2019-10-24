from flask import Flask, render_template, request, session
import os
app = Flask(__name__)

app.secret_key = os.urandom(32)

@app.route('/')
def root():
    if "username" in session.keys():
        print("Logged In: " + session['username'])
        return render_template("welcome.html", userName = session['username'])
    else:
        return render_template("login.html", msg = "")


@app.route('/signupCheck')
def signupCheck():
    enteredU = request.args['username']
    enteredP = request.args['password']
    '''
    if (addUser(enteredU,enteredP)):
        return render_template("login.html", msg = Signed up succesfully!")
    '''

@app.route('/loginCheck')
def loginCheck():
    enteredU = request.args['username']
    enteredP = request.args['password']
    '''
    if (userValid(enteredU,enteredP)):
        return render_template("welcome.html")
    else:
        return render_teamplate("loginFailed.html")
'''
    


@app.route('/signedUp')
def signedUp():
    #addUser(request.args[username],request.args[password])
    return render_template("signedUp.html")
    

if __name__ == '__main__':
    app.debug = True
    app.run()
