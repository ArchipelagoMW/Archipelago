from typing import NamedTuple

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

BASE_ID = 6500000

level_event_table = {
	   #"AtlH 1 Star" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"AtlH 2 Gate" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"AtlH 2 Star" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"AtlH 3 Gate" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"AtlH 3 Star" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"AtlH Boss Gate" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"AtlH Boss Star" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"AtlH Bonus Gate" : 					ItemData(BASE_ID + 0, 1, "", None),
	   #"AtlH Bonus Star" : 					ItemData(BASE_ID + 0, 1, "", None),
	   "Atl1 Gate" : 							ItemData(BASE_ID + 9, 1, "Useful", "Atl1: Glover Switch")#,
	   #"Atl2 Elevator" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"Atl2 Ballswitch Drain" : 				ItemData(BASE_ID + 0, 1, "", None),
	   #"Atl2 Gate" : 							ItemData(BASE_ID + 0, 1, "", None),
	   #"Atl3 Waterwheel" : 					ItemData(BASE_ID + 0, 1, "", None),
	   #"Atl3 Cave Platforms" : 				ItemData(BASE_ID + 0, 1, "", None),
	   #"CrnH 1 Star" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"CrnH 2 Gate" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"CrnH 2 Star" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"CrnH 3 Gate" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"CrnH 3 Star" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"CrnH Boss Gate" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"CrnH Boss Star" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"CrnH Bonus Gate" : 					ItemData(BASE_ID + 0, 1, "", None),
	   #"CrnH Bonus Star" : 					ItemData(BASE_ID + 0, 1, "", None),
	   #"Crn1 Elevator" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"Crn1 Gate" : 							ItemData(BASE_ID + 0, 1, "", None),
	   #"Crn1 Door A" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"Crn1 Door B" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"Crn1 Door C" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"Crn1 Rocket 1" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"Crn1 Rocket 2" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"Crn1 Rocket 3" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"Crn2 Drop Garibs" : 					ItemData(BASE_ID + 0, 1, "", None),
	   #"Crn2 Fan" : 							ItemData(BASE_ID + 0, 1, "", None),
	   #"Crn3 Spin Door" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"Crn3 Hands" : 							ItemData(BASE_ID + 0, 1, "", None),
	   #"PrtH 1 Star" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"PrtH 2 Gate" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"PrtH 2 Star" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"PrtH 3 Gate" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"PrtH 3 Star" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"PrtH Boss Gate" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"PrtH Boss Star" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"PrtH Bonus Gate" : 					ItemData(BASE_ID + 0, 1, "", None),
	   #"PrtH Bonus Star" : 					ItemData(BASE_ID + 0, 1, "", None),
	   #"Prt1 Raise Beach" : 					ItemData(BASE_ID + 0, 1, "", None),
	   #"Prt1 Elevator" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"Prt1 Chest" : 							ItemData(BASE_ID + 0, 1, "", None),
	   #"Prt1 Sandpile" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"Prt1 Waterspout" : 					ItemData(BASE_ID + 0, 1, "", None),
	   #"Prt1 Lighthouse" : 					ItemData(BASE_ID + 0, 1, "", None),
	   #"Prt1 Raise Ship" : 					ItemData(BASE_ID + 0, 1, "", None),
	   #"Prt1 Bridge" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"Prt2 Lower Water" : 					ItemData(BASE_ID + 0, 1, "", None),
	   #"Prt2 Ramp" : 							ItemData(BASE_ID + 0, 1, "", None),
	   #"Prt2 Gate" : 							ItemData(BASE_ID + 0, 1, "", None),
	   #"Prt3 Platform Spin" : 					ItemData(BASE_ID + 0, 1, "", None),
	   #"Prt3 Trampoline" : 					ItemData(BASE_ID + 0, 1, "", None),
	   #"Prt3 Stairs" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"Prt3 Elevator" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"PhtH 1 Star" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"PhtH 2 Gate" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"PhtH 2 Star" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"PhtH 3 Gate" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"PhtH 3 Star" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"PhtH Boss Gate" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"PhtH Boss Star" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"PhtH Bonus Gate" : 					ItemData(BASE_ID + 0, 1, "", None),
	   #"PhtH Bonus Star" : 					ItemData(BASE_ID + 0, 1, "", None),
	   #"Pht1 Life Drop" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"Pht2 Platform 1" : 					ItemData(BASE_ID + 0, 1, "", None),
	   #"Pht2 Platform 2" : 					ItemData(BASE_ID + 0, 1, "", None),
	   #"Pht2 Lower Ball Switch" : 				ItemData(BASE_ID + 0, 1, "", None),
	   #"Pht3 Drop Garibs" : 					ItemData(BASE_ID + 0, 1, "", None),
	   #"Pht3 Spin Stones" : 					ItemData(BASE_ID + 0, 1, "", None),
	   #"Pht3 Progressive Lower Monolith 1" : 	ItemData(BASE_ID + 0, 1, "", None),
	   #"Pht3 Progressive Lower Monolith 2" : 	ItemData(BASE_ID + 0, 1, "", None),
	   #"Pht3 Progressive Lower Monolith 3" : 	ItemData(BASE_ID + 0, 1, "", None),
	   #"Pht3 Progressive Lower Monolith 4" : 	ItemData(BASE_ID + 0, 1, "", None),
	   #"Pht3 Floating Platforms" : 			ItemData(BASE_ID + 0, 1, "", None),
	   #"Pht3 Lava Spinning" : 					ItemData(BASE_ID + 0, 1, "", None),
	   #"Pht3 Dirt Elevator" : 					ItemData(BASE_ID + 0, 1, "", None),
	   #"FoFH 1 Star" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"FoFH 2 Gate" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"FoFH 2 Star" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"FoFH 3 Gate" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"FoFH 3 Star" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"FoFH Boss Gate" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"FoFH Boss Star" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"FoFH Bonus Gate" : 					ItemData(BASE_ID + 0, 1, "", None),
	   #"FoFH Bonus Star" : 					ItemData(BASE_ID + 0, 1, "", None),
	   #"FoF1 Coffin" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"FoF1 Doorway" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"FoF1 Drawbridge" : 					ItemData(BASE_ID + 0, 1, "", None),
	   #"FoF2 Garibs Fall" : 					ItemData(BASE_ID + 0, 1, "", None),
	   #"FoF2 Checkpoint Gates" : 				ItemData(BASE_ID + 0, 1, "", None),
	   #"FoF2 Mummy Gate" : 					ItemData(BASE_ID + 0, 1, "", None),
	   #"FoF3 Gate" : 							ItemData(BASE_ID + 0, 1, "", None),
	   #"FoF3 Spikes" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"OtwH 1 Star" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"OtwH 2 Gate" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"OtwH 2 Star" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"OtwH 3 Gate" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"OtwH 3 Star" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"OtwH Boss Gate" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"OtwH Boss Star" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"OtwH Bonus Gate" : 					ItemData(BASE_ID + 0, 1, "", None),
	   #"OtwH Bonus Star" : 					ItemData(BASE_ID + 0, 1, "", None),
	   #"Otw1 Aliens" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"Otw1 Fans" : 							ItemData(BASE_ID + 0, 1, "", None),
	   #"Otw1 Flying Platforms" : 				ItemData(BASE_ID + 0, 1, "", None),
	   #"Otw1 Goo Platforms" : 					ItemData(BASE_ID + 0, 1, "", None),
	   #"Otw1 UFO" : 							ItemData(BASE_ID + 0, 1, "", None),
	   #"Otw1 Missile" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"Otw2 Mashers" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"Otw2 Ramp" : 							ItemData(BASE_ID + 0, 1, "", None),
	   #"Otw3 Hazard Gate" : 					ItemData(BASE_ID + 0, 1, "", None),
	   #"Otw3 Sign" : 							ItemData(BASE_ID + 0, 1, "", None),
	   #"Otw3 Fan" : 							ItemData(BASE_ID + 0, 1, "", None),
	   #"Otw3 Bridge" : 						ItemData(BASE_ID + 0, 1, "", None),
	   #"Otw3 Glass Gate" : 					ItemData(BASE_ID + 0, 1, "", None),
	   #"Hubworld Atlantis Gate" : 				ItemData(BASE_ID + 0, 1, "", None),
	   #"Hubworld Carnival Gate" : 				ItemData(BASE_ID + 0, 1, "", None),
	   #"Hubworld Pirate's Cove Gate" : 		ItemData(BASE_ID + 0, 1, "", None),
	   #"Hubworld Prehistoric Gate" : 			ItemData(BASE_ID + 0, 1, "", None),
	   #"Hubworld Fortress of Fear Gate" : 		ItemData(BASE_ID + 0, 1, "", None),
	   #"Hubworld Out of This World Gate" : 	ItemData(BASE_ID + 0, 1, "", None),
	   #"Training Sandpit" : 					ItemData(BASE_ID + 0, 1, "", None),
	   #"Training Lower Target" : 				ItemData(BASE_ID + 0, 1, "", None),
	   #"Training Stairs" : 					ItemData(BASE_ID + 0, 1, "", None)
	}

checkpoint_table = {
	"Atl1 Checkpoint 1" : 						ItemData(BASE_ID + 130, 1,"Useful","Atl1: Checkpoint 1"),
	"Atl1 Checkpoint 2" : 						ItemData(BASE_ID + 131, 1,"Useful","Atl1: Checkpoint 2"),#,
	#"Atl2 Checkpoint 2" : 						ItemData(1,"",None),
	#"Atl2 Checkpoint 3" : 						ItemData(1,"",None),
	#"Atl2 Checkpoint 1" : 						ItemData(1,"",None),
	#"Atl3 Checkpoint 2" : 						ItemData(1,"",None),
	#"Atl3 Checkpoint 3" : 						ItemData(1,"",None),
	#"Atl3 Checkpoint 1" : 						ItemData(1,"",None),
	#"Crn1 Checkpoint 2" : 						ItemData(1,"",None),
	#"Crn1 Checkpoint 3" : 						ItemData(1,"",None),
	#"Crn1 Checkpoint 4" : 						ItemData(1,"",None),
	#"Crn1 Checkpoint 1" : 						ItemData(1,"",None),
	#"Crn2 Checkpoint 2" : 						ItemData(1,"",None),
	#"Crn2 Checkpoint 3" : 						ItemData(1,"",None),
	#"Crn2 Checkpoint 4" : 						ItemData(1,"",None),
	#"Crn2 Checkpoint 5" : 						ItemData(1,"",None),
	#"Crn2 Checkpoint 1" : 						ItemData(1,"",None),
	#"Crn3 Checkpoint 2" : 						ItemData(1,"",None),
	#"Crn3 Checkpoint 3" : 						ItemData(1,"",None),
	#"Crn3 Checkpoint 4" : 						ItemData(1,"",None),
	#"Crn3 Checkpoint 1" : 						ItemData(1,"",None),
	#"Prt1 Checkpoint 2" : 						ItemData(1,"",None),
	#"Prt1 Checkpoint 3" : 						ItemData(1,"",None),
	#"Prt1 Checkpoint 1" : 						ItemData(1,"",None),
	#"Prt2 Checkpoint 2" : 						ItemData(1,"",None),
	#"Prt2 Checkpoint 3" : 						ItemData(1,"",None),
	#"Prt2 Checkpoint 1" : 						ItemData(1,"",None),
	#"Prt3 Checkpoint 2" : 						ItemData(1,"",None),
	#"Prt3 Checkpoint 3" : 						ItemData(1,"",None),
	#"Prt3 Checkpoint 4" : 						ItemData(1,"",None),
	#"Prt3 Checkpoint 1" : 						ItemData(1,"",None),
	#"Pht1 Checkpoint 2" : 						ItemData(1,"",None),
	#"Pht1 Checkpoint 3" : 						ItemData(1,"",None),
	#"Pht1 Checkpoint 1" : 						ItemData(1,"",None),
	#"Pht2 Checkpoint 2" : 						ItemData(1,"",None),
	#"Pht2 Checkpoint 3" : 						ItemData(1,"",None),
	#"Pht2 Checkpoint 4" : 						ItemData(1,"",None),
	#"Pht2 Checkpoint 1" : 						ItemData(1,"",None),
	#"Pht3 Checkpoint 2" : 						ItemData(1,"",None),
	#"Pht3 Checkpoint 3" : 						ItemData(1,"",None),
	#"Pht3 Checkpoint 4" : 						ItemData(1,"",None),
	#"Pht3 Checkpoint 1" : 						ItemData(1,"",None),
	#"FoF1 Checkpoint 2" : 						ItemData(1,"",None),
	#"FoF1 Checkpoint 3" : 						ItemData(1,"",None),
	#"FoF1 Checkpoint 1" : 						ItemData(1,"",None),
	#"FoF2 Checkpoint 2" : 						ItemData(1,"",None),
	#"FoF2 Checkpoint 3" : 						ItemData(1,"",None),
	#"FoF2 Checkpoint 1" : 						ItemData(1,"",None),
	#"FoF3 Checkpoint 2" : 						ItemData(1,"",None),
	#"FoF3 Checkpoint 3" : 						ItemData(1,"",None),
	#"FoF3 Checkpoint 4" : 						ItemData(1,"",None),
	#"FoF3 Checkpoint 5" : 						ItemData(1,"",None),
	#"FoF3 Checkpoint 1" : 						ItemData(1,"",None),
	#"Otw1 Checkpoint 2" : 						ItemData(1,"",None),
	#"Otw1 Checkpoint 1" : 						ItemData(1,"",None),
	#"Otw2 Checkpoint 1" : 						ItemData(1,"",None),
	#"Otw3 Checkpoint 2" : 						ItemData(1,"",None),
	#"Otw3 Checkpoint 3" : 						ItemData(1,"",None),
	#"Otw3 Checkpoint 4" : 						ItemData(1,"",None),
	#"Otw3 Checkpoint 1" : 						ItemData(1,"",None),
	}

world_garib_table = {
	"Atl1 1 Garibs" : 							ItemData(BASE_ID + 190, 1,"Useful",None),
	"Atl1 2 Garibs" : 							ItemData(BASE_ID + 191, 3,"Useful",None),
	"Atl1 3 Garibs" : 							ItemData(BASE_ID + 192, 1,"Useful",None),
	"Atl1 4 Garibs" : 							ItemData(BASE_ID + 193, 5,"Useful",None),
	"Atl1 5 Garibs" : 							ItemData(BASE_ID + 194, 1,"Useful",None),
	"Atl1 6 Garibs" : 							ItemData(BASE_ID + 195, 1,"Useful",None),
	"Atl1 9 Garibs" : 							ItemData(BASE_ID + 196, 1,"Useful",None)
	#"Atl2 1 Garibs" : 							ItemData(1,"",None),
	#"Atl2 2 Garibs" : 							ItemData(2,,)
	#"Atl2 3 Garibs" : 							ItemData(3,,)
	#"Atl2 4 Garibs" : 							ItemData(1,"",None),
	#"Atl2 5 Garibs" : 							ItemData(5,,)
	#"Atl2 7 Garibs" : 							ItemData(1,"",None),
	#"Atl2 10 Garibs" : 						ItemData(1,"",None),
	#"Atl3 1 Garibs" : 							ItemData(2,,)
	#"Atl3 2 Garibs" : 							ItemData(1,"",None),
	#"Atl3 3 Garibs" : 							ItemData(2,,)
	#"Atl3 4 Garibs" : 							ItemData(4,,)
	#"Atl3 5 Garibs" : 							ItemData(3,,)
	#"Atl3 6 Garibs" : 							ItemData(1,"",None),
	#"Atl3 8 Garibs" : 							ItemData(3,,)
	#"Atl3 9 Garibs" : 							ItemData(1,"",None),
	#"Atl? 5 Garibs" : 							ItemData(5,,)
	#"Crn1 1 Garibs" : 							ItemData(1,"",None),
	#"Crn1 4 Garibs" : 							ItemData(3,,)
	#"Crn1 7 Garibs" : 							ItemData(1,"",None),
	#"Crn1 8 Garibs" : 							ItemData(3,,)
	#"Crn1 10 Garibs" : 						ItemData(1,"",None),
	#"Crn1 11 Garibs" : 						ItemData(1,"",None),
	#"Crn2 1 Garibs" : 							ItemData(3,,)
	#"Crn2 2 Garibs" : 							ItemData(1,"",None),
	#"Crn2 3 Garibs" : 							ItemData(1,"",None),
	#"Crn2 4 Garibs" : 							ItemData(4,,)
	#"Crn2 6 Garibs" : 							ItemData(3,,)
	#"Crn2 8 Garibs" : 							ItemData(2,,)
	#"Crn2 10 Garibs" : 						ItemData(1,"",None),
	#"Crn2 12 Garibs" : 						ItemData(1,"",None),
	#"Crn3 1 Garibs" : 							ItemData(1,"",None),
	#"Crn3 2 Garibs" : 							ItemData(1,"",None),
	#"Crn3 3 Garibs" : 							ItemData("6",,)
	#"Crn3 4 Garibs" : 							ItemData("6",,)
	#"Crn3 6 Garibs" : 							ItemData(1,"",None),
	#"Crn3 8 Garibs" : 							ItemData(1,"",None),
	#"Crn3 9 Garibs" : 							ItemData(1,"",None),
	#"Crn3 12 Garibs" : 						ItemData(1,"",None),
	#"Crn? 8 Garibs" : 							ItemData(1,"",None),
	#"Crn? 12 Garibs" : 						ItemData(1,"",None),
	#"Prt1 1 Garibs" : 							ItemData(4,,)
	#"Prt1 4 Garibs" : 							ItemData("7",,)
	#"Prt1 5 Garibs" : 							ItemData(1,"",None),
	#"Prt1 6 Garibs" : 							ItemData(3,,)
	#"Prt1 7 Garibs" : 							ItemData(1,"",None),
	#"Prt1 8 Garibs" : 							ItemData(1,"",None),
	#"Prt2 1 Garibs" : 							ItemData("6",,)
	#"Prt2 2 Garibs" : 							ItemData(1,"",None),
	#"Prt2 3 Garibs" : 							ItemData(1,"",None),
	#"Prt2 4 Garibs" : 							ItemData(5,,)
	#"Prt2 8 Garibs" : 							ItemData(1,"",None),
	#"Prt2 9 Garibs" : 							ItemData(1,"",None),
	#"Prt2 12 Garibs" : 						ItemData(1,"",None),
	#"Prt3 1 Garibs" : 							ItemData(3,,)
	#"Prt3 2 Garibs" : 							ItemData(5,,)
	#"Prt3 3 Garibs" : 							ItemData(3,,)
	#"Prt3 4 Garibs" : 							ItemData("7",,)
	#"Prt3 6 Garibs" : 							ItemData(1,"",None),
	#"Prt3 8 Garibs" : 							ItemData(1,"",None),
	#"Prt3 16 Garibs" : 						ItemData(1,"",None),
	#"Prt? 3 Garibs" : 							ItemData("15",,)
	#"Prt? 5 Garibs" : 							ItemData(1,"",None),
	#"Pht1 1 Garibs" : 							ItemData(1,"",None),
	#"Pht1 2 Garibs" : 							ItemData(5,,)
	#"Pht1 3 Garibs" : 							ItemData("6",,)
	#"Pht1 4 Garibs" : 							ItemData(1,"",None),
	#"Pht1 5 Garibs" : 							ItemData(1,"",None),
	#"Pht1 6 Garibs" : 							ItemData(1,"",None),
	#"Pht1 8 Garibs" : 							ItemData(3,,)
	#"Pht1 12 Garibs" : 						ItemData(1,"",None),
	#"Pht2 1 Garibs" : 							ItemData("6",,)
	#"Pht2 2 Garibs" : 							ItemData(1,"",None),
	#"Pht2 3 Garibs" : 							ItemData(3,,)
	#"Pht2 4 Garibs" : 							ItemData("6",,)
	#"Pht2 5 Garibs" : 							ItemData(4,,)
	#"Pht2 8 Garibs" : 							ItemData(1,"",None),
	#"Pht2 11 Garibs" : 						ItemData(1,"",None),
	#"Pht3 1 Garibs" : 							ItemData(1,"",None),
	#"Pht3 2 Garibs" : 							ItemData(2,,)
	#"Pht3 3 Garibs" : 							ItemData(2,,)
	#"Pht3 5 Garibs" : 							ItemData(1,"",None),
	#"Pht3 7 Garibs" : 							ItemData(1,"",None),
	#"Pht3 8 Garibs" : 							ItemData(2,,)
	#"Pht3 10 Garibs" : 						ItemData(1,"",None),
	#"Pht3 15 Garibs" : 						ItemData(1,"",None),
	#"Pht3 16 Garibs" : 						ItemData(1,"",None),
	#"Pht? 10 Garibs" : 						ItemData("6",,)
	#"FoF1 1 Garibs" : 							ItemData(4,,)
	#"FoF1 2 Garibs" : 							ItemData(1,"",None),
	#"FoF1 3 Garibs" : 							ItemData(4,,)
	#"FoF1 4 Garibs" : 							ItemData(3,,)
	#"FoF1 5 Garibs" : 							ItemData(2,,)
	#"FoF1 6 Garibs" : 							ItemData(2,,)
	#"FoF1 8 Garibs" : 							ItemData(1,"",None),
	#"FoF2 1 Garibs" : 							ItemData(1,"",None),
	#"FoF2 2 Garibs" : 							ItemData(1,"",None),
	#"FoF2 3 Garibs" : 							ItemData(3,,)
	#"FoF2 5 Garibs" : 							ItemData(5,,)
	#"FoF2 6 Garibs" : 							ItemData(1,"",None),
	#"FoF2 7 Garibs" : 							ItemData(1,"",None),
	#"FoF2 10 Garibs" : 						ItemData(1,"",None),
	#"FoF3 1 Garibs" : 							ItemData(1,"",None),
	#"FoF3 2 Garibs" : 							ItemData(4,,)
	#"FoF3 3 Garibs" : 							ItemData(4,,)
	#"FoF3 4 Garibs" : 							ItemData(3,,)
	#"FoF3 5 Garibs" : 							ItemData(1,"",None),
	#"FoF3 6 Garibs" : 							ItemData(1,"",None),
	#"FoF3 8 Garibs" : 							ItemData(2,,)
	#"FoF3 10 Garibs" : 						ItemData(1,"",None),
	#"FoF? 14 Garibs" : 						ItemData(4,,)
	#"Otw1 1 Garibs" : 							ItemData("6",,)
	#"Otw1 2 Garibs" : 							ItemData(1,"",None),
	#"Otw1 3 Garibs" : 							ItemData(4,,)
	#"Otw1 4 Garibs" : 							ItemData(1,"",None),
	#"Otw1 10 Garibs" : 						ItemData(1,"",None),
	#"Otw1 16 Garibs" : 						ItemData(1,"",None),
	#"Otw2 2 Garibs" : 							ItemData(2,,)
	#"Otw2 3 Garibs" : 							ItemData(2,,)
	#"Otw2 4 Garibs" : 							ItemData(3,,)
	#"Otw2 5 Garibs" : 							ItemData(2,,)
	#"Otw2 6 Garibs" : 							ItemData(1,"",None),
	#"Otw2 12 Garibs" : 						ItemData(1,"",None),
	#"Otw3 3 Garibs" : 							ItemData(1,"",None),
	#"Otw3 4 Garibs" : 							ItemData(3,,)
	#"Otw3 5 Garibs" : 							ItemData(2,,)
	#"Otw3 6 Garibs" : 							ItemData(2,,)
	#"Otw3 7 Garibs" : 							ItemData(2,,)
	#"Otw3 8 Garibs" : 							ItemData(1,"",None),
	#"Otw3 9 Garibs" : 							ItemData(1,"",None),
	#"Otw3 12 Garibs" : 						ItemData(1,"",None),
	#"Otw? 6 Garibs" : 							ItemData(3,,),
	#"Otw? 8 Garibs" : 							ItemData(4,,)
	}

ability_table = {
	"Jump" : 									ItemData(BASE_ID + 329, 1,"Progression",None),
	"Cartwheel" : 								ItemData(BASE_ID + 330, 1,"Progression",None),
	"Crawl" : 									ItemData(BASE_ID + 331, 1,"Useful",None),
	"Double Jump" : 							ItemData(BASE_ID + 332, 1,"Progression",None),
	"Fist Slam" : 								ItemData(BASE_ID + 333, 1,"Progression",None),
	"Ledge Grab" : 								ItemData(BASE_ID + 334, 1,"Progression",None),
	"Push" : 									ItemData(BASE_ID + 335, 1,"Progression",None),
#	"Locate Garibs" : 							ItemData(BASE_ID + 336, 1,"Useful",None),
#	"Locate Ball" : 							ItemData(BASE_ID + 337, 1,"Useful",None),
	"Dribble" : 								ItemData(BASE_ID + 338, 1,"Progression",None),
#	"Quick Swap" : 								ItemData(BASE_ID + 339, 1,"Useful",None),
	"Slap" : 									ItemData(BASE_ID + 340, 1,"Progression",None),
	"Throw" : 									ItemData(BASE_ID + 341, 1,"Progression",None),
	"Ball Toss" : 								ItemData(BASE_ID + 342, 1,"Progression",None),
#	"Beachball" : 								ItemData(BASE_ID + 343, 1,"Progression",None),
#	"Death Potion" : 							ItemData(BASE_ID + 344, 1,"Useful",None),
#	"Helicopter Potion" : 						ItemData(BASE_ID + 345, 1,"Progression",None),
#	"Frog Potion" : 							ItemData(BASE_ID + 346, 1,"Useful",None),
#	"Boomerang Ball" : 							ItemData(BASE_ID + 347, 1,"Progression",None),
#	"Speed Potion" : 							ItemData(BASE_ID + 348, 1,"Progression",None),
#	"Sticky Potion" : 							ItemData(BASE_ID + 349, 1,"Progression",None),
#	"Hercules Potion" : 						ItemData(BASE_ID + 350, 1,"Progression",None),
#	"Grab" : 									ItemData(BASE_ID + 351, 1,"Progression",None),
	"Rubber Ball" : 							ItemData(BASE_ID + 352, 1,"Progression",None),
	"Bowling Ball" : 							ItemData(BASE_ID + 353, 1,"Progression",None),
	"Ball Bearing" : 							ItemData(BASE_ID + 354, 1,"Progression",None),
	"Crystal" : 								ItemData(BASE_ID + 355, 1,"Progression",None),
	"Power Ball" : 								ItemData(BASE_ID + 356, 1,"Progression",None)
    }

filler_table = {
    "Extra Garibs" : 							ItemData(BASE_ID + 357, -1,"Useful",None),
    "Chicken Sound" : 							ItemData(BASE_ID + 358, -1,"Useful",None),
	"Life" : 									ItemData(BASE_ID + 359, -1,"Useful",None),
    "Boomerang" : 								ItemData(BASE_ID + 360, -1,"Useful",None),
    "Beachball" : 								ItemData(BASE_ID + 361, -1,"Useful",None),
    "Hercules" : 								ItemData(BASE_ID + 362, -1,"Useful",None),
    "Helicopter" : 								ItemData(BASE_ID + 363, -1,"Useful",None),
    "Speed" : 									ItemData(BASE_ID + 364, -1,"Useful",None),
    "Frog" : 									ItemData(BASE_ID + 365, -1,"Useful",None),
    "Death" : 									ItemData(BASE_ID + 366, -1,"Useful",None),
    "Sticky" : 									ItemData(BASE_ID + 367, -1,"Useful",None)
	}

trap_table = {
	"Frog Spell" : 								ItemData(BASE_ID + 368, -1,"Trap",None),
    "Cursed Ball" :								ItemData(BASE_ID + 369, -1,"Trap",None),
    "Instant Crystal" :							ItemData(BASE_ID + 370, -1,"Trap",None),
    "Camera Rotate" :							ItemData(BASE_ID + 371, -1,"Trap",None),
    "Tip Trap" :								ItemData(BASE_ID + 372, -1,"Trap",None)
	}

garibsanity_world_table = {
	"Atl1 Garib" : 								ItemData(BASE_ID + 2001, 50,"Useful",None)#,
	#"Atl2 Garib" : 							ItemData(BASE_ID + 2002, 60,"",None),
	#"Atl3 Garib" : 							ItemData(BASE_ID + 2003, 80,"",None),
	#"Atl? Garib" : 							ItemData(BASE_ID + 2004, 25,"",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 2004, 65,"",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 2004, 80,"",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 2004, 80,"",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 2004, 20,"",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 2004, 70,"",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 2004, 60,"",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 2004, 80,"",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 2004, 50,"",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 2004, 80,"",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 2004, 80,"",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 2004, 80,"",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 2004, 60,"",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 2004, 60,"",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 2004, 60,"",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 2004, 70,"",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 2004, 56,"",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 2004, 50,"",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 2004, 50,"",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 2004, 80,"",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 2004, 50,"",None)
	}

#decoupled_garib_table = {
#	"Garib" : 									ItemData(BASE_ID + 1001, 42,"",None),
#	"2 Garibs" : 								ItemData(BASE_ID + 1002, 31,"",None),
#	"3 Garibs" : 								ItemData(BASE_ID + 1003, 61,"",None),
#	"4 Garibs" : 								ItemData(BASE_ID + 1004, 62,"",None),
#	"5 Garibs" : 								ItemData(BASE_ID + 1005, 34,"",None),
#	"6 Garibs" : 								ItemData(BASE_ID + 1006, 21,"",None),
#	"7 Garibs" : 								ItemData(BASE_ID + 1007, 7,"",None),
#	"8 Garibs" : 								ItemData(BASE_ID + 1008, 27,"",None),
#	"9 Garibs" : 								ItemData(BASE_ID + 1009, 5,"",None),
#	"10 Garibs" : 								ItemData(BASE_ID + 1010, 13,"",None),
#	"11 Garibs" : 								ItemData(BASE_ID + 1011, 2,"",None),
#	"12 Garibs" : 								ItemData(BASE_ID + 1012, 7,"",None),
#	#"13 Garibs" : 								ItemData(BASE_ID + 1013, 0,"",None),
#	"14 Garibs" : 								ItemData(BASE_ID + 1014, 4,"",None),
#	"15 Garibs" : 								ItemData(BASE_ID + 1015, 1,"",None),
#	"16 Garibs" : 								ItemData(BASE_ID + 1016, 3,"",None),
#}
#
#garbinsanity = ItemData(BASE_ID + 1001, 1496,"",None)

#Atlantis 1
decoupled_garib_table = {
	"Garib" : 									ItemData(BASE_ID + 1001, 1, "Useful", None),
	"2 Garibs" : 								ItemData(BASE_ID + 1002, 3, "Useful", None),
	"3 Garibs" : 								ItemData(BASE_ID + 1003, 1, "Useful", None),
	"4 Garibs" : 								ItemData(BASE_ID + 1004, 5, "Useful", None),
	"5 Garibs" : 								ItemData(BASE_ID + 1005, 1, "Useful", None),
	"6 Garibs" : 								ItemData(BASE_ID + 1006, 1, "Useful", None),
	"9 Garibs" : 								ItemData(BASE_ID + 1009, 1, "Useful", None),
}
garbinsanity = ItemData(BASE_ID + 10001, 50,"Useful", None)

all_items = {
	**level_event_table, 
	**checkpoint_table, 
	**world_garib_table, 
	**ability_table, 
	**filler_table, 
	**trap_table, 
	**garibsanity_world_table
}

def generate_item_name_to_id() -> dict:
	output : dict = {}
	for name, data in all_items.items():
		output[name] = data.glid
	return output

def generate_item_name_groups() -> dict:
	output : dict = {}
	return output
