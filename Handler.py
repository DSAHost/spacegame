import webapp2
import cgi
import os
import jinja2
import logging
import hashlib
from google.appengine.ext import ndb
from utils import *
import hmac
import json
from google.appengine.api import memcache
from datetime import *
from google.appengine.ext.db import Key
import UserDatabase

class Handler(webapp2.RequestHandler):

	# calls default initializer (syntax for future, does nothing yet)
 	def initialize(self, *a, **kw):
 		# default initializer
		webapp2.RequestHandler.initialize(self, *a, **kw)
		# set up login data
		self.user_cookie_name = 'user_id'
		uid = self.read_secure_cookie(self.user_cookie_name)
		key=None
		self.user=None
		if uid:
			key=ndb.Key(urlsafe=uid)
			self.user=key.get()
		# set up jinja2 workspace
		self.template_dir = os.path.join(os.path.dirname(__file__), 'html')
		self.jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(self.template_dir), autoescape=True)

	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	# returns html from jinja template with parameters as a string
	# takes template file name as first argument
	def render_str(self, template, **params):
		if self.user:
			self.user.getHomeUnits()
			username=self.user.username.capitalize()
			resources=self.user.getResources()
			attacks=self.user.getAttacks()
			times=self.user.getReturnTimes()
			num_attacks=range(len(attacks))
			params['username']=username
			params['currency']=resources[0]
			params['attacks']=attacks
			params['times']=times
			params['num_attacks']=num_attacks
			params['user']=self.user
			params['drones']=self.user.drones
		t = self.jinja_env.get_template(template)
		return t.render(params)

	# writes to webpage from jinja template
	# takes template file name as first argument
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

	# add a hashed cookie to the user's browser
	def set_secure_cookie(self, name, val, days = None):
		cookie_val = make_secure_val(str(val))
		if not val:
			self.response.headers.add_header('Set-Cookie', '%s=; Path=/;' % name)
		elif days == None:
			self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/;' % (name, cookie_val))
		else:
			expiration = datetime.datetime.now() + datetime.timedelta(days = days)
			self.response.headers.add_header('Set-Cookie', '%s=%s; expires=%s; Path=/;' % (name, cookie_val, expiration.strftime("%a, %d-%b-%Y %H:%M:%S GMT")))

	# returns value from user's browser cookie, or None if cookie is invalid
	def read_secure_cookie(self, name):
		cookie_val = self.request.cookies.get(name)
		if cookie_val and check_secure_val(cookie_val):
			return cookie_val.split('|')[0]
