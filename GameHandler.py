from Handler import *

class GameHandler(Handler):
	def render_front(self):
		self.render("game.html")
	def get(self):
		self.render_front()