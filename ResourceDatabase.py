from Handler import *

class Resources(ndb.Model):
	username=ndb.StringProperty(required=True)
	
	currency=ndb.IntegerProperty(required=True)
	currency_add=ndb.IntegerProperty()
	currency_updated=ndb.DateTimeProperty(auto_now_add=True)
	
	combat_units=ndb.IntegerProperty(required=True)
	home_units=ndb.IntegerProperty()
	
def resources(update=False):
	key="resources"
	poss=memcache.get(key)
	if poss is None or update:
		poss=ndb.gql("SELECT * FROM Resources")
		poss=list(poss)
		memcache.set(key,poss)
	return poss
	
def getResources(key):
	rec=resources()
	resource=None
	for i in rec:
		if i.key == key:
			resource=i
	time=datetime.now()
	value_adj=currencyAdjust(resource,time)
	return [resource.currency+value_adj,resource.home_units]

def setResources(key,currency,combat_units):
	resource=key.get()
	resource.currency=currency
	resource.home_units=combat_units
	resource.currency_updated=datetime.now()
	resource.put()
	resources(True)

def addCombatUnits(key,num):
	resource=key.get()
	resource.combat_units+=num
	resource.home_units+=num
	resource.put()
	resources(True)

def addCurrency(key,num):
	resource=key.get()
	time=datetime.now()
	resource.currency+=num+currencyAdjust(resource,time)
	resource.currency_updated=time
	resource.put()
	resources(True)
	
def setIncomeRate(key,num):
	resource=key.get()
	resource.currency_add=num
	resource.put()
	resources(True)
	
def currencyAdjust(resource,time):
	return (int)(((time-resource.currency_updated).total_seconds())/60)*resource.currency_add

#def get_Home_Units(key):
	
