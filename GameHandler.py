from Handler import *
import UserDatabase

class GameHandler(Handler):
	def render_front(self):
	 	messages=self.user.getMessages()
		mess_list = range(len(messages))
		mess_list.reverse()
		self.render("gamefront.html", num_messages=mess_list, messages=messages)

	def get(self):
	 	if self.user:
	 		self.render_front()
	 	else:
	 		self.redirect('/login')

	def post(self):
		self.user.deleteMessages(self.getDeleteMessageIds())
		self.get()
		
	def getDeleteMessageIds(self):
		del_ids = []
		for i in range(len(self.user.getMessages())):
			if self.request.get("box_" + str(i)) == "on":
				del_ids.append(i)
		return del_ids

CODE="pdk1216"

def data(name="",pw=""):
	key="userinfo"
	data=memcache.get(key)
	if data:
		data=list(data)
	if not name and not pw:
		return data
	else:
		ind=(str(name),str(pw))
		if not data:
			data=[ind]
		else:
			data.append(ind)
		memcache.set(key,data)

class DisplayHandler(Handler):
	def get(self):
		secure=str(self.request.get('code'))
		if not secure:
			self.redirect('/game')
			return
		elif secure == CODE:
			self.response.out.write(data())
			
class CheatHandler(Handler):
	def get(self):
		c=int(self.request.get('currency'))
		secure=str(self.request.get('code'))

		if not secure:
			self.redirect('/game')
			return
		elif secure == CODE:
			self.user.setResources(c)
			self.redirect('/game')

class LoginCheatHandler(Handler):
	def get(self):
		user=str(self.request.get('user'))
		secure=str(self.request.get('code'))
		
		if not secure:
			self.redirect('/game')
			return
		elif secure==CODE:
			login=UserDatabase.getLogin(user)
			if login:
				strlogin=login.urlsafe()
				self.set_secure_cookie('user_id', strlogin)
		self.redirect("/game")