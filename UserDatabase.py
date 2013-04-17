from Handler import *
import ResourceDatabase

class User(ndb.Model):
	username=ndb.StringProperty(required=True)
	password=ndb.StringProperty(required=True)
	email=ndb.StringProperty(required=True)
	prefs=ndb.JsonProperty()
	last_login=ndb.DateTimeProperty(auto_now_add=True)
	resource_key=ndb.KeyProperty()

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

def setPassword(cookie,password):
	if cookie:
		key=check_secure_val(cookie)
		if key:
			account=key.get()
			account.password=hash_str(password)
			account.put()
			users(True)
			return True
	return False
	
def setEmail(user,email):
	user.email=email
	user.put()
	users(True)

def setPrefs(user,json):
	user.prefs=json
	user.put()
	users(True)

def setLastLogin(user):
	user.last_login=datetime.now()
	user.put()
	users(True)

def getResources(user):
	return ResourceDatabase.getResources(user.resource_key)
	
def getResources(key):
	accs=users()
	for i in accs:
		if i.key==key:
			return ResourceDatabase.getResources(i.resource_key)
	
def setResources(user,currency,combat_units):
	ResourceDatabase.setResources(user.resource_key,currency,combat_units)
	
def addCombatUnits(user,num):
	ResourceDatabase.addCombatUnits(user.resource_key,num)

def addCurrency(user,num):
	ResourceDatabase.addCurrency(user.resource_key,num)
	
def setIncomeRate(user,num):
	ResourceDatabase.setIncomeRate(user.resource_key,num)
	
def updateCurrency(user):
	ResourceDatabase.updateCurrency(user.resource_key)

