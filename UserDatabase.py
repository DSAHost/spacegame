from Handler import *

class Ship(ndb.Model):
	armor=ndb.IntegerProperty(required=True)
	damage=ndb.IntegerProperty(required=True)
	mobility=ndb.IntegerProperty(required=True)
	shipclass=ndb.StringProperty(required=True)
	name=ndb.StringProperty(required=True)
	cost=ndb.IntegerProperty(required=True)
	num_of_upgrades=ndb.IntegerProperty(required=True)
	
	def toString(self):
		s=str(self.armor) + "," + str(self.damage) + "," + str(self.mobility) + "," + str(self.shipclass) + "," + self.name + "," + str(self.cost) + "," + str(self.num_of_upgrades)
		return s

def stringToShip(s):
	stats=s.split(',')
	return Ship(armor=int(stats[0]),damage=int(stats[1]),mobility=int(stats[2]),shipclass=str(stats[3]),name=str(stats[4]),cost=int(stats[5]),num_of_upgrades=int(stats[6]))

class Attack(ndb.Model):
	attacker_key=ndb.KeyProperty(required=True)
	all_ships=ndb.StringProperty()
	time_fought=ndb.DateTimeProperty(auto_now_add=True)
	return_time=ndb.IntegerProperty(required=True)
	defender_name=ndb.StringProperty(required=True)

class Message(ndb.Model):
	subject=ndb.StringProperty(required=True)
	content=ndb.StringProperty(required=True)
	created=ndb.DateTimeProperty(auto_now_add=True)

class Resources(ndb.Model):	
	currency=ndb.IntegerProperty(required=True)
	currency_add=ndb.IntegerProperty()
	currency_updated=ndb.DateTimeProperty(auto_now_add=True)
	
class User(ndb.Model):
	attacks=ndb.StructuredProperty(Attack,repeated=True)
	email=ndb.StringProperty(required=True)
	last_login=ndb.DateTimeProperty(auto_now_add=True)
	messages=ndb.StructuredProperty(Message, repeated=True)
	password=ndb.StringProperty(required=True)
	prefs=ndb.JsonProperty()
	resources=ndb.StructuredProperty(Resources)
	username=ndb.StringProperty(required=True)
	fleet=ndb.StructuredProperty(Ship,repeated=True)
	drones=ndb.IntegerProperty(required=True)

	def addShip(self,ship,half=True):
		newship=None
		if half:
			newship=Ship(armor=ship.armor,damage=ship.damage,mobility=ship.mobility,shipclass=ship.shipclass,cost=int(ship.cost/2),name=ship.name,num_of_upgrades=0)
		else:
			newship=Ship(armor=ship.armor,damage=ship.damage,mobility=ship.mobility,shipclass=ship.shipclass,cost=int(ship.cost),name=ship.name,num_of_upgrades=ship.num_of_upgrades)

		if not self.fleet:
			self.fleet=[newship]
		else:
			self.fleet.append(newship)
		self.put()
		users(True)

	def newMessage(self,s,c):
		if not self.messages:
			self.messages=[Message(subject=s,content=c)]
		else:
			self.messages.append(Message(subject=s, content=c))

		key=self.put()
		users(True)
		return key

	def newAttack(self,dname,ships,time):
		accs=users()
		serial=""
		for ship in ships:
			serial+=ship.toString() + "|"
		if not self.attacks:
			self.attacks=[Attack(attacker_key=self.key,defender_name=dname,all_ships=serial,return_time=time)]
		else:
			self.attacks.append(Attack(attacker_key=self.key,defender_name=dname,all_ships=serial,return_time=time))
		self.put()
		users(True)
		
	def getMessages(self):
		mess=[]
		for i in self.messages:
			mess.append(i)
		return mess
		
	def deleteMessages(self, message_ids):
		try:
			message_ids.sort()
			i=len(self.messages)
			while i>=0:
				if i in message_ids:
					self.messages.remove(self.messages[i])
				i-=1
		except AttributeError:
			pass
		self.put()
		users(True)

	def sellShips(self, ship_ids):
		try:
			ship_ids.sort()
			i=len(self.fleet)
			while i>=0:
				if i in ship_ids:
					self.addCurrency(int(self.fleet[i].cost))
					self.fleet.remove(self.fleet[i])
				i-=1
		except AttributeError:
			pass
		self.put()
		users(True)

	def upgradeShip(self, ship_ids):
			try:
				ship_ids.sort()
				i=len(self.fleet)
				while i>=0:
					if i in ship_ids:
						ship = self.fleet[int(i)]
						if self.user.getResources[0] > int(self.fleet[i].cost*.2):
							if ship.num_of_upgrades < 3:
								ship.armor += int(ship.armor*.2+1)
								ship.damage += int(ship.damage*.2+1)
								ship.mobility += int(ship.mobility*.2+1)
								ship.cost += int(ship.cost*.2)
								#ship.num_of_upgrades+=1
								self.addCurrency(-1*int(self.fleet[i].cost*.2))
					i-=1
			except AttributeError:
				pass
			self.put()
			users(True)

	def getAttacks(self):
		attks=[]
		for i in self.attacks:
			attks.append(i)
		return attks
	
	def getReturnTimes(self):
		attks=self.getAttacks()
		times=[]
		for i in attks:
			times.append(int(i.return_time-(datetime.now()-i.time_fought).total_seconds()))
				     
		return times

	def setPassword(cookie,password):
		if cookie:
			key=check_secure_val(cookie)
			if key==self.key:
				self.password=hash_str(password)
				users(True)
				return True
		return False

	def setEmail(self,email):
		self.email=email
		self.put()
		users(True)

	def setPrefs(self,json):
		self.prefs=json
		self.put()
		users(True)

	def setLastLogin(self):
		self.last_login=datetime.now()
		self.put()
		users(True)

	def addDrones(self,num):
		self.drones+=num
		if self.drones<=100:
			self.resources.currency_add=self.drones
		elif self.drones<=200:
			self.resources.currency_add=int(100+(0.8*(self.drones-100)))
		elif self.drones<=300:
			self.resources.currency_add=int(180+(0.6*(self.drones-200)))
		elif self.drones<=700:
			self.resources.currency_add=int(240+(0.4*(self.drones-300)))
		elif self.drones<=1000:
			self.resources.currency_add=int(400+(0.333333333*(self.drones-700)))
		elif self.drones<=2000:
			self.resources.currency_add=int(500+(0.1*(self.drones-1000)))
		elif self.drones<=7000:
			self.resources.currency_add=int(600+(0.05*(self.drones-2000)))
		else:
			self.resources.currency_add=int(700+(0.01*(self.drones-7000)))
		self.put()
		users(True)

	def getResources(self):
		time=datetime.now()
		value_adj=currencyAdjust(self,time)
		return [self.resources.currency+value_adj,self.drones]
		
	def setResources(self,currency):
		self.resources.currency=currency
		self.resources.currency_updated=datetime.now()
		self.put()
		users(True)
		
	def setIncomeRate(self,num):
		self.resources.currency_add=num
		self.put()
		users(True)

	def addCurrency(self,num):
		time=datetime.now()
		self.resources.currency+=num+int(currencyAdjust(self,time))
		self.resources.currency_updated=time
		self.put()
		users(True)

	def getHomeUnits(self):
		if not self.attacks:
			return self.fleet
		i=0
		n=len(self.attacks)
		needUpdate=False
		while i<n:
			dif=(datetime.now()-self.attacks[i].time_fought).total_seconds()
			if dif>self.attacks[i].return_time:
				s=self.attacks[i].all_ships.split('|')
				logging.error(s)
				for j in range(len(s)-1):
					attributes=s[j].split(',')
					add=stringToShip(s[j])
					self.addShip(add)
				self.attacks.remove(self.attacks[i])
				needUpdate=True
				i-=1
			i+=1
			n=len(self.attacks)
		if needUpdate:
			self.put()
			users(True)	
		return self.fleet

def currencyAdjust(user,time):
	return (int)(((time-user.resources.currency_updated).total_seconds())/60)*user.resources.currency_add
def users(update=False):
	key="users"
	accs=memcache.get(key)
	if accs is None or update:
		accs = ndb.gql("SELECT * FROM User")
		accs=list(accs)
		memcache.set(key,accs)
	return accs

def NewAccount(username="",password="",email=""):
	a=User(username=username, password=hash_str(password), email=email, resources=Resources(currency=100, currency_add=5),drones=5)
	a.newMessage("Welcome to Text Sector!", "For help and tutorials go to www.textsector.com/game/tutorials")
	key=a.newMessage("Notice","You have been awarded 100 currency and 10 units.")
	users(True)
	return key

def isValidLogin(username,password):
	accs=users()
	for i in accs:
		if i.username == username:
			cpassword=i.password
			if i.password == hash_str(password):
				return i.key
	return None

def getResources(key):
	accs=users()
	for i in accs:
		if i.key==key:
			return ResourceDatabase.getResources(i.resource_key)

def getUsername(key):
	a=key.get()
	return a.username
