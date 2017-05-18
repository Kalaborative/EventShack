# import the Flask class from the flask module
from flask import Flask, render_template, request, url_for, redirect
from time import sleep

# create the application object
app = Flask(__name__)

names = {
	"admin": "admin",
	"Natsu": "sadist",
	"Fumucat": "nyanya123"
}

# use decorators to link the function to a URL
@app.route('/', methods=["GET", "POST"])
def home():
	error = None
	if request.method == "POST":
		if request.form['username'] not in names:
			error = "We don't recognize that name. Please try again."
			return render_template('welcome.html', error=error)
		elif request.form['password'] != names[request.form['username']]:
			error = "You entered an incorrect password for that name. Please try again."
			return render_template('welcome.html', error=error)
		else:
			sleep(2)
			return redirect(url_for('success'))
	return render_template('welcome.html', error=error)

@app.route('/success')
def success():
	return render_template('success.html')

if __name__ == "__main__":
	app.run(debug=True)