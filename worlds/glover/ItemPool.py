from BaseClasses import Item
from typing import NamedTuple

class GloverItem(Item):
	#Start at 650000
	game: str = "Glover"

class ItemData(NamedTuple):
	glid: int|None = None
	qty: int = 0
	type: str = ""
	default_location: str = ""

def find_item_data(name : str) -> ItemData:
	#Garibs
	if name in world_garib_table:
		return world_garib_table[name]
	if name in garibsanity_world_table:
		return garibsanity_world_table[name]
	if name in decoupled_garib_table:
		return decoupled_garib_table[name]
	if name == "Garibsanity":
		return garbinsanity
	
    #Core
	if name in level_event_table:
		return level_event_table[name]
	if name in checkpoint_table:
		return checkpoint_table[name]
	if name in ability_table:
		return ability_table[name]
	
    #Filler
	if name in filler_table:
		return filler_table[name]
	if name in trap_table:
		return trap_table[name]
	
    #Fallthrough
	return ItemData()
	

level_event_table = {
	   #"AtlH 1 Star" : 						ItemData(None, 1, "", ""),
	   #"AtlH 2 Gate" : 						ItemData(None, 1, "", ""),
	   #"AtlH 2 Star" : 						ItemData(None, 1, "", ""),
	   #"AtlH 3 Gate" : 						ItemData(None, 1, "", ""),
	   #"AtlH 3 Star" : 						ItemData(None, 1, "", ""),
	   #"AtlH Boss Gate" : 						ItemData(None, 1, "", ""),
	   #"AtlH Boss Star" : 						ItemData(None, 1, "", ""),
	   #"AtlH Bonus Gate" : 					ItemData(None, 1, "", ""),
	   #"AtlH Bonus Star" : 					ItemData(None, 1, "", ""),
	   "Atl1 Gate" : 							ItemData(None, 1,  "Useful", "Atl1: Glover Switch")#,
	   #"Atl2 Elevator" : 						ItemData(None, 1, "", ""),
	   #"Atl2 Ballswitch Drain" : 				ItemData(None, 1, "", ""),
	   #"Atl2 Gate" : 							ItemData(None, 1, "", ""),
	   #"Atl3 Waterwheel" : 					ItemData(None, 1, "", ""),
	   #"Atl3 Cave Platforms" : 				ItemData(None, 1, "", ""),
	   #"CrnH 1 Star" : 						ItemData(None, 1, "", ""),
	   #"CrnH 2 Gate" : 						ItemData(None, 1, "", ""),
	   #"CrnH 2 Star" : 						ItemData(None, 1, "", ""),
	   #"CrnH 3 Gate" : 						ItemData(None, 1, "", ""),
	   #"CrnH 3 Star" : 						ItemData(None, 1, "", ""),
	   #"CrnH Boss Gate" : 						ItemData(None, 1, "", ""),
	   #"CrnH Boss Star" : 						ItemData(None, 1, "", ""),
	   #"CrnH Bonus Gate" : 					ItemData(None, 1, "", ""),
	   #"CrnH Bonus Star" : 					ItemData(None, 1, "", ""),
	   #"Crn1 Elevator" : 						ItemData(None, 1, "", ""),
	   #"Crn1 Gate" : 							ItemData(None, 1, "", ""),
	   #"Crn1 Door A" : 						ItemData(None, 1, "", ""),
	   #"Crn1 Door B" : 						ItemData(None, 1, "", ""),
	   #"Crn1 Door C" : 						ItemData(None, 1, "", ""),
	   #"Crn1 Rocket 1" : 						ItemData(None, 1, "", ""),
	   #"Crn1 Rocket 2" : 						ItemData(None, 1, "", ""),
	   #"Crn1 Rocket 3" : 						ItemData(None, 1, "", ""),
	   #"Crn2 Drop Garibs" : 					ItemData(None, 1, "", ""),
	   #"Crn2 Fan" : 							ItemData(None, 1, "", ""),
	   #"Crn3 Spin Door" : 						ItemData(None, 1, "", ""),
	   #"Crn3 Hands" : 							ItemData(None, 1, "", ""),
	   #"PrtH 1 Star" : 						ItemData(None, 1, "", ""),
	   #"PrtH 2 Gate" : 						ItemData(None, 1, "", ""),
	   #"PrtH 2 Star" : 						ItemData(None, 1, "", ""),
	   #"PrtH 3 Gate" : 						ItemData(None, 1, "", ""),
	   #"PrtH 3 Star" : 						ItemData(None, 1, "", ""),
	   #"PrtH Boss Gate" : 						ItemData(None, 1, "", ""),
	   #"PrtH Boss Star" : 						ItemData(None, 1, "", ""),
	   #"PrtH Bonus Gate" : 					ItemData(None, 1, "", ""),
	   #"PrtH Bonus Star" : 					ItemData(None, 1, "", ""),
	   #"Prt1 Raise Beach" : 					ItemData(None, 1, "", ""),
	   #"Prt1 Elevator" : 						ItemData(None, 1, "", ""),
	   #"Prt1 Chest" : 							ItemData(None, 1, "", ""),
	   #"Prt1 Sandpile" : 						ItemData(None, 1, "", ""),
	   #"Prt1 Waterspout" : 					ItemData(None, 1, "", ""),
	   #"Prt1 Lighthouse" : 					ItemData(None, 1, "", ""),
	   #"Prt1 Raise Ship" : 					ItemData(None, 1, "", ""),
	   #"Prt1 Bridge" : 						ItemData(None, 1, "", ""),
	   #"Prt2 Lower Water" : 					ItemData(None, 1, "", ""),
	   #"Prt2 Ramp" : 							ItemData(None, 1, "", ""),
	   #"Prt2 Gate" : 							ItemData(None, 1, "", ""),
	   #"Prt3 Platform Spin" : 					ItemData(None, 1, "", ""),
	   #"Prt3 Trampoline" : 					ItemData(None, 1, "", ""),
	   #"Prt3 Stairs" : 						ItemData(None, 1, "", ""),
	   #"Prt3 Elevator" : 						ItemData(None, 1, "", ""),
	   #"PhtH 1 Star" : 						ItemData(None, 1, "", ""),
	   #"PhtH 2 Gate" : 						ItemData(None, 1, "", ""),
	   #"PhtH 2 Star" : 						ItemData(None, 1, "", ""),
	   #"PhtH 3 Gate" : 						ItemData(None, 1, "", ""),
	   #"PhtH 3 Star" : 						ItemData(None, 1, "", ""),
	   #"PhtH Boss Gate" : 						ItemData(None, 1, "", ""),
	   #"PhtH Boss Star" : 						ItemData(None, 1, "", ""),
	   #"PhtH Bonus Gate" : 					ItemData(None, 1, "", ""),
	   #"PhtH Bonus Star" : 					ItemData(None, 1, "", ""),
	   #"Pht1 Life Drop" : 						ItemData(None, 1, "", ""),
	   #"Pht2 Platform 1" : 					ItemData(None, 1, "", ""),
	   #"Pht2 Platform 2" : 					ItemData(None, 1, "", ""),
	   #"Pht2 Lower Ball Switch" : 				ItemData(None, 1, "", ""),
	   #"Pht3 Drop Garibs" : 					ItemData(None, 1, "", ""),
	   #"Pht3 Spin Stones" : 					ItemData(None, 1, "", ""),
	   #"Pht3 Progressive Lower Monolith 1" : 	ItemData(None, 1, "", ""),
	   #"Pht3 Progressive Lower Monolith 2" : 	ItemData(None, 1, "", ""),
	   #"Pht3 Progressive Lower Monolith 3" : 	ItemData(None, 1, "", ""),
	   #"Pht3 Progressive Lower Monolith 4" : 	ItemData(None, 1, "", ""),
	   #"Pht3 Floating Platforms" : 			ItemData(None, 1, "", ""),
	   #"Pht3 Lava Spinning" : 					ItemData(None, 1, "", ""),
	   #"Pht3 Dirt Elevator" : 					ItemData(None, 1, "", ""),
	   #"FoFH 1 Star" : 						ItemData(None, 1, "", ""),
	   #"FoFH 2 Gate" : 						ItemData(None, 1, "", ""),
	   #"FoFH 2 Star" : 						ItemData(None, 1, "", ""),
	   #"FoFH 3 Gate" : 						ItemData(None, 1, "", ""),
	   #"FoFH 3 Star" : 						ItemData(None, 1, "", ""),
	   #"FoFH Boss Gate" : 						ItemData(None, 1, "", ""),
	   #"FoFH Boss Star" : 						ItemData(None, 1, "", ""),
	   #"FoFH Bonus Gate" : 					ItemData(None, 1, "", ""),
	   #"FoFH Bonus Star" : 					ItemData(None, 1, "", ""),
	   #"FoF1 Coffin" : 						ItemData(None, 1, "", ""),
	   #"FoF1 Doorway" : 						ItemData(None, 1, "", ""),
	   #"FoF1 Drawbridge" : 					ItemData(None, 1, "", ""),
	   #"FoF2 Garibs Fall" : 					ItemData(None, 1, "", ""),
	   #"FoF2 Checkpoint Gates" : 				ItemData(None, 1, "", ""),
	   #"FoF2 Mummy Gate" : 					ItemData(None, 1, "", ""),
	   #"FoF3 Gate" : 							ItemData(None, 1, "", ""),
	   #"FoF3 Spikes" : 						ItemData(None, 1, "", ""),
	   #"OtwH 1 Star" : 						ItemData(None, 1, "", ""),
	   #"OtwH 2 Gate" : 						ItemData(None, 1, "", ""),
	   #"OtwH 2 Star" : 						ItemData(None, 1, "", ""),
	   #"OtwH 3 Gate" : 						ItemData(None, 1, "", ""),
	   #"OtwH 3 Star" : 						ItemData(None, 1, "", ""),
	   #"OtwH Boss Gate" : 						ItemData(None, 1, "", ""),
	   #"OtwH Boss Star" : 						ItemData(None, 1, "", ""),
	   #"OtwH Bonus Gate" : 					ItemData(None, 1, "", ""),
	   #"OtwH Bonus Star" : 					ItemData(None, 1, "", ""),
	   #"Otw1 Aliens" : 						ItemData(None, 1, "", ""),
	   #"Otw1 Fans" : 							ItemData(None, 1, "", ""),
	   #"Otw1 Flying Platforms" : 				ItemData(None, 1, "", ""),
	   #"Otw1 Goo Platforms" : 					ItemData(None, 1, "", ""),
	   #"Otw1 UFO" : 							ItemData(None, 1, "", ""),
	   #"Otw1 Missile" : 						ItemData(None, 1, "", ""),
	   #"Otw2 Mashers" : 						ItemData(None, 1, "", ""),
	   #"Otw2 Ramp" : 							ItemData(None, 1, "", ""),
	   #"Otw3 Hazard Gate" : 					ItemData(None, 1, "", ""),
	   #"Otw3 Sign" : 							ItemData(None, 1, "", ""),
	   #"Otw3 Fan" : 							ItemData(None, 1, "", ""),
	   #"Otw3 Bridge" : 						ItemData(None, 1, "", ""),
	   #"Otw3 Glass Gate" : 					ItemData(None, 1, "", ""),
	   #"Hubworld Atlantis Gate" : 				ItemData(None, 1, "", ""),
	   #"Hubworld Carnival Gate" : 				ItemData(None, 1, "", ""),
	   #"Hubworld Pirate's Cove Gate" : 		ItemData(None, 1, "", ""),
	   #"Hubworld Prehistoric Gate" : 			ItemData(None, 1, "", ""),
	   #"Hubworld Fortress of Fear Gate" : 		ItemData(None, 1, "", ""),
	   #"Hubworld Out of This World Gate" : 	ItemData(None, 1, "", ""),
	   #"Training Sandpit" : 					ItemData(None, 1, "", ""),
	   #"Training Lower Target" : 				ItemData(None, 1, "", ""),
	   #"Training Stairs" : 					ItemData(None, 1, "", "")
	}

checkpoint_table = {
	"Atl1 Checkpoint 1" : 						ItemData(650130, 1,"Useful","Atl1: Checkpoint 1"),
	"Atl1 Checkpoint 2" : 						ItemData(650131, 1,"Useful","Atl1: Checkpoint 2"),#,
	#"Atl2 Checkpoint 2" : 						ItemData(1,"",""),
	#"Atl2 Checkpoint 3" : 						ItemData(1,"",""),
	#"Atl2 Checkpoint 1" : 						ItemData(1,"",""),
	#"Atl3 Checkpoint 2" : 						ItemData(1,"",""),
	#"Atl3 Checkpoint 3" : 						ItemData(1,"",""),
	#"Atl3 Checkpoint 1" : 						ItemData(1,"",""),
	#"Crn1 Checkpoint 2" : 						ItemData(1,"",""),
	#"Crn1 Checkpoint 3" : 						ItemData(1,"",""),
	#"Crn1 Checkpoint 4" : 						ItemData(1,"",""),
	#"Crn1 Checkpoint 1" : 						ItemData(1,"",""),
	#"Crn2 Checkpoint 2" : 						ItemData(1,"",""),
	#"Crn2 Checkpoint 3" : 						ItemData(1,"",""),
	#"Crn2 Checkpoint 4" : 						ItemData(1,"",""),
	#"Crn2 Checkpoint 5" : 						ItemData(1,"",""),
	#"Crn2 Checkpoint 1" : 						ItemData(1,"",""),
	#"Crn3 Checkpoint 2" : 						ItemData(1,"",""),
	#"Crn3 Checkpoint 3" : 						ItemData(1,"",""),
	#"Crn3 Checkpoint 4" : 						ItemData(1,"",""),
	#"Crn3 Checkpoint 1" : 						ItemData(1,"",""),
	#"Prt1 Checkpoint 2" : 						ItemData(1,"",""),
	#"Prt1 Checkpoint 3" : 						ItemData(1,"",""),
	#"Prt1 Checkpoint 1" : 						ItemData(1,"",""),
	#"Prt2 Checkpoint 2" : 						ItemData(1,"",""),
	#"Prt2 Checkpoint 3" : 						ItemData(1,"",""),
	#"Prt2 Checkpoint 1" : 						ItemData(1,"",""),
	#"Prt3 Checkpoint 2" : 						ItemData(1,"",""),
	#"Prt3 Checkpoint 3" : 						ItemData(1,"",""),
	#"Prt3 Checkpoint 4" : 						ItemData(1,"",""),
	#"Prt3 Checkpoint 1" : 						ItemData(1,"",""),
	#"Pht1 Checkpoint 2" : 						ItemData(1,"",""),
	#"Pht1 Checkpoint 3" : 						ItemData(1,"",""),
	#"Pht1 Checkpoint 1" : 						ItemData(1,"",""),
	#"Pht2 Checkpoint 2" : 						ItemData(1,"",""),
	#"Pht2 Checkpoint 3" : 						ItemData(1,"",""),
	#"Pht2 Checkpoint 4" : 						ItemData(1,"",""),
	#"Pht2 Checkpoint 1" : 						ItemData(1,"",""),
	#"Pht3 Checkpoint 2" : 						ItemData(1,"",""),
	#"Pht3 Checkpoint 3" : 						ItemData(1,"",""),
	#"Pht3 Checkpoint 4" : 						ItemData(1,"",""),
	#"Pht3 Checkpoint 1" : 						ItemData(1,"",""),
	#"FoF1 Checkpoint 2" : 						ItemData(1,"",""),
	#"FoF1 Checkpoint 3" : 						ItemData(1,"",""),
	#"FoF1 Checkpoint 1" : 						ItemData(1,"",""),
	#"FoF2 Checkpoint 2" : 						ItemData(1,"",""),
	#"FoF2 Checkpoint 3" : 						ItemData(1,"",""),
	#"FoF2 Checkpoint 1" : 						ItemData(1,"",""),
	#"FoF3 Checkpoint 2" : 						ItemData(1,"",""),
	#"FoF3 Checkpoint 3" : 						ItemData(1,"",""),
	#"FoF3 Checkpoint 4" : 						ItemData(1,"",""),
	#"FoF3 Checkpoint 5" : 						ItemData(1,"",""),
	#"FoF3 Checkpoint 1" : 						ItemData(1,"",""),
	#"Otw1 Checkpoint 2" : 						ItemData(1,"",""),
	#"Otw1 Checkpoint 1" : 						ItemData(1,"",""),
	#"Otw2 Checkpoint 1" : 						ItemData(1,"",""),
	#"Otw3 Checkpoint 2" : 						ItemData(1,"",""),
	#"Otw3 Checkpoint 3" : 						ItemData(1,"",""),
	#"Otw3 Checkpoint 4" : 						ItemData(1,"",""),
	#"Otw3 Checkpoint 1" : 						ItemData(1,"",""),
	}

world_garib_table = {
	"Atl1 1 Garibs" : 							ItemData(650190, 1,"Useful",""),
	"Atl1 2 Garibs" : 							ItemData(650191, 3,"Useful",""),
	"Atl1 3 Garibs" : 							ItemData(650192, 1,"Useful",""),
	"Atl1 4 Garibs" : 							ItemData(650193, 5,"Useful",""),
	"Atl1 5 Garibs" : 							ItemData(650194, 1,"Useful",""),
	"Atl1 6 Garibs" : 							ItemData(650195, 1,"Useful",""),
	"Atl1 9 Garibs" : 							ItemData(650196, 1,"Useful","")
	#"Atl2 1 Garibs" : 							ItemData(1,"",""),
	#"Atl2 2 Garibs" : 							ItemData(2,,)
	#"Atl2 3 Garibs" : 							ItemData(3,,)
	#"Atl2 4 Garibs" : 							ItemData(1,"",""),
	#"Atl2 5 Garibs" : 							ItemData(5,,)
	#"Atl2 7 Garibs" : 							ItemData(1,"",""),
	#"Atl2 10 Garibs" : 						ItemData(1,"",""),
	#"Atl3 1 Garibs" : 							ItemData(2,,)
	#"Atl3 2 Garibs" : 							ItemData(1,"",""),
	#"Atl3 3 Garibs" : 							ItemData(2,,)
	#"Atl3 4 Garibs" : 							ItemData(4,,)
	#"Atl3 5 Garibs" : 							ItemData(3,,)
	#"Atl3 6 Garibs" : 							ItemData(1,"",""),
	#"Atl3 8 Garibs" : 							ItemData(3,,)
	#"Atl3 9 Garibs" : 							ItemData(1,"",""),
	#"Atl? 5 Garibs" : 							ItemData(5,,)
	#"Crn1 1 Garibs" : 							ItemData(1,"",""),
	#"Crn1 4 Garibs" : 							ItemData(3,,)
	#"Crn1 7 Garibs" : 							ItemData(1,"",""),
	#"Crn1 8 Garibs" : 							ItemData(3,,)
	#"Crn1 10 Garibs" : 						ItemData(1,"",""),
	#"Crn1 11 Garibs" : 						ItemData(1,"",""),
	#"Crn2 1 Garibs" : 							ItemData(3,,)
	#"Crn2 2 Garibs" : 							ItemData(1,"",""),
	#"Crn2 3 Garibs" : 							ItemData(1,"",""),
	#"Crn2 4 Garibs" : 							ItemData(4,,)
	#"Crn2 6 Garibs" : 							ItemData(3,,)
	#"Crn2 8 Garibs" : 							ItemData(2,,)
	#"Crn2 10 Garibs" : 						ItemData(1,"",""),
	#"Crn2 12 Garibs" : 						ItemData(1,"",""),
	#"Crn3 1 Garibs" : 							ItemData(1,"",""),
	#"Crn3 2 Garibs" : 							ItemData(1,"",""),
	#"Crn3 3 Garibs" : 							ItemData("6",,)
	#"Crn3 4 Garibs" : 							ItemData("6",,)
	#"Crn3 6 Garibs" : 							ItemData(1,"",""),
	#"Crn3 8 Garibs" : 							ItemData(1,"",""),
	#"Crn3 9 Garibs" : 							ItemData(1,"",""),
	#"Crn3 12 Garibs" : 						ItemData(1,"",""),
	#"Crn? 8 Garibs" : 							ItemData(1,"",""),
	#"Crn? 12 Garibs" : 						ItemData(1,"",""),
	#"Prt1 1 Garibs" : 							ItemData(4,,)
	#"Prt1 4 Garibs" : 							ItemData("7",,)
	#"Prt1 5 Garibs" : 							ItemData(1,"",""),
	#"Prt1 6 Garibs" : 							ItemData(3,,)
	#"Prt1 7 Garibs" : 							ItemData(1,"",""),
	#"Prt1 8 Garibs" : 							ItemData(1,"",""),
	#"Prt2 1 Garibs" : 							ItemData("6",,)
	#"Prt2 2 Garibs" : 							ItemData(1,"",""),
	#"Prt2 3 Garibs" : 							ItemData(1,"",""),
	#"Prt2 4 Garibs" : 							ItemData(5,,)
	#"Prt2 8 Garibs" : 							ItemData(1,"",""),
	#"Prt2 9 Garibs" : 							ItemData(1,"",""),
	#"Prt2 12 Garibs" : 						ItemData(1,"",""),
	#"Prt3 1 Garibs" : 							ItemData(3,,)
	#"Prt3 2 Garibs" : 							ItemData(5,,)
	#"Prt3 3 Garibs" : 							ItemData(3,,)
	#"Prt3 4 Garibs" : 							ItemData("7",,)
	#"Prt3 6 Garibs" : 							ItemData(1,"",""),
	#"Prt3 8 Garibs" : 							ItemData(1,"",""),
	#"Prt3 16 Garibs" : 						ItemData(1,"",""),
	#"Prt? 3 Garibs" : 							ItemData("15",,)
	#"Prt? 5 Garibs" : 							ItemData(1,"",""),
	#"Pht1 1 Garibs" : 							ItemData(1,"",""),
	#"Pht1 2 Garibs" : 							ItemData(5,,)
	#"Pht1 3 Garibs" : 							ItemData("6",,)
	#"Pht1 4 Garibs" : 							ItemData(1,"",""),
	#"Pht1 5 Garibs" : 							ItemData(1,"",""),
	#"Pht1 6 Garibs" : 							ItemData(1,"",""),
	#"Pht1 8 Garibs" : 							ItemData(3,,)
	#"Pht1 12 Garibs" : 						ItemData(1,"",""),
	#"Pht2 1 Garibs" : 							ItemData("6",,)
	#"Pht2 2 Garibs" : 							ItemData(1,"",""),
	#"Pht2 3 Garibs" : 							ItemData(3,,)
	#"Pht2 4 Garibs" : 							ItemData("6",,)
	#"Pht2 5 Garibs" : 							ItemData(4,,)
	#"Pht2 8 Garibs" : 							ItemData(1,"",""),
	#"Pht2 11 Garibs" : 						ItemData(1,"",""),
	#"Pht3 1 Garibs" : 							ItemData(1,"",""),
	#"Pht3 2 Garibs" : 							ItemData(2,,)
	#"Pht3 3 Garibs" : 							ItemData(2,,)
	#"Pht3 5 Garibs" : 							ItemData(1,"",""),
	#"Pht3 7 Garibs" : 							ItemData(1,"",""),
	#"Pht3 8 Garibs" : 							ItemData(2,,)
	#"Pht3 10 Garibs" : 						ItemData(1,"",""),
	#"Pht3 15 Garibs" : 						ItemData(1,"",""),
	#"Pht3 16 Garibs" : 						ItemData(1,"",""),
	#"Pht? 10 Garibs" : 						ItemData("6",,)
	#"FoF1 1 Garibs" : 							ItemData(4,,)
	#"FoF1 2 Garibs" : 							ItemData(1,"",""),
	#"FoF1 3 Garibs" : 							ItemData(4,,)
	#"FoF1 4 Garibs" : 							ItemData(3,,)
	#"FoF1 5 Garibs" : 							ItemData(2,,)
	#"FoF1 6 Garibs" : 							ItemData(2,,)
	#"FoF1 8 Garibs" : 							ItemData(1,"",""),
	#"FoF2 1 Garibs" : 							ItemData(1,"",""),
	#"FoF2 2 Garibs" : 							ItemData(1,"",""),
	#"FoF2 3 Garibs" : 							ItemData(3,,)
	#"FoF2 5 Garibs" : 							ItemData(5,,)
	#"FoF2 6 Garibs" : 							ItemData(1,"",""),
	#"FoF2 7 Garibs" : 							ItemData(1,"",""),
	#"FoF2 10 Garibs" : 						ItemData(1,"",""),
	#"FoF3 1 Garibs" : 							ItemData(1,"",""),
	#"FoF3 2 Garibs" : 							ItemData(4,,)
	#"FoF3 3 Garibs" : 							ItemData(4,,)
	#"FoF3 4 Garibs" : 							ItemData(3,,)
	#"FoF3 5 Garibs" : 							ItemData(1,"",""),
	#"FoF3 6 Garibs" : 							ItemData(1,"",""),
	#"FoF3 8 Garibs" : 							ItemData(2,,)
	#"FoF3 10 Garibs" : 						ItemData(1,"",""),
	#"FoF? 14 Garibs" : 						ItemData(4,,)
	#"Otw1 1 Garibs" : 							ItemData("6",,)
	#"Otw1 2 Garibs" : 							ItemData(1,"",""),
	#"Otw1 3 Garibs" : 							ItemData(4,,)
	#"Otw1 4 Garibs" : 							ItemData(1,"",""),
	#"Otw1 10 Garibs" : 						ItemData(1,"",""),
	#"Otw1 16 Garibs" : 						ItemData(1,"",""),
	#"Otw2 2 Garibs" : 							ItemData(2,,)
	#"Otw2 3 Garibs" : 							ItemData(2,,)
	#"Otw2 4 Garibs" : 							ItemData(3,,)
	#"Otw2 5 Garibs" : 							ItemData(2,,)
	#"Otw2 6 Garibs" : 							ItemData(1,"",""),
	#"Otw2 12 Garibs" : 						ItemData(1,"",""),
	#"Otw3 3 Garibs" : 							ItemData(1,"",""),
	#"Otw3 4 Garibs" : 							ItemData(3,,)
	#"Otw3 5 Garibs" : 							ItemData(2,,)
	#"Otw3 6 Garibs" : 							ItemData(2,,)
	#"Otw3 7 Garibs" : 							ItemData(2,,)
	#"Otw3 8 Garibs" : 							ItemData(1,"",""),
	#"Otw3 9 Garibs" : 							ItemData(1,"",""),
	#"Otw3 12 Garibs" : 						ItemData(1,"",""),
	#"Otw? 6 Garibs" : 							ItemData(3,,),
	#"Otw? 8 Garibs" : 							ItemData(4,,)
	}

ability_table = {
	"Jump" : 									ItemData(650329, 1,"Progression",""),
	"Cartwheel" : 								ItemData(650330, 1,"Progression",""),
	"Crawl" : 									ItemData(650331, 1,"Useful",""),
	"Double Jump" : 							ItemData(650332, 1,"Progression",""),
	"Fist Slam" : 								ItemData(650333, 1,"Progression",""),
	"Ledge Grab" : 								ItemData(650334, 1,"Progression",""),
	"Push" : 									ItemData(650335, 1,"",""),
	"Locate Garibs" : 							ItemData(650336, 1,"Useful",""),
	"Locate Ball" : 							ItemData(650337, 1,"Useful",""),
	"Dribble" : 								ItemData(650338, 1,"Progression",""),
	"Quick Swap" : 								ItemData(650339, 1,"",""),
	"Slap" : 									ItemData(650340, 1,"Progression",""),
	"Throw" : 									ItemData(650341, 1,"Progression",""),
	"Ball Toss" : 								ItemData(650342, 1,"Progression",""),
	#"Beachball" : 								ItemData(650343, 1,"",""),
	#"Death Potion" : 							ItemData(650344, 1,"",""),
	#"Helicopter Potion" : 						ItemData(650345, 1,"",""),
	#"Frog Potion" : 							ItemData(650346, 1,"",""),
	#"Boomerang Ball" : 						ItemData(650347, 1,"",""),
	#"Speed Potion" : 							ItemData(650348, 1,"",""),
	#"Sticky Potion" : 							ItemData(650349, 1,"",""),
	#"Hercules Potion" : 						ItemData(650350, 1,"",""),
	#"Grab" : 									ItemData(650351, 1,"",""),
	"Rubber Ball" : 							ItemData(650352, 1,"Progression",""),
	"Bowling Ball" : 							ItemData(650353, 1,"Progression",""),
	"Ball Bearing" : 							ItemData(650354, 1,"Progression",""),
	"Crystal" : 								ItemData(650355, 1,"Progression",""),
	"Power Ball" : 								ItemData(650356, 1,"Progression","")
    }

filler_table = {
	"Life" : 									ItemData(650357, -1,"Useful",""),
	}

trap_table = {
	"Frog Spell" : 								ItemData(650358, -1,"Trap",""),
	}

garibsanity_world_table = {
	"Atl1 Garib" : 								ItemData(652001, 50,"Useful","")#,
	#"Atl2 Garib" : 							ItemData(652002, 60,"",""),
	#"Atl3 Garib" : 							ItemData(652003, 80,"",""),
	#"Atl? Garib" : 							ItemData(652004, 25,"",""),
	#"4 Garibs" : 								ItemData(652004, 65,"",""),
	#"4 Garibs" : 								ItemData(652004, 80,"",""),
	#"4 Garibs" : 								ItemData(652004, 80,"",""),
	#"4 Garibs" : 								ItemData(652004, 20,"",""),
	#"4 Garibs" : 								ItemData(652004, 70,"",""),
	#"4 Garibs" : 								ItemData(652004, 60,"",""),
	#"4 Garibs" : 								ItemData(652004, 80,"",""),
	#"4 Garibs" : 								ItemData(652004, 50,"",""),
	#"4 Garibs" : 								ItemData(652004, 80,"",""),
	#"4 Garibs" : 								ItemData(652004, 80,"",""),
	#"4 Garibs" : 								ItemData(652004, 80,"",""),
	#"4 Garibs" : 								ItemData(652004, 60,"",""),
	#"4 Garibs" : 								ItemData(652004, 60,"",""),
	#"4 Garibs" : 								ItemData(652004, 60,"",""),
	#"4 Garibs" : 								ItemData(652004, 70,"",""),
	#"4 Garibs" : 								ItemData(652004, 56,"",""),
	#"4 Garibs" : 								ItemData(652004, 50,"",""),
	#"4 Garibs" : 								ItemData(652004, 50,"",""),
	#"4 Garibs" : 								ItemData(652004, 80,"",""),
	#"4 Garibs" : 								ItemData(652004, 50,"","")
	}

#decoupled_garib_table = {
#	"Garib" : 									ItemData(651001, 42,"",""),
#	"2 Garibs" : 								ItemData(651002, 31,"",""),
#	"3 Garibs" : 								ItemData(651003, 61,"",""),
#	"4 Garibs" : 								ItemData(651004, 62,"",""),
#	"5 Garibs" : 								ItemData(651005, 34,"",""),
#	"6 Garibs" : 								ItemData(651006, 21,"",""),
#	"7 Garibs" : 								ItemData(651007, 7,"",""),
#	"8 Garibs" : 								ItemData(651008, 27,"",""),
#	"9 Garibs" : 								ItemData(651009, 5,"",""),
#	"10 Garibs" : 								ItemData(651010, 13,"",""),
#	"11 Garibs" : 								ItemData(651011, 2,"",""),
#	"12 Garibs" : 								ItemData(651012, 7,"",""),
#	#"13 Garibs" : 								ItemData(651013, 0,"",""),
#	"14 Garibs" : 								ItemData(651014, 4,"",""),
#	"15 Garibs" : 								ItemData(651015, 1,"",""),
#	"16 Garibs" : 								ItemData(651016, 3,"",""),
#}
#
#garbinsanity = ItemData(651001, 1496,"","")

#Atlantis 1
decoupled_garib_table = {
	"Garib" : 									ItemData(651001, 1, "Useful", ""),
	"2 Garibs" : 								ItemData(651002, 3, "Useful", ""),
	"3 Garibs" : 								ItemData(651003, 1, "Useful", ""),
	"4 Garibs" : 								ItemData(651004, 5, "Useful", ""),
	"5 Garibs" : 								ItemData(651005, 1, "Useful", ""),
	"6 Garibs" : 								ItemData(651006, 1, "Useful", ""),
	"9 Garibs" : 								ItemData(651009, 1, "Useful", ""),
}
garbinsanity = ItemData(651001, 50,"Useful","")