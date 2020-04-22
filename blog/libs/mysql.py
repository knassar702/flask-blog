from flask_mysqldb import MySQL

class SQL:
	def __init__(self,app):
		global mysql
		mysql = MySQL(app)
	def mysql(self):
		c = mysql.connection
		cmd = c.cursor()
		return c ,cmd
