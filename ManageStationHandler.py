from Handler import *
from utils import *

class ManageStationHandler(Handler):
	def render_front(self,error=""):
		self.render("managestation.html",error=error)
	def get(self):
	 	if self.user:
	 		self.render_front()
	 	else:
	 		self.redirect('/login')

	def post(self):
		buying=0
	 	try:
	 		buying=int(self.request.get('units'))
	 	except ValueError:
	 		self.render_front(error="You must enter a valid number.")
	 		return
	 	resources=self.user.getResources()[0]
	 	cost=buying*35
	 	if buying<=0:
	 		self.render_front(error="You must enter a valid number.")
	 		return
	 	if cost>resources:
	 		self.render_front(error="You do not have enough credits.")
	 		return
