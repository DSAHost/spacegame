from Handler import *

class Attack(ndb.Model):
	attacker_key=ndb.StringProperty(required=True)
	defender_key=ndb.StringProperty(required=True)
	units=ndb.IntegerProperty(required=True)
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

def is_Finished(key):
	attk=key.get()
	dif=(datetime.datetime.now()-attk.time_fought).total_seconds()
	if dif>attk.return_time:
		key.delete()
		return True
	return False

