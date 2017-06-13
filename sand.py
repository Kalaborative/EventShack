# Test file when testing things out in Python
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort

app = Flask(__name__)
app.secret_key = "cookies"

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if request.form['password'] == 'password' and request.form['username'] == 'admin':
            session['logged_in'] = True
        else:
            flash('wrong password!')
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
