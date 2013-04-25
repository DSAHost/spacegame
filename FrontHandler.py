from Handler import *
from utils import *

class FrontHandler(Handler):
    def get(self):
    	if self.user:
    		self.redirect('/game')
    	else:
        	self.render("front.html", user=self.user)
