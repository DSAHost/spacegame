from Handler import *
from utils import *
from UserDatabase import *
import RiskCombat

class AttackHandler(Handler):
	def render_front(self,error=""):
		self.user.getHomeUnits()
 		username=self.user.username
 		resources=self.user.getResources()
 		users = UserDatabase.users()
 		attacks=self.user.getAttacks()
 		times=self.user.getReturnTimes()	
 		fxusr=[]
		for i in users:
			if i.username != username:
				fxusr.append(i)
		self.render("attack_creator.html",username=username,currency=resources[0], units=resources[1], users=fxusr, attacks=attacks,error=error,times=times,num_attacks=range(len(attacks)))

	def get(self):
	 	if self.user:
	 		self.render_front()
	 	else:
	 		self.redirect('/login')
		
	def post(self):
		troops=self.request.get('num_troops')
		person=self.request.get('target')
		person=str(person)
		try:
			troops=int(troops)
		except ValueError:
			self.render_front("You must enter a valid number.")
			return
		if troops<4:
			error="You must send at least 4 troops to attack."
			self.render_front(error)
			return
		elif troops>self.user.resources.home_units:
			error="You do not have enough units."
			self.render_front(error)
			return

		accs=users()
		accs=list(accs)
		if troops and person:
			for i in accs:
				if i.username == person:
					self.user.addCombatUnits(-1*troops)
					om=troops
					myunits=troops
					theirunits=i.resources.home_units
					ot=theirunits
					myunits,theirunits=RiskCombat.combat(myunits,theirunits)
					self.user.newAttack(i.username,myunits,60)
					self.user.addCurrency(10)
					self.user.newMessage("You attacked %s." % i.username, "You lost %d troops and plundered 10 Currency." % (om-myunits))
		self.redirect('/game')