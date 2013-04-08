import webapp2
import jinja2
import os
from google.appengine.ext import ndb
import logging
import hmac
import hashlib
import json
from time import strftime
from google.appengine.api import memcache
from datetime import *
from UserDatabase import *
from ResourceDatabase import *
from Handler import *

template_dir =os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),autoescape=True)

class Handler(webapp2.RequestHandler):
	def write(self,*a,**kw):
		self.response.out.write(*a,**kw)

	def render_str(self,template,**params):
		t=jinja_env.get_template(template)
		return t.render(params)

	def render(self,template, **kw):
		self.write(self.render_str(template,**kw))

class LoginHandler(Handler):
	def render_front(self,username="",error=""):
		self.render("login.html",username=username,error=error)
	def get(self):	
		self.render_front()
	def post(self):
		username=self.request.get('username')
		password=self.request.get('password')

		cookieval=""

		login=UserDatabase.is_Valid_Login(username,password)

		if login:
			cookieval=UserDatabase.get_Cookie_Val(login)
			self.response.headers['Content-Type'] = 'text/plain'
			self.response.headers.add_header('Set-Cookie', 'key=%s; Path=/;' % cookieval)
			self.redirect("/")
		else:
			error="Your username or password could not be verified"
			self.render_front(username,error)


