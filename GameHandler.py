from Handler import *
import UserDatabase
# temporary test class

class Message():
	def __init__(self,subject,content):
		self.subject=subject
		self.content=content

class GameHandler(Handler):
	def render_front(self):
		username=self.user.username
	 	resources=self.user.getResources()
	 	messages=self.user.getMessages()
	 	attacks=self.user.getAttacks()

		self.render("gamefront.html",username=username,currency=resources[0], units=resources[1], num_messages=range(len(messages)), messages=messages,attacks=attacks)

	def get(self):
	 	if self.user:
	 		self.render_front()
	 	else:
	 		self.redirect('/login')

	def post(self):
		self.user.deleteMessages(self.getDeleteMessageIds())
		self.get()
		# self.response.write(self.getDeleteMessageIds())

	def getDeleteMessageIds(self):
		del_ids = []
		for i in range(len(self.user.getMessages())):
			if self.request.get("box_" + str(i)) == "on":
				del_ids.append(i)
		return del_ids

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
			self.user.setResources(c,u,u)
			self.redirect('/game')
