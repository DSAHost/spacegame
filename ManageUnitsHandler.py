from Handler import *
from utils import *

class ManageUnitsHandler(Handler):
	def render_front(self):
		self.render("manageunits.html",ships=self.user.fleet,num_ships=range(len(self.user.fleet)))
	def get(self):
	 	if self.user:
	 		self.render_front()
	 	else:
	 		self.redirect('/login')

	def post(self):
		ids=self.request.get('ship')
		ids=list(ids)
		if ids:
			self.user.sellShips(ids)
		self.redirect('/game')
	 		