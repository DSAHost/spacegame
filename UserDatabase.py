from Handler import *
import AttackDatabase

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

def getResources(key):
	rec=resources()
	resource=None
	for i in rec:
		if i.key == key:
			resource=i
	time=datetime.now()
	value_adj=currencyAdjust(resource,time)
	return [resource.currency+value_adj,resource.home_units]
	
class User(ndb.Model):
	username=ndb.StringProperty(required=True)
	password=ndb.StringProperty(required=True)
	email=ndb.StringProperty(required=True)
	prefs=ndb.JsonProperty()
	last_login=ndb.DateTimeProperty(auto_now_add=True)
	resources=ndb.StructuredProperty(Resources)
	attacks=ndb.KeyProperty(repeated=True)
	messages=ndb.StructuredProperty(Message, repeated=True)

	def newMessage(self,s,c):
		messages=Message(subject=s,content=c)

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
			a=AttackDatabase.isFinished(i)
			if a>0:
				self.home_units+=a
				attacks.remove(i)
def currencyAdjust(user,time):
	return (int)(((time-user.resources.currency_updated).total_seconds())/60)*user.resources.currency_add
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
	a=User(username=username, password=hash_str(password), email=email, resources=Resources(currency=0, currency_add=20,combat_units=0, home_units=0))
	a.newMessage("Welcome to Text Sector!", "For help and tutorials go to www.textsector.com/game/tutorials")
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




