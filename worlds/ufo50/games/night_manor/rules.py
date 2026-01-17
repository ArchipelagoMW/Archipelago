from typing import TYPE_CHECKING, Dict
from BaseClasses import Region
from worlds.generic.Rules import set_rule

if TYPE_CHECKING:
    from ... import UFO50World

spoon = "Night Manor - Spoon"
bowl = "Night Manor - Bowl"
coins = "Night Manor - Coins"
hairpin = "Night Manor - Hairpin"
hook = "Night Manor - Hook"
tweezers = "Night Manor - Tweezers"
matches = "Night Manor - Matches"
batteries = "Night Manor - Batteries"
kitchen_knife = "Night Manor - Kitchen Knife"
drain_cleaner = "Night Manor - Drain Cleaner"
flashlight = "Night Manor - Flashlight"
oil_can = "Night Manor - Oil Can"
gas_can = "Night Manor - Gas Can"
crowbar = "Night Manor - Crowbar"
duct_tape = "Night Manor - Duct Tape"
ornamental_egg = "Night Manor - Ornamental Egg"
pool_cue = "Night Manor - Pool Cue"
sheet_music = "Night Manor - Sheet Music"
copper_key = "Night Manor - Copper Key"
brass_key = "Night Manor - Brass Key"
wrench = "Night Manor - Wrench"
hedge_shears = "Night Manor - Hedge Shears"
shovel = "Night Manor - Shovel"
motor = "Night Manor - Motor"
bronze_key = "Night Manor - Bronze Key"
gold_key = "Night Manor - Gold Key"
steel_key = "Night Manor - Steel Key"
hacksaw = "Night Manor - Hacksaw"
silver_key = "Night Manor - Silver Key"
ring = "Night Manor - Ring"
magnifying_glass = "Night Manor - Magnifying Glass"
doll = "Night Manor - Doll"
tea_tree_oil = "Night Manor - Tea Tree Oil"
hydrogen_peroxide = "Night Manor - Hydrogen Peroxide"
cigar_butt = "Night Manor - Cigar Butt"
aluminum_key = "Night Manor - Aluminum Key"
glasses = "Night Manor - Glasses"
red_gemstone = "Night Manor - Ruby"
green_gemstone = "Night Manor - Emerald"
yellow_gemstone = "Night Manor - Topaz"
white_gemstone = "Night Manor - Diamond"
maze_directions = "Night Manor - Maze Directions"
crossbow = "Night Manor - Crossbow"
crossbow_bolt = "Night Manor - Crossbow Bolt"
screwdriver = "Night Manor - Screwdriver"
gear = "Night Manor - Gear"
piano_wire = "Night Manor - Piano Wire"
iron_key = "Night Manor - Iron Key"
fungicide = "Night Manor - Fungicide"
safe_combo = "Night Manor - Safe Combination"
password = "Night Manor - Computer Password"


def create_rules(world: "UFO50World", regions: Dict[str, Region]) -> None:
    player = world.player
    regions["Menu"].connect(regions["Starting Room"])
    regions["Starting Room"].connect(regions["First Floor & Exterior"],
                                     rule=lambda state: state.has(hairpin, player))
    regions["First Floor & Exterior"].connect(regions["Second Floor"],
                                              rule=lambda state: state.has_all((flashlight, batteries), player))
    regions["First Floor & Exterior"].connect(regions["Shed"],
                                              rule=lambda state: state.has(copper_key, player))
    regions["First Floor & Exterior"].connect(regions["Maze"],
                                              rule=lambda state: state.has_all((red_gemstone, green_gemstone,
                                                                                yellow_gemstone, white_gemstone),
                                                                               player))
    regions["First Floor & Exterior"].connect(regions["Basement"],
                                              rule=lambda state: state.has(iron_key, player))
    regions["Second Floor"].connect(regions["Master Bedroom"],
                                    rule=lambda state: state.has(gold_key, player))

    set_rule(world.get_location("Night Manor - Starting Room - Yellow Note"),
             rule=lambda state: state.has(spoon, player))
    set_rule(world.get_location("Night Manor - Starting Room - Hairpin"),
             rule=lambda state: state.has(spoon, player))
    set_rule(world.get_location("Night Manor - Foyer - Gear"),
             rule=lambda state: state.has(brass_key, player))
    set_rule(world.get_location("Night Manor - Garage - Gas Can"),
             rule=lambda state: state.has(oil_can, player))
    set_rule(world.get_location("Night Manor - Garage - Crowbar"),
             rule=lambda state: state.has(oil_can, player))
    set_rule(world.get_location("Night Manor - Dining Room - Ornamental Egg"),
             rule=lambda state: state.has_any((crowbar, wrench, shovel), player)),
    set_rule(world.get_location("Night Manor - Living Room - Red Gemstone"),
             rule=lambda state: state.has_all((gas_can, matches), player))
    set_rule(world.get_location("Night Manor - Pool - Copper Key"),
             rule=lambda state: state.has_all((hook, duct_tape, pool_cue), player))
    set_rule(world.get_location("Night Manor - Shed - Bronze Key"),
             rule=lambda state: state.has(kitchen_knife, player))
    set_rule(world.get_location("Night Manor - Shed - Gold Key"),
             rule=lambda state: state.has(ornamental_egg, player))
    set_rule(world.get_location("Night Manor - Backyard - Motor"),
             rule=lambda state: state.has(wrench, player))
    set_rule(world.get_location("Night Manor - Garden - Steel Key"),
             rule=lambda state: state.has(shovel, player))
    set_rule(world.get_location("Night Manor - Sunroom - Hacksaw"),
             rule=lambda state: state.has(hedge_shears, player))
    set_rule(world.get_location("Night Manor - First Floor Bathroom - Silver Key"),
             rule=lambda state: state.has_all((tweezers, drain_cleaner), player))
    set_rule(world.get_location("Night Manor - First Floor Bathroom - Ring"),
             rule=lambda state: state.has(hacksaw, player))
    set_rule(world.get_location("Night Manor - Guest Bedroom - Brass Key"),
             rule=lambda state: state.has(silver_key, player))
    set_rule(world.get_location("Night Manor - Exterior Front - Green Gemstone"),
             rule=lambda state: state.has(ring, player))
    set_rule(world.get_location("Night Manor - Master Bathroom - Safe Combination"),
             rule=lambda state: state.has_any((crowbar, wrench, shovel), player))
    set_rule(world.get_location("Night Manor - Garden - Yellow Gemstone"),
             rule=lambda state: state.has_all((hacksaw, kitchen_knife), player)),
    set_rule(world.get_location("Night Manor - Kids Bedroom - Computer Password"),
             rule=lambda state: state.has(magnifying_glass, player))
    set_rule(world.get_location("Night Manor - Attic - Piano Wire"),
             rule=lambda state: state.has(sheet_music, player))
    set_rule(world.get_location("Night Manor - Attic - Crossbow"),
             rule=lambda state: state.has(bronze_key, player))
    set_rule(world.get_location("Night Manor - Manor - Aluminum Key"),
             rule=lambda state: state.has_all((kitchen_knife, doll), player))
    set_rule(world.get_location("Night Manor - Kids Bedroom - Glasses"),
             rule=lambda state: state.has(aluminum_key, player))
    set_rule(world.get_location("Night Manor - Play Room - Maze Directions"),
             rule=lambda state: state.has(glasses, player))
    set_rule(world.get_location("Night Manor - Lounge - Sheet Music"),
             rule=lambda state: state.has(coins, player))
    set_rule(world.get_location("Night Manor - Maze - Crossbow Bolt"),
             rule=lambda state: state.has(maze_directions, player))
    set_rule(world.get_location("Night Manor - Manor - Iron Key"),
             rule=lambda state: state.has_all((crossbow, crossbow_bolt), player))
    set_rule(world.get_location("Night Manor - Master Bedroom - White Gemstone"),
             rule=lambda state: state.has(safe_combo, player))
    set_rule(world.get_location("Night Manor - Office - Fungicide Recipe"),
             rule=lambda state: state.has(password, player))

    set_rule(world.get_location("Night Manor - Gold"),
             rule=lambda state: state.has_all((wrench, motor, steel_key), player))

    if "Night Manor" in world.options.cherry_allowed_games:
        set_rule(world.get_location("Night Manor - Cherry"),
                 rule=lambda state: state.has_all((screwdriver, gear, oil_can, piano_wire, bowl, tea_tree_oil,
                                                   hydrogen_peroxide, cigar_butt), player))
