import webapp2
import jinja2
import os
from google.appengine.ext import ndb
import hashlib
import hmac
import logging
import json
from google.appengine.api import memcache

class User(ndb.Model):
	username=ndb.StringProperty(required=True)
	password=ndb.StringProperty(required=True)
	email=ndb.StringProperty(required=True)
	prefs=ndb.JsonProperty()
	last_login=ndb.DateTimeProperty(auto_now_add=True)

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
		a.put()
		users(True)
		return {} 
	return errors

def get_Login_Cookie(username=""):
	return make_secure_val(username)




