from Handler import *

class GameHandler(Handler):
	def render_front(self, username, currency, units):
		self.render("gamebase.html",username=username,currency=currency, units=units)
	def get(self):
		username=self.user.username
		resources=ResourceDatabase.getResources(self.user.resource_key)
		self.render_front(username,resources[0],resources[1])
