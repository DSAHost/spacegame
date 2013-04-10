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
	b=ResourceDatabase.Resources(username=username,currency=0,combat_units=0)
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
			return True
	return False
	
def setEmail(key,email):
	account=key.get()
	account.email=email
	account.put()

def setPrefs(key,json):
	account=key.get()
	account.prefs=json
	account.put()

def setLastLogin(key):
	account=key.get()
	account.last_login=datetime.now()
	account.put()
	
def getResources(key):
	account=key.get()
	return ResourceDatabase.getResources(account.resource_key)
	
def setResources(key,currency,combat_units):
	account=key.get()
	ResourceDatabase.setResources(account.resource_key,currency,combat_units)
	
def addCombatUnits(key,num):
	account=key.get()
	ResourceDatabase.addCombatUnits(account.resource_key,num)

def addCurrency(key,num):
	account=key.get()
	ResourceDatabase.addCurrency(account.resource_key,num)
	
def setIncomeRate(key,num):
	account=key.get()
	ResourceDatabase.setIncomeRate(account.resource_key,num)
	
def updateCurrency(key):
	account=key.get()
	ResourceDatabase.updateCurrency(account.resource_key)

