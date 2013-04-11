from Handler import *
from utils import *
from UserDatabase import *

class AttackHandler(Handler):
	def render_front(self,available_targets=None):
		self.render("attack.html",available_targets=available_targets)
	def get(self):
		units = self.request.get('num_troops')
		users=users()
		users=list(users)
		self.render_front(users)
		
	def post(self):
		units = self.request.get('num_troops')
		action = self.request.get('action')
		target = self.request.get('target')
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
