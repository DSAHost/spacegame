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
					theirunits=i.getHomeUnits()
					ot=theirunits
					myunits,theirunits=RiskCombat.combat(myunits,theirunits)
					i.addCombatUnits(-1*(ot-theirunits))
					self.user.newAttack(i.username,myunits,60)
					spoils=RiskCombat.spoilsOfWar(om-myunits,ot-theirunits,i.getResources()[0])
					spoils=int(spoils)
					self.user.addCurrency(spoils)
					i.addCurrency(-1*spoils)
					self.user.newMessage("You attacked %s." % i.username, "You lost %d troops and plundered %d currency." % (om-myunits,spoils))
					i.newMessage("You were attacked by %s." % self.user.username, "You lost %d troops and %d currency." % (ot-theirunits,spoils))
					return
		self.redirect('/game')
