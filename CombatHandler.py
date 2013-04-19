from Handler import *
from utils import *
import UserDatabase

class CombatHandler(Handler):
	def render_front(self,error=""):
 		username=self.user.username
 		resources=self.user.getResources()
 		users = UserDatabase.users()
 		attacks=self.user.getAttacks()
 		times=self.user.getReturnTimes()	
 		fxusr=[]
		for i in users:
			if i.username != username:
				fxusr.append(i)
		self.render("combat.html",username=username,currency=resources[0], units=resources[1], users=fxusr, attacks=attacks,error=error,times=times,num_attacks=range(len(attacks)))

	def get(self):
	 	if self.user:
	 		self.render_front()
	 	else:
	 		self.redirect('/login')

	def post(self):
		troops=self.request.get('num_troops')
		try:
			troops=int(troops)
		except ValueError:
			self.render_front("You must enter a valid number.")
			return
		if troops<4:
			error="You must send at least 4 troops to attack."
			self.render_front(error)
			return
			
