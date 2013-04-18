from Handler import *
from utils import *

class FrontHandler(Handler):
    def get(self):
        self.render("front.html", username=self.user)
