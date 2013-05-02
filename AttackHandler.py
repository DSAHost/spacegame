from Handler import *
from utils import *
from UserDatabase import *
import RiskCombat

class AttackHandler(Handler):
	def render_front(self,error=""):
 		users = UserDatabase.users()
 		fxusr=[]
		for i in users:
			if i.username != self.user.username:
				fxusr.append(i)
		self.render("attack_creator.html",users=fxusr,error=error)

	def get(self):
	 	if self.user:
	 		self.render_front()
	 	else:
	 		self.redirect('/login')
		
	def post(self):
		s=self.user.fleet  #testing only.  s will be a list of all the ships you choose to send on an attack
  		if not s or len(s)==0:
			error="You must send at least 1 ship to attack."
			self.render_front(error)
			return

		person=self.request.get('target')
		person=str(person)
		accs=users()
		accs=list(accs)
		na=0
		nd=0
		ta=0
		td=0

		if s and person:
			for i in accs:
				if i.username == person:
					na=len(s)
					self.user.newAttack(person,s,60)
					for j in xrange(len(s)-1):
						self.user.fleet.remove(s[j]) 
					if i.fleet:
						nd=len(i.fleet)
						(natk,ndef)=RiskCombat.combat(s,i.fleet)
						datk=[]
						ddef=[]
						for ship in natk:
							if ship in s:
								datk.append(ship)
						ta=len(natk)
						for ship in ndef:
							if ship in i.fleet:
								ddef.append(ship)
						td=len(ndef)
						spoils=RiskCombat.spoilsOfWar(datk,ddef,i.resources.currency)
						spoils=int(spoils)
						self.user.addCurrency(spoils)
					else:
						spoils=int(i.resources.currency*.65)
						self.user.addCurrency(spoils)
						ta=na
					i.addCurrency(-1*spoils)
					self.user.newMessage("You attacked %s." % i.username, "You lost %d troops and plundered %d currency." % (na-ta,spoils))
					i.newMessage("You were attacked by %s." % self.user.username, "You lost %d troops and %d currency." % (nd-td,spoils))
					break
		self.redirect('/game')
