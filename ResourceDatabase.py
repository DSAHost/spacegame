from Handler import *

class Resources(ndb.Model):
	username=ndb.StringProperty(required=True)
	
	currency=ndb.IntegerProperty(required=True)
	currency_add=ndb.IntegerProperty()
	currency_updated=ndb.DateTimeProperty()
	
	combat_units=ndb.IntegerProperty(required=True)
	home_units=ndb.IntegerProperty()
	
def resources(update=False):
	key="resources"
	poss=memcache.get(key)
	if poss is None or update:
		#logging.error("RESOURCE QUERY")
		poss=ndb.gql("SELECT * FROM Resources")
		poss=list(poss)
		memcache.set(key,poss)
	return poss
	
def get_Resources(key):
	resources=key.get()
	value_adj=(((datetime.datetime.now()-resources.currency_updated).total_seconds())%60)*resources.currency_add
	return [resources.currency+value_adj,resources.combat_units]

def set_Resources(key,currency,combat_units):
	resources=key.get()
	resources.currency=currency
	resources.combat_units=combat_units
	resources.put()

def add_Combat_Units(key,num):
	resources=key.get()
	resources.combat_units+=num
	resources.put()

def add_Currency(key,num):
	resources=key.get()
	resources.currency+=num
	resources.put()
	
def set_Income_Rate(key,num):
	resources=key.get()
	resources.currency_add=num
	resources.put()
	
def update_Currency(key):
	resources=key.get()
	time=datetime.datetime.now()
	resources.currency+=(((time-resources.currency_updated).total_seconds())%60)*resources.currency_add
	resources.currency_updated=time
	resources.put()

def get_Home_Units(key):
	
