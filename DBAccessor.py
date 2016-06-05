"""
DBAccessor Class for sqllite3 DKE Keg DB
"""
import sqllite3

class DBAccessor:

	# TODO: Figure out db file name
	DBNAME = ""

	def __init__(self):
		self.conn = sqllite3.connect(DBNAME)
		self.c = conn.cursor()


	"""
	Get the balance of the user with a specified kerberos
	@param kerberos string kerberos ID
	"""
	def getBalance(kerberos):
		t = (kerberos)
		balance_statement = "SELECT balance FROM Users WHERE kerberos=?"
		self.c.execute(balance_statement,t)
		current_balance = self.c.fetchone()
		return current_balance

	"""
	Get the full name of the user with a specified kerberos
	@param kerberos string kerberos ID
	"""
	def getName(kerberos):
		t = (kerberos)
		name_statement = "SELECT name FROM Users WHERE kerberos=?"
		self.c.execute(name_statement,t)
		name = self.c.fetchone()
		return name

	"""
	Update the given users balance
	@param kerberos string kerberos ID
	@param balance float updated balance
	"""
	def updateBalance(kerberos,balance):
		t = (balance,kerberos)
		update_statement = "UPDATE Users SET balance=? WHERE kerberos=?"
		self.c.execute(update_statement,t)
		self.conn.commit()

	"""
	Save the changes and close the current connection
	"""
	def closeConnection():
		self.conn.commit()
		self.conn.close()