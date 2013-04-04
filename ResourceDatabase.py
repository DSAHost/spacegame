import webapp2
import jinja2
import os
from google.appengine.ext import ndb
import hashlib
import hmac
import logging
import json
from google.appengine.api import memcache

class Resources(ndb.Model):
	username=ndb.StringProperty(required=True)
	currency=ndb.IntegerProperty(required=True)
	combat_units=ndb.IntegerProperty(required=True)

def resources(update=False):
	key="resources"
	poss=memcache.get(key)
	if poss is None or update:
		logging.error("RESOURCE QUERY")
		poss=ndb.gql("SELECT * FROM Resources")
		poss=list(poss)
		memcache.set(key,poss)
	return poss
	
def get_Resources(key):
	resources=key.get()
	return [resources.currency,resources.combat_units]

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
