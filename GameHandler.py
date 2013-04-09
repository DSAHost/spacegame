from Handler import *

class GameHandler(Handler):
	def render_front(self, username, currency, units):
		self.render("gamebase.html",username=username,currency=currency, units=units)
	def get(self):
<<<<<<< HEAD
		
		self.render_front()
=======
		self.render("gamefront.html")
>>>>>>> lotsa stuff
