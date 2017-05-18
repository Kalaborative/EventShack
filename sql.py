import sqlite3

# format our data into a list of tuples
names = [
	("admin", "admin"),
	("Natsu", "sadist"),
	("Fumucat", "nyanya123")
	]

# connect to the database and insert new values	
with sqlite3.connect("sample.db") as connection:
	c = connection.cursor()
	c.execute("DROP TABLE IF EXISTS users")
	c.execute("""CREATE TABLE users(username TEXT, password TEXT)""")
	c.executemany("INSERT INTO users VALUES(?, ?)", names)

