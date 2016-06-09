"""
Creates Payment object
"""

class Payment():

	"""
	Create a new payment object from a json object in Venmo Webhook response format
	"""
	def __init__(self, json):
		self.json = json

	"""
	Checks whether or not json object is a payment
	@param json json object to check
	"""
	@staticmethod
	def checkPayment(json):
		if json["data"]["status"] != "settled":
			return false
		return true

	"""
	Get the payment amount
	"""
	def getAmount():
		return float(self.json["data"]["amount"])

	"""
	Get the username of the payer
	"""
	def getUsername():
		return self.json["data"]["actor"]["username"]

	"""
	Get the full name of the payer
	"""
	def getFullName():
		return self.json["data"]["actor"]["display_name"]