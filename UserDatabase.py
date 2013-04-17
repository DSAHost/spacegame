from Handler import *
import ResourceDatabase
import MessageDatabase
import AttackDatabase

class User(ndb.Model):
	username=ndb.StringProperty(required=True)
	password=ndb.StringProperty(required=True)
	email=ndb.StringProperty(required=True)
	prefs=ndb.JsonProperty()
	last_login=ndb.DateTimeProperty(auto_now_add=True)
	resource_key=ndb.KeyProperty()
	attacks=ndb.KeyProperty(repeated=True)
	messages=ndb.KeyProperty(repeated=True)

	def newMessage(self,s,c):
		messages=MessageDatabase.newMessage(s,c)

	def newAttack(self,dname,troops,time):
		attacks=AttackDatabase.newAttack(self.key,dname,troops,time)

	def getMessages(self):
		mess=[]
		for i in self.messages:
			mess.append(i.get())
		return mess
		
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
		return ResourceDatabase.getResources(self.resource_key)
		
	def setResources(self,currency,combat_units):
		ResourceDatabase.setResources(self.resource_key,currency,combat_units)
		
	def addCombatUnits(self,num):
		ResourceDatabase.addCombatUnits(self.resource_key,num)

	def addCurrency(self,num):
		ResourceDatabase.addCurrency(self.resource_key,num)
		
	def setIncomeRate(self,num):
		ResourceDatabase.setIncomeRate(self.resource_key,num)
		
	def updateCurrency(self):
		ResourceDatabase.updateCurrency(self.resource_key)

	def getHomeUnits(self):
		for i in self.attacks:
			a=AttackDatabase.isFinished(i)
			if a>0:
				self.home_units+=a
				attacks.remove(i)

def users(update=False):
	key="users"
	accs=memcache.get(key)
	if accs is None or update:
		logging.error("USER QUERY")
		accs = ndb.gql("SELECT * FROM User")
		accs=list(accs)
		memcache.set(key,accs)
	return accs

def NewAccount(username="",password="",email=""):
	a=User(username=username, password=hash_str(password), email=email)
	b=ResourceDatabase.Resources(username=username,currency=0,combat_units=0,home_units=0,currency_add=20)
	a.resource_key=b.put()
	a.messages=None
	a.attacks=None
	key=a.put()
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




