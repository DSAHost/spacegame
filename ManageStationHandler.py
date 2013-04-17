from Handler import *
from utils import *

class ManageStationHandler(Handler):
	def render_front(self, username, currency, units):
		self.render("managestation.html",username=username,currency=currency, units=units)
	def get(self):
	 	if self.user:
	 		username=self.user.username
	 		resources=self.user.getResources()
	 		self.render_front(username,resources[0],resources[1])
	 	else:
	 		self.redirect('/login')