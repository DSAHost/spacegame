from Handler import *

class SignupHandler(Handler):
	def render_front(self,username,usererror,password,passerror,error):
		self.render("signup.html",username=username, usererror=usererror, password=password, passerror=passerror, error=error)

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