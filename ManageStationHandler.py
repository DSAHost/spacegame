from Handler import *
from utils import *

class ManageStationHandler(Handler):
	def render_front(self):
		username=self.user.username
	 	resources=self.user.getResources()
	 	attacks=self.user.getAttacks()
		self.render("managestation.html",username=username,currency=resources[0], units=resources[1],attacks=attacks)
	def get(self):
	 	if self.user:
	 		self.render_front()
	 	else:
	 		self.redirect('/login')