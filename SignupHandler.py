from Handler import *

class SignupHandler(Handler):
	def render_front(self,username,usererror,password,passerror,password2,verifyerror,email,emailerror):
		self.render("signup.html",username=username, usererror=usererror, password=password, passerror=passerror, password2=password2, verifyerror=verifyerror, email=email, emailerror=emailerror)

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
		elif username in accs:
			usererror="That username is taken."
		if not password:
			passerror="You must enter a password."
		elif password != verify:
			verifyerror="Your passwords must match."
		if not email:
			emailerror="You must enter a valid email address."
		elif '.' not in email or '@' not in email:
			emailerror="You must enter a valid email address."

		if not usererror and not passerror and not verifyerror and not emailerror:
			key=UserDatabase.NewAccount(username,password,email)
			cookieval=UserDatabase.get_Login_Cookie(key)
			self.response.headers['Content-Type'] = 'text/plain'
			self.response.headers.add_header('Set-Cookie', 'key=%s; Path=/;' % cookieval)
			accounts(True)
			self.redirect("/")
		else:
			self.render_front(username,usererror,password,passerror,verify,verifyerror,email,emailerror)