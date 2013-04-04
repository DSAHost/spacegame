import webapp2
import jinja2
import os
from google.appengine.ext import ndb
import hashlib
import hmac
import logging
import json
from google.appengine.api import memcache

class Attack(ndb.Model):
	attacker_key=ndb.StringProperty(required=True)
	defender_key=ndb.StringProperty(required=True)
	units=ndb.IntegerProperty(required=True)
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

 
