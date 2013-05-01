import random
import logging

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
	# troops are now lists!
	atk_all_fighters=[]
	atk_all_bombers=[]
	atk_all_corvettes=[]
	atk_all_frigates=[]
	atk_all_capitals=[]
	def_all_fighters=[]
	def_all_bombers=[]
	def_all_corvettes=[]
	def_all_frigates=[]
	def_all_capitals=[]

	atk_fighters_armor=0
	atk_fighters_damage=0
	atk_fighters_mobility=0
	atk_bombers_armor=0
	atk_bombers_damage=0
	atk_bombers_mobility=0
	atk_corvettes_armor=0
	atk_corvettes_damage=0
	atk_corvettes_mobility=0
	atk_big_armor=0
	atk_big_damage=0
	atk_big_mobility=0
	atk_num_ships=0
	atk_num_fighters=0
	atk_num_bombers=0
	atk_num_corvettes=0
	atk_num_frigates=0
	for i in attacking_troops:
		i=Ship(i)
		atk_num_ships+=1
		if i.shipclass=="Fighter":
			atk_fighters_armor+=i.armor
			atk_fighters_damage+=i.damage
			atk_fighters_mobility+=i.mobility
			atk_num_fighters+=1
			atk_all_fighters.append(i)
		elif i.shipclass=="Bomber":
			atk_bombers_armor+=i.armor
			atk_bombers_damage+=i.damage
			atk_bombers_mobility+=i.mobility
			atk_num_bombers+=1
			atk_all_bombers.append(i)
		elif i.shipclass=="Corvette":
			atk_corvettes_armor+=i.armor
			atk_corvettes_damage+=i.damage
			atk_corvettes_mobility+=i.mobility
			atk_num_corvettes+=1
			atk_all_corvettes.append(i)
		else:
			atk_big_armor+=i.armor
			atk_big_damage+=i.damage
			atk_big_mobility+=i.mobility
			if i.shipclass=="Frigate":
				atk_num_frigates+=1
				atk_all_frigates.append(i)
			else:
				atk_all_capitals.append(i)
	atk_fighters_mobility/=atk_num_fighters
	atk_fighters_armor/=atk_num_fighters
	atk_bombers_mobility/=atk_num_bombers
	atk_corvettes_mobility/=atk_num_corvettes
	atk_big_mobility/=atk_num_fighters
	atk_big_armor+=atk_num_frigates

	def_fighters_armor=0
	def_fighters_damage=0
	def_fighters_mobility=0
	def_bombers_armor=0
	def_bombers_damage=0
	def_bombers_mobility=0
	def_corvettes_armor=0
	def_corvettes_damage=0
	def_corvettes_mobility=0
	def_big_armor=0
	def_big_damage=0
	def_big_mobility=0
	def_num_ships=0
	def_num_fighters=0
	def_num_bombers=0
	def_num_corvettes=0
	def_num_frigates=0
	for i in defending_troops:
		i=Ship(i)
		def_num_ships+=1
		if i.shipclass=="Fighter":
			def_fighters_armor+=i.armor
			def_fighters_damage+=i.damage
			def_fighters_mobility+=i.mobility
			def_num_fighters+=1
			def_all_fighters.append(i)
		elif i.shipclass=="Bomber":
			def_bombers_armor+=i.armor
			def_bombers_damage+=i.damage
			def_bombers_mobility+=i.mobility
			def_num_bombers+=1
			def_all_bombers.append(i)
		elif i.shipclass=="Corvette":
			def_corvettes_armor+=i.armor
			def_corvettes_damage+=i.damage
			def_corvettes_mobility+=i.mobility
			def_num_corvettes+=1
			def_all_corvettes.append(i)
		else:
			def_big_armor+=i.armor
			def_big_damage+=i.damage
			def_big_mobility+=i.mobility
			if i.shipclass=="Frigate":
				def_num_frigates+=1
				def_all_frigates.append(i)
			else:
				def_all_capitals.append(i)
	def_fighters_mobility/=def_num_fighters
	def_fighters_armor/=def_num_fighters
	def_bombers_mobility/=def_num_bombers
	def_corvettes_mobility/=def_num_corvettes
	def_big_mobility/=def_num_fighters
	def_big_armor+=def_num_frigates
	atk_damage_to_small=random.uniform((atk_fighters_damage+atk_corvettes_damage*2)*.7,(atk_fighters_damage+atk_corvettes_damage*2)*1.1)
	def_damage_to_small=random.uniform((def_fighters_damage+def_corvettes_damage*2)*.85,(def_fighters_damage+def_corvettes_damage*2)*1.15)
	def_fighters_to_del=atk_damage_to_small/(def_fighters_armor*def_fighters_mobility+1)
	atk_fighters_to_del=def_damage_to_small/(atk_fighters_armor*atk_fighters_mobility+1)-def_fighters_to_del/3

	randomDestroy(def_all_fighters,def_fighters_to_del,.75)
	randomDestroy(def_all_bombers,def_fighters_to_del/3,.24)
	randomDestroy(atk_all_fighters,atk_fighters_to_del,.75)
	randomDestroy(atk_all_bombers,atk_fighters_to_del/3,.24)

	atk_damage_to_big=random.uniform((atk_bombers_damage*2+atk_big_damage)*.7,(atk_bombers_damage*2+atk_big_damage)*1.1)
	def_damage_to_big=random.uniform((def_bombers_damage*2+def_big_damage)*.85,(def_bombers_damage*2+def_big_damage)*1.15)
	def_frigates_to_del=atk_damage_to_big/(def_big_armor+1)
	atk_frigates_to_del=def_damage_to_big/(atk_big_armor+1)
	randomDestroy(def_all_frigates,def_frigates_to_del,.75)
	randomDestroy(def_all_capitals,def_frigates_to_del/3,.24)
	randomDestroy(atk_all_frigates,atk_frigates_to_del,.75)
	randomDestroy(atk_all_capitals,atk_frigates_to_del/3,.24)

	atk_extra_dead=(def_damage_to_big*1.5+def_damage_to_small)/(atk_num_corvettes+atk_num_bombers+atk_corvettes_mobility+1)
	def_extra_dead=(atk_damage_to_big*1.4+atk_damage_to_small)/(def_num_corvettes*.9+def_num_bombers+def_corvettes_mobility+1)
	randomDestroy(def_all_corvettes,def_extra_dead,.85)
	randomDestroy(atk_all_corvettes,atk_extra_dead,.83)

	atk_all=[]
	atk_all.extend(atk_all_fighters)
	atk_all.extend(atk_all_bombers)
	atk_all.extend(atk_all_corvettes)
	atk_all.extend(atk_all_frigates)
	atk_all.extend(atk_all_capitals)
	def_all=[]
	def_all.extend(def_all_fighters)
	def_all.extend(def_all_bombers)
	def_all.extend(def_all_corvettes)
	def_all.extend(def_all_frigates)
	def_all.extend(def_all_capitals)
	return (atk_all,def_all)
	
def randomDestroy(troop_list,max_dead,pref):
	dead=0
	troop_list=random.shuffle(troop_list.reverse())
	for i in troop_list:
		if dead<max_dead:
			if random.random()<pref:
				troop_list.remove(i)
				dead+=1
	return troop_list

def spoilsOfWar(attackers_dead,defenders_dead,defender_currency):
	if defenders_dead>(1.5*attackers_dead):
		return .15*defender_currency
	if defenders_dead>(.8*attackers_dead):
		return .09*defender_currency
	if defenders_dead<=(.8*attackers_dead):
		return .02*defender_currency
	return 0
