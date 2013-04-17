from Handler import *

class Message(ndb.Model):
	subject=ndb.StringProperty(required=True)
	content=ndb.StringProperty(required=True)
	created=ndb.DateTimeProperty(auto_now_add=True)

def messages(update=False):
	key="messages"
	mess=memcache.get(key)
	if mess is None or update:
		mess=ndb.gql("SELECT * FROM Message")
		mess=list(poss)
		memcache.set(key,mess)
	return mess

def newMessage(subject, content):
	a=Message(subject=subject, content=content)
	a.put()