from flask import Flask, render_template 
app = Flask(__name__)

@app.route('/')

def root():
    return render_template('welcome.html')

@app.route('/login')

def login():
    return render_template("auth.html")

@app.route('/signup')

def signup():
    return render_template("create.html")

@app.route('/create')

def create():
    return ''

@app.route('/auth')

def auth():
    return ''

@app.route('/home')

def home():
    return render_template('homepage.html')

@app.route('/profile')

def profile():
    return render_template('profile.html')

@app.route('/search')

def search():
    return render_template("results.html")


if __name__ == '__main__':
    app.debug = True
    app.run()
