"""
DBAccessor Class for sqllite3 DKE Keg DB
"""
import sqlite3

class DBAccessor:

	def __init__(self):
		self.conn = sqlite3.connect("dkekeg.db")
		self.c = self.conn.cursor()

	"""
	Get the balance of the user with a specified kerberos
	@param kerberos string kerberos ID
	"""
	def getBalance(self, kerberos):
		t = (kerberos,)
		balance_statement = "SELECT balance FROM BROTHERS WHERE id=?"
		try:
			self.c.execute(balance_statement,t)
			current_balance = self.c.fetchone()
			return current_balance
		except:
			return 0.0

	"""
	Get the full name of the user with a specified kerberos
	@param kerberos string kerberos ID
	"""
	def getName(self, kerberos):
		t = (kerberos,)
		name_statement = "SELECT name FROM BROTHERS WHERE id=?"
		try:
			self.c.execute(name_statement,t)
			name = self.c.fetchone()
			return name
		except:
			return "User is not in database"
			
	"""
	Update the given users balance
	@param kerberos string kerberos ID
	@param balance float updated balance
	"""
	def updateBalance(self, kerberos, balance):
		t = (balance,kerberos)
		update_statement = "UPDATE BROTHERS SET balance=? WHERE id=?"
		try:
			self.c.execute(update_statement,t)
			self.conn.commit()
		except:
			print "User is not in database"

	"""
	Get the kerberos of the user with a specified name
	@param string name
	@return string kerberos
	"""
	def getKerberos(self, name):
		t = (name,)
		name_statement = "SELECT id FROM BROTHERS WHERE name=?"
		try:
			self.c.execute(name_statement,t)
			kerberos = self.c.fetchone()
			print kerberos
			return kerberos
		except:
			return "User is not in Database"

	def addUser(self, name, kerberos):
		t = (name,kerberos,0.0)
		insert_statement = "INSERT INTO BROTHERS (name, id, balance) VALUES (?,?,?)"
		self.c.execute(insert_statement,t)
		self.conn.commit()

	"""
	Save the changes and close the current connection
	"""
	def closeConnection(self):
		self.conn.commit()
		self.conn.close()
