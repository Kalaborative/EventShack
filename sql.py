import sqlite3

# format our data into a list of tuples
names = [
	("admin", "admin"),
	("Natsu", "sadist"),
	("Fumucat", "nyanya123")
	]

tasks = [
	("Natsu", "game night, movie night"),
	("Fumucat", "game night"),
	("dylansymm", "game night, karaoke night")
]

# connect to the database and insert new values	
with sqlite3.connect("sample.db") as connection:
	c = connection.cursor()
	c.execute("DROP TABLE IF EXISTS users")
	c.execute("""CREATE TABLE users(username TEXT, password TEXT)""")
	c.executemany("INSERT INTO users VALUES(?, ?)", names)

with sqlite3.connect('tasks.db') as connection:
	c = connection.cursor()
	c.execute("DROP TABLE IF EXISTS tasks")
	c.execute("CREATE TABLE tasks(user TEXT, duties TEXT)")
	c.executemany("INSERT INTO tasks VALUES(?, ?)", tasks)