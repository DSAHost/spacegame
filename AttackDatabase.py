from Handler import *
from UserDatabase import *

class Attack(ndb.Model):
	attacker_key=ndb.KeyProperty(required=True)
	defender_key=ndb.KeyProperty(required=True)
	num_troops=ndb.IntegerProperty(required=True)
	time_fought=ndb.DateTimeProperty(auto_now_add=True)
	return_time=ndb.IntegerProperty(required=True)

def attacks(update=False):
	key="attacks"
	attks=memcache.get(key)
	if attks is None or update:
		attks=ndb.gql("SELECT * FROM Attack")
		attks=list(attks)
		memcache.set(key,attks)
	return attks

def isFinished(key):
	attacks=attacks()
	t=0
	for i in attacks:
		if i.key==key:
			dif=(datetime.datetime.now()-i.time_fought).total_seconds()
			if dif>i.return_time:
				t=i.num_troops
				key.delete()
				attacks(True)
				return t
	return t

def newAttack(attkerkey,defender,troops,time):
	accs=users()
	dkey=None
	for i in accs:
		if i.username==defender:
			dkey=i.key
	attk=Attack(attacker_key=attkerkey, defender_key=dkey, num_troops=troops, return_time=time)
	a=attk.put()
	attacks(True)
	return a

def timeToReturn(key):
	attacks=attacks()
	for i in attacks:
		