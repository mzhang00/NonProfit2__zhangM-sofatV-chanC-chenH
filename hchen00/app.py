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

if __name__ == '__main__':
    app.debug = True
    app.run()
