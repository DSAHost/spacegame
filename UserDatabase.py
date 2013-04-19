from Handler import *

class Attack(ndb.Model):
	attacker_key=ndb.KeyProperty(required=True)
	defender_key=ndb.KeyProperty(required=True)
	num_troops=ndb.IntegerProperty(required=True)
	time_fought=ndb.DateTimeProperty(auto_now_add=True)
	return_time=ndb.IntegerProperty(required=True)

class Message(ndb.Model):
	subject=ndb.StringProperty(required=True)
	content=ndb.StringProperty(required=True)
	created=ndb.DateTimeProperty(auto_now_add=True)

class Resources(ndb.Model):	
	currency=ndb.IntegerProperty(required=True)
	currency_add=ndb.IntegerProperty()
	currency_updated=ndb.DateTimeProperty(auto_now_add=True)
	
	combat_units=ndb.IntegerProperty(required=True)
	home_units=ndb.IntegerProperty()
	
class User(ndb.Model):
	attacks=ndb.StructuredProperty(Attack,repeated=True)
	email=ndb.StringProperty(required=True)
	last_login=ndb.DateTimeProperty(auto_now_add=True)
	messages=ndb.StructuredProperty(Message, repeated=True)
	password=ndb.StringProperty(required=True)
	prefs=ndb.JsonProperty()
	resources=ndb.StructuredProperty(Resources)
	username=ndb.StringProperty(required=True)

	def newMessage(self,s,c):
		if not self.messages:
			self.messages=[Message(subject=s,content=c)]
		else:
			self.messages.append(Message(subject=s, content=c))

		return self.put()

	def newAttack(self,dname,troops,time):
		accs=users()
		dkey=None
		for i in users:
			if i.username==defender:
				dkey=i.key
		if not self.attacks:
			self.attacks=[Attack(self.key,dkey,troops,time)]
		else:
			self.attacks.append(Attack(self.key,dkey,troops,time))
		self.put()

	def getMessages(self):
		mess=[]
		for i in self.messages:
			mess.append(i)
		return mess
		
	def deleteMessages(self, message_ids):
		try:
			message_ids.sort()
			message_ids.reverse()
			for message_id in message_ids:
				self.messages.remove(self.messages[message_id])
		except AttributeError:
			pass
		self.put()

	def getAttacks(self):
		attks=[]
		for i in self.attacks:
			attks.append(i)
		return attks
	
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
		return [self.resources.currency+value_adj,self.resources.home_units]
		
	def setResources(self,currency,combat_units,home_units):
		self.resources.currency=currency
		self.resources.combat_units=combat_units
		self.resources.home_units=home_units
		self.put()
		users(True)

	def addCombatUnits(self,num):
		self.resources.combat_units+=num
		self.resources.home_units+=num
		self.put()
		users(True)
	def setIncomeRate(self,num):
		self.resources.currency_add=num
		self.put()
		users(True)

	def addCurrency(self,num):
		time=datetime.now()
		self.resources.currency+=num+currencyAdjust(self,time)
		self.resources.currency_updated=time
		self.put()
		users(True)

	def getHomeUnits(self):
		for i in self.attacks:
			dif=(datetime.datetime.now()-i.time_fought).total_seconds()
			if dif>i.return_time:
				self.home_units+=i.num_troops
				attacks.remove(i)

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
	a=User(username=username, password=hash_str(password), email=email, resources=Resources(currency=100, currency_add=20,combat_units=10, home_units=10))
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
