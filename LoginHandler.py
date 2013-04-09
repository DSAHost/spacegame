from Handler import *
from utils import *
import UserDatabase

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
			# cookieval=UserDatabase.get_Cookie_Val(login)
			# self.response.headers['Content-Type'] = 'text/plain'
			# self.response.headers.add_header('Set-Cookie', 'key=%s; Path=/;' % cookieval)
			self.set_secure_cookie(self.user_cookie_name, login)
			self.redirect("/")
		else:
			error="Your username or password could not be verified"
			self.render_front(username,error)


