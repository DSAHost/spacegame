from Handler import *
from utils import *

class ManageUnitsHandler(Handler):
    def get(self):
        self.render("manageunits.html", username=self.user)
