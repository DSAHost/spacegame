from Handler import *
from utils import *
from UserDatabase import *

class AttackHandler(Handler):
	def render_front(self,available_targets=None,attack_id=None):
		if attack_id:
			self.render("attack.html",attack_id=attack_id,num_troops=attks[attack_id].num_troops)
		else:
			self.render("attack_creator.html",available_targets=available_targets)
	def get(self):
		units = self.request.get('num_troops')
		usrs=users()
		usrs=list(usrs)
		fusrs=[]
		for i in usrs:
			fusrs.append(i.username)
		self.render_front(available_targets=fusrs)
		
	def post(self):
		units = self.request.get('num_troops')
		target = self.request.get('target')
		action = self.request.get('action')
		attack_id = self.request.get('attack_id')

		if units and target:
			attack = Attack(attacker_key = self.user.key, defender_key = target.key, units = units)
			attack.put()
			return units

		if action and attack_id:
			attack = attacks()[attack_id]
			if action == 'attack':
				defender = get_Resources(attack.defender_key)
				units, defender.home_units = combat(attack.units, defender.home_units)
				return units, defender.home_units
				
			if action == 'retreat':
				attack.return_time = datetime().now + dattime.timedelta(minutes = return_time)
				return units, defender.home_units
