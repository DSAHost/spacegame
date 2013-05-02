from Handler import *

class PasswordChangeHandler(Handler):
	def render_front(self,error="",verifyerror="",passerror="",olderror=""):
		self.render("password.html",error=error,verifyerror=verifyerror,passerror=passerror,olderror=olderror)

	def get(self):
	 	if self.user:
	 		self.render_front()
	 	else:
	 		self.redirect('/login')

	def post(self):
		try:
			oldpass=str(self.request.get('old'))
			newpass=str(self.request.get('password'))
			verify=str(self.request.get('verify'))
		except ValueError:
			self.render_front(error="There was an error in your input.")
			if newpass==verify:
				if self.user.setPassword(oldpass,newpass):
					self.redirect('/game')
				else:
					self.render_front(olderror="Your current password could not be verified.")
					return

			else:
				self.render_front(verifyerror="Your passwords must match.")