from typing import NamedTuple

class ItemData(NamedTuple):
	glid: int|None = None
	qty: int = 0
	type: str = ""
	default_location: str = ""

def find_item_data(self, name : str) -> ItemData:
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
		#As event item?
		if self.options.switches_checks:
			return level_event_table[name]
		else:
			modified_item = level_event_table[name]
			return ItemData(None, modified_item.qty, modified_item.type, modified_item.default_location)
	if name in checkpoint_table:
		if self.options.checkpoint_checks:
			return checkpoint_table[name]
		else:
			modified_item = checkpoint_table[name]
			return ItemData(None, modified_item.qty, modified_item.type, modified_item.default_location)
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
	#"AtlH 1 Star" : 						ItemData(BASE_ID + 0, 1, "Progression", ),
	#"AtlH 2 Gate" : 						ItemData(BASE_ID + 1, 1, "Progression", ),
	#"AtlH 2 Star" : 						ItemData(BASE_ID + 2, 1, "Progression", ),
	#"AtlH 3 Gate" : 						ItemData(BASE_ID + 3, 1, "Progression", ),
	#"AtlH 3 Star" : 						ItemData(BASE_ID + 4, 1, "Progression", ),
	#"AtlH Boss Gate" : 						ItemData(BASE_ID + 5, 1, "Progression", ),
	#"AtlH Boss Star" : 						ItemData(BASE_ID + 6, 1, "Progression", ),
	#"AtlH Bonus Gate" : 					ItemData(BASE_ID + 7, 1, "Progression", ),
	#"AtlH Bonus Star" : 					ItemData(BASE_ID + 8, 1, "Progression", ),
	"Atl1 Gate" : 							ItemData(BASE_ID + 9, 1, "Progression", "Atl1: Glover Switch"),
	"Atl2 Elevator" : 						ItemData(BASE_ID + 10, 1, "Progression", "Atl2: Drain Block"),
	"Atl2 Ball Switch Drain" : 				ItemData(BASE_ID + 11, 1, "Progression", "Atl2: Ball Switch"),
	"Atl2 Gate" : 							ItemData(BASE_ID + 12, 1, "Progression", "Atl2: Glover Switch"),
	"Atl3 Waterwheel" : 					ItemData(BASE_ID + 13, 1, "Progression", "Atl3: Pyramid Ball Switch"),
	"Atl3 Cave Platforms" : 				ItemData(BASE_ID + 14, 1, "Progression", "Atl3: Cliff Ball Switch")#,
	#"CrnH 1 Star" : 						ItemData(BASE_ID + 15, 1, "Progression", ),
	#"CrnH 2 Gate" : 						ItemData(BASE_ID + 16, 1, "Progression", ),
	#"CrnH 2 Star" : 						ItemData(BASE_ID + 17, 1, "Progression", ),
	#"CrnH 3 Gate" : 						ItemData(BASE_ID + 18, 1, "Progression", ),
	#"CrnH 3 Star" : 						ItemData(BASE_ID + 19, 1, "Progression", ),
	#"CrnH Boss Gate" : 						ItemData(BASE_ID + 20, 1, "Progression", ),
	#"CrnH Boss Star" : 						ItemData(BASE_ID + 21, 1, "Progression", ),
	#"CrnH Bonus Gate" : 					ItemData(BASE_ID + 22, 1, "Progression", ),
	#"CrnH Bonus Star" : 					ItemData(BASE_ID + 23, 1, "Progression", ),
	#"Crn1 Elevator" : 						ItemData(BASE_ID + 24, 1, "Progression", ),
	#"Crn1 Gate" : 							ItemData(BASE_ID + 25, 1, "Progression", ),
	#"Crn1 Door A" : 						ItemData(BASE_ID + 26, 1, "Progression", ),
	#"Crn1 Door B" : 						ItemData(BASE_ID + 27, 1, "Progression", ),
	#"Crn1 Door C" : 						ItemData(BASE_ID + 28, 1, "Progression", ),
	#"Crn1 Rocket 1" : 						ItemData(BASE_ID + 29, 1, "Progression", ),
	#"Crn1 Rocket 2" : 						ItemData(BASE_ID + 30, 1, "Progression", ),
	#"Crn1 Rocket 3" : 						ItemData(BASE_ID + 31, 1, "Progression", ),
	#"Crn2 Drop Garibs" : 					ItemData(BASE_ID + 32, 1, "Progression", ),
	#"Crn2 Fan" : 							ItemData(BASE_ID + 33, 1, "Progression", ),
	#"Crn3 Spin Door" : 						ItemData(BASE_ID + 34, 1, "Progression", ),
	#"Crn3 Hands" : 							ItemData(BASE_ID + 35, 1, "Progression", ),
	#"PrtH 1 Star" : 						ItemData(BASE_ID + 36, 1, "Progression", ),
	#"PrtH 2 Gate" : 						ItemData(BASE_ID + 37, 1, "Progression", ),
	#"PrtH 2 Star" : 						ItemData(BASE_ID + 38, 1, "Progression", ),
	#"PrtH 3 Gate" : 						ItemData(BASE_ID + 39, 1, "Progression", ),
	#"PrtH 3 Star" : 						ItemData(BASE_ID + 40, 1, "Progression", ),
	#"PrtH Boss Gate" : 						ItemData(BASE_ID + 41, 1, "Progression", ),
	#"PrtH Boss Star" : 						ItemData(BASE_ID + 42, 1, "Progression", ),
	#"PrtH Bonus Gate" : 					ItemData(BASE_ID + 43, 1, "Progression", ),
	#"PrtH Bonus Star" : 					ItemData(BASE_ID + 44, 1, "Progression", ),
	#"Prt1 Raise Beach" : 					ItemData(BASE_ID + 45, 1, "Progression", ),
	#"Prt1 Elevator" : 						ItemData(BASE_ID + 46, 1, "Progression", ),
	#"Prt1 Chest" : 							ItemData(BASE_ID + 47, 1, "Progression", ),
	#"Prt1 Sandpile" : 						ItemData(BASE_ID + 48, 1, "Progression", ),
	#"Prt1 Waterspout" : 					ItemData(BASE_ID + 49, 1, "Progression", ),
	#"Prt1 Lighthouse" : 					ItemData(BASE_ID + 50, 1, "Progression", ),
	#"Prt1 Raise Ship" : 					ItemData(BASE_ID + 51, 1, "Progression", ),
	#"Prt1 Bridge" : 						ItemData(BASE_ID + 52, 1, "Progression", ),
	#"Prt2 Lower Water" : 					ItemData(BASE_ID + 53, 1, "Progression", ),
	#"Prt2 Ramp" : 							ItemData(BASE_ID + 54, 1, "Progression", ),
	#"Prt2 Gate" : 							ItemData(BASE_ID + 55, 1, "Progression", ),
	#"Prt3 Platform Spin" : 					ItemData(BASE_ID + 56, 1, "Progression", ),
	#"Prt3 Trampoline" : 					ItemData(BASE_ID + 57, 1, "Progression", ),
	#"Prt3 Stairs" : 						ItemData(BASE_ID + 58, 1, "Progression", ),
	#"Prt3 Elevator" : 						ItemData(BASE_ID + 59, 1, "Progression", ),
	#"PhtH 1 Star" : 						ItemData(BASE_ID + 60, 1, "Progression", ),
	#"PhtH 2 Gate" : 						ItemData(BASE_ID + 61, 1, "Progression", ),
	#"PhtH 2 Star" : 						ItemData(BASE_ID + 62, 1, "Progression", ),
	#"PhtH 3 Gate" : 						ItemData(BASE_ID + 63, 1, "Progression", ),
	#"PhtH 3 Star" : 						ItemData(BASE_ID + 64, 1, "Progression", ),
	#"PhtH Boss Gate" : 						ItemData(BASE_ID + 65, 1, "Progression", ),
	#"PhtH Boss Star" : 						ItemData(BASE_ID + 66, 1, "Progression", ),
	#"PhtH Bonus Gate" : 					ItemData(BASE_ID + 67, 1, "Progression", ),
	#"PhtH Bonus Star" : 					ItemData(BASE_ID + 68, 1, "Progression", ),
	#"Pht1 Life Drop" : 						ItemData(BASE_ID + 69, 1, "Progression", ),
	#"Pht2 Platform 1" : 					ItemData(BASE_ID + 70, 1, "Progression", ),
	#"Pht2 Platform 2" : 					ItemData(BASE_ID + 71, 1, "Progression", ),
	#"Pht2 Lower Ball Switch" : 				ItemData(BASE_ID + 72, 1, "Progression", ),
	#"Pht3 Drop Garibs" : 					ItemData(BASE_ID + 73, 1, "Progression", ),
	#"Pht3 Spin Stones" : 					ItemData(BASE_ID + 74, 1, "Progression", ),
	#"Pht3 Progressive Lower Monolith 1" : 	ItemData(BASE_ID + 75, 1, "Progression", ),
	#"Pht3 Progressive Lower Monolith 2" : 	ItemData(BASE_ID + 76, 1, "Progression", ),
	#"Pht3 Progressive Lower Monolith 3" : 	ItemData(BASE_ID + 77, 1, "Progression", ),
	#"Pht3 Progressive Lower Monolith 4" : 	ItemData(BASE_ID + 78, 1, "Progression", ),
	#"Pht3 Floating Platforms" : 			ItemData(BASE_ID + 79, 1, "Progression", ),
	#"Pht3 Lava Spinning" : 					ItemData(BASE_ID + 80, 1, "Progression", ),
	#"Pht3 Dirt Elevator" : 					ItemData(BASE_ID + 81, 1, "Progression", ),
	#"FoFH 1 Star" : 						ItemData(BASE_ID + 82, 1, "Progression", ),
	#"FoFH 2 Gate" : 						ItemData(BASE_ID + 83, 1, "Progression", ),
	#"FoFH 2 Star" : 						ItemData(BASE_ID + 84, 1, "Progression", ),
	#"FoFH 3 Gate" : 						ItemData(BASE_ID + 85, 1, "Progression", ),
	#"FoFH 3 Star" : 						ItemData(BASE_ID + 86, 1, "Progression", ),
	#"FoFH Boss Gate" : 						ItemData(BASE_ID + 87, 1, "Progression", ),
	#"FoFH Boss Star" : 						ItemData(BASE_ID + 88, 1, "Progression", ),
	#"FoFH Bonus Gate" : 					ItemData(BASE_ID + 89, 1, "Progression", ),
	#"FoFH Bonus Star" : 					ItemData(BASE_ID + 90, 1, "Progression", ),
	#"FoF1 Coffin" : 						ItemData(BASE_ID + 91, 1, "Progression", ),
	#"FoF1 Doorway" : 						ItemData(BASE_ID + 92, 1, "Progression", ),
	#"FoF1 Drawbridge" : 					ItemData(BASE_ID + 93, 1, "Progression", ),
	#"FoF2 Garibs Fall" : 					ItemData(BASE_ID + 94, 1, "Progression", ),
	#"FoF2 Checkpoint Gates" : 				ItemData(BASE_ID + 95, 1, "Progression", ),
	#"FoF2 Mummy Gate" : 					ItemData(BASE_ID + 96, 1, "Progression", ),
	#"FoF3 Gate" : 							ItemData(BASE_ID + 97, 1, "Progression", ),
	#"FoF3 Spikes" : 						ItemData(BASE_ID + 98, 1, "Progression", ),
	#"OtwH 1 Star" : 						ItemData(BASE_ID + 99, 1, "Progression", ),
	#"OtwH 2 Gate" : 						ItemData(BASE_ID + 100, 1, "Progression", ),
	#"OtwH 2 Star" : 						ItemData(BASE_ID + 101, 1, "Progression", ),
	#"OtwH 3 Gate" : 						ItemData(BASE_ID + 102, 1, "Progression", ),
	#"OtwH 3 Star" : 						ItemData(BASE_ID + 103, 1, "Progression", ),
	#"OtwH Boss Gate" : 						ItemData(BASE_ID + 104, 1, "Progression", ),
	#"OtwH Boss Star" : 						ItemData(BASE_ID + 105, 1, "Progression", ),
	#"OtwH Bonus Gate" : 					ItemData(BASE_ID + 106, 1, "Progression", ),
	#"OtwH Bonus Star" : 					ItemData(BASE_ID + 107, 1, "Progression", ),
	#"Otw1 Aliens" : 						ItemData(BASE_ID + 108, 1, "Progression", ),
	#"Otw1 Fans" : 							ItemData(BASE_ID + 109, 1, "Progression", ),
	#"Otw1 Flying Platforms" : 				ItemData(BASE_ID + 110, 1, "Progression", ),
	#"Otw1 Goo Platforms" : 					ItemData(BASE_ID + 111, 1, "Progression", ),
	#"Otw1 UFO" : 							ItemData(BASE_ID + 112, 1, "Progression", ),
	#"Otw1 Missile" : 						ItemData(BASE_ID + 113, 1, "Progression", ),
	#"Otw2 Mashers" : 						ItemData(BASE_ID + 114, 1, "Progression", ),
	#"Otw2 Ramp" : 							ItemData(BASE_ID + 115, 1, "Progression", ),
	#"Otw3 Hazard Gate" : 					ItemData(BASE_ID + 116, 1, "Progression", ),
	#"Otw3 Sign" : 							ItemData(BASE_ID + 117, 1, "Progression", ),
	#"Otw3 Fan" : 							ItemData(BASE_ID + 118, 1, "Progression", ),
	#"Otw3 Bridge" : 						ItemData(BASE_ID + 119, 1, "Progression", ),
	#"Otw3 Glass Gate" : 					ItemData(BASE_ID + 120, 1, "Progression", ),
	#"Hubworld Atlantis Gate" : 				ItemData(BASE_ID + 121, 1, "Progression", ),
	#"Hubworld Carnival Gate" : 				ItemData(BASE_ID + 122, 1, "Progression", ),
	#"Hubworld Pirate's Cove Gate" : 		ItemData(BASE_ID + 123, 1, "Progression", ),
	#"Hubworld Prehistoric Gate" : 			ItemData(BASE_ID + 124, 1, "Progression", ),
	#"Hubworld Fortress of Fear Gate" : 		ItemData(BASE_ID + 125, 1, "Progression", ),
	#"Hubworld Out of This World Gate" : 	ItemData(BASE_ID + 126, 1, "Progression", ),
	#"Training Sandpit" : 					ItemData(BASE_ID + 127, 1, "Progression", ),
	#"Training Lower Target" : 				ItemData(BASE_ID + 128, 1, "Progression", ),
	#"Training Stairs" : 					ItemData(BASE_ID + 129, 1, "Progression", )
	}

checkpoint_table = {
	"Atl1 Checkpoint 1" : 						ItemData(BASE_ID + 130, 1, "Progression", "Atl1: Checkpoint 1"),
	"Atl1 Checkpoint 2" : 						ItemData(BASE_ID + 131, 1, "Progression", "Atl1: Checkpoint 2"),
	"Atl2 Checkpoint 1" : 						ItemData(BASE_ID + 132, 1, "Progression", "Atl2: Checkpoint 1"),
	"Atl2 Checkpoint 2" : 						ItemData(BASE_ID + 133, 1, "Progression", "Atl2: Checkpoint 2"),
	"Atl2 Checkpoint 3" : 						ItemData(BASE_ID + 134, 1, "Progression", "Atl2: Checkpoint 3"),
	"Atl3 Checkpoint 1" : 						ItemData(BASE_ID + 135, 1, "Progression", "Atl3: Checkpoint 1"),
	"Atl3 Checkpoint 2" : 						ItemData(BASE_ID + 136, 1, "Progression", "Atl3: Checkpoint 2"),
	"Atl3 Checkpoint 3" : 						ItemData(BASE_ID + 137, 1, "Progression", "Atl3: Checkpoint 3")#,
	#"Crn1 Checkpoint 1" : 						ItemData(BASE_ID + 138, 1, "Progression", "Crn1: Checkpoint 1"),
	#"Crn1 Checkpoint 2" : 						ItemData(BASE_ID + 139, 1, "Progression", "Crn1: Checkpoint 2"),
	#"Crn1 Checkpoint 3" : 						ItemData(BASE_ID + 140, 1, "Progression", "Crn1: Checkpoint 3"),
	#"Crn1 Checkpoint 4" : 						ItemData(BASE_ID + 141, 1, "Progression", "Crn1: Checkpoint 4"),
	#"Crn2 Checkpoint 1" : 						ItemData(BASE_ID + 142, 1, "Progression", "Crn2: Checkpoint 1"),
	#"Crn2 Checkpoint 2" : 						ItemData(BASE_ID + 143, 1, "Progression", "Crn2: Checkpoint 2"),
	#"Crn2 Checkpoint 3" : 						ItemData(BASE_ID + 144, 1, "Progression", "Crn2: Checkpoint 3"),
	#"Crn2 Checkpoint 4" : 						ItemData(BASE_ID + 145, 1, "Progression", "Crn2: Checkpoint 4"),
	#"Crn2 Checkpoint 5" : 						ItemData(BASE_ID + 146, 1, "Progression", "Crn2: Checkpoint 5"),
	#"Crn3 Checkpoint 1" : 						ItemData(BASE_ID + 147, 1, "Progression", "Crn3: Checkpoint 1"),
	#"Crn3 Checkpoint 2" : 						ItemData(BASE_ID + 148, 1, "Progression", "Crn3: Checkpoint 2"),
	#"Crn3 Checkpoint 3" : 						ItemData(BASE_ID + 149, 1, "Progression", "Crn3: Checkpoint 3"),
	#"Crn3 Checkpoint 4" : 						ItemData(BASE_ID + 150, 1, "Progression", "Crn3: Checkpoint 4"),
	#"Prt1 Checkpoint 1" : 						ItemData(BASE_ID + 151, 1, "Progression", "Prt1: Checkpoint 1"),
	#"Prt1 Checkpoint 2" : 						ItemData(BASE_ID + 152, 1, "Progression", "Prt1: Checkpoint 2"),
	#"Prt1 Checkpoint 3" : 						ItemData(BASE_ID + 153, 1, "Progression", "Prt1: Checkpoint 3"),
	#"Prt2 Checkpoint 1" : 						ItemData(BASE_ID + 154, 1, "Progression", "Prt2: Checkpoint 1"),
	#"Prt2 Checkpoint 2" : 						ItemData(BASE_ID + 155, 1, "Progression", "Prt2: Checkpoint 2"),
	#"Prt2 Checkpoint 3" : 						ItemData(BASE_ID + 156, 1, "Progression", "Prt2: Checkpoint 3"),
	#"Prt3 Checkpoint 1" : 						ItemData(BASE_ID + 157, 1, "Progression", "Prt3: Checkpoint 1"),
	#"Prt3 Checkpoint 2" : 						ItemData(BASE_ID + 158, 1, "Progression", "Prt3: Checkpoint 2"),
	#"Prt3 Checkpoint 3" : 						ItemData(BASE_ID + 159, 1, "Progression", "Prt3: Checkpoint 3"),
	#"Prt3 Checkpoint 4" : 						ItemData(BASE_ID + 160, 1, "Progression", "Prt3: Checkpoint 4"),
	#"Pht1 Checkpoint 1" : 						ItemData(BASE_ID + 161, 1, "Progression", "Pht1: Checkpoint 1"),
	#"Pht1 Checkpoint 2" : 						ItemData(BASE_ID + 162, 1, "Progression", "Pht1: Checkpoint 2"),
	#"Pht1 Checkpoint 3" : 						ItemData(BASE_ID + 163, 1, "Progression", "Pht1: Checkpoint 3"),
	#"Pht2 Checkpoint 1" : 						ItemData(BASE_ID + 164, 1, "Progression", "Pht2: Checkpoint 1"),
	#"Pht2 Checkpoint 2" : 						ItemData(BASE_ID + 165, 1, "Progression", "Pht2: Checkpoint 2"),
	#"Pht2 Checkpoint 3" : 						ItemData(BASE_ID + 166, 1, "Progression", "Pht2: Checkpoint 3"),
	#"Pht2 Checkpoint 4" : 						ItemData(BASE_ID + 167, 1, "Progression", "Pht2: Checkpoint 4"),
	#"Pht3 Checkpoint 1" : 						ItemData(BASE_ID + 168, 1, "Progression", "Pht3: Checkpoint 1"),
	#"Pht3 Checkpoint 2" : 						ItemData(BASE_ID + 169, 1, "Progression", "Pht3: Checkpoint 2"),
	#"Pht3 Checkpoint 3" : 						ItemData(BASE_ID + 170, 1, "Progression", "Pht3: Checkpoint 3"),
	#"Pht3 Checkpoint 4" : 						ItemData(BASE_ID + 171, 1, "Progression", "Pht3: Checkpoint 4"),
	#"FoF1 Checkpoint 1" : 						ItemData(BASE_ID + 172, 1, "Progression", "FoF1: Checkpoint 1"),
	#"FoF1 Checkpoint 2" : 						ItemData(BASE_ID + 173, 1, "Progression", "FoF1: Checkpoint 2"),
	#"FoF1 Checkpoint 3" : 						ItemData(BASE_ID + 174, 1, "Progression", "FoF1: Checkpoint 3"),
	#"FoF2 Checkpoint 1" : 						ItemData(BASE_ID + 175, 1, "Progression", "FoF2: Checkpoint 1"),
	#"FoF2 Checkpoint 2" : 						ItemData(BASE_ID + 176, 1, "Progression", "FoF2: Checkpoint 2"),
	#"FoF2 Checkpoint 3" : 						ItemData(BASE_ID + 177, 1, "Progression", "FoF2: Checkpoint 3"),
	#"FoF3 Checkpoint 1" : 						ItemData(BASE_ID + 178, 1, "Progression", "FoF3: Checkpoint 1"),
	#"FoF3 Checkpoint 2" : 						ItemData(BASE_ID + 179, 1, "Progression", "FoF3: Checkpoint 2"),
	#"FoF3 Checkpoint 3" : 						ItemData(BASE_ID + 180, 1, "Progression", "FoF3: Checkpoint 3"),
	#"FoF3 Checkpoint 4" : 						ItemData(BASE_ID + 181, 1, "Progression", "FoF3: Checkpoint 4"),
	#"FoF3 Checkpoint 5" : 						ItemData(BASE_ID + 182, 1, "Progression", "FoF3: Checkpoint 5"),
	#"Otw1 Checkpoint 1" : 						ItemData(BASE_ID + 183, 1, "Progression", "Otw1: Checkpoint 1"),
	#"Otw1 Checkpoint 2" : 						ItemData(BASE_ID + 184, 1, "Progression", "Otw1: Checkpoint 2"),
	#"Otw2 Checkpoint 1" : 						ItemData(BASE_ID + 185, 1, "Progression", "Otw2: Checkpoint 1"),
	#"Otw3 Checkpoint 1" : 						ItemData(BASE_ID + 186, 1, "Progression", "Otw3: Checkpoint 1"),
	#"Otw3 Checkpoint 2" : 						ItemData(BASE_ID + 187, 1, "Progression", "Otw3: Checkpoint 2"),
	#"Otw3 Checkpoint 3" : 						ItemData(BASE_ID + 188, 1, "Progression", "Otw3: Checkpoint 3"),
	#"Otw3 Checkpoint 4" : 						ItemData(BASE_ID + 189, 1, "Progression", "Otw3: Checkpoint 4"),
	}

world_garib_table = {
	"Atl1 1 Garibs" : 							ItemData(BASE_ID + 190, 1, "Garib", None),
	"Atl1 2 Garibs" : 							ItemData(BASE_ID + 191, 3, "Garib", None),
	"Atl1 3 Garibs" : 							ItemData(BASE_ID + 192, 1, "Garib", None),
	"Atl1 4 Garibs" : 							ItemData(BASE_ID + 193, 5, "Garib", None),
	"Atl1 5 Garibs" : 							ItemData(BASE_ID + 194, 1, "Garib", None),
	"Atl1 6 Garibs" : 							ItemData(BASE_ID + 195, 1, "Garib", None),
	"Atl1 9 Garibs" : 							ItemData(BASE_ID + 196, 1, "Garib", None),
	"Atl2 1 Garibs" : 							ItemData(BASE_ID + 197, 1, "Garib", None),
	"Atl2 2 Garibs" : 							ItemData(BASE_ID + 198, 2, "Garib", None),
	"Atl2 3 Garibs" : 							ItemData(BASE_ID + 199, 3, "Garib", None),
	"Atl2 4 Garibs" : 							ItemData(BASE_ID + 200, 1, "Garib", None),
	"Atl2 5 Garibs" : 							ItemData(BASE_ID + 201, 5, "Garib", None),
	"Atl2 7 Garibs" : 							ItemData(BASE_ID + 202, 1, "Garib", None),
	"Atl2 10 Garibs" : 							ItemData(BASE_ID + 203, 1, "Garib", None),
	"Atl3 1 Garibs" : 							ItemData(BASE_ID + 204, 2, "Garib", None),
	"Atl3 2 Garibs" : 							ItemData(BASE_ID + 205, 1, "Garib", None),
	"Atl3 3 Garibs" : 							ItemData(BASE_ID + 206, 2, "Garib", None),
	"Atl3 4 Garibs" : 							ItemData(BASE_ID + 207, 4, "Garib", None),
	"Atl3 5 Garibs" : 							ItemData(BASE_ID + 208, 3, "Garib", None),
	"Atl3 6 Garibs" : 							ItemData(BASE_ID + 209, 1, "Garib", None),
	"Atl3 8 Garibs" : 							ItemData(BASE_ID + 210, 3, "Garib", None),
	"Atl3 9 Garibs" : 							ItemData(BASE_ID + 211, 1, "Garib", None)#,
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
#	"Cartwheel" : 								ItemData(BASE_ID + 330, 1,"Progression",None),
#	"Crawl" : 									ItemData(BASE_ID + 331, 1,"Useful",None),
	"Double Jump" : 							ItemData(BASE_ID + 332, 1,"Progression",None),
	"Fist Slam" : 								ItemData(BASE_ID + 333, 1,"Progression",None),
#	"Ledge Grab" : 								ItemData(BASE_ID + 334, 1,"Progression",None),
#	"Push" : 									ItemData(BASE_ID + 335, 1,"Progression",None),
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
	"Speed Potion" : 							ItemData(BASE_ID + 348, 1,"Progression",None),
	"Sticky Potion" : 							ItemData(BASE_ID + 349, 1,"Progression",None),
	"Hercules Potion" : 						ItemData(BASE_ID + 350, 1,"Progression",None),
#	"Grab" : 									ItemData(BASE_ID + 351, 1,"Progression",None),
	"Rubber Ball" : 							ItemData(BASE_ID + 352, 1,"Progression",None),
	"Bowling Ball" : 							ItemData(BASE_ID + 353, 1,"Progression",None),
	"Ball Bearing" : 							ItemData(BASE_ID + 354, 1,"Progression",None),
	"Crystal" : 								ItemData(BASE_ID + 355, 1,"Progression",None),
	"Power Ball" : 								ItemData(BASE_ID + 356, 1,"Progression",None)
    }

filler_table = {
    "Extra Garibs" : 							ItemData(BASE_ID + 357, -1,"Useful",None),
    "Chicken Sound" : 							ItemData(BASE_ID + 358, -1,"Trap",None),
	"Life" : 									ItemData(BASE_ID + 359, -1,"Filler",None),
    "Boomerang" : 								ItemData(BASE_ID + 360, -1,"Filler",None),
    "Beachball" : 								ItemData(BASE_ID + 361, -1,"Filler",None),
    "Hercules" : 								ItemData(BASE_ID + 362, -1,"Filler",None),
    "Helicopter" : 								ItemData(BASE_ID + 363, -1,"Filler",None),
    "Speed" : 									ItemData(BASE_ID + 364, -1,"Filler",None),
    "Frog" : 									ItemData(BASE_ID + 365, -1,"Filler",None),
    "Death" : 									ItemData(BASE_ID + 366, -1,"Filler",None),
    "Sticky" : 									ItemData(BASE_ID + 367, -1,"Filler",None)
	}

trap_table = {
	"Frog Trap" : 								ItemData(BASE_ID + 368, -1,"Trap",None),
    "Cursed Ball" :								ItemData(BASE_ID + 369, -1,"Trap",None),
    "Instant Crystal" :							ItemData(BASE_ID + 370, -1,"Trap",None),
    "Camera Rotate" :							ItemData(BASE_ID + 371, -1,"Trap",None),
    "Tip Trap" :								ItemData(BASE_ID + 372, -1,"Trap",None)
	}

garibsanity_world_table = {
	"Atl1 Garib" : 								ItemData(BASE_ID + 20001, 50,"Garib",None),
	"Atl2 Garib" : 								ItemData(BASE_ID + 20002, 60,"Garib",None),
	"Atl3 Garib" : 								ItemData(BASE_ID + 20003, 80,"Garib",None)#,
	#"Atl? Garib" : 							ItemData(BASE_ID + 20004, 25,"Garib",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 20004, 65,"Garib",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 20004, 80,"Garib",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 20004, 80,"Garib",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 20004, 20,"Garib",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 20004, 70,"Garib",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 20004, 60,"Garib",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 20004, 80,"Garib",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 20004, 50,"Garib",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 20004, 80,"Garib",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 20004, 80,"Garib",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 20004, 80,"Garib",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 20004, 60,"Garib",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 20004, 60,"Garib",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 20004, 60,"Garib",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 20004, 70,"Garib",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 20004, 56,"Garib",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 20004, 50,"Garib",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 20004, 50,"Garib",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 20004, 80,"Garib",None),
	#"4 Garibs" : 								ItemData(BASE_ID + 20004, 50,"Garib",None)
	}

#decoupled_garib_table = {
#	"Garib" : 									ItemData(BASE_ID + 10001, 42,"Garib",None),
#	"2 Garibs" : 								ItemData(BASE_ID + 10002, 31,"Garib",None),
#	"3 Garibs" : 								ItemData(BASE_ID + 10003, 61,"Garib",None),
#	"4 Garibs" : 								ItemData(BASE_ID + 10004, 62,"Garib",None),
#	"5 Garibs" : 								ItemData(BASE_ID + 10005, 34,"Garib",None),
#	"6 Garibs" : 								ItemData(BASE_ID + 10006, 21,"Garib",None),
#	"7 Garibs" : 								ItemData(BASE_ID + 10007, 7,"Garib",None),
#	"8 Garibs" : 								ItemData(BASE_ID + 10008, 27,"Garib",None),
#	"9 Garibs" : 								ItemData(BASE_ID + 10009, 5,"Garib",None),
#	"10 Garibs" : 								ItemData(BASE_ID + 10010, 13,"Garib",None),
#	"11 Garibs" : 								ItemData(BASE_ID + 10011, 2,"Garib",None),
#	"12 Garibs" : 								ItemData(BASE_ID + 10012, 7,"Garib",None),
#	#"13 Garibs" : 								ItemData(BASE_ID + 10013, 0,"Garib",None),
#	"14 Garibs" : 								ItemData(BASE_ID + 10014, 4,"Garib",None),
#	"15 Garibs" : 								ItemData(BASE_ID + 10015, 1,"Garib",None),
#	"16 Garibs" : 								ItemData(BASE_ID + 10016, 3,"Garib",None),
#}
#
#garbinsanity = ItemData(BASE_ID + 10001, 1496,"Garib",None)

#Atlantis 1&2
decoupled_garib_table = {
	"Garib" : 									ItemData(BASE_ID + 10001, 2, "Garib", None),
	"2 Garibs" : 								ItemData(BASE_ID + 10002, 5, "Garib", None),
	"3 Garibs" : 								ItemData(BASE_ID + 10003, 4, "Garib", None),
	"4 Garibs" : 								ItemData(BASE_ID + 10004, 6, "Garib", None),
	"5 Garibs" : 								ItemData(BASE_ID + 10005, 6, "Garib", None),
	"6 Garibs" : 								ItemData(BASE_ID + 10006, 1, "Garib", None),
	"7 Garibs" : 								ItemData(BASE_ID + 10007, 1, "Garib", None),
	"9 Garibs" : 								ItemData(BASE_ID + 10009, 1, "Garib", None),
	"10 Garibs" : 								ItemData(BASE_ID + 10010, 1, "Garib", None)
}
garbinsanity = ItemData(BASE_ID + 10001, 110, "Garib", None)

all_items = {
	**level_event_table, 
	**checkpoint_table, 
	**ability_table, 
	**filler_table, 
	**trap_table, 
	**world_garib_table, 
	**garibsanity_world_table,
	**{"Garibsanity" : garbinsanity},
	**decoupled_garib_table
}

def generate_item_name_to_id() -> dict:
	output : dict = {}
	for name, data in all_items.items():
		output[name] = data.glid
	return output

def generate_item_name_groups() -> dict:
	output : dict = {
		"Level Events" :				level_event_table.keys(),
		"Checkpoints" :					checkpoint_table.keys(),
		"Not Crystal" :					["Rubber Ball", "Bowling Ball", "Ball Bearing", "Power Ball"],
		"Not Bowling" :					["Rubber Ball", "Ball Bearing", "Crystal", "Power Ball"],
		"Not Bowling or Crystal" :		["Rubber Ball", "Ball Bearing", "Power Ball"],
		"Sinks" :						["Bowling Ball", "Ball Bearing"],
		"Floats" :						["Rubber Ball", "Crystal", "Power Ball"],
		"Ball Up" :						["Throw", "Dribble", "Lob Ball"]
	}
	return output
