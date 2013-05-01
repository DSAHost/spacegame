from Handler import *
from utils import *

class ManageUnitsHandler(Handler):
	def render_front(self,error="",num=""):
		self.render("manageunits.html",ships=self.user.fleet,num_ships=range(len(self.user.fleet)),error=error,num=num)
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
			resources=self.user.getResources()
			if int(self.user.fleet[ids[0]].cost*.2)>resources[0]:
				self.render_front(error="You do not have enough money to upgrade this ship.",num=ids[0])
				return
			elif self.user.fleet[ids[0]].num_of_upgrades>=3:
				self.render_front(error="This ship has been fully upgraded.",num=ids[0])
				return
			else:
				if ids:
					self.user.upgradeShip(ids)
		self.redirect('/game/manageunits')

	 		