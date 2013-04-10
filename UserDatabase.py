from Handler import *
from ResourceDatabase import *

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
	b=Resources(username=username,currency=0,combat_units=0)
	a.resource_key=b.put()
	key=a.put()
	users(True)
	return key

def get_Login_Cookie(key):
	return make_secure_val(key)

def is_Valid_Login(username,password):
	accs=users()
	for i in accs:
		if i is username:
			cpassword=i.password
			if i.password is hash_str(password):
				return i.key
	return None

def set_Password(cookie,password):
	if cookie:
		key=check_secure_val(cookie)
		if key:
			account=key.get()
			account.password=hash_str(password)
			account.put()
			return True
	return False
	
def set_Email(key,email):
	account=key.get()
	account.email=email
	account.put()

def set_Prefs(key,json):
	account=key.get()
	account.prefs=json
	account.put()

def set_Last_Login(key):
	account=key.get()
	account.last_login=datetime.now()
	account.put()
	
def get_Resources(key):
	account=key.get()
	return ResourceDatabase.get_Resources(account.resource_key)
	
def set_Resources(key,currency,combat_units):
	account=key.get()
	ResourceDatabase.set_Resources(account.resource_key,currency,combat_units)
	
def add_Combat_Units(key,num):
	account=key.get()
	ResourceDatabase.add_Combat_Units(accounts.resource_key,num)

def add_Currency(key,num):
	account=key.get()
	ResourceDatabase.add_Currency(accounts.resource_key,num)
	
def set_Income_Rate(key,num):
	account=key.get()
	ResourceDatabase.set_Income_Rate(accounts.resource_key,num)
	
def update_Currency(key):
	account=key.get()
	ResourceDatabase.update_Currency(accounts.resource_key)

