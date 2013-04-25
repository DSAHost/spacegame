import random

def old_combat(attacking_troops, defending_troops):
	attack = [random.randint(1,6)]
	if attacking_troops >= 3:
		attack.append(random.randint(1,6))
	if attacking_troops >= 9:
		attack.append(random.randint(1,6))
	if attacking_troops >= 27:
		attack.append(random.randint(1,6))
	attack.sort()
	defense = [random.randint(1,6)]
	if defending_troops >= 2:
		defense.append(random.randint(1,6))
	if defending_troops >= 10:
		defense.append(random.randint(1,6))
	defense.sort()
	i=0
	while i<len(attack) and i<len(defense):
		if attack[i] > defense[i]:
			defending_troops-=1
		else:
			attacking_troops-=1
		i+=1
	return (attacking_troops,defending_troops)

def combat(attacking_troops,defending_troops):
	atk_f=float(attacking_troops)
	attack=random.randint((int(atk_f*.7),int(atk_f*1.1)
	def_f=float(defending_troops)
	defense=random.randint(int(def_f*.85),int(def_f))
	diff=float(defense-attack)
	atk_r=attacking_troops-int(diff*1.1)
	def_r=defending_troops-int(diff*.95)
	return (atk_r,def_r)

def spoilsOfWar(attackers_dead,defenders_dead,defender_currency):
	if defenders_dead>(1.5*attackers_dead):
		return .15*defender_currency
	if defenders_dead>(.8*attackers_dead):
		return .09*defender_currency
	if defenders_dead<=(.8*attackers_dead):
		return .02*defender_currency
	return 0