from Handler import *
from utils import *

class UnitPurchaseHandler(Handler):
    def get(self):
        self.render("unitpurchase.html", username=self.user)
