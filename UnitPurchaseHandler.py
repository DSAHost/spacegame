from Handler import *
from utils import *

class UnitPurchaseHandler(Handler):
	def render_front(self, username, currency, units, error=""):
		self.render("unitpurchase.html",username=username,currency=currency, units=units, error=error)
	def get(self):
	 	if self.user:
	 		username=self.user.username
	 		resources=ResourceDatabase.getResources(self.user.resource_key)
	 		self.render_front(username,resources[0],resources[1])
	 	else:
	 		self.redirect('/login')

	def post(self):
		units = int(self.request.get("units"))
		cost = units*10
		resources=UserDatabase.getResources(self.user.key)
		if cost>resources[0]:
			error="You do not have enough credits to train that many units."
			self.render_front(self.user.username,resources[0],resources[1],error)
			return
		UserDatabase.addCombatUnits(self.user.key,units)
		UserDatabase.addCurrency(self.user.key,-cost)
		self.redirect('/game')