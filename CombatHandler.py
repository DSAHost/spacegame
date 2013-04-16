from Handler import *
from utils import *

class CombatHandler(Handler):
    def get(self):
        self.render("combat.html", username=self.user)
