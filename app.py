# import the Flask class from the flask module
from flask import Flask, render_template, request, url_for, redirect, session, flash, g
from time import sleep
from functools import wraps
import sqlite3
from random import choice
from textprocess import grabber

# create the application object
app = Flask(__name__)
app.secret_key = "my precious"
app.database = "sample.db"

names = {
	"admin": "admin",
	"Natsu": "sadist",
	"Fumucat": "nyanya123"
}

greetings = ["Hello", "Hi there", "Welcome", "Good to see you", "Hey", "Long time no see", "Heya", "Sup"]

logged_in_name = []
grabbed = []
# login required decorator
def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('You need to login first.')
			return redirect(url_for('home'))
	return wrap

# use decorators to link the function to a URL
@app.route('/', methods=["GET", "POST"])
def home():
	error = None
	if request.method == "POST":
		g.db = connect_db()
		cur = g.db.execute('select * from admins')
		names = cur.fetchall()
		g.db.close()
		for n in names:
			if request.form['username'] in n[0]:
				error = None
				break
			else:
				error = "We don't recognize that name. Please try again."
		if not error:
			with connect_db() as connection:
				c = connection.cursor()
				c.execute('select * from admins')
				fads = c.fetchall()
				for f in fads:
					if request.form['password'] in f[1]:
						error = None
						break
					else:
						error = "You entered an incorrect password for that name. Please try again."
		if not error:
			global logged_in_name
			logged_in_name = request.form['username']
			sleep(2)
			session['logged_in'] = True
			return redirect(url_for('success'))
	return render_template('welcome.html', error=error)

@app.route('/success')
@login_required
def success():
	with sqlite3.connect('sample.db') as connection:
		cur = connection.cursor()
		cur.execute('SELECT * FROM orgs')
		datafils = cur.fetchall()
		greet = choice(greetings)
		return render_template('success.html', data=datafils, greet=greet, login_name=logged_in_name)

@app.route('/register', methods=["GET", "POST"])
def register():
	error = None
	success = None
	if request.method == "POST":
		if request.form['passnew'] != request.form['passconfirm']:
			error = "It looks like your passwords don't match. Try again!"
		else:
			newdata = list((request.form["usernew"].encode('utf-8'), request.form['passnew'].encode('utf-8')))
			g.db = connect_db()
			cur = g.db.execute('insert into admins values(?, ?)', newdata)
			g.db.commit()
			g.db.close()
			success = "You've signed up!"
	return render_template('register.html', error=error, success=success)

def connect_db():
	return sqlite3.connect(app.database)

@app.route('/strikes', methods=["GET", "POST"])
def strikes():
	status = None
	if request.method == "POST":
		global grabbed
		grabbed = grabber(request.form['query'])
		status = grabbed[0]
	return render_template('strikes.html', status=status)

@app.route("/strikeenter")
def strikeenter():
	with sqlite3.connect('sample.db') as connection:
		c = connection.cursor()
		c.execute("UPDATE strikes SET strike = strike + 1 WHERE username=?", [grabbed[1]])
		return render_template("strikesuccess.html")

@app.route("/strikeexit")
def strikeexit():
	with sqlite3.connect('sample.db') as connection:
		c = connection.cursor()
		c.execute("UPDATE strikes SET strike = strike - 1 WHERE username=?", [grabbed[1]])
		return render_template("strikesuccess.html")


if __name__ == "__main__":
	app.run(debug=True)