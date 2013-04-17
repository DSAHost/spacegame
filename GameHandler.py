from Handler import *
import ResourceDatabase
import UserDatabase

# temporary test class
class Message():
	def __init__(self,subject,content):
		self.subject=subject
		self.content=content

class GameHandler(Handler):
	def render_front(self, username, currency, units):
		self.render("gamefront.html", username=username,currency=currency, units=units, messages=[Message('Hello','world!'),Message('Attacked by tgillani','You lost: 12 Opponent lost: 4')])
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