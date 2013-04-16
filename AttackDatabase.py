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
		logging.error("ATTACKS QUERY")
		attks=ndb.gql("SELECT * FROM Attack")
		attks=list(attks)
		memcache.set(key,attks)
	return attks

def isFinished(key):
	attk=key.get()
	dif=(datetime.datetime.now()-attk.time_fought).total_seconds()
	if dif>attk.return_time:
		key.delete()
		return True
	return False

def newAttack(attkerkey,defender,troops,time):
	accs=users()
	dkey=None
	for i in accs:
		if i.username==defender:
			dkey=i.key
	attk=Attack(attacker_key=attkerkey, defender_key=dkey, num_troops=troops, return_time=time)
	attk.put()