from Handler import *
from utils import *

class UnitPurchaseHandler(Handler):
	def render_front(self, username, currency, units):
		self.render("unitpurchase.html",username=username,currency=currency, units=units)
	def get(self):
	 	if self.user:
	 		username=self.user.username
	 		resources=ResourceDatabase.getResources(self.user.resource_key)
	 		self.render_front(username,resources[0],resources[1])
	 	else:
	 		self.redirect('/login')

	def post(self):
		units = int(self.request.get("units"))
		cost = int(self.request.get("cost"))
		UserDatabase.addCombatUnits(self.user.key,units)
		UserDatabase.addCurrency(self.user.key,-cost)
