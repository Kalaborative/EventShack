import sqlite3

# format our data into a list of tuples
admins = [
	("admin", "admin")]

orgs = ["alice", "dylan symm", "natsu", "destyn", "esm", "smol bunny", "rope bunny", "panda", "helix", "nitro", "bailey", "fumucat"]

# Use zip function to give every org a strike value of zero.
strikes = zip(orgs, [0]*len(orgs))
roles = zip(orgs, ["organizer"]*len(orgs))

# connect to the database and insert new values	
with sqlite3.connect("sample.db") as connection:
	c = connection.cursor()
	c.execute("DROP TABLE IF EXISTS admins")
	c.execute("DROP TABLE IF EXISTS strikes")
	c.execute("DROP TABLE IF EXISTS orgs")
	c.execute("DROP TABLE IF EXISTS users")
	c.execute("DROP TABLE IF EXISTS logs")
	c.execute("""CREATE TABLE admins(username TEXT, password TEXT)""")
	c.execute("""CREATE TABLE strikes(username TEXT, strike INT)""")
	c.execute("""CREATE TABLE orgs(username TEXT, role TEXT)""")
	c.execute("""CREATE TABLE logs(admin TEXT, action TEXT, org TEXT)""")
	c.executemany("INSERT INTO admins VALUES(?, ?)", admins)
	c.executemany("INSERT INTO orgs VALUES(?, ?)", roles)
	c.executemany("INSERT INTO strikes VALUES(?, ?)", strikes)
