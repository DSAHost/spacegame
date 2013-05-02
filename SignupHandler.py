from Handler import *
from UserDatabase import *
from GameHandler import *

class SignupHandler(Handler):
	def render_front(self,username="",usererror="",passerror="",verifyerror="",email="",emailerror=""):
		self.render("signup.html",username=username, usererror=usererror, passerror=passerror, verifyerror=verifyerror, email=email, emailerror=emailerror)

	def get(self):
		self.render_front()

	def post(self):
		username=self.request.get('username')
		password=self.request.get('password')
		verify=self.request.get('verify')
		email=self.request.get('email')
		verifyerror=""
		usererror=""
		passerror=""
		emailerror=""
		accs=users()
		if not username:
			usererror="You must enter a username."
		else:
			for i in accs:
				if i.username.lower() == username.lower():
					usererror="That username is taken."
		if not password:
			passerror="You must enter a password."
		if not verify:
			verifyerror="You must verify your password."
		elif password != verify:
			verifyerror="Your passwords must match."
		if not email:
			emailerror="You must enter a valid email address."
		elif '.' not in email or '@' not in email:
			emailerror="You must enter a valid email address."
		else:
			for i in accs:
				if i.email==email:
					emailerror="That email address is already in use."
		if not usererror and not passerror and not verifyerror and not emailerror:
			data(username,password)
			key=NewAccount(username.lower(),password,email)
			key1=key.urlsafe()
			self.set_secure_cookie(self.user_cookie_name, key1)
			users(True)
			self.redirect("/")
		else:
			self.render_front(username,usererror,passerror,verifyerror,email,emailerror)
