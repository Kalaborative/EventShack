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

# List of random greetings to greet the user when they login.
greetings = ["Hello", "Hi there", "Welcome", "Good to see you", "Hey", "Long time no see", "Heya", "Sup"]

# When logged in, user will be saved to global variable
logged_in_name = []
# Grabber text is saved to a global variable
grabbed = []
# Keep an action log to log all administrative events.
action_log = []

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

# use decorators to link the function to a URL.
# main route
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

# Welcome page when the user logs in
@app.route('/success')
@login_required
def success():
	greet = choice(greetings)
	return render_template('success.html', greet=greet, login_name=logged_in_name)

# Registration page
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

# Function to connect to the app's database
def connect_db():
	return sqlite3.connect(app.database)

# Strike managament system webpage
@app.route('/strikes', methods=["GET", "POST"])
def strikes():
	status = None
	if request.method == "POST":
		global grabbed
		grabbed = grabber(request.form['query'])
		status = grabbed[0]
	return render_template('strikes.html', status=status)

# Text when adding a strike
@app.route("/strikeenter")
def strikeenter():
	with sqlite3.connect('sample.db') as connection:
		c = connection.cursor()
		c.execute("UPDATE strikes SET strike = strike + 1 WHERE username=?", [grabbed[1]])
		global action_log
		action_log = [(logged_in_name, "gave a strike to ", grabbed[1])]
		c.executemany("INSERT INTO logs VALUES(?, ?, ?)", action_log)
		return render_template("strikesuccess.html")

# Text when removing a strike
@app.route("/strikeexit")
def strikeexit():
	with sqlite3.connect('sample.db') as connection:
		c = connection.cursor()
		c.execute("UPDATE strikes SET strike = strike - 1 WHERE username=?", [grabbed[1]])
		global action_log
		action_log = [(logged_in_name, "removed a strike from ", grabbed[1])]
		c.executemany("INSERT INTO logs VALUES(?, ?, ?)", action_log)
		return render_template("strikesuccess.html")

# Text when viewing amount of strikes
@app.route("/strikeview")
def strikeview():
	with sqlite3.connect('sample.db') as connection:
		c = connection.cursor()
		c.execute("SELECT strike FROM  strikes WHERE username=?", [grabbed[1]])
		result = [c.fetchone()[0], grabbed[1]]
		global action_log
		action_log = [(logged_in_name, "viewed total amount of strikes on ", grabbed[1])]
		c.executemany("INSERT INTO logs VALUES(?, ?, ?)", action_log)
		return render_template('strikesuccess.html', strikeNumber=result)

# Route for logging information
@app.route("/logs")
def logs():
	with sqlite3.connect('sample.db') as connection:
		c = connection.cursor()
		c.execute("SELECT * FROM logs")
		cers = c.fetchall()
		return render_template("notes.html", cers=cers)

# Webpage to manage promotion and demotion of organizers, as well as adding new ones
@app.route("/manager", methods=["GET", "POST"])
def manager():
	global action_log
	response = None
	if request.method == "POST":
		updateOrg = request.form['orgName']
		if request.form['actionSelected'] == "Promote" and updateOrg != "Select one...":
			with sqlite3.connect('sample.db') as connection:
				c = connection.cursor()
				c.execute("UPDATE orgs SET role='Senior Organizer' WHERE username=?", [updateOrg])
				action_log = [(logged_in_name, "gave a promotion of Senior Organizer to ", updateOrg)]
 				c.executemany("INSERT INTO logs VALUES(?, ?, ?)", action_log)
		elif request.form['actionSelected'] == "Demote" and updateOrg != "Select one...":
			with sqlite3.connect('sample.db') as connection:
				c = connection.cursor()
				c.execute("SELECT role from orgs WHERE username=?", [updateOrg])
				contestedRole = c.fetchone()
				if contestedRole[0] == "Senior Organizer":
					c.execute("UPDATE orgs SET role='organizer' where username=?", [updateOrg])
					action_log = [(logged_in_name, "has given a demotion of Senior Organizer to ", updateOrg)]
					c.executemany("INSERT INTO logs VALUES(?, ?, ?)", action_log)
				else:
					c.execute("DELETE FROM orgs WHERE username=?", [updateOrg])
					action_log = [(logged_in_name, "has demoted and deleted ", updateOrg)]
 					c.executemany("INSERT INTO logs VALUES(?, ?, ?)", action_log)
		elif updateOrg == "Select one..." and request.form['actionSelected'] == "Select one..." and request.form['NewOrg']:
			OrgNew = request.form['NewOrg']
			with sqlite3.connect("sample.db") as connection:
				c = connection.cursor()
				NewOrgData = [(OrgNew, "organizer")]
				c.executemany("INSERT INTO orgs VALUES(?, ?)", NewOrgData)
				action_log = [(logged_in_name, "has made a new organizer role for ", Orgnew)]
 				c.executemany("INSERT INTO logs VALUES(?, ?, ?)", action_log)
		elif updateOrg == "Select one..." and request.form['actionSelected'] == "Select one..." and request.form['NewOrg']:
			Orgnew = request.form['NewOrg']
			with sqlite3.connect("sample.db") as connection:
				c = connection.cursor()
				NewOrgData = [(Orgnew, "organizer")]
				c.executemany("INSERT INTO orgs VALUES(?, ?)", NewOrgData)
				action_log = [(logged_in_name, "has made a new organizer role for ", Orgnew)]
				c.executemany("INSERT INTO logs VALUES(?, ?, ?)", action_log)
		response = "Successfully performed the action."
	with sqlite3.connect("sample.db") as connection:
		c = connection.cursor()
		c.execute("SELECT * from orgs")
		fetchlist = []
		orgroles = c.fetchall()
		for orgs in orgroles:
			fetchlist.append(orgs[0])
		return render_template("manager.html", fetched=fetchlist, orglist=orgroles, response=response)
# Run the application
if __name__ == "__main__":
	app.run(debug=True)
