from Handler import *
from utils import *
import UserDatabase
import AttackDatabase

class CombatHandler(Handler):
	def render_front(self):
 		username=self.user.username
 		resources=self.user.getResources()
 		users = UserDatabase.users()
 		attacks=self.user.getAttacks()
 		peeps=[]
 		for i in attacks:
 			peeps.append(UserDatabase.getUsername(i.defender_key))
 			
 		fxusr=[]
		for i in users:
			if i.username != username:
				fxusr.append(i)
		self.render("combat.html",username=username,currency=resources[0], units=resources[1], users=fxusr, attacks=attacks, peeps=peeps)

	def get(self):
	 	if self.user:
	 		self.render_front()
	 	else:
	 		self.redirect('/login')

	def post(self):
		troops=self.request.get('num_troops')