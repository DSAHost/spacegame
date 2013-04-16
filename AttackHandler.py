from Handler import *
from utils import *
from UserDatabase import *

class AttackHandler(Handler):
	def render_front(self,username,currency,units,available_targets=None,attack_id=None):
		if attack_id:
			self.render("attack.html",attack_id=attack_id,num_troops=attks[attack_id].num_troops,username=username,currency=currency, units=units)
		else:
			self.render("attack_creator.html",available_targets=available_targets,username=username,currency=currency, units=units)
	def get(self):
		units = self.request.get('num_troops')
		usrs=users()
		usrs=list(usrs)
		fusrs=[]
		for i in usrs:
			fusrs.append(i.username)
		if self.user:
	 		username=self.user.username
	 		resources=ResourceDatabase.getResources(self.user.resource_key)
	 		self.render_front(username,resources[0],resources[1],available_targets=fusrs)
	 	else:
	 		self.redirect('/login')
		
	def post(self):
		units = self.request.get('num_troops')
		target = self.request.get('target')
		action = self.request.get('action')
		attack_id = self.request.get('attack_id')

		if units and target:
			# attack = new Attack(attacker_key=self.user.key, defender_key=target.key, units=units)
			attack.put()
			return

		if action and attack_id:
			attack = attacks()[attack_id]
			if action == 'attack':
				defender = get_Resources(attack.defender_key)
				units, defender.home_units = combat(attack.units, defender.home_units)
				return
				
			if action == 'retreat':
				attack.return_time = datetime().now + dattime.timedelta(minutes = return_time)
				return