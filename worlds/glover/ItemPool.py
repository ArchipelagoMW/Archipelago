from typing import NamedTuple
from .Options import GaribLogic, GaribSorting

class ItemData(NamedTuple):
	glid: int|None = None
	qty: int = 0
	type: str = ""
	default_location: str = ""

def find_item_data(self, name : str) -> ItemData:
	#Garib Groups
	if name in world_garib_table:
		return world_garib_table[name]
	if name in garibsanity_world_table:
		return garibsanity_world_table[name]
	#Decoupled garibs
	if name in decoupled_garib_table:
		#Include bonus level garibs in the count
		if self.options.bonus_levels:
			return decoupled_garib_table[name]
		else:
			#If there's no bonus garib groups with this count, the quantity stays the same
			if not name in decoupled_garib_bonus_count:
				return decoupled_garib_table[name]
			#Otherwise remove bonus level garibs from the count
			modified_item = decoupled_garib_table[name]
			return ItemData(modified_item.glid, modified_item.qty - decoupled_garib_bonus_count[name], modified_item.type, modified_item.default_location)
	if name == "Garibsanity":
		#Include bonus level garibs in the count
		if self.options.bonus_levels:
			return garbinsanity
		else:
			#Remove bonus level garibs from the count
			return ItemData(garbinsanity.glid, garbinsanity.qty - garbinsanity_bonus_count, garbinsanity.type, garbinsanity.default_location)
	#Extra garibs become other items
	if name == "Extra Garibs":
		modified_item = convert_extra_garibs(self)
		#But filler
		return ItemData(modified_item.glid, modified_item.qty, "Filler", modified_item.default_location)

	#Core
	if name in portalsanity_table:
		#As event item?
		if self.options.portalsanity:
			return portalsanity_table[name]
		else:
			modified_item = portalsanity_table[name]
			return ItemData(None, modified_item.qty, modified_item.type, modified_item.default_location)
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

portalsanity_table = {
	"AtlH 1 Star" : 						ItemData(BASE_ID + 0, 1, "Progression", "Atl1: All Garibs"),
	"AtlH 2 Gate" : 						ItemData(BASE_ID + 1, 1, "Progression", "Atl1: Goal"),
	"AtlH 2 Star" : 						ItemData(BASE_ID + 2, 1, "Progression", "Atl2: All Garibs"),
	"AtlH 3 Gate" : 						ItemData(BASE_ID + 3, 1, "Progression", "Atl2: Goal"),
	"AtlH 3 Star" : 						ItemData(BASE_ID + 4, 1, "Progression", "Atl3: All Garibs"),
	"AtlH Boss Gate" : 						ItemData(BASE_ID + 5, 1, "Progression", "Atl3: Goal"),
	"AtlH Boss Star" : 						ItemData(BASE_ID + 6, 1, "Progression", "Atl!: Goal"),
	"AtlH Bonus Gate" : 					ItemData(BASE_ID + 7, 1, "Progression", "AtlH: Bonus Unlock"),
	"AtlH Bonus Star" : 					ItemData(BASE_ID + 8, 1, "Progression", "Atl?: All Garibs"),
	"CrnH 1 Star" : 						ItemData(BASE_ID + 15, 1, "Progression", "Crn1: All Garibs"),
	"CrnH 2 Gate" : 						ItemData(BASE_ID + 16, 1, "Progression", "Crn1: Goal"),
	"CrnH 2 Star" : 						ItemData(BASE_ID + 17, 1, "Progression", "Crn2: All Garibs"),
	"CrnH 3 Gate" : 						ItemData(BASE_ID + 18, 1, "Progression", "Crn2: Goal"),
	"CrnH 3 Star" : 						ItemData(BASE_ID + 19, 1, "Progression", "Crn3: All Garibs"),
	"CrnH Boss Gate" : 						ItemData(BASE_ID + 20, 1, "Progression", "Crn3: Goal"),
	"CrnH Boss Star" : 						ItemData(BASE_ID + 21, 1, "Progression", "Crn!: Goal"),
	"CrnH Bonus Gate" : 					ItemData(BASE_ID + 22, 1, "Progression", "CrnH: Bonus Unlock"),
	"CrnH Bonus Star" : 					ItemData(BASE_ID + 23, 1, "Progression", "Crn?: All Garibs"),
	"PrtH 1 Star" : 						ItemData(BASE_ID + 36, 1, "Progression", "Prt1: All Garibs"),
	"PrtH 2 Gate" : 						ItemData(BASE_ID + 37, 1, "Progression", "Prt1: Goal"),
	"PrtH 2 Star" : 						ItemData(BASE_ID + 38, 1, "Progression", "Prt2: All Garibs"),
	"PrtH 3 Gate" : 						ItemData(BASE_ID + 39, 1, "Progression", "Prt2: Goal"),
	"PrtH 3 Star" : 						ItemData(BASE_ID + 40, 1, "Progression", "Prt3: All Garibs"),
	"PrtH Boss Gate" : 						ItemData(BASE_ID + 41, 1, "Progression", "Prt3: Goal"),
	"PrtH Boss Star" : 						ItemData(BASE_ID + 42, 1, "Progression", "Prt!: Goal"),
	"PrtH Bonus Gate" : 					ItemData(BASE_ID + 43, 1, "Progression", "PrtH: Bonus Unlock"),
	"PrtH Bonus Star" : 					ItemData(BASE_ID + 44, 1, "Progression", "Prt?: All Garibs"),
	"PhtH 1 Star" : 						ItemData(BASE_ID + 60, 1, "Progression", "Pht1: All Garibs"),
	"PhtH 2 Gate" : 						ItemData(BASE_ID + 61, 1, "Progression", "Pht1: Goal"),
	"PhtH 2 Star" : 						ItemData(BASE_ID + 62, 1, "Progression", "Pht2: All Garibs"),
	"PhtH 3 Gate" : 						ItemData(BASE_ID + 63, 1, "Progression", "Pht2: Goal"),
	"PhtH 3 Star" : 						ItemData(BASE_ID + 64, 1, "Progression", "Pht3: All Garibs"),
	"PhtH Boss Gate" : 						ItemData(BASE_ID + 65, 1, "Progression", "Pht3: Goal"),
	"PhtH Boss Star" : 						ItemData(BASE_ID + 66, 1, "Progression", "Pht!: Goal"),
	"PhtH Bonus Gate" : 					ItemData(BASE_ID + 67, 1, "Progression", "PhtH: Bonus Unlock"),
	"PhtH Bonus Star" : 					ItemData(BASE_ID + 68, 1, "Progression", "Pht?: All Garibs"),
	#"FoFH 1 Star" : 						ItemData(BASE_ID + 82, 1, "Progression", ),
	#"FoFH 2 Gate" : 						ItemData(BASE_ID + 83, 1, "Progression", ),
	#"FoFH 2 Star" : 						ItemData(BASE_ID + 84, 1, "Progression", ),
	#"FoFH 3 Gate" : 						ItemData(BASE_ID + 85, 1, "Progression", ),
	#"FoFH 3 Star" : 						ItemData(BASE_ID + 86, 1, "Progression", ),
	#"FoFH Boss Gate" : 						ItemData(BASE_ID + 87, 1, "Progression", ),
	#"FoFH Boss Star" : 						ItemData(BASE_ID + 88, 1, "Progression", ),
	#"FoFH Bonus Gate" : 					ItemData(BASE_ID + 89, 1, "Progression", ),
	#"FoFH Bonus Star" : 					ItemData(BASE_ID + 90, 1, "Progression", ),
	#"OtwH 1 Star" : 						ItemData(BASE_ID + 99, 1, "Progression", ),
	#"OtwH 2 Gate" : 						ItemData(BASE_ID + 100, 1, "Progression", ),
	#"OtwH 2 Star" : 						ItemData(BASE_ID + 101, 1, "Progression", ),
	#"OtwH 3 Gate" : 						ItemData(BASE_ID + 102, 1, "Progression", ),
	#"OtwH 3 Star" : 						ItemData(BASE_ID + 103, 1, "Progression", ),
	#"OtwH Boss Gate" : 						ItemData(BASE_ID + 104, 1, "Progression", ),
	#"OtwH Boss Star" : 						ItemData(BASE_ID + 105, 1, "Progression", ),
	#"OtwH Bonus Gate" : 					ItemData(BASE_ID + 106, 1, "Progression", ),
	#"OtwH Bonus Star" : 					ItemData(BASE_ID + 107, 1, "Progression", ),
	"Hubworld Atlantis Gate" : 				ItemData(BASE_ID + 121, 1, "Progression", "Ball Turn-In 1"),
	"Hubworld Carnival Gate" : 				ItemData(BASE_ID + 122, 1, "Progression", "Ball Turn-In 2A"),
	"Hubworld Pirate's Cove Gate" : 		ItemData(BASE_ID + 123, 1, "Progression", "Ball Turn-In 2B")#,
	#"Hubworld Prehistoric Gate" : 			ItemData(BASE_ID + 124, 1, "Progression", "Ball Turn-In 4A"),
	#"Hubworld Fortress of Fear Gate" : 		ItemData(BASE_ID + 125, 1, "Progression", "Ball Turn-In 4B"),
	#"Hubworld Out of This World Gate" : 	ItemData(BASE_ID + 126, 1, "Progression", "Ball Turn-In 6"),
}

level_event_table = {
	"Atl1 Gate" : 							ItemData(BASE_ID + 9, 1, "Progression", "Atl1: Glover Switch"),
	"Atl2 Elevator" : 						ItemData(BASE_ID + 10, 1, "Progression", "Atl2: Drain Block"),
	"Atl2 Ball Switch Drain" : 				ItemData(BASE_ID + 11, 1, "Progression", "Atl2: Ball Switch"),
	"Atl2 Gate" : 							ItemData(BASE_ID + 12, 1, "Progression", "Atl2: Glover Switch"),
	"Atl3 Waterwheel" : 					ItemData(BASE_ID + 13, 1, "Progression", "Atl3: Pyramid Ball Switch"),
	"Atl3 Cave Platforms" : 				ItemData(BASE_ID + 14, 1, "Progression", "Atl3: Cliff Ball Switch"),
	"Crn1 Elevator" : 						ItemData(BASE_ID + 24, 1, "Progression", "Crn1: Conveyor Target"),
	"Crn1 Gate" : 							ItemData(BASE_ID + 25, 1, "Progression", "Crn1: Bars Glover Switch"),
	"Crn1 Door A" : 						ItemData(BASE_ID + 26, 1, "Progression", "Crn1: Ramp Ball Switch"),
	"Crn1 Door B" : 						ItemData(BASE_ID + 27, 1, "Progression", "Crn1: Ice Cream Glover Switch"),
	"Crn1 Door C" : 						ItemData(BASE_ID + 28, 1, "Progression", "Crn1: Slide Glover Switch"),
	"Crn1 Rocket" : 						ItemData(BASE_ID + 29, 3, "Progression"),
	"Crn2 Drop Garibs" : 					ItemData(BASE_ID + 32, 1, "Progression", "Crn2: Clown Teeth"),
	"Crn2 Fan" : 							ItemData(BASE_ID + 33, 1, "Progression", "Crn2: Ball Switch"),
	"Crn3 Spin Door" : 						ItemData(BASE_ID + 34, 1, "Progression", "Crn3: Glover Switch"),
	"Crn3 Hands" : 							ItemData(BASE_ID + 35, 1, "Progression", "Crn3: Ball Switch"),
	"Prt1 Raise Beach" : 					ItemData(BASE_ID + 45, 1, "Progression", "Prt1: Ship Target"),
	"Prt1 Elevator" : 						ItemData(BASE_ID + 46, 1, "Progression", "Prt1: Tower Glover Switch"),
	"Prt1 Chest" : 							ItemData(BASE_ID + 47, 1, "Progression", "Prt1: Coast Target"),
	"Prt1 Sandpile" : 						ItemData(BASE_ID + 48, 1, "Progression", "Prt1: Fan Ball Switch"),
	"Prt1 Waterspout" : 					ItemData(BASE_ID + 49, 1, "Progression", "Prt1: Sand Ball Switch"),
	"Prt1 Lighthouse" : 					ItemData(BASE_ID + 50, 1, "Progression", "Prt1: Lighthouse Target"),
	"Prt1 Raise Ship" : 					ItemData(BASE_ID + 51, 1, "Progression", "Prt1: Lighthouse Glover Switch"),
	"Prt1 Bridge" : 						ItemData(BASE_ID + 52, 1, "Progression", "Prt1: Crate Ball Switch"),
	"Prt2 Lower Water" : 					ItemData(BASE_ID + 53, 1, "Progression", "Prt2: Glover Switch"),
	"Prt2 Ramp" : 							ItemData(BASE_ID + 54, 1, "Progression", "Prt2: Water Ball Switch"),
	"Prt2 Gate" : 							ItemData(BASE_ID + 55, 1, "Progression", "Prt2: Platform Ball Switch"),
	#"Prt3 Platform Spin" : 					ItemData(BASE_ID + 56, 1, "Progression", ),
	"Prt3 Trampoline" : 					ItemData(BASE_ID + 57, 1, "Progression", "Prt3: Cliff Glover Switch"),
	"Prt3 Stairs" : 						ItemData(BASE_ID + 58, 1, "Progression", "Prt3: Target"),
	"Prt3 Elevator" : 						ItemData(BASE_ID + 59, 1, "Progression", "Prt3: Ball Switch"),
	"Pht1 Life Drop" : 						ItemData(BASE_ID + 69, 1, "Progression", "Pht1: Icicles"),
	"Pht2 Platform 1" : 					ItemData(BASE_ID + 70, 1, "Progression", "Pht2: Lavafall Ball Switch"),
	"Pht2 Platform 2" : 					ItemData(BASE_ID + 71, 1, "Progression", "Pht2: Switches Ball Switch"),
	"Pht2 Lower Ball Switch" : 				ItemData(BASE_ID + 72, 1, "Progression", "Pht2: Glover Switch"),
	"Pht3 Drop Garibs" : 					ItemData(BASE_ID + 73, 1, "Progression", "Pht3: Tracey Tree"),
	"Pht3 Spin Stones" : 					ItemData(BASE_ID + 74, 1, "Progression", "Pht3: Trees Glover Switch"),
	"Pht3 Lower Monolith" : 				ItemData(BASE_ID + 75, 4, "Progression", ""),
	"Pht3 Floating Platforms" : 			ItemData(BASE_ID + 79, 1, "Progression", "Pht3: Monolith Ball Switch"),
	"Pht3 Lava Spinning" : 					ItemData(BASE_ID + 80, 1, "Progression", "Pht3: Flying Lava Ball Switch"),
	"Pht3 Dirt Elevator" : 					ItemData(BASE_ID + 81, 1, "Progression", "Pht3: Lava Pit Ball Switch")#,
	#"FoF1 Coffin" : 						ItemData(BASE_ID + 91, 1, "Progression", ),
	#"FoF1 Doorway" : 						ItemData(BASE_ID + 92, 1, "Progression", ),
	#"FoF1 Drawbridge" : 					ItemData(BASE_ID + 93, 1, "Progression", )#,
	#"FoF2 Garibs Fall" : 					ItemData(BASE_ID + 94, 1, "Progression", ),
	#"FoF2 Checkpoint Gates" : 				ItemData(BASE_ID + 95, 1, "Progression", ),
	#"FoF2 Mummy Gate" : 					ItemData(BASE_ID + 96, 1, "Progression", )#,
	#"FoF3 Gate" : 							ItemData(BASE_ID + 97, 1, "Progression", ),
	#"FoF3 Spikes" : 						ItemData(BASE_ID + 98, 1, "Progression", )#,
	#"Otw1 Aliens" : 						ItemData(BASE_ID + 108, 1, "Progression", ),
	#"Otw1 Fans" : 							ItemData(BASE_ID + 109, 1, "Progression", ),
	#"Otw1 Flying Platforms" : 				ItemData(BASE_ID + 110, 1, "Progression", ),
	#"Otw1 Goo Platforms" : 					ItemData(BASE_ID + 111, 1, "Progression", ),
	#"Otw1 UFO" : 							ItemData(BASE_ID + 112, 1, "Progression", ),
	#"Otw1 Missile" : 						ItemData(BASE_ID + 113, 1, "Progression", )#,
	#"Otw2 Mashers" : 						ItemData(BASE_ID + 114, 1, "Progression", ),
	#"Otw2 Ramp" : 							ItemData(BASE_ID + 115, 1, "Progression", )#,
	#"Otw3 Hazard Gate" : 					ItemData(BASE_ID + 116, 1, "Progression", ),
	#"Otw3 Sign" : 							ItemData(BASE_ID + 117, 1, "Progression", ),
	#"Otw3 Fan" : 							ItemData(BASE_ID + 118, 1, "Progression", ),
	#"Otw3 Bridge" : 						ItemData(BASE_ID + 119, 1, "Progression", ),
	#"Otw3 Glass Gate" : 					ItemData(BASE_ID + 120, 1, "Progression", )#,
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
	"Atl3 Checkpoint 3" : 						ItemData(BASE_ID + 137, 1, "Progression", "Atl3: Checkpoint 3"),
	"Crn1 Checkpoint 1" : 						ItemData(BASE_ID + 138, 1, "Progression", "Crn1: Checkpoint 1"),
	"Crn1 Checkpoint 2" : 						ItemData(BASE_ID + 139, 1, "Progression", "Crn1: Checkpoint 2"),
	"Crn1 Checkpoint 3" : 						ItemData(BASE_ID + 140, 1, "Progression", "Crn1: Checkpoint 3"),
	"Crn1 Checkpoint 4" : 						ItemData(BASE_ID + 141, 1, "Progression", "Crn1: Checkpoint 4"),
	"Crn2 Checkpoint 1" : 						ItemData(BASE_ID + 142, 1, "Progression", "Crn2: Checkpoint 1"),
	"Crn2 Checkpoint 2" : 						ItemData(BASE_ID + 143, 1, "Progression", "Crn2: Checkpoint 2"),
	"Crn2 Checkpoint 3" : 						ItemData(BASE_ID + 144, 1, "Progression", "Crn2: Checkpoint 3"),
	"Crn2 Checkpoint 4" : 						ItemData(BASE_ID + 145, 1, "Progression", "Crn2: Checkpoint 4"),
	"Crn2 Checkpoint 5" : 						ItemData(BASE_ID + 146, 1, "Progression", "Crn2: Checkpoint 5"),
	"Crn3 Checkpoint 1" : 						ItemData(BASE_ID + 147, 1, "Progression", "Crn3: Checkpoint 1"),
	"Crn3 Checkpoint 2" : 						ItemData(BASE_ID + 148, 1, "Progression", "Crn3: Checkpoint 2"),
	"Crn3 Checkpoint 3" : 						ItemData(BASE_ID + 149, 1, "Progression", "Crn3: Checkpoint 3"),
	"Crn3 Checkpoint 4" : 						ItemData(BASE_ID + 150, 1, "Progression", "Crn3: Checkpoint 4"),
	"Prt1 Checkpoint 1" : 						ItemData(BASE_ID + 151, 1, "Progression", "Prt1: Checkpoint 1"),
	"Prt1 Checkpoint 2" : 						ItemData(BASE_ID + 152, 1, "Progression", "Prt1: Checkpoint 2"),
	"Prt1 Checkpoint 3" : 						ItemData(BASE_ID + 153, 1, "Progression", "Prt1: Checkpoint 3"),
	"Prt2 Checkpoint 1" : 						ItemData(BASE_ID + 154, 1, "Progression", "Prt2: Checkpoint 1"),
	"Prt2 Checkpoint 2" : 						ItemData(BASE_ID + 155, 1, "Progression", "Prt2: Checkpoint 2"),
	"Prt2 Checkpoint 3" : 						ItemData(BASE_ID + 156, 1, "Progression", "Prt2: Checkpoint 3"),
	"Prt3 Checkpoint 1" : 						ItemData(BASE_ID + 157, 1, "Progression", "Prt3: Checkpoint 1"),
	"Prt3 Checkpoint 2" : 						ItemData(BASE_ID + 158, 1, "Progression", "Prt3: Checkpoint 2"),
	"Prt3 Checkpoint 3" : 						ItemData(BASE_ID + 159, 1, "Progression", "Prt3: Checkpoint 3"),
	"Prt3 Checkpoint 4" : 						ItemData(BASE_ID + 160, 1, "Progression", "Prt3: Checkpoint 4"),
	"Pht1 Checkpoint 1" : 						ItemData(BASE_ID + 161, 1, "Progression", "Pht1: Checkpoint 1"),
	"Pht1 Checkpoint 2" : 						ItemData(BASE_ID + 162, 1, "Progression", "Pht1: Checkpoint 2"),
	"Pht1 Checkpoint 3" : 						ItemData(BASE_ID + 163, 1, "Progression", "Pht1: Checkpoint 3"),
	"Pht2 Checkpoint 1" : 						ItemData(BASE_ID + 164, 1, "Progression", "Pht2: Checkpoint 1"),
	"Pht2 Checkpoint 2" : 						ItemData(BASE_ID + 165, 1, "Progression", "Pht2: Checkpoint 2"),
	"Pht2 Checkpoint 3" : 						ItemData(BASE_ID + 166, 1, "Progression", "Pht2: Checkpoint 3"),
	"Pht2 Checkpoint 4" : 						ItemData(BASE_ID + 167, 1, "Progression", "Pht2: Checkpoint 4"),
	"Pht3 Checkpoint 1" : 						ItemData(BASE_ID + 168, 1, "Progression", "Pht3: Checkpoint 1"),
	"Pht3 Checkpoint 2" : 						ItemData(BASE_ID + 169, 1, "Progression", "Pht3: Checkpoint 2"),
	"Pht3 Checkpoint 3" : 						ItemData(BASE_ID + 170, 1, "Progression", "Pht3: Checkpoint 3"),
	"Pht3 Checkpoint 4" : 						ItemData(BASE_ID + 171, 1, "Progression", "Pht3: Checkpoint 4")#,
	#"FoF1 Checkpoint 1" : 						ItemData(BASE_ID + 172, 1, "Progression", "FoF1: Checkpoint 1"),
	#"FoF1 Checkpoint 2" : 						ItemData(BASE_ID + 173, 1, "Progression", "FoF1: Checkpoint 2"),
	#"FoF1 Checkpoint 3" : 						ItemData(BASE_ID + 174, 1, "Progression", "FoF1: Checkpoint 3")#,
	#"FoF2 Checkpoint 1" : 						ItemData(BASE_ID + 175, 1, "Progression", "FoF2: Checkpoint 1"),
	#"FoF2 Checkpoint 2" : 						ItemData(BASE_ID + 176, 1, "Progression", "FoF2: Checkpoint 2"),
	#"FoF2 Checkpoint 3" : 						ItemData(BASE_ID + 177, 1, "Progression", "FoF2: Checkpoint 3")#,
	#"FoF3 Checkpoint 1" : 						ItemData(BASE_ID + 178, 1, "Progression", "FoF3: Checkpoint 1"),
	#"FoF3 Checkpoint 2" : 						ItemData(BASE_ID + 179, 1, "Progression", "FoF3: Checkpoint 2"),
	#"FoF3 Checkpoint 3" : 						ItemData(BASE_ID + 180, 1, "Progression", "FoF3: Checkpoint 3"),
	#"FoF3 Checkpoint 4" : 						ItemData(BASE_ID + 181, 1, "Progression", "FoF3: Checkpoint 4"),
	#"FoF3 Checkpoint 5" : 						ItemData(BASE_ID + 182, 1, "Progression", "FoF3: Checkpoint 5")#,
	#"Otw1 Checkpoint 1" : 						ItemData(BASE_ID + 183, 1, "Progression", "Otw1: Checkpoint 1"),
	#"Otw1 Checkpoint 2" : 						ItemData(BASE_ID + 184, 1, "Progression", "Otw1: Checkpoint 2")#,
	#"Otw2 Checkpoint 1" : 						ItemData(BASE_ID + 185, 1, "Progression", "Otw2: Checkpoint 1")#,
	#"Otw3 Checkpoint 1" : 						ItemData(BASE_ID + 186, 1, "Progression", "Otw3: Checkpoint 1"),
	#"Otw3 Checkpoint 2" : 						ItemData(BASE_ID + 187, 1, "Progression", "Otw3: Checkpoint 2"),
	#"Otw3 Checkpoint 3" : 						ItemData(BASE_ID + 188, 1, "Progression", "Otw3: Checkpoint 3"),
	#"Otw3 Checkpoint 4" : 						ItemData(BASE_ID + 189, 1, "Progression", "Otw3: Checkpoint 4")
	}

world_garib_table = {
	"Atl1 1 Garib" : 							ItemData(BASE_ID + 30101, 1, "Garib", None),
	"Atl1 2 Garibs" : 							ItemData(BASE_ID + 30102, 3, "Garib", None),
	"Atl1 3 Garibs" : 							ItemData(BASE_ID + 30103, 1, "Garib", None),
	"Atl1 4 Garibs" : 							ItemData(BASE_ID + 30104, 5, "Garib", None),
	"Atl1 5 Garibs" : 							ItemData(BASE_ID + 30105, 1, "Garib", None),
	"Atl1 6 Garibs" : 							ItemData(BASE_ID + 30106, 1, "Garib", None),
	"Atl1 9 Garibs" : 							ItemData(BASE_ID + 30109, 1, "Garib", None),
	"Atl2 1 Garib" : 							ItemData(BASE_ID + 30201, 1, "Garib", None),
	"Atl2 2 Garibs" : 							ItemData(BASE_ID + 30202, 2, "Garib", None),
	"Atl2 3 Garibs" : 							ItemData(BASE_ID + 30203, 3, "Garib", None),
	"Atl2 4 Garibs" : 							ItemData(BASE_ID + 30204, 1, "Garib", None),
	"Atl2 5 Garibs" : 							ItemData(BASE_ID + 30205, 5, "Garib", None),
	"Atl2 7 Garibs" : 							ItemData(BASE_ID + 30207, 1, "Garib", None),
	"Atl2 10 Garibs" : 							ItemData(BASE_ID + 30210, 1, "Garib", None),
	"Atl3 1 Garib" : 							ItemData(BASE_ID + 30301, 2, "Garib", None),
	"Atl3 2 Garibs" : 							ItemData(BASE_ID + 30302, 1, "Garib", None),
	"Atl3 3 Garibs" : 							ItemData(BASE_ID + 30303, 2, "Garib", None),
	"Atl3 4 Garibs" : 							ItemData(BASE_ID + 30304, 4, "Garib", None),
	"Atl3 5 Garibs" : 							ItemData(BASE_ID + 30305, 3, "Garib", None),
	"Atl3 6 Garibs" : 							ItemData(BASE_ID + 30306, 1, "Garib", None),
	"Atl3 8 Garibs" : 							ItemData(BASE_ID + 30308, 3, "Garib", None),
	"Atl3 9 Garibs" : 							ItemData(BASE_ID + 30309, 1, "Garib", None),
	"Atl? 5 Garibs" : 							ItemData(BASE_ID + 30505, 5, "Garib", None),
	"Crn1 1 Garib" : 							ItemData(BASE_ID + 31101, 1, "Garib", None),
	"Crn1 4 Garibs" : 							ItemData(BASE_ID + 31104, 3, "Garib", None),
	"Crn1 7 Garibs" : 							ItemData(BASE_ID + 31107, 1, "Garib", None),
	"Crn1 8 Garibs" : 							ItemData(BASE_ID + 31108, 3, "Garib", None),
	"Crn1 10 Garibs" : 							ItemData(BASE_ID + 31110, 1, "Garib", None),
	"Crn1 11 Garibs" : 							ItemData(BASE_ID + 31111, 1, "Garib", None),
	"Crn2 1 Garib" : 							ItemData(BASE_ID + 31201, 3, "Garib", None),
	"Crn2 2 Garibs" : 							ItemData(BASE_ID + 31202, 1, "Garib", None),
	"Crn2 3 Garibs" : 							ItemData(BASE_ID + 31203, 1, "Garib", None),
	"Crn2 4 Garibs" : 							ItemData(BASE_ID + 31204, 4, "Garib", None),
	"Crn2 6 Garibs" : 							ItemData(BASE_ID + 31206, 3, "Garib", None),
	"Crn2 8 Garibs" : 							ItemData(BASE_ID + 31208, 2, "Garib", None),
	"Crn2 10 Garibs" : 							ItemData(BASE_ID + 31210, 1, "Garib", None),
	"Crn2 12 Garibs" : 							ItemData(BASE_ID + 31212, 1, "Garib", None),
	"Crn3 1 Garib" : 							ItemData(BASE_ID + 31301, 1, "Garib", None),
	"Crn3 2 Garibs" : 							ItemData(BASE_ID + 31302, 1, "Garib", None),
	"Crn3 3 Garibs" : 							ItemData(BASE_ID + 31303, 6, "Garib", None),
	"Crn3 4 Garibs" : 							ItemData(BASE_ID + 31304, 6, "Garib", None),
	"Crn3 6 Garibs" : 							ItemData(BASE_ID + 31306, 1, "Garib", None),
	"Crn3 8 Garibs" : 							ItemData(BASE_ID + 31308, 1, "Garib", None),
	"Crn3 9 Garibs" : 							ItemData(BASE_ID + 31309, 1, "Garib", None),
	"Crn3 12 Garibs" : 							ItemData(BASE_ID + 31312, 1, "Garib", None),
	"Crn? 8 Garibs" : 							ItemData(BASE_ID + 31508, 1, "Garib", None),
	"Crn? 12 Garibs" : 							ItemData(BASE_ID + 31512, 1, "Garib", None),
	"Prt1 1 Garib" : 							ItemData(BASE_ID + 32101, 4, "Garib", None),
	"Prt1 4 Garibs" : 							ItemData(BASE_ID + 32104, 7, "Garib", None),
	"Prt1 5 Garibs" : 							ItemData(BASE_ID + 32105, 1, "Garib", None),
	"Prt1 6 Garibs" : 							ItemData(BASE_ID + 32106, 3, "Garib", None),
	"Prt1 7 Garibs" : 							ItemData(BASE_ID + 32107, 1, "Garib", None),
	"Prt1 8 Garibs" : 							ItemData(BASE_ID + 32108, 1, "Garib", None),
	"Prt2 1 Garib" : 							ItemData(BASE_ID + 32201, 6, "Garib", None),
	"Prt2 2 Garibs" : 							ItemData(BASE_ID + 32202, 1, "Garib", None),
	"Prt2 3 Garibs" : 							ItemData(BASE_ID + 32203, 1, "Garib", None),
	"Prt2 4 Garibs" : 							ItemData(BASE_ID + 32204, 5, "Garib", None),
	"Prt2 8 Garibs" : 							ItemData(BASE_ID + 32208, 1, "Garib", None),
	"Prt2 9 Garibs" : 							ItemData(BASE_ID + 32209, 1, "Garib", None),
	"Prt2 12 Garibs" : 							ItemData(BASE_ID + 32212, 1, "Garib", None),
	"Prt3 1 Garib" : 							ItemData(BASE_ID + 32301, 3, "Garib", None),
	"Prt3 2 Garibs" : 							ItemData(BASE_ID + 32302, 5, "Garib", None),
	"Prt3 3 Garibs" : 							ItemData(BASE_ID + 32303, 3, "Garib", None),
	"Prt3 4 Garibs" : 							ItemData(BASE_ID + 32304, 7, "Garib", None),
	"Prt3 6 Garibs" : 							ItemData(BASE_ID + 32306, 1, "Garib", None),
	"Prt3 8 Garibs" : 							ItemData(BASE_ID + 32308, 1, "Garib", None),
	"Prt3 16 Garibs" : 							ItemData(BASE_ID + 32316, 1, "Garib", None),
	"Prt? 3 Garibs" : 							ItemData(BASE_ID + 32503, 15, "Garib", None),
	"Prt? 5 Garibs" : 							ItemData(BASE_ID + 32505, 1, "Garib", None),
	"Pht1 1 Garib" : 							ItemData(BASE_ID + 33101, 1, "Garib", None),
	"Pht1 2 Garibs" : 							ItemData(BASE_ID + 33102, 5, "Garib", None),
	"Pht1 3 Garibs" : 							ItemData(BASE_ID + 33103, 6, "Garib", None),
	"Pht1 4 Garibs" : 							ItemData(BASE_ID + 33104, 1, "Garib", None),
	"Pht1 5 Garibs" : 							ItemData(BASE_ID + 33105, 1, "Garib", None),
	"Pht1 6 Garibs" : 							ItemData(BASE_ID + 33106, 1, "Garib", None),
	"Pht1 8 Garibs" : 							ItemData(BASE_ID + 33108, 3, "Garib", None),
	"Pht1 12 Garibs" : 							ItemData(BASE_ID + 33112, 1, "Garib", None),
	"Pht2 1 Garib" : 							ItemData(BASE_ID + 33201, 6, "Garib", None),
	"Pht2 2 Garibs" : 							ItemData(BASE_ID + 33202, 1, "Garib", None),
	"Pht2 3 Garibs" : 							ItemData(BASE_ID + 33203, 3, "Garib", None),
	"Pht2 4 Garibs" : 							ItemData(BASE_ID + 33204, 6, "Garib", None),
	"Pht2 5 Garibs" : 							ItemData(BASE_ID + 33205, 4, "Garib", None),
	"Pht2 8 Garibs" : 							ItemData(BASE_ID + 33208, 1, "Garib", None),
	"Pht2 11 Garibs" : 							ItemData(BASE_ID + 33211, 1, "Garib", None),
	"Pht3 1 Garib" : 							ItemData(BASE_ID + 33301, 1, "Garib", None),
	"Pht3 2 Garibs" : 							ItemData(BASE_ID + 33302, 2, "Garib", None),
	"Pht3 3 Garibs" : 							ItemData(BASE_ID + 33303, 2, "Garib", None),
	"Pht3 5 Garibs" : 							ItemData(BASE_ID + 33305, 1, "Garib", None),
	"Pht3 7 Garibs" : 							ItemData(BASE_ID + 33307, 1, "Garib", None),
	"Pht3 8 Garibs" : 							ItemData(BASE_ID + 33308, 2, "Garib", None),
	"Pht3 10 Garibs" : 							ItemData(BASE_ID + 33310, 1, "Garib", None),
	"Pht3 15 Garibs" : 							ItemData(BASE_ID + 33315, 1, "Garib", None),
	"Pht3 16 Garibs" : 							ItemData(BASE_ID + 33316, 1, "Garib", None),
	"Pht? 10 Garibs" : 							ItemData(BASE_ID + 33510, 6, "Garib", None)#,
	#"FoF1 1 Garib" : 							ItemData(BASE_ID + 34101, 4, "Garib", None),
	#"FoF1 2 Garibs" : 							ItemData(BASE_ID + 34102, 1, "Garib", None),
	#"FoF1 3 Garibs" : 							ItemData(BASE_ID + 34103, 4, "Garib", None),
	#"FoF1 4 Garibs" : 							ItemData(BASE_ID + 34104, 3, "Garib", None),
	#"FoF1 5 Garibs" : 							ItemData(BASE_ID + 34105, 2, "Garib", None),
	#"FoF1 6 Garibs" : 							ItemData(BASE_ID + 34106, 2, "Garib", None),
	#"FoF1 8 Garibs" : 							ItemData(BASE_ID + 34108, 1, "Garib", None)#,
	#"FoF2 1 Garib" : 							ItemData(BASE_ID + 34201, 1, "Garib", None),
	#"FoF2 2 Garibs" : 							ItemData(BASE_ID + 34202, 1, "Garib", None),
	#"FoF2 3 Garibs" : 							ItemData(BASE_ID + 34203, 3, "Garib", None),
	#"FoF2 5 Garibs" : 							ItemData(BASE_ID + 34205, 5, "Garib", None),
	#"FoF2 6 Garibs" : 							ItemData(BASE_ID + 34206, 1, "Garib", None),
	#"FoF2 7 Garibs" : 							ItemData(BASE_ID + 34207, 1, "Garib", None),
	#"FoF2 10 Garibs" : 						ItemData(BASE_ID + 34210, 1, "Garib", None)#,
	#"FoF3 1 Garib" : 							ItemData(BASE_ID + 34301, 1, "Garib", None),
	#"FoF3 2 Garibs" : 							ItemData(BASE_ID + 34302, 4, "Garib", None),
	#"FoF3 3 Garibs" : 							ItemData(BASE_ID + 34303, 4, "Garib", None),
	#"FoF3 4 Garibs" : 							ItemData(BASE_ID + 34304, 3, "Garib", None),
	#"FoF3 5 Garibs" : 							ItemData(BASE_ID + 34305, 1, "Garib", None),
	#"FoF3 6 Garibs" : 							ItemData(BASE_ID + 34306, 1, "Garib", None),
	#"FoF3 8 Garibs" : 							ItemData(BASE_ID + 34308, 2, "Garib", None),
	#"FoF3 10 Garibs" : 						ItemData(BASE_ID + 34310, 1, "Garib", None),
	#"FoF? 4 Garibs" : 							ItemData(BASE_ID + 34504, 2, "Garib", None),
	#"FoF? 5 Garibs" : 							ItemData(BASE_ID + 34505, 4, "Garib", None),
	#"FoF? 7 Garibs" : 							ItemData(BASE_ID + 34507, 4, "Garib", None)#,
	#"Otw1 1 Garib" : 							ItemData(BASE_ID + 35101, 6, "Garib", None),
	#"Otw1 2 Garibs" : 							ItemData(BASE_ID + 35102, 1, "Garib", None),
	#"Otw1 3 Garibs" : 							ItemData(BASE_ID + 35103, 4, "Garib", None),
	#"Otw1 4 Garibs" : 							ItemData(BASE_ID + 35104, 1, "Garib", None),
	#"Otw1 10 Garibs" : 						ItemData(BASE_ID + 35110, 1, "Garib", None),
	#"Otw1 16 Garibs" : 						ItemData(BASE_ID + 35116, 1, "Garib", None)#,
	#"Otw2 2 Garibs" : 							ItemData(BASE_ID + 35202, 2, "Garib", None),
	#"Otw2 3 Garibs" : 							ItemData(BASE_ID + 35203, 2, "Garib", None),
	#"Otw2 4 Garibs" : 							ItemData(BASE_ID + 35204, 3, "Garib", None),
	#"Otw2 5 Garibs" : 							ItemData(BASE_ID + 35205, 2, "Garib", None),
	#"Otw2 6 Garibs" : 							ItemData(BASE_ID + 35206, 1, "Garib", None),
	#"Otw2 12 Garibs" : 						ItemData(BASE_ID + 35212, 1, "Garib", None)#,
	#"Otw3 3 Garibs" : 							ItemData(BASE_ID + 35303, 1, "Garib", None),
	#"Otw3 4 Garibs" : 							ItemData(BASE_ID + 35304, 3, "Garib", None),
	#"Otw3 5 Garibs" : 							ItemData(BASE_ID + 35305, 2, "Garib", None),
	#"Otw3 6 Garibs" : 							ItemData(BASE_ID + 35306, 2, "Garib", None),
	#"Otw3 7 Garibs" : 							ItemData(BASE_ID + 35307, 2, "Garib", None),
	#"Otw3 8 Garibs" : 							ItemData(BASE_ID + 35308, 1, "Garib", None),
	#"Otw3 9 Garibs" : 							ItemData(BASE_ID + 35309, 1, "Garib", None),
	#"Otw3 12 Garibs" : 						ItemData(BASE_ID + 35312, 1, "Garib", None)#,
	#"Otw? 6 Garibs" : 							ItemData(BASE_ID + 35506, 3, "Garib", None),
	#"Otw? 8 Garibs" : 							ItemData(BASE_ID + 35508, 4, "Garib", None)#
	}

def construct_blank_world_garibs(world_prefixes : list[str], level_prefixes : list[str]):
	output_table : dict[str, ItemData] = {}
	levels_with_garibs = []

	#World/Level prefix constructor
	for world_prefix in world_prefixes:
		for level_prefix in level_prefixes:
			if level_prefix != "H" and level_prefix != "!":
				levels_with_garibs.append(world_prefix + level_prefix)

	#Go over all the garibs
	for garib_level in levels_with_garibs:
		for garib_count in range(1, 17):
			#Get the text prefix for all garib counts
			garib_suffix : str = " 1 Garib"
			if garib_count > 1:
				garib_suffix : str = " " + str(garib_count) + " Garibs"
			#If a level doesn't have that count of garibs
			if not (garib_level + garib_suffix in world_garib_table.keys()):
				world_offset = 1000 * world_prefixes.index(garib_level[:3])
				level_offset = 100 * level_prefixes.index(garib_level[3:4])
				item_id = BASE_ID + 30000 + world_offset + level_offset + garib_count
				output_table[garib_level + garib_suffix] = ItemData(item_id, 0, "Filler", None)
	return output_table

ability_table = {
	"Jump" : 									ItemData(BASE_ID + 329, 1, "Progression", None),
	"Cartwheel" : 								ItemData(BASE_ID + 330, 1, "Progression", None),
	"Crawl" : 									ItemData(BASE_ID + 331, 1, "Useful", None),
	"Double Jump" : 							ItemData(BASE_ID + 332, 1, "Progression", None),
	"Fist Slam" : 								ItemData(BASE_ID + 333, 1, "Progression", None),
	"Ledge Grab" : 								ItemData(BASE_ID + 334, 1, "Progression", None),
	"Push" : 									ItemData(BASE_ID + 335, 1, "Progression", None),
	"Locate Garibs" : 							ItemData(BASE_ID + 336, 1, "Useful", None),
	"Locate Ball" : 							ItemData(BASE_ID + 337, 1, "Progression", None),
	"Dribble" : 								ItemData(BASE_ID + 338, 1, "Progression", None),
	"Quick Swap" : 								ItemData(BASE_ID + 339, 1, "Progression", None),
	"Slap" : 									ItemData(BASE_ID + 340, 1, "Progression", None),
	"Throw" : 									ItemData(BASE_ID + 341, 1, "Progression", None),
	"Ball Toss" : 								ItemData(BASE_ID + 342, 1, "Progression", None),
#	"Beachball Potion" : 						ItemData(BASE_ID + 343, 1, "Progression", None),
	"Death Potion" : 							ItemData(BASE_ID + 344, 1, "Progression", None),
	"Helicopter Potion" : 						ItemData(BASE_ID + 345, 1, "Progression", None),
	"Frog Potion" : 							ItemData(BASE_ID + 346, 1, "Progression", None),
	"Boomerang Ball Potion" : 					ItemData(BASE_ID + 347, 1, "Progression", None),
	"Speed Potion" : 							ItemData(BASE_ID + 348, 1, "Progression", None),
	"Sticky Potion" : 							ItemData(BASE_ID + 349, 1, "Progression", None),
	"Hercules Potion" : 						ItemData(BASE_ID + 350, 1, "Progression", None),
	"Grab" : 									ItemData(BASE_ID + 351, 1, "Progression", None),
	"Rubber Ball" : 							ItemData(BASE_ID + 352, 1, "Progression", None),
	"Bowling Ball" : 							ItemData(BASE_ID + 353, 1, "Progression", None),
	"Ball Bearing" : 							ItemData(BASE_ID + 354, 1, "Progression", None),
	"Crystal" : 								ItemData(BASE_ID + 355, 1, "Progression", None),
	"Power Ball" : 								ItemData(BASE_ID + 356, 1, "Progression", None)
	}

filler_table = {
	"Extra Garibs" : 							ItemData(BASE_ID + 357, -1, "Useful", None),
	"Chicken Sound" : 							ItemData(BASE_ID + 358, -1, "Filler", None),
	"Life" : 									ItemData(BASE_ID + 359, -1, "Filler", None),
	"Boomerang Spell" : 						ItemData(BASE_ID + 360, -1, "Filler", None),
	"Beachball Spell" : 						ItemData(BASE_ID + 361, -1, "Filler", None),
	"Hercules Spell" : 							ItemData(BASE_ID + 362, -1, "Filler", None),
	"Helicopter Spell" : 						ItemData(BASE_ID + 363, -1, "Filler", None),
	"Speed Spell" : 							ItemData(BASE_ID + 364, -1, "Filler", None),
	"Frog Spell" : 								ItemData(BASE_ID + 365, -1, "Filler", None),
	"Death Spell" : 							ItemData(BASE_ID + 366, -1, "Filler", None),
	"Sticky Spell" : 							ItemData(BASE_ID + 367, -1, "Filler", None)
	}

trap_table = {
	"Frog Trap" : 								ItemData(BASE_ID + 368, -1, "Trap", None),
	"Cursed Ball Trap" :						ItemData(BASE_ID + 369, -1, "Trap", None),
	"Instant Crystal Trap" :					ItemData(BASE_ID + 370, -1, "Trap", None),
	"Camera Rotate Trap" :						ItemData(BASE_ID + 371, -1, "Trap", None),
	"Tip Trap" :								ItemData(BASE_ID + 372, -1, "Trap", None)
	}

garibsanity_world_table = {
	"Atl1 Garib" : 								ItemData(BASE_ID + 20001, 50, "Garib", None),
	"Atl2 Garib" : 								ItemData(BASE_ID + 20002, 60, "Garib", None),
	"Atl3 Garib" : 								ItemData(BASE_ID + 20003, 80, "Garib", None),
	"Atl? Garib" :	 							ItemData(BASE_ID + 20005, 25, "Garib", None),
	"Crn1 Garib" : 								ItemData(BASE_ID + 20011, 65, "Garib", None),
	"Crn2 Garib" : 								ItemData(BASE_ID + 20012, 80, "Garib", None),
	"Crn3 Garib" : 								ItemData(BASE_ID + 20013, 80, "Garib", None),
	"Crn? Garib" : 								ItemData(BASE_ID + 20015, 20, "Garib", None),
	"Prt1 Garib" : 								ItemData(BASE_ID + 20021, 70, "Garib", None),
	"Prt2 Garib" : 								ItemData(BASE_ID + 20022, 60, "Garib", None),
	"Prt3 Garib" : 								ItemData(BASE_ID + 20023, 80, "Garib", None),
	"Prt? Garib" : 								ItemData(BASE_ID + 20025, 50, "Garib", None),
	"Pht1 Garib" : 								ItemData(BASE_ID + 20031, 80, "Garib", None),
	"Pht2 Garib" : 								ItemData(BASE_ID + 20032, 80, "Garib", None),
	"Pht3 Garib" : 								ItemData(BASE_ID + 20033, 80, "Garib", None),
	"Pht? Garib" : 								ItemData(BASE_ID + 20035, 60, "Garib", None)#,
	#"FoF1 Garib" : 								ItemData(BASE_ID + 20041, 60, "Garib", None)#,
	#"FoF2 Garib" : 								ItemData(BASE_ID + 20042, 60, "Garib", None)#,
	#"FoF3 Garib" : 								ItemData(BASE_ID + 20043, 70, "Garib", None)#,
	#"FoF? Garib" : 								ItemData(BASE_ID + 20045, 56, "Garib", None)#,
	#"Otw1 Garib" : 								ItemData(BASE_ID + 20051, 50, "Garib", None)#,
	#"Otw2 Garib" : 								ItemData(BASE_ID + 20052, 50, "Garib", None)#,
	#"Otw3 Garib" : 								ItemData(BASE_ID + 20053, 80, "Garib", None)#,
	#"Otw? Garib" : 								ItemData(BASE_ID + 20055, 50, "Garib", None)
	}

#decoupled_garib_table = {
#	"Garib" : 									ItemData(BASE_ID + 10001, 42, "Garib", None),
#	"2 Garibs" : 								ItemData(BASE_ID + 10002, 31, "Garib", None),
#	"3 Garibs" : 								ItemData(BASE_ID + 10003, 61, "Garib", None),
#	"4 Garibs" : 								ItemData(BASE_ID + 10004, 62, "Garib", None),
#	"5 Garibs" : 								ItemData(BASE_ID + 10005, 34, "Garib", None),
#	"6 Garibs" : 								ItemData(BASE_ID + 10006, 21, "Garib", None),
#	"7 Garibs" : 								ItemData(BASE_ID + 10007, 7, "Garib", None),
#	"8 Garibs" : 								ItemData(BASE_ID + 10008, 27, "Garib", None),
#	"9 Garibs" : 								ItemData(BASE_ID + 10009, 5, "Garib", None),
#	"10 Garibs" : 								ItemData(BASE_ID + 10010, 13, "Garib", None),
#	"11 Garibs" : 								ItemData(BASE_ID + 10011, 2, "Garib", None),
#	"12 Garibs" : 								ItemData(BASE_ID + 10012, 7, "Garib", None),
#	"13 Garibs" : 								ItemData(BASE_ID + 10013, 0, "Garib", None),
#	"14 Garibs" : 								ItemData(BASE_ID + 10014, 4, "Garib", None),
#	"15 Garibs" : 								ItemData(BASE_ID + 10015, 1, "Garib", None),
#	"16 Garibs" : 								ItemData(BASE_ID + 10016, 3, "Garib", None),
#}
#
#garbinsanity = ItemData(BASE_ID + 10001, 1496, "Garib", None)

decoupled_garib_table = {
	"1 Garib" : 								ItemData(BASE_ID + 10001, 30, "Garib", None),
	"2 Garibs" : 								ItemData(BASE_ID + 10002, 22, "Garib", None),
	"3 Garibs" : 								ItemData(BASE_ID + 10003, 43, "Garib", None),
	"4 Garibs" : 								ItemData(BASE_ID + 10004, 49, "Garib", None),
	"5 Garibs" : 								ItemData(BASE_ID + 10005, 22, "Garib", None),
	"6 Garibs" : 								ItemData(BASE_ID + 10006, 11, "Garib", None),
	"7 Garibs" : 								ItemData(BASE_ID + 10007, 4, "Garib", None),
	"8 Garibs" : 								ItemData(BASE_ID + 10008, 19, "Garib", None),
	"9 Garibs" : 								ItemData(BASE_ID + 10009, 4, "Garib", None),
	"10 Garibs" : 								ItemData(BASE_ID + 10010, 10, "Garib", None),
	"11 Garibs" : 								ItemData(BASE_ID + 10011, 2, "Garib", None),
	"12 Garibs" : 								ItemData(BASE_ID + 10012, 5, "Garib", None),
	"15 Garibs" : 								ItemData(BASE_ID + 10015, 1, "Garib", None),
	"16 Garibs" : 								ItemData(BASE_ID + 10012, 2, "Garib", None)
} 

garbinsanity = ItemData(BASE_ID + 10001, 1020, "Garib", None)

decoupled_garib_bonus_count = {
	"3 Garibs" : 		15,
	"5 Garibs" : 		6,
	"8 Garibs" :		1,
	"10 Garibs" :		6,
	"12 Garibs" :		1#,
}

garbinsanity_bonus_count = 155


all_items = {
	**portalsanity_table,
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

def generate_item_name_to_id(world_prefixes : list[str], level_prefixes : list[str]) -> dict:
	output : dict = {}
	all_items.update(construct_blank_world_garibs(world_prefixes, level_prefixes))
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

def select_trap_item_name(self, original_name : str) -> str:
	#Just give the actual item name
	if self.random.randint(0, 99) == 0:
		return original_name
	fake_name = self.random.choice(self.fake_item_names)
	#Word 'Garib' corruption
	if fake_name.count("Garib") > 0:
		#50/50 the name corrupts
		match self.random.randint(0, 11):
			case 0:
				fake_name.replace("Garib", "Garid")
			case 1:
				fake_name.replace("Garib", "Gerib")
			case 2:
				fake_name.replace("Garib", "Ganib")
			case 3:
				fake_name.replace("Garib", "Garip")
			case 4:
				fake_name.replace("Garib", "Carib")
			case 5:
				fake_name.replace("Garib", "Garlb")
	
	#Level prefix corruption
	if fake_name.startswith(tuple(self.world_prefixes)):
		#1 in every 20 of these has funny prefixes
		if self.random.randint(1, 20) == 20:
			level_swaps = [
			#Plumber
				"BoB",
			#The Blue Ninja
				"TBN",
			#Hill Zone
				"GHZ",
			#Glitter Gulch
				"GGM",
			#Burgered
				"BKd",
			#Wrong prefix
				"Alt",
				"Crm",
				"Prc",
				"Phc",
				"F0F",
				"Otm",
				]
			fake_name = self.random.choice(level_swaps) + fake_name[3:]
	return fake_name

def create_trap_name_table(self) -> list[str]:
	trap_name_table = [
		#Fake balls
		"Basketball",
		"Snow Ball",
		"Tennis Ball",
		"Disco Ball",
		"Monkey Ball",
		"Golf Ball",
		"Dodgeball",
		"Soccer Ball",
		"Pebball",
		"Football",
		"Hockey Puck",
		"Master Ball",
		#Fake glover moves
		"Triple Jump",
		"Backflip",
		#Fake Tools
		"Golf Club",
		"Tennis Racket",
		"Curling Broom",
		"Shovel",
		"Lawnmower",
		"Bus",
		"Magic Wand",
		#Fake ball moves
		"Spin Ball",
		"Flick Ball",
		"Juggle",
		#Funny
		"Cross-Stitch",
		"Free Wizard",
		"Permission to Cheat",
		"Running Boots",
		"Trap (WOULD Be Funny)",
		#Fake potions
		"Awkward Potion",
		"Strength Potion",
		"Toad Potion",
		"Invisibility Potion",
		"Cauldron Potion",
		"Mana Potion",
		"Health Potion",
		"Potion Bottle",
		"Boornerang Ball Potion",
		#Lotions
		"Beachball Lotion",
		"Death Lotion",
		"Helicopter Lotion",
		"Frog Lotion",
		"Boomerang Ball Lotion",
		"Speed Lotion",
		"Sticky Lotion",
		"Hercules Lotion",
		#Fake Filler
		"Line",
		"Lice",
		"Lime",
		"Live",
		"Like",
		"Chicken Song",
		#Things you already have
		"Garib Counter",
		"Lives Display",
		"Roll Ball",
		"Drop Ball",
		"Ledge Sit",
		"Transform Ball",
		#Not Traps
		"Not a Frog Trap",
		"Not a Cursed Ball Trap",
		"Not an Instant Crystal Trap",
		"Not a Camera Rotate Trap",
		"Not a Tip Trap"
	]
	
	#Fake portal entries
	if self.options.portalsanity:
		for each_prefix in self.level_prefixes:
			trap_name_table.append(each_prefix + "H Exit Gate")
			trap_name_table.append(each_prefix + "H 1 Gate")
			trap_name_table.append(each_prefix + "H 4 Gate")
			trap_name_table.append(each_prefix + "H 2 Stars")
			trap_name_table.append(each_prefix + "H Secret Star")
			trap_name_table.append(each_prefix + "H Secret Gate")
		trap_name_table.extend([
			"Hubworld Tree Gate",
			"Hubworld Castle Cave Gate",
			"OtwH Final Boss Gate"
		])
	
	#Fake level events
	if self.options.switches_checks:
		trap_name_table.extend([
			"Atl1 Raise Water",
			"Atl2 Free Mermaid",
			"Atl3 Yellow Submarine",
			"Crn1 Fireworks",
			"Crn2 Baseball Minigame",
			"Crn3 Ferris Wheel",
			"Prt1 Dirt Jar",
			"Prt2 Sink Ship",
			"Prt3 Release Kraken",
			"Pht1 Melt Ice",
			"Pht2 Erupt Volcano",
			"Pht3 Dino Wedding",
			"FoF1 Mr Bones",
			"FoF2 Green Door",
			"FoF3 Drawbridge",
			"Otw1 Ancienter Aliens",
			"Otw2 Bomb",
			"Otw3 Second Magnet",
			"Training Wheel"
		])
	else:
		trap_name_table.extend(level_event_table.keys())

	#Fake Checkpoints
	if not self.options.checkpoint_checks:
		trap_name_table.extend(checkpoint_table.keys())
	elif not self.options.spawning_checkpoint_randomizer:
		for each_prefix in self.level_prefixes:
			trap_name_table.extend([
				each_prefix + "1 Checkpoint 1",
				each_prefix + "2 Checkpoint 1",
				each_prefix + "3 Checkpoint 1"
			])
	
	#Fake Garibs
	match self.options.garib_logic:
		#Garibs shouldn't be items at all, add ALL of them
		case GaribLogic.option_level_garibs:
			trap_name_table.extend(garibsanity_world_table.keys())
			trap_name_table.extend(world_garib_table.keys())
			trap_name_table.extend(decoupled_garib_table.keys())
		#Groups can show up, exclude those
		case GaribLogic.option_garib_groups:
			if self.options.garib_sorting != GaribSorting.option_by_level:
				#Anything but the world garib table
				trap_name_table.extend(garibsanity_world_table.keys())
				trap_name_table.extend(decoupled_garib_table.keys())
			else:
				#Anything but decoupled garibs
				trap_name_table.extend(garibsanity_world_table.keys())
				trap_name_table.extend(world_garib_table.keys())
		#Garibsanity exists, exclude singles
		case GaribLogic.option_garibsanity:
			if self.options.garib_sorting != GaribSorting.option_by_level:
				#Anything but the garibsanity world table
				trap_name_table.extend(decoupled_garib_table.keys())
				trap_name_table.extend(world_garib_table.keys())
			else:
				#Anything but a single decoupled garib
				trap_name_table.extend(garibsanity_world_table.keys())
				trap_name_table.extend(world_garib_table.keys())
				trap_name_table.extend(decoupled_garib_table.keys())
	#'Jump'
	if not self.options.randomize_jump:
		trap_name_table.append("Jump")
	else:
		trap_name_table.append("Lump")
	
	#Misnamed Balls
	not_spawning_balls = [
		"Rubber Ball",
		"Bowling Ball",
		"Ball Bearing",
		"Crystal",
		"Power Ball"]
	#Remove the default ball from the list of misnamed balls
	not_spawning_balls.remove(self.starting_ball)
	#Make it an item you can find though, spelled correctly
	trap_name_table.append(self.starting_ball)
	for other_balls in not_spawning_balls:
		trap_name_table.append(other_balls)
		#Ball Mispellings
		if other_balls.count("Ball") > 0:
			trap_name_table.append(other_balls.replace("Ball", "Bell"))
			trap_name_table.append(other_balls.replace("Ball", "Bill"))
			trap_name_table.append(other_balls.replace("Ball", "Bull"))
			trap_name_table.append(other_balls.replace("Ball", "").removeprefix(" ").removesuffix(" "))
		#Other Mispellings
		match other_balls:
			case "Rubber Ball":
				trap_name_table.extend([
					"Robber Ball",
					"Rudder Ball"
					])
			case "Bowling Ball":
				trap_name_table.extend([
					"Bowling Pin",
					"Bowing Ball"
					])
			case "Ball Bearing":
				trap_name_table.extend([
					"Ball Baering",
					"Ball Pearing"
					])
			case "Crystal":
				trap_name_table.extend([
					"Crystal Ball",
					"Christal",
					"Krystal",
					"Crystall",
					"Cryztal",
					"Crstal",
					])
			case "Power Ball":
				trap_name_table.extend([
					"Powder Ball",
					"Powerball"
				])
	return trap_name_table

def convert_extra_garibs(self) -> ItemData:
	#Level garibs shouldn't show up
	if self.options.garib_logic == GaribLogic.option_level_garibs:
		raise ValueError("Extra garibs cannot show up while garib logic is by level! Set your Filler Extra Garibs to 0.")
	#Get the garib count
	extra_garibs_value : int = self.options.extra_garibs_value.value
	if self.options.garib_sorting != GaribSorting.option_by_level:
		#"Garibs" or "Garib"?
		garib_name = " Garibs"
		if extra_garibs_value == 1:
			garib_name = " Garib"
		#Index to name
		return decoupled_garib_table[str(extra_garibs_value) + garib_name]
	#Level Garib Groups
	else:
		#"Garibs" or "Garib"?
		garib_name = " Garibs"
		if extra_garibs_value == 1:
			garib_name = " Garib"
		#Pick the next valid garib level
		level_name = self.next_garib_level()
		return world_garib_table[level_name + " " + str(extra_garibs_value) + garib_name]