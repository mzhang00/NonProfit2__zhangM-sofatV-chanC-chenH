from flask import Flask, render_template,request,redirect,session
app = Flask(__name__)

@app.route('/')

def root():
    return render_template('welcome.html')

@app.route('/login')

def login():
    return render_template("auth.html")

@app.route('/error')

def error():
    return render_template("error.html")

@app.route('/signup')

def signup():
    return render_template("create.html")

@app.route('/create')

def create():
    return redirect('/login')

@app.route('/auth')

def auth():
    return redirect('/home')

@app.route('/home')

def home():
    return render_template('homepage.html')

@app.route('/profile')

def profile():
    return render_template('profile.html')

@app.route('/search')

def search():
    return render_template("results.html")

@app.route('/logout')

def logout():
    return redirect('/')


if __name__ == '__main__':
    app.debug = True
    app.run()
