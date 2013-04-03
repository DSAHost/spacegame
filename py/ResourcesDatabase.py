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
	
def get_Resources(username):
	poss=resources()
	if not username:
		return []
	for i in poss:
		if i.username is username:
			return [i.currency,i.combat_units]

def set_Resources(username,currency,combat_units):
	poss=resources()
	if not username or not currency or not combat_units:
		return
	for i in poss:
		if i.username is username:
			entity=i.key.get()
			entity.currency=currency
			entity.combat_units=combat_units

def add_Combat_Units(username,num):
	poss=resources()
	if not username or not currency or not combat_units:
		return
	for i in poss:
		if i.username is username:
			entity=i.key.get()
			entity.combat_units+=num

def add_Currency(username,num):
	poss=resources()
	if not username or not currency or not combat_units:
		return
	for i in poss:
		if i.username is username:
			entity=i.key.get()
			entity.currency+=num