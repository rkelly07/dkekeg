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
		t = (kerberos)
		balance_statement = "SELECT balance FROM BROTHERS WHERE id=?"
		self.c.execute(balance_statement,t)
		current_balance = self.c.fetchone()
		return current_balance

	"""
	Get the full name of the user with a specified kerberos
	@param kerberos string kerberos ID
	"""
	def getName(self, kerberos):
		t = (kerberos)
		name_statement = "SELECT name FROM BROTHERS WHERE id=?"
		self.c.execute(name_statement,t)
		name = self.c.fetchone()
		return name

	"""
	Update the given users balance
	@param kerberos string kerberos ID
	@param balance float updated balance
	"""
	def updateBalance(self, kerberos, balance):
		t = (balance,kerberos)
		update_statement = "UPDATE BROTHERS SET balance=? WHERE id=?"
		self.c.execute(update_statement,t)
		self.conn.commit()

	"""
	Get the kerberos of the user with a specified name
	@param string name
	@return string kerberos
	"""
	def getKerberos(self, name):
		t = (name)
		name_statement = "SELECT id FROM BROTHERS WHERE name=?"
		self.c.execute(name_statement,t)
		kerberos = self.c.fetchone()
		return kerberos

	"""
	Save the changes and close the current connection
	"""
	def closeConnection(self):
		self.conn.commit()
		self.conn.close()
