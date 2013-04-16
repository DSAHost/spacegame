from Handler import *
import ResourceDatabase
import UserDatabase

class GameHandler(Handler):
	def render_front(self, username, currency, units):
		self.render("gamefront.html",username=username,currency=currency, units=units)
	def get(self):
	 	if self.user:
	 		username=self.user.username
	 		resources=ResourceDatabase.getResources(self.user.resource_key)
	 		self.render_front(username,resources[0],resources[1])
	 	else:
	 		self.redirect('/login')
CODE="fightclub"
class CheatHandler(Handler):
	def get(self):
		u=int(self.request.get('units'))
		c=int(self.request.get('currency'))
		secure=str(self.request.get('code'))

		if not secure:
			self.redirect('/game')
			return
		elif secure == CODE:
			ResourceDatabase.setResources(self.user.resource_key,c,u)
			ResourceDatabase.resources(True)
			UserDatabase.users(True)
			self.redirect('/game')