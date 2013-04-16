from Handler import *
from UserDatabase import *

class LoginHandler(Handler):
	def render_front(self,username="",error=""):
		self.render("login.html",username=username,error=error)
	def get(self):	
		self.render_front()
	def post(self):
		username=self.request.get('username')
		password=self.request.get('password')

		cookieval=""

		login=isValidLogin(username,password)
		strlogin=None
		if login:
			strlogin=login.urlsafe()
		logging.error(strlogin)
		if login:
			self.set_secure_cookie('user_id', strlogin)
			self.redirect("/game")
		else:
			error="Your username or password could not be verified."
			self.render_front(username,error)


class LogoutHandler(Handler):
	def get(self):
		self.set_secure_cookie('user_id', None)
		self.redirect('/')