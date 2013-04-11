from Handler import *
import ResourceDatabase
import UserDatabase

class GameHandler(Handler):
	def render_front(self, username, currency, units):
		self.render("gamefront.html",username=username,currency=currency, units=units)
	def get(self):
	 	if self.user:
	 		username=self.user.username
	 		resources=ResourceDatabase.getResources(self.user.resource_key)
	 		self.render_front(username,resources[0],resources[1])
	 	else:
	 		self.redirect('/login')
