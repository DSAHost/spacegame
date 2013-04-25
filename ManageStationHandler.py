from Handler import *
from utils import *

class ManageStationHandler(Handler):
	def render_front(self):
		self.render("managestation.html")
	def get(self):
	 	if self.user:
	 		self.render_front()
	 	else:
	 		self.redirect('/login')
