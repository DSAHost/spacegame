from Handler import *
import ResourceDatabase
import UserDatabase
from MessageDatabase import *
# temporary test class

class Message():
	def __init__(self,subject,content):
		self.subject=subject
		self.content=content

class GameHandler(Handler):
	def render_front(self, username, currency, units, messages):
		self.render("gamefront.html", username=username,currency=currency, units=units, messages=messages)
	def get(self):
	 	if self.user:
	 		username=self.user.username
	 		resources=self.user.getResources()

	 		self.render_front(username,resources[0],resources[1],self.user.getMessages())
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
			self.user.setResources(c,u)
			self.redirect('/game')