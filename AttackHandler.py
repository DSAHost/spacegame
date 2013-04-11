from Handler import *
from utils import *

class AttackHandler(Handler):
	def get(self):
		Handler.render("attack.html")

	def post(self):
		units = self.request.get('num_troops')
		action = self.request.get('action')
		target = self.request.get('target')
		attack_id = self.request.get('attack_id')

		if units and target:
			attack = Attack(attacker_key = self.user.key, defender_key = target.key, units = units)
			attack.put()
			return

		if action and attack_id:
			attack = attacks()[attack_id]
			if action = 'attack':
				defender = get_Resources(attack.defender_key)
				units, defender.home_units = combat(attack.units, defender.home_units)
				return
				
			if action == 'retreat':
				attack.return_time = datetime().now + dattime.timedelta(minutes = return_time)
				return