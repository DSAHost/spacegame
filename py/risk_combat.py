def combat(attacking_troops, defending_troops):
    attack = [random.randint(1,6)]
	if attacking_troops >= 2:
		attack.append(random.randint(1,6))
	if attacking_troops >= 3:
		attack.append(random.randint(1,6))
	attack.sort()
	defense = [random.randint(1,6)]
	if defending_troops >= 2:
		defense.append(random.randint(1,6))
	defense.sort()
	if attack[0] > defense[0]
		defending_troops = defending_troops - 1
	else:
		attacking_troops = attacking_troops - 1
	if attack[1] > defence[1]:
		defending_troops = defending_troops - 1
		return attacking_troops, defending_troops
	else:
		attacking_troops = attacking_troops - 1
		return attacking_troops, defending_troops
