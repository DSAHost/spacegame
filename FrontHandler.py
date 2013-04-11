from Handler import *
from utils import *

class FrontHandler(Handler):
    def get(self):
    	#if self.user:
    	#	self.redirect("/game")
        self.render("front.html", username=self.user)
