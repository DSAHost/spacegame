def combat(attacking_troops, defending_troops):
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
