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
		oldpass=""
		newpass=""
		verify=""
		error=""
		olderror=""
		verifyerror=""
		passerror=""
		try:
			oldpass=str(self.request.get('old'))
			newpass=str(self.request.get('password'))
			verify=str(self.request.get('verify'))
		except ValueError:
			error="There was an error in your input."
		if not oldpass:
			olderror="Your current password could not be verified."
		if not newpass:
			passerror="You must enter a new password."
		if not verify:
			verifyerror="You must verify your password."
		if passerror or verifyerror or olderror or error:
			self.render_front(error=error,verifyerror=verifyerror,passerror=passerror,olderror=olderror)
			return
		if newpass==verify:
			if oldpass==newpass:
				self.render_front(error="Your old and new passwords may not match.")
				return
			if self.user.setPassword(oldpass,newpass):
				self.redirect('/game')
			else:
				self.render_front(olderror="Your current password could not be verified.")
				return
		else:
			self.render_front(verifyerror="Your passwords must match.")