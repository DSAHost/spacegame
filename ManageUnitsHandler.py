from Handler import *
from utils import *

class ManageUnitsHandler(Handler):
	def render_front(self):
	 	username=self.user.username
	 	resources=self.user.getResources()
	 	attacks=self.user.getAttacks()
		times=self.user.getReturnTimes()
		self.render("manageunits.html",username=username,currency=resources[0], units=resources[1],attacks=attacks,times=times,num_attacks=range(len(attacks)))
	def get(self):
	 	if self.user:
	 		self.render_front()
	 	else:
	 		self.redirect('/login')
