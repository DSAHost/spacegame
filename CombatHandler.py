from Handler import *
from utils import *

class CombatHandler(Handler):
	def render_front(self, username, currency, units):
		self.render("combat.html",username=username,currency=currency, units=units)
	def get(self):
	 	if self.user:
	 		username=self.user.username
	 		resources=ResourceDatabase.getResources(self.user.resource_key)
	 		self.render_front(username,resources[0],resources[1])
	 	else:
	 		self.redirect('/login')
