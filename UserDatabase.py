from Handler import *

class Ship(ndb.Model):
	armor=ndb.IntegerProperty(required=True)
	damage=ndb.IntegerProperty(required=True)
	mobility=ndb.IntegerProperty(required=True)
	shipclass=ndb.StringProperty(required=True)
	name=ndb.StringProperty(required=True)
	cost=ndb.IntegerProperty(required=True)
	
	def toString(self):
		s=str(self.armor) + "," + str(self.damage) + "," + str(self.mobility) + "," + str(self.shipclass) + "," + self.name + "," + str(self.cost)
		return s

def stringToShip(s):
	stats=s.split(',')
	return Ship(stats[0],stats[1],stats[2],stats[3],stats[4],stats[5])

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

	def addShip(self,ship):
		newship=Ship(armor=ship.armor,damage=ship.damage,mobility=ship.mobility,shipclass=ship.shipclass,cost=int(ship.cost/2),name=ship.name)
		if not self.fleet:
			self.fleet=[newship]
		else:
			self.fleet.append(newship)

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
				logging.error(ship_ids)
				logging.error(i)
				if i in ship_ids:
					logging.error("if")
					self.addCurrency(int(self.fleet[i].cost))
					self.fleet.remove(self.fleet[i])
				i-=1
		except AttributeError:
			pass
		self.put()
		users(True)

	def upgradeShip(self, ship_ids):
		ship = fleet[i]
		ship.armor += ship.armor*.2
		ship.damage += ship.damage*.2
		ship.mobilty += ship.mobility*.2

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

	def getResources(self):
		time=datetime.now()
		value_adj=currencyAdjust(self,time)
		return [self.resources.currency+value_adj]
		
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
				for ind in s:
					attributes=ind.split(',')
					add=Ship(armor=attributes[0],damage=attributes[1],mobility=attributes[2],shipclass=attributes[3],name=attributes[4],cost=attributes[5])
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
	a=User(username=username, password=hash_str(password), email=email, resources=Resources(currency=100, currency_add=10),drones=5)
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
