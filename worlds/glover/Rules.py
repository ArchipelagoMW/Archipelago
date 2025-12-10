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
    "Crn3: Ball Switch" : "Crn3 Hands",
    "Prt1: Ship Target" : "Prt1 Raise Beach",
    "Prt1: Tower Glover Switch" : "Prt1 Elevator",
    "Prt1: Coast Target" : "Prt1 Chest",
    "Prt1: Fan Ball Switch" : "Prt1 Sandpile",
    "Prt1: Sand Ball Switch" : "Prt1 Waterspout",
    "Prt1: Lighthouse Target" : "Prt1 Lighthouse",
    "Prt1: Lighthouse Glover Switch" : "Prt1 Raise Ship",
    "Prt1: Crate Ball Switch" : "Prt1 Bridge",
    "Prt2: Glover Switch" : "Prt2 Lower Water",
    "Prt2: Water Ball Switch" : "Prt2 Ramp",
    "Prt2: Platform Ball Switch" : "Prt2 Gate",
    #"Prt3: " : "Prt3 Platform Spin",
    "Prt3: Cliff Glover Switch" : "Prt3 Trampoline",
    "Prt3: Target" : "Prt3 Stairs",
    "Prt3: Ball Switch" : "Prt3 Elevator",
    "Pht1: Icicles" : "Pht1 Life Drop",
    "Pht2: Lavafall Ball Switch" : "Pht2 Platform 1",
    "Pht2: Switches Ball Switch" : "Pht2 Platform 2",
    "Pht2: Glover Switch" : "Pht2 Lower Ball Switch",
    "Pht3: Tracey Tree" : "Pht3 Drop Garibs",
    "Pht3: Trees Glover Switch" : "Pht3 Spin Stones",
    "Pht3: Monolith A" : "Pht3 Lower Monolith",
    "Pht3: Monolith B" : "Pht3 Lower Monolith",
    "Pht3: Monolith C" : "Pht3 Lower Monolith",
    "Pht3: Monolith D" : "Pht3 Lower Monolith",
    "Pht3: Monolith Ball Switch" : "Pht3 Floating Platforms",
    "Pht3: Flying Lava Ball Switch" : "Pht3 Lava Spinning",
    "Pht3: Lava Pit Ball Switch" : "Pht3 Dirt Elevator",
    "FoF1: Dead-End Glover Switch" : "FoF1 Coffin",
    "FoF1: Left Target" : "FoF1 Progressive Doorway",
    "FoF1: Right Target" : "FoF1 Progressive Doorway",
    "FoF1: Push Blocks" : "FoF1 Coffin Lightning",
    "FoF1: Coffin Glover Switch" : "FoF1 Drawbridge",
    "FoF2: Push Target" : "FoF2 Garibs Fall",
    "FoF2: Push Switch" : "FoF2 Progressive Gate",
    "FoF2: Slope Target" : "FoF2 Progressive Gate",
    "FoF2: Mummy" : "FoF2 Mummy Gate",
    "FoF3: Target" : "FoF3 Gate",
    "FoF3: Ball Switch" : "FoF3 Spikes",
    #"Otw1: " : "Otw1 Aliens",
    "Otw1: Sign Glover Switch" : "Otw1 Fans",
    "Otw1: Stone Pillar Ball Switch" : "Otw1 Flying Platforms",
    "Otw1: Cliff Glover Switch" : "Otw1 Goo Platforms",
    "Otw1: Hazard Stripe Ball Switch" : "Otw1 UFO",
    "Otw1: UFO Glover Switch" : "Otw1 Missile",
    "Otw2: Right Platform Ball Switch" : "Otw2 Mashers",
    "Otw2: Cliff Ball Switch" : "Otw2 Ramp",
    "Otw3: Duel Switch" : "Otw3 Hazard Gate",
    "Otw3: Conveyor Glover Switch" : "Otw3 Sign",
    "Otw3: Above Fan Red Switch" : "Otw3 Fan",
    "Otw3: Magnet Ball Switch" : "Otw3 Bridge",
    "Otw3: Ball Switch" : "Otw3 Glass Gate",
    "Training: Ball Switch" : "Training Sandpit",
    "Training: Glover Switch" : "Training Lower Target",
    "Training: Target" : "Training Stairs"
}

def access_methods_to_rules(self, all_methods, spot : Location | Entrance):
    nonblank_methods = []
    for each_method in all_methods:
        if len(each_method.required_items) == 0:
            continue
        nonblank_methods.append(each_method)
    #If there's no nonblank methods at this step, it must be open
    if len(nonblank_methods) == 0:
        return
    #Reorder the access methods to get around the 'or'ing problem
    nonblank_methods.sort(key=sort_access_method)
    #Otherwise, go over each valid method and assign
    for index, each_method in enumerate(nonblank_methods):
        #Start with the rule set
        if index == 0:
            set_rule(spot, lambda state, required_items = each_method.required_items : state.has_all(required_items, self.player))
            continue
        #Otherwise, this is an alternate method
        add_rule(spot, lambda state, required_items = each_method.required_items : state.has_all(required_items, self.player), "or")

#Move all methods that require switches to the end of the list
def sort_access_method(in_method):
    for each_requirement in in_method.required_items:
        #Switches
        if not each_requirement in move_lookup:
            return 1
    return 0
