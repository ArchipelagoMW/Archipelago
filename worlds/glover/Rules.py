from BaseClasses import Entrance, Location
from worlds.generic.Rules import add_rule, set_rule
from .Options import DifficultyLogic
#from .JsonReader import AccessMethod
#from . import GloverWorld

move_lookup = [
    "Cartwheel",
    "Crawl",
    "Double Jump",
    "Fist Slam",
    "Ledge Grab",
    "Push",
    "Locate Garib",
    "Locate Ball",
    "Dribble",
    "Quick Swap",
    "Slap",
    "Throw",
    "Ball Toss",
    "Rubber Ball",
    "Bowling Ball",
    "Ball Bearing",
    "Crystal",
    "Beachball Potion",
    "Death Potion",
    "Helicopter Potion",
    "Frog Potion",
    "Boomerang Ball Potion",
    "Speed Potion",
    "Sticky Potion",
    "Hercules Potion",
    "Jump",
    "Not Crystal",
    "Not Bowling",
    "Sinks",
    "Floats",
    "Grab",
    "Ball Up",
    "Power Ball",
    "Not Bowling or Crystal"
]

switches_to_event_items = {
    "Atl1: Glover Switch" : "Atl1 Gate",
    "Atl2: Drain Block" : "Atl2 Elevator",
    "Atl2: Ball Switch" : "Atl2 Ballswitch Drain",
    "Atl2: Glover Switch" : "Atl2 Gate",
    "Atl3: Pyramid Ball Switch" : "Atl3 Waterwheel",
    "Atl3: Cliff Ball Switch" : "Atl3 Cave Platforms",
    "Crn1: Conveyor Target" : "Crn1 Elevator",
    "Crn1: Bars Glover Switch" : "Crn1 Gate",
    "Crn1: Ramp Ball Switch" : "Crn1 Door A",
    "Crn1: Ice Cream Glover Switch" : "Crn1 Door B",
    "Crn1: Slide Glover Switch" : "Crn1 Door C",
    "Crn1: Whack-A-Mole Glover Switch" : "Crn1 Rocket",
    "Crn1: Plinko Glover Switch" : "Crn1 Rocket",
    "Crn1: Slots Glover Switch" : "Crn1 Rocket",
    "Crn2: Clown Teeth" : "Crn2 Drop Garibs",
    "Crn2: Ball Switch" : "Crn2 Fan",
    "Crn3: Glover Switch" : "Crn3 Spin Door",
    "Crn3: Ball Switch" : "Crn3 Hands"#,
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
    ##"Prt3: " : "Prt3 Platform Spin",
    #"Prt3: " : "Prt3 Trampoline",
    #"Prt3: " : "Prt3 Stairs",
    #"Prt3: " : "Prt3 Elevator",
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
    #"FoF1: " : "FoF1 Coffin",
    #"FoF1: " : "FoF1 Doorway",
    #"FoF1: " : "FoF1 Drawbridge",
    #"FoF2: " : "FoF2 Garibs Fall",
    #"FoF2: " : "FoF2 Checkpoint Gates",
    #"FoF2: " : "FoF2 Mummy Gate",
    #"FoF3: " : "FoF3 Gate",
    #"FoF3: " : "FoF3 Spikes",
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
    #"" : "Training Sandpit",
    #"" : "Training Lower Target",
    #"" : "Training Stairs"
}

def access_methods_to_rules(self, all_methods, spot : Location | Entrance):
    valid_methods = []
    for each_method in all_methods:
        #Is this method in difficulty for you?
        match each_method.difficulty:
            #Intended only
            case 0:
                if self.options.difficulty_logic != DifficultyLogic.option_intended:
                    continue
            #Easy tricks only
            case 1:
                if self.options.difficulty_logic == DifficultyLogic.option_hard_tricks:
                    continue
        if len(each_method.required_items) == 0:
            continue
        valid_methods.append(each_method)
    #If there's no valid methods, it must be open
    if len(valid_methods) == 0:
        return
    
    #Otherwise, go over each valid method and assign
    for index, each_method in enumerate(valid_methods):
        #Start with the rule set
        if index == 0:
            set_rule(spot, lambda state, required_items = each_method.required_items : state.has_all(required_items, self.player))
            continue
        #Otherwise, this is an alternate method
        add_rule(spot, lambda state, required_items = each_method.required_items : state.has_all(required_items, self.player), "or")
