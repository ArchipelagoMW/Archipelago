from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule, forbid_item, add_item_rule

#Basic rules
def rule_cartwheel(self, state : CollectionState) -> bool:
    return state.has("Cartwheel", self.player)
def rule_crawl(self, state : CollectionState) -> bool:
    return state.has("Crawl", self.player)
def rule_double_jump(self, state : CollectionState) -> bool:
    return state.has("Double Jump", self.player)
def rule_fist_slam(self, state : CollectionState) -> bool:
    return state.has("Fist Slam", self.player)
def rule_ledge(self, state : CollectionState) -> bool:
    return state.has("Ledge Grab", self.player)
def rule_push(self, state : CollectionState) -> bool:
    return state.has("Push", self.player)
def rule_locate_garib(self, state : CollectionState) -> bool:
    return state.has("Locate Garibs", self.player)
def rule_locate_ball(self, state : CollectionState) -> bool:
    return state.has("Locate Ball", self.player)
def rule_dribble(self, state : CollectionState) -> bool:
    return state.has("Dribble", self.player)
def rule_quick_swap(self, state : CollectionState) -> bool:
    return state.has("Quick Swap", self.player)
def rule_slap(self, state : CollectionState) -> bool:
    return state.has("Slap", self.player)
def rule_throw(self, state : CollectionState) -> bool:
    return state.has("Throw", self.player)
def rule_lob_ball(self, state : CollectionState) -> bool:
    return state.has("Ball Toss", self.player)
def rule_rubber_ball(self, state : CollectionState) -> bool:
    return state.has("Rubber Ball", self.player)
def rule_bowling_ball(self, state : CollectionState) -> bool:
    return state.has("Bowling Ball", self.player)
def rule_ball_bearing(self, state : CollectionState) -> bool:
    return state.has("Ball Bearing", self.player)
def rule_crystal(self, state : CollectionState) -> bool:
    return state.has("Crystal", self.player)
def rule_beachball(self, state : CollectionState) -> bool:
    return state.has("Beachball", self.player)
def rule_death_potion(self, state : CollectionState) -> bool:
    return state.has("Death Potion", self.player)
def rule_helicopter_potion(self, state : CollectionState) -> bool:
    return state.has("Helicopter Potion", self.player)
def rule_frog_potion(self, state : CollectionState) -> bool:
    return state.has("Frog Potion", self.player)
def rule_boomerang_ball(self, state : CollectionState) -> bool:
    return state.has("Boomerang Ball", self.player)
def rule_speed_potion(self, state : CollectionState) -> bool:
    return state.has("Speed Potion", self.player)
def rule_sticky_potion(self, state : CollectionState) -> bool:
    return state.has("Sticky Potion", self.player)
def rule_hercules_potion(self, state : CollectionState) -> bool:
    return state.has("Hercules Potion", self.player)
def rule_jump(self, state : CollectionState) -> bool:
    return state.has("Jump", self.player)
def rule_grab(self, state : CollectionState) -> bool:
    return state.has("Grab", self.player)
def rule_power_ball(self, state : CollectionState) -> bool:
    return state.has("Power Ball", self.player)

#Special rules
def rule_not_crystal(self, state : CollectionState) -> bool:
    return state.has_group("Not Crystal", self.player)
def rule_not_bowling(self, state : CollectionState) -> bool:
    return state.has_group("Not Bowling", self.player)
def rule_not_bowling_or_crystal(self, state : CollectionState) -> bool:
    return state.has_group("Not Bowling or Crystal", self.player)
def rule_sinks(self, state : CollectionState) -> bool:
    return state.has_group("Sinks", self.player)
def rule_floats(self, state : CollectionState) -> bool:
    return state.has_group("Floats", self.player)
def rule_ball_up(self, state : CollectionState) -> bool:
    return state.has_group("Ball Up", self.player)

#


move_lookup = {
    "Cartwheel" :               rule_cartwheel,
    "Crawl" :                   rule_crawl,
    "Double Jump" :             rule_double_jump,
    "Fist Slam" :               rule_fist_slam,
    "Ledge Grab" :              rule_ledge,
    "Push" :                    rule_push,
    "Locate Garib" :            rule_locate_garib,
    "Locate Ball" :             rule_locate_ball,
    "Dribble" :                 rule_dribble,
    "Quick Swap" :              rule_quick_swap,
    "Slap" :                    rule_slap,
    "Throw" :                   rule_throw,
    "Lob Ball" :                rule_lob_ball,
    "Rubber Ball" :             rule_rubber_ball,
    "Bowling Ball" :            rule_bowling_ball,
    "Ball Bearing" :            rule_ball_bearing,
    "Crystal" :                 rule_crystal,
    "Beachball" :               rule_beachball,
    "Death Potion" :            rule_death_potion,
    "Helicopter Potion" :       rule_helicopter_potion,
    "Frog Potion" :             rule_frog_potion,
    "Boomerang Ball" :          rule_boomerang_ball,
    "Speed Potion" :            rule_speed_potion,
    "Sticky Potion" :           rule_sticky_potion,
    "Hercules Potion" :         rule_hercules_potion,
    "Jump" :                    rule_jump,
    "Not Crystal" :             rule_not_crystal,
    "Not Bowling" :             rule_not_bowling,
    "Sinks" :                   rule_sinks,
    "Floats" :                  rule_floats,
    "Grab" :                    rule_grab,
    "Ball Up" :                 rule_ball_up,
    "Power Ball" :              rule_power_ball,
    "Not Bowling or Crystal" :  rule_not_bowling_or_crystal
}

   #"AtlH 1 Star" : 						
   #"AtlH 2 Gate" : 						
   #"AtlH 2 Star" : 						
   #"AtlH 3 Gate" : 						
   #"AtlH 3 Star" : 						
   #"AtlH Boss Gate" : 						
   #"AtlH Boss Star" : 						
   #"AtlH Bonus Gate" : 					
   #"AtlH Bonus Star" : 					

switches_to_event_items = {
    #"AtlH: " : "AtlH 1 Star",
    #"AtlH: " : "AtlH 2 Gate",
    #"AtlH: " : "AtlH 2 Star",
    #"AtlH: " : "AtlH 3 Gate",
    #"AtlH: " : "AtlH 3 Star",
    #"AtlH: " : "AtlH Boss Gate",
    #"AtlH: " : "AtlH Boss Star",
    #"AtlH: " : "AtlH Bonus Gate",
    #"AtlH: " : "AtlH Bonus Star",
    "Atl1: Glover Switch" : "Atl1 Gate",
    #"Atl2: " : "Atl2 Elevator",
    #"Atl2: " : "Atl2 Ballswitch Drain",
    #"Atl2: " : "Atl2 Gate",
    #"Atl3: " : "Atl3 Waterwheel",
    #"Atl3: " : "Atl3 Cave Platforms",
    #"CrnH: " : "CrnH 1 Star",
    #"CrnH: " : "CrnH 2 Gate",
    #"CrnH: " : "CrnH 2 Star",
    #"CrnH: " : "CrnH 3 Gate",
    #"CrnH: " : "CrnH 3 Star",
    #"CrnH: " : "CrnH Boss Gate",
    #"CrnH: " : "CrnH Boss Star",
    #"CrnH: " : "CrnH Bonus Gate",
    #"CrnH: " : "CrnH Bonus Star",
    #"Crn1: " : "Crn1 Elevator",
    #"Crn1: " : "Crn1 Gate",
    #"Crn1: " : "Crn1 Door A",
    #"Crn1: " : "Crn1 Door B",
    #"Crn1: " : "Crn1 Door C",
    #"Crn1: " : "Crn1 Rocket 1",
    #"Crn1: " : "Crn1 Rocket 2",
    #"Crn1: " : "Crn1 Rocket 3",
    #"Crn2: " : "Crn2 Drop Garibs",
    #"Crn2: " : "Crn2 Fan",
    #"Crn3: " : "Crn3 Spin Door",
    #"Crn3: " : "Crn3 Hands",
    #"PrtH: " : "PrtH 1 Star",
    #"PrtH: " : "PrtH 2 Gate",
    #"PrtH: " : "PrtH 2 Star",
    #"PrtH: " : "PrtH 3 Gate",
    #"PrtH: " : "PrtH 3 Star",
    #"PrtH: " : "PrtH Boss Gate",
    #"PrtH: " : "PrtH Boss Star",
    #"PrtH: " : "PrtH Bonus Gate",
    #"PrtH: " : "PrtH Bonus Star",
    #"Prt1: " : "Prt1 Raise Beach",
    #"Prt1: " : "Prt1 Elevator",
    #"Prt1: " : "Prt1 Chest",
    #"Prt1: " : "Prt1 Sandpile",
    #"Prt1: " : "Prt1 Waterspout",
    #"Prt1: " : "Prt1 Lighthouse",
    #"Prt1: " : "Prt1 Raise Ship",
    #"Prt1: " : "Prt1 Bridge",
    #"Prt2: " : "Prt2 Lower Water",
    #"Prt2: " : "Prt2 Ramp",
    #"Prt2: " : "Prt2 Gate",
    #"Prt3: " : "Prt3 Platform Spin",
    #"Prt3: " : "Prt3 Trampoline",
    #"Prt3: " : "Prt3 Stairs",
    #"Prt3: " : "Prt3 Elevator",
    #"PhtH: " : "PhtH 1 Star",
    #"PhtH: " : "PhtH 2 Gate",
    #"PhtH: " : "PhtH 2 Star",
    #"PhtH: " : "PhtH 3 Gate",
    #"PhtH: " : "PhtH 3 Star",
    #"PhtH: " : "PhtH Boss Gate",
    #"PhtH: " : "PhtH Boss Star",
    #"PhtH: " : "PhtH Bonus Gate",
    #"PhtH: " : "PhtH Bonus Star",
    #"Pht1: " : "Pht1 Life Drop",
    #"Pht2: " : "Pht2 Platform 1",
    #"Pht2: " : "Pht2 Platform 2",
    #"Pht2: " : "Pht2 Lower Ball Switch",
    #"Pht3: " : "Pht3 Drop Garibs",
    #"Pht3: " : "Pht3 Spin Stones",
    #"Pht3: " : "Pht3 Progressive Lower Monolith 1",
    #"Pht3: " : "Pht3 Progressive Lower Monolith 2",
    #"Pht3: " : "Pht3 Progressive Lower Monolith 3",
    #"Pht3: " : "Pht3 Progressive Lower Monolith 4",
    #"Pht3: " : "Pht3 Floating Platforms",
    #"Pht3: " : "Pht3 Lava Spinning",
    #"Pht3: " : "Pht3 Dirt Elevator",
    #"FoFH: " : "FoFH 1 Star",
    #"FoFH: " : "FoFH 2 Gate",
    #"FoFH: " : "FoFH 2 Star",
    #"FoFH: " : "FoFH 3 Gate",
    #"FoFH: " : "FoFH 3 Star",
    #"FoFH: " : "FoFH Boss Gate",
    #"FoFH: " : "FoFH Boss Star",
    #"FoFH: " : "FoFH Bonus Gate",
    #"FoFH: " : "FoFH Bonus Star",
    #"FoF1: " : "FoF1 Coffin",
    #"FoF1: " : "FoF1 Doorway",
    #"FoF1: " : "FoF1 Drawbridge",
    #"FoF2: " : "FoF2 Garibs Fall",
    #"FoF2: " : "FoF2 Checkpoint Gates",
    #"FoF2: " : "FoF2 Mummy Gate",
    #"FoF3: " : "FoF3 Gate",
    #"FoF3: " : "FoF3 Spikes",
    #"OtwH: " : "OtwH 1 Star",
    #"OtwH: " : "OtwH 2 Gate",
    #"OtwH: " : "OtwH 2 Star",
    #"OtwH: " : "OtwH 3 Gate",
    #"OtwH: " : "OtwH 3 Star",
    #"OtwH: " : "OtwH Boss Gate",
    #"OtwH: " : "OtwH Boss Star",
    #"OtwH: " : "OtwH Bonus Gate",
    #"OtwH: " : "OtwH Bonus Star",
    #"Otw1: " : "Otw1 Aliens",
    #"Otw1: " : "Otw1 Fans",
    #"Otw1: " : "Otw1 Flying Platforms",
    #"Otw1: " : "Otw1 Goo Platforms",
    #"Otw1: " : "Otw1 UFO",
    #"Otw1: " : "Otw1 Missile",
    #"Otw2: " : "Otw2 Mashers",
    #"Otw2: " : "Otw2 Ramp",
    #"Otw3: " : "Otw3 Hazard Gate",
    #"Otw3: " : "Otw3 Sign",
    #"Otw3: " : "Otw3 Fan",
    #"Otw3: " : "Otw3 Bridge",
    #"Otw3: " : "Otw3 Glass Gate",
    #"" : "Hubworld Atlantis Gate",
    #"" : "Hubworld Carnival Gate",
    #"" : "Hubworld Pirate's Cove Gate" ,
    #"" : "Hubworld Prehistoric Gate",
    #"" : "Hubworld Fortress of Fear Gate" ,
    #"" : "Hubworld Out of This World Gate",
    #"" : "Training Sandpit",
    #"" : "Training Lower Target",
    #"" : "Training Stairs"
}