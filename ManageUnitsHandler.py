from Handler import *
from utils import *

class ManageUnitsHandler(Handler):
	def render_front(self):
		self.render("manageunits.html",ships=self.user.fleet,num_ships=range(len(self.user.fleet)))
	def get(self):
	 	if self.user:
	 		self.render_front()
	 	else:
	 		self.redirect('/login')

	def post(self):
		x=self.request.get('ship')
		x = x.split("|")
		variable = x[0]
		ids = x[1]
		ids=int(ids)
		ids=[ids]
		if variable == 'sell':
			if ids:
				self.user.sellShips(ids)
		if variable == 'upgrade':
			if ids:
				self.user.upgradeShip(ids)
		self.redirect('/game')

	 		