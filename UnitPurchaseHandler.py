from Handler import *
from utils import *

class UnitPurchaseHandler(Handler):
	def render_front(self,error=""):
		username=self.user.username
	 	resources=self.user.getResources()
		attacks=self.user.getAttacks()
		self.render("unitpurchase.html",username=username,currency=currency, units=units, attacks=attackserror=error)
	def get(self):
	 	if self.user:
	 		self.render_front()
	 	else:
	 		self.redirect('/login')

	def post(self):
		units = self.request.get("units")
		resources=self.user.getResources()
		if units:
			try:
				units=int(units)
			except ValueError:
				self.render_front("You must enter a valid number.")
				return
			if units<=0:
				self.render_front("You must enter a valid number.")
				return
			cost = units*10
		
			if cost>resources[0]:
				error="You do not have enough credits to train that many units."
				self.render_front(error)
				return
			self.user.addCurrency(-cost)
			self.user.addCombatUnits(units)
			self.redirect('/game')
		else:
			self.render_front()
