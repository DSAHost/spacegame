from Handler import *
from utils import *
from UserDatabase import *

Infringer=Ship(armor=40,damage=45,mobility=1,shipclass="Capital",cost=12000,name="Infringer")
Dagger=Ship(armor=4,damage=8,mobility=10,shipclass="Fighter",cost=800,name="Dagger")
Artifact=Ship(armor=23,damage=24,mobility=4,shipclass="Cruiser",cost=7000,name="Artifact")
Hawk=Ship(armor=8,damage=12,mobility=8,shipclass="Bomber",cost=1800,name="Hawk")
Ogre=Ship(armor=29,damage=28,mobility=3,shipclass="Cruiser",cost=9200,name="Ogre")
Songbird=Ship(armor=1,damage=5,mobility=18,shipclass="Fighter",cost=200,name="Songbird")
Frisbee=Ship(armor=18,damage=22,mobility=7,shipclass="Frigate",cost=4200,name="Frisbee")
Pestilence=Ship(armor=10,damage=15,mobility=5,shipclass="Corvette",cost=2200,name="Pestilence")
Flounder=Ship(armor=15,damage=18,mobility=9,shipclass="Frigate",cost=3700,name="Flounder")
Longbow=Ship(armor=20,damage=22,mobility=9,shipclass="Frigate",cost=5000,name="Longbow")
Parrot=Ship(armor=99,damage=124,mobility=1,shipclass="Capital",cost=28000,name="Parrot")

ships=[Songbird,Dagger,Hawk,Pestilence,Flounder,Frisbee,Longbow,Artifact,Ogre,Infringer,Parrot]
match={"Songbird":Songbird,"Dagger":Dagger,"Hawk":Hawk,"Pestilence":Pestilence,"Flounder":Flounder,"Frisbee":Frisbee,"Longbow":Longbow,"Artifact":Artifact,"Ogre":Ogre,"Infringer":Infringer,"Parrot":Parrot}
class UnitPurchaseHandler(Handler):
	def render_front(self,error="",name=""):
		self.render("unitpurchase.html",ships=ships,error=error,name=name)
	
	def get(self):
	 	if self.user:
	 		self.render_front()
	 	else:
	 		self.redirect('/login')

	def post(self):
		id=self.request.get("ship") #testing.  This must correspond to which buy button was pressed
		ship=match[id]
		if ship.cost<self.user.getResources()[0]:
			self.user.addShip(ship)
			self.user.addCurrency(-ship.cost)
			self.redirect('/game')
			return
		else:
			self.render_front(error="You do not have enough credits to purchase this ship.",name=id)
