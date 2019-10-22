from flask import Flask, render_template 
app = Flask(__name__)

@app.route('/')

def root():
    return render_template('welcome.html')

@app.route('/login')

def login():
    return render_template("auth.html",
                           display = """<form action='/auth'>
                                        Username:
                                        <br>
                                        <input type="text" name="username"><br>
                                        Password:<br>
                                        <input type="password" name="password">
                                        <br>
                                        <input type="submit" value="Login">
                                        </form>""")

@app.route('/signup')

def signup():
    return ""
    

if __name__ == '__main__':
    app.debug = True
    app.run()
