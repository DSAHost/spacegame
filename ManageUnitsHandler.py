from Handler import *
from utils import *

class ManageUnitsHandler(Handler):
	def render_front(self):
		self.render("manageunits.html",ships=self.user.fleet)
	def get(self):
	 	if self.user:
	 		self.render_front()
	 	else:
	 		self.redirect('/login')

	def post(self):
		id=self.request.get('ship')
		for ship in self.user.fleet:
			return
	 		