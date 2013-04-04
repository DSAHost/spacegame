import webapp2
import jinja2
import os
from google.appengine.ext import ndb
import hashlib
import hmac
import logging
import json
from google.appengine.api import memcache
from ResourcesDatabase import *
from datetime import *

class User(ndb.Model):
	username=ndb.StringProperty(required=True)
	password=ndb.StringProperty(required=True)
	email=ndb.StringProperty(required=True)
	prefs=ndb.JsonProperty()
	last_login=ndb.DateTimeProperty(auto_now_add=True)
	resource_key=ndb.StringProperty()

SECRET = 'M82D94M'

def hash_str(s):
	return hmac.new(SECRET,s).hexdigest()

def make_secure_val(s):
	return "%s|%s" % (s,hash_str(s))

def check_secure_val(h):
	val=h.split('|')[0]
	if h==make_secure_val(val):
		return val

def users(update=False):
	key="users"
	accs=memcache.get(key)
	if accs is None or update:
		logging.error("USER QUERY")
		accs = ndb.gql("SELECT * FROM User")
		accs=list(accs)
		memecache.set(key,accs)
	return accs

def NewAccount(username="",password="",email=""):
	errors={}
	accs=users()
	if not username:
		errors['usererror']="You must enter a username."
	elif username in accs:
		errors['usererror']="That username is taken."
	if not password:
		errors['passerror']="You must enter a password."
	elif password != verify:
		errors['verifyerror']="Your passwords must match."
	if not email:
		errors['emailerror']="You must enter a valid email address"
	elif '.' not in email or '@' not in email:
		errors['emailerror']="You must enter a valid email address"

	if not errors:
		a=User(username=username, password=hash_str(password), email=email)
		b=Resources(username=username,currency=0,combat_units=0)
		a.resource_key=b.put()
		key=a.put()
		users(True)
		return {'key':key} 
	else:
		return errors

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

