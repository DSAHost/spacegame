from Handler import *
from utils import *

class UnitPurchaseHandler(Handler):
	def render_front(self, username, currency, units, error=""):
		self.render("unitpurchase.html",username=username,currency=currency, units=units, error=error)
	def get(self):
	 	if self.user:
	 		username=self.user.username
	 		resources=self.user.getResources()
	 		self.render_front(username,resources[0],resources[1])
	 	else:
	 		self.redirect('/login')

	def post(self):
		units = self.request.get("units")
		resources=self.user.getResources()
		if units:
			try:
				units=int(units)
			except ValueError:
				self.render_front(self.user.username,resources[0],resources[1],"You must enter a valid number.")
				return
			if units<=0:
				self.render_front(self.user.username,resources[0],resources[1],"You must enter a valid number.")
				return
			cost = units*10
		
			if cost>resources[0]:
				error="You do not have enough credits to train that many units."
				self.render_front(self.user.username,resources[0],resources[1],error)
				return
			self.user.addCombatUnits(units)
			self.user.addCurrency(-cost)
			self.redirect('/game')
		else:
			self.render_front(self.user.username,resources[0],resources[1])