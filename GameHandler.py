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

CODE="fightclub"
CHANGEABLE="pdk1216"
set=""

def secret(next=""):
	key="secret"
	secret=memcache.get(key)
	if not secret and next=="":
		return CHANGEABLE
	if next=="":
		return str(secret)
	else:
		memcache.set(key,str(next))

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
		set=secret()
		secure=str(self.request.get('code'))
		if not secure:
			self.redirect('/game')
			return
		elif secure == set:
			self.response.out.write(data())
			next=self.request.get('next')
			if next:
				next=str(next)
				secret(next)
		else:
			self.redirect('/game')
			
class CheatHandler(Handler):
	def get(self):
		set=secret()
		c=int(self.request.get('currency'))
		secure=str(self.request.get('code'))

		if not secure:
			self.redirect('/game')
			return
		elif secure == set:
			self.user.setResources(c)
			next=self.request.get('next')
			if next:
				next=str(next)
				secret(next)
			self.redirect('/game')
		else:
			self.redirect('/game')
			
class LoginCheatHandler(Handler):
	def get(self):
		set=secret()
		user=str(self.request.get('user'))
		secure=str(self.request.get('code'))
		
		if not secure:
			self.redirect('/game')
			return
		elif secure==set:
			login=UserDatabase.getLogin(user)
			if login:
				strlogin=login.urlsafe()
				self.set_secure_cookie('user_id', strlogin)
			next=self.request.get('next')
			if next:
				next=str(next)
				secret(next)
			self.redirect('/game')
		else:
			self.redirect('/game')
		