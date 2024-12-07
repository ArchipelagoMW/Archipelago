import typing
from typing import NamedTuple, Dict, List

from BaseClasses import Entrance, CollectionState, Region
from worlds.generic.Rules import CollectionRule


class LoonylandEntrance(Entrance):
    game = "Loonyland"


class EntranceData(NamedTuple):
    source_region: str
    target_region: str
    is_real_loading_zone: bool
    #rule: typing.Callable[[player, state], bool]
    rule: CollectionRule

def have_light_source(state: CollectionState, player: int) -> bool:
    return state.has("Lantern", player) or (state.has("Stick", player) and state.has("Boots", player))

def set_entrances(multiworld, world, player):

    loonyland_entrance_table: List[EntranceData] = [
        #base
        EntranceData("Menu", "Halloween Hill", False, lambda state: True ),

        # loading zones, can be randomized
        EntranceData("Halloween Hill", "A Cabin Trees", True, lambda state: True ),
        EntranceData("Halloween Hill", "The Witch's Cabin Front", True, lambda state: True ),
        EntranceData("Halloween Hill", "Bonita's Cabin", True, lambda state: True ),
        EntranceData("Halloween Hill", "Underground Tunnel Top", True, lambda state: True ),
        EntranceData("Halloween Hill", "The Bog Pit", True, lambda state: True ),
        EntranceData("Slurpy Swamp Mud", "Swamp Gas Cavern Front", True, lambda state: True ),
        EntranceData("Slurpy Swamp Mud", "Swamp Gas Cavern Back", True, lambda state: True ),
        EntranceData("Halloween Hill", "A Tiny Cabin", True, lambda state: state.has("Skull Key", player)),
        EntranceData("Halloween Hill", "The Witch's Cabin Back", True, lambda state: True),
        EntranceData("Zombiton", "A Cabin Seer", True, lambda state: True),
        EntranceData("Zombiton", "Benny's Cocktails", True, lambda state: True),
        EntranceData("Halloween Hill", "Dusty Crypt", True, lambda state: True),
        EntranceData("Zombiton", "Musty Crypt", True, lambda state: True),
        EntranceData("Zombiton", "A Messy Cabin", True, lambda state: True),
        EntranceData("Halloween Hill", "Rusty Crypt", True, lambda state: True),
        EntranceData("Halloween Hill", "Under The Lake", True, lambda state: have_light_source(state, player) and state.has("Orb", player, 4)),
        EntranceData("Halloween Hill", "Haunted Tower", True, lambda state: True),
        EntranceData("Rocky Cliffs", "Abandoned Mines", True, lambda state: True),
        EntranceData("Rocky Cliffs", "The Shrine Of Bombulus", True, lambda state: True),
        EntranceData("Rocky Cliffs", "A Gloomy Cavern", True, lambda state: True),
        EntranceData("Halloween Hill", "Happy Stick Woods", True, lambda state: True),
        EntranceData("Zombiton", "A Cabin Larry", True, lambda state: True),
        EntranceData("Halloween Hill", "The Wolf Den", True, lambda state: True),
        EntranceData("Rocky Cliffs", "Upper Creepy Caverns", True, lambda state: state.has("Bombs", player)),
        EntranceData("Rocky Cliffs", "Creepy Caverns Left", True, lambda state: True),
        EntranceData("Vampy Land", "Castle Vampy", True, lambda state: True),
        EntranceData("Halloween Hill", "Cabin In The Woods", True, lambda state: True),
        EntranceData("Halloween Hill", "A Cabin Collector", True, lambda state: True),
        EntranceData("Halloween Hill", "A Hidey-Hole", True, lambda state: True),
        EntranceData("Vampy Land", "Creepy Caverns Right", True, lambda state: True),
        EntranceData("Halloween Hill", "Swampdog Lair", True, lambda state: True),
        EntranceData("A Cabin Trees", "Halloween Hill", True,lambda state: True),
        EntranceData("The Witch's Cabin Front", "Halloween Hill", True, lambda state: True),
        EntranceData("The Witch's Cabin Back", "Halloween Hill", True, lambda state: True),
        EntranceData("Bonita's Cabin", "Halloween Hill", True, lambda state: True),
        EntranceData("The Bog Pit", "Halloween Hill", True, lambda state: have_light_source(state, player)),
        EntranceData("Underground Tunnel Top", "Halloween Hill", True, lambda state: True),
        EntranceData("Underground Tunnel Zombie", "Benny's Cocktails", True, lambda state: True),
        EntranceData("Swamp Gas Cavern Front", "Slurpy Swamp Mud", True, lambda state: state.has("Boots")),
        EntranceData("Swamp Gas Cavern Back", "Slurpy Swamp Mud", True, lambda state: state.has("Boots")),
        EntranceData("A Tiny Cabin", "Halloween Hill", True, lambda state: True),
        EntranceData("A Cabin Seer", "Zombiton", True, lambda state: True),
        EntranceData("Benny's Cocktails", "Zombiton", True,lambda state: True),
        EntranceData("Benny's Cocktails", "Underground Tunnel Zombie", True, lambda state: True),
        EntranceData("Dusty Crypt", "Halloween Hill", True, lambda state: True),
        EntranceData("Musty Crypt", "Zombiton", True, lambda state: True),
        EntranceData("Rusty Crypt", "Halloween Hill", True, lambda state: True),
        EntranceData("A Messy Cabin", "Zombiton", True, lambda state: True),
        EntranceData("Under The Lake", "Halloween Hill", True, lambda state: True),
        EntranceData("Under The Lake", "Deeper Under The Lake", True, lambda state: True),
        EntranceData("Deeper Under The Lake", "Under The Lake", True, lambda state: True),
        EntranceData("Deeper Under The Lake", "Frankenjulie's Laboratory", True, lambda state: True),
        EntranceData("Frankenjulie's Laboratory", "Deeper Under The Lake", True, lambda state: True),
        EntranceData("Frankenjulie's Laboratory", "Halloween Hill", True, lambda state: True),
        EntranceData("Haunted Tower", "Halloween Hill", True, lambda state: True),
        EntranceData("Haunted Tower", "Haunted Tower, Floor 2", True, lambda state: state.has("Ghost Potion", player)),
        EntranceData("Haunted Tower", "Haunted Basement", True, lambda state: state.has("Bat Key", player) and
                                                                              state.has("Pumpkin Key", player) and
                                                                              state.has("Skull Key", player)),
        EntranceData("Haunted Tower, Floor 2", "Haunted Tower", True, lambda state: True),
        EntranceData("Haunted Tower, Floor 2", "Haunted Tower, Floor 3", True, lambda state: state.has("Ghost Potion", player)),
        EntranceData("Haunted Tower, Floor 3", "Haunted Tower, Floor 2", True, lambda state: state.has("Ghost Potion", player)),
        EntranceData("Haunted Tower, Floor 3", "Haunted Tower Roof", True, lambda state: state.has("Ghost Potion", player)),
        EntranceData("Haunted Tower Roof", "Halloween Hill", True, lambda state: True),
        EntranceData("Haunted Tower Roof", "Haunted Tower, Floor 3", True, lambda state: True),
        EntranceData("Haunted Basement", "Haunted Tower", True, lambda state: True),
        EntranceData("Abandoned Mines", "Rocky Cliffs", True, lambda state: True),
        EntranceData("The Shrine Of Bombulus", "Rocky Cliffs", True, lambda state: True),
        EntranceData("A Gloomy Cavern", "Rocky Cliffs", True, lambda state: True),
        EntranceData("Happy Stick Woods", "Halloween Hill", True, lambda state: True),
        EntranceData("The Wolf Den", "Halloween Hill", True, lambda state: True),
        EntranceData("The Wolf Den", "Larry's Lair", True, lambda state: state.has("Silver Sling", player)),
        EntranceData("A Cabin Larry", "Zombiton", True, lambda state: True),
        EntranceData("Upper Creepy Caverns", "Rocky Cliffs", True, lambda state: state.has("Bombs", player)),
        EntranceData("Upper Creepy Caverns", "Creepy Caverns Left", True, lambda state: True),
        EntranceData("Upper Creepy Caverns", "Creepy Caverns Middle", True, lambda state: True),
        EntranceData("Under The Ravine", "Creepy Caverns Middle", True, lambda state: True),
        EntranceData("Under The Ravine", "Creepy Caverns Right", True, lambda state: True),
        EntranceData("Creepy Caverns Left", "Rocky Cliffs", True, lambda state: True),
        EntranceData("Creepy Caverns Left", "Upper Creepy Caverns", True, lambda state: True),
        EntranceData("Creepy Caverns Middle", "Upper Creepy Caverns", True, lambda state: True),
        EntranceData("Creepy Caverns Middle", "Under The Ravine", True, lambda state: True),
        EntranceData("Creepy Caverns Right", "Under The Ravine", True, lambda state: True),
        EntranceData("Creepy Caverns Right", "Vampy Land", True, lambda state: True),
        EntranceData("Castle Vampy", "Halloween Hill", True, lambda state: True),
        EntranceData("Castle Vampy", "Castle Vampy Skull Jail", False, lambda state: state.has("Skull Key", player)),
        EntranceData("Castle Vampy Skull Jail", "Castle Vampy II Main", True, lambda state: state.has("Skull Key", player)),
        EntranceData("Castle Vampy", "Castle Vampy II NE", True, lambda state: state.has("Bat Statue", player, 4)),
        EntranceData("Castle Vampy", "Castle Vampy II SE", True, lambda state: state.has("Bat Statue", player,4)),
        EntranceData("Castle Vampy", "Castle Vampy II SW", True, lambda state: state.has("Bat Statue", player,4)),
        EntranceData("Castle Vampy", "Castle Vampy II NW", True, lambda state: state.has("Bat Statue", player,4)),
        EntranceData("Castle Vampy II Main", "Castle Vampy Skull Jail", True, lambda state: True),
        EntranceData("Castle Vampy II Main", "Castle Vampy II Bat Jail", True, lambda state: state.has("Bat Key", player)),
        EntranceData("Castle Vampy II Bat Jail", "Castle Vampy III Main", True, lambda state: state.has("Bat Key", player)),
        EntranceData("Castle Vampy II NE", "Castle Vampy", True, lambda state: True),
        EntranceData("Castle Vampy II NE", "Castle Vampy III NE", True, lambda state: True),
        EntranceData("Castle Vampy II SE", "Castle Vampy", True, lambda state: True),
        EntranceData("Castle Vampy II SE", "Castle Vampy III SE", True, lambda state: True),
        EntranceData("Castle Vampy II SW", "Castle Vampy", True, lambda state: True),
        EntranceData("Castle Vampy II SW", "Castle Vampy III SW", True, lambda state: True),
        EntranceData("Castle Vampy II NW", "Castle Vampy", True, lambda state: True),
        EntranceData("Castle Vampy II NW", "Castle Vampy III NW", True, lambda state: True),
        EntranceData("Cabin In The Woods", "Halloween Hill", True, lambda state: True),
        EntranceData("Castle Vampy III Main", "Castle Vampy II Bat Jail", True, lambda state: True),
        EntranceData("Castle Vampy III Main", "Castle Vampy III Pumpkin Jail", True, lambda state: state.has("Pumpkin Key", player)),
        EntranceData("Castle Vampy III Pumpkin Jail", "Castle Vampy IV Main", True, lambda state: state.has("Pumpkin Key", player)),
        EntranceData("Castle Vampy III NE", "Castle Vampy II NE", True, lambda state: True),
        EntranceData("Castle Vampy III NE", "Castle Vampy IV NE", True, lambda state: True),
        EntranceData("Castle Vampy III SE", "Castle Vampy II SE", True, lambda state: True),
        EntranceData("Castle Vampy III SE", "Castle Vampy IV SE", True, lambda state: True),
        EntranceData("Castle Vampy III SW", "Castle Vampy II SW", True, lambda state: True),
        EntranceData("Castle Vampy III SW", "Castle Vampy IV SW", True, lambda state: True),
        EntranceData("Castle Vampy III NW", "Castle Vampy II NW", True, lambda state: True),
        EntranceData("Castle Vampy III NW", "Castle Vampy IV NW", True, lambda state: True),
        EntranceData("Castle Vampy IV Main", "Castle Vampy III Pumpkin Jail", True, lambda state: True),
        EntranceData("Castle Vampy IV Main", "The Heart Of Terror", True, lambda state: state.has("Vamp Statue", player, 8)),
        EntranceData("Castle Vampy IV NE", "Castle Vampy III NE", True, lambda state: True),
        EntranceData("Castle Vampy IV NE", "Castle Vampy Roof NE", True, lambda state: True),
        EntranceData("Castle Vampy IV SE", "Castle Vampy III SE", True, lambda state: True),
        EntranceData("Castle Vampy IV SE", "Castle Vampy Roof SE", True, lambda state: True),
        EntranceData("Castle Vampy IV SW", "Castle Vampy III SW", True, lambda state: True),
        EntranceData("Castle Vampy IV SW", "Castle Vampy Roof SW", True, lambda state: True),
        EntranceData("Castle Vampy IV NW", "Castle Vampy III NW", True, lambda state: True),
        EntranceData("Castle Vampy IV NW", "Castle Vampy Roof NW", True, lambda state: True),
        EntranceData("A Cabin Collector", "Halloween Hill", True, lambda state: True),
        EntranceData("Castle Vampy Roof NE", "Castle Vampy IV NE", True, lambda state: True),
        EntranceData("Castle Vampy Roof SE", "Castle Vampy IV SE", True, lambda state: True),
        EntranceData("Castle Vampy Roof SW", "Castle Vampy IV SW", True, lambda state: True),
        EntranceData("Castle Vampy Roof NW", "Castle Vampy IV NW", True, lambda state: True),
        EntranceData("The Evilizer", "Halloween Hill", True, lambda state: True),
        EntranceData("The Heart Of Terror", "The Evilizer", True, lambda state: True),
        EntranceData("A Hidey-Hole", "Halloween Hill", True, lambda state: True),
        EntranceData("Empty Rooftop", "Halloween Hill", True, lambda state: True),
        EntranceData("Swampdog Lair", "Halloween Hill", True, lambda state: True),
        EntranceData("Larry's Lair", "Halloween Hill", True, lambda state: True),

        #logical zone connections, cant be randomized

        EntranceData("Halloween Hill", "Slurpy Swamp Mud", False, lambda state: state.has("Boots", player)),
        EntranceData("Slurpy Swamp Mud", "Halloween Hill", False, lambda state: state.has("Boots", player)),

        EntranceData("Zombiton", "Halloween Hill", False, lambda state: True), #one way
        #EntranceData("Halloween Hill", "Zombiton ", False), todo possible with badges

        EntranceData("Halloween Hill", "Rocky Cliffs", False, lambda state: state.has("Big Gem", player)),
        EntranceData("Rocky Cliffs", "Halloween Hill", False, lambda state: state.has("Big Gem", player)),

        EntranceData("Vampy Land", "Halloween Hill", False, lambda state: True), #one way
        #EntranceData("Halloween Hill", "Vampy Land", False), TODO possible with badges/rando

        EntranceData("Underground Tunnel Top", "Underground Tunnel Mud", False,  lambda state: state.has("Boots", player)),
        EntranceData("Underground Tunnel Mud", "Underground Tunnel Top", False,  lambda state: state.has("Boots", player)),
        EntranceData("Underground Tunnel Mud", "Underground Tunnel Zombie", False,  lambda state: state.has("Boots", player)), #one way
        #EntranceData("Underground Tunnel Zombie", "Underground Tunnel Mud", False),  # TODO possible with badges/bridge rando

        EntranceData("Swamp Gas Cavern Front", "Swamp Gas Cavern Back", False, lambda state: state.has("Boots", player)),  # one way
        #EntranceData("Swamp Gas Cavern Back", "Swamp Gas Cavern Front", False),  # TODO possible with badges


        #probably need these with molecular dispersion
        # "The Witch's Cabin Front -> The Witch's Cabin Back": EntranceData("The Witch's Cabin Front", "The Witch's Cabin Back", False),
        # "The Witch's Cabin Back -> The Witch's Cabin Front": EntranceData("The Witch's Cabin Back", "The Witch's Cabin Front", False),
        # "Creepy Caverns Left -> Creepy Caverns Middle": EntranceData("Creepy Caverns Left", "Creepy Caverns Middle", False),
        # "Creepy Caverns Middle -> Creepy Caverns Left": EntranceData("Creepy Caverns Middle", "Creepy Caverns Left", False),
        # "Creepy Caverns Middle -> Creepy Caverns Right": EntranceData("Creepy Caverns Middle", "Creepy Caverns Right", False),
        # "Creepy Caverns Right -> Creepy Caverns Middle": EntranceData("Creepy Caverns Right", "Creepy Caverns Middle", False),

        # "Castle Vampy II Main -> Castle Vampy II NE": EntranceData("Castle Vampy II Main", "Castle Vampy II NE", False),
        # "Castle Vampy II NE -> Castle Vampy II Main": EntranceData("Castle Vampy II NE", "Castle Vampy II Main", False),
        # "Castle Vampy II Main -> Castle Vampy II SE": EntranceData("Castle Vampy II Main", "Castle Vampy II SE", False),
        # "Castle Vampy II SE -> Castle Vampy II Main": EntranceData("Castle Vampy II SE", "Castle Vampy II Main", False),
        # "Castle Vampy II Main -> Castle Vampy II SW": EntranceData("Castle Vampy II Main", "Castle Vampy II SW", False),
        # "Castle Vampy II SW -> Castle Vampy II Main": EntranceData("Castle Vampy II SW", "Castle Vampy II Main", False),
        # "Castle Vampy II Main -> Castle Vampy II NW": EntranceData("Castle Vampy II Main", "Castle Vampy II NW", False),
        # "Castle Vampy II NW -> Castle Vampy II Main": EntranceData("Castle Vampy II NW", "Castle Vampy II Main", False),

        # "Castle Vampy III Main -> Castle Vampy III NE": EntranceData("Castle Vampy III Main", "Castle Vampy III NE", False),
        # "Castle Vampy III NE -> Castle Vampy III Main": EntranceData("Castle Vampy III NE", "Castle Vampy III Main", False),
        # "Castle Vampy III Main -> Castle Vampy III SE": EntranceData("Castle Vampy III Main", "Castle Vampy III SE", False),
        # "Castle Vampy III SE -> Castle Vampy III Main": EntranceData("Castle Vampy III SE", "Castle Vampy III Main", False),
        # "Castle Vampy III Main -> Castle Vampy III SW": EntranceData("Castle Vampy III Main", "Castle Vampy III SW", False),
        # "Castle Vampy III SW -> Castle Vampy III Main": EntranceData("Castle Vampy III SW", "Castle Vampy III Main", False),
        # "Castle Vampy III Main -> Castle Vampy III NW": EntranceData("Castle Vampy III Main", "Castle Vampy III NW", False),
        # "Castle Vampy III NW -> Castle Vampy III Main": EntranceData("Castle Vampy III NW", "Castle Vampy III Main", False),

        # "Castle Vampy IV Main -> Castle Vampy IV NE": EntranceData("Castle Vampy IV Main", "Castle Vampy IV NE", False),
        # "Castle Vampy IV NE -> Castle Vampy IV Main": EntranceData("Castle Vampy IV NE", "Castle Vampy IV Main", False),
        # "Castle Vampy IV Main -> Castle Vampy IV SE": EntranceData("Castle Vampy IV Main", "Castle Vampy IV SE", False),
        # "Castle Vampy IV SE -> Castle Vampy IV Main": EntranceData("Castle Vampy IV SE", "Castle Vampy IV Main", False),
        # "Castle Vampy IV Main -> Castle Vampy IV SW": EntranceData("Castle Vampy IV Main", "Castle Vampy IV SW", False),
        # "Castle Vampy IV SW -> Castle Vampy IV Main": EntranceData("Castle Vampy IV SW", "Castle Vampy IV Main", False),
        # "Castle Vampy IV Main -> Castle Vampy IV NW": EntranceData("Castle Vampy IV Main", "Castle Vampy IV NW", False),
        # "Castle Vampy IV NW -> Castle Vampy IV Main": EntranceData("Castle Vampy IV NW", "Castle Vampy IV Main", False),
    ]
    for region in multiworld.get_regions(player):
        for entry in loonyland_entrance_table:
            if entry.source_region == region.name:
                region.connect(connecting_region= world.get_region(entry.target_region), rule= entry.rule)
