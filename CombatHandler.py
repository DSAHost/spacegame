from Handler import *
from utils import *
import UserDatabase

class CombatHandler(Handler):
	def render_front(self):
 		username=self.user.username
 		resources=self.user.getResources()
 		users = UserDatabase.users()
 		attacks=self.user.getAttacks()
 			
 		fxusr=[]
		for i in users:
			if i.username != username:
				fxusr.append(i)
		self.render("combat.html",username=username,currency=resources[0], units=resources[1], users=fxusr, attacks=attacks)

	def get(self):
	 	if self.user:
	 		self.render_front()
	 	else:
	 		self.redirect('/login')

	def post(self):
		troops=self.request.get('num_troops')
