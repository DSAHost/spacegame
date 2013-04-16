from Handler import *
from utils import *

class ManageStationHandler(Handler):
    def get(self):
        self.render("managestation.html", username=self.user)
