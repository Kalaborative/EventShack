# Flask app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://samp:asdf@localhost/mydb"
db = SQLAlchemy(app)

class Admins (db.Model):
    __tablename__ = "admins"
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String)
    password = db.Column('password', db.String)

    def __init__(self, username, password):
    	self.username = username
    	self.password = password

