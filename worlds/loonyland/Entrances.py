from typing import NamedTuple, Dict

from BaseClasses import Entrance


class LoonylandEntrance(Entrance):
    game = "Loonyland"


class EntranceData(NamedTuple):
    source_region: str
    target_region: str
    is_real_loading_zone: bool

loonyland_entrance_table: Dict[str, EntranceData] = {
    #base
    "Menu -> Halloween Hill": EntranceData("Menu", "Halloween Hill", False),

    #loading zones, can be randomized
    "Halloween Hill -> A Cabin Trees": EntranceData("Halloween Hill", "A Cabin Trees", True),
    "Halloween Hill -> The Witch's Cabin Front": EntranceData("Halloween Hill", "The Witch's Cabin Front", True),
    "Halloween Hill -> Bonita's Cabin": EntranceData("Halloween Hill", "Bonita's Cabin", True),
    "Halloween Hill -> Underground Tunnel Top": EntranceData("Halloween Hill", "Underground Tunnel Top", True),
    "Halloween Hill -> The Bog Pit": EntranceData("Halloween Hill", "The Bog Pit", True),
    "Slurpy Swamp Mud -> Swamp Gas Cavern Front": EntranceData("Slurpy Swamp Mud", "Swamp Gas Cavern", True),
    "Slurpy Swamp Mud -> Swamp Gas Cavern Back": EntranceData("Slurpy Swamp Mud", "Swamp Gas Cavern", True),
    "Halloween Hill -> A Tiny Cabin": EntranceData("Halloween Hill", "A Tiny Cabin", True),
    "Halloween Hill -> The Witch's Cabin Back": EntranceData("Halloween Hill", "The Witch's Cabin Back", True),
    "Zombiton -> A Cabin Seer": EntranceData("Zombiton", "A Cabin Seer", True),
    "Zombiton -> Benny's Cocktails": EntranceData("Zombiton", "Benny's Cocktails", True),
    "Halloween Hill -> Dusty Crypt": EntranceData("Halloween Hill", "Dusty Crypt", True),
    "Zombiton -> Musty Crypt": EntranceData("Zombiton", "Musty Crypt", True),
    "Zombiton -> A Messy Cabin": EntranceData("Zombiton", "A Messy Cabin", True),
    "Halloween Hill -> Rusty Crypt": EntranceData("Halloween Hill", "Rusty Crypt", True),
    "Halloween Hill -> Under The Lake": EntranceData("Halloween Hill", "Under The Lake", True),
    "Halloween Hill -> Haunted Tower": EntranceData("Halloween Hill", "Haunted Tower", True),
    "Halloween Hill -> Abandoned Mines": EntranceData("Halloween Hill", "Abandoned Mines", True),
    "Halloween Hill -> The Shrine Of Bombulus": EntranceData("Halloween Hill", "The Shrine Of Bombulus", True),
    "Halloween Hill -> A Gloomy Cavern": EntranceData("Halloween Hill", "A Gloomy Cavern", True),
    "Halloween Hill -> Happy Stick Woods": EntranceData("Halloween Hill", "Happy Stick Woods", True),
    "Zombiton -> A Cabin Larry": EntranceData("Zombiton", "A Cabin Larry", True),
    "Halloween Hill -> The Wolf Den": EntranceData("Halloween Hill", "The Wolf Den", True),
    "Halloween Hill -> Upper Creepy Caverns": EntranceData("Halloween Hill", "Upper Creepy Caverns", True),
    "Halloween Hill -> Creepy Caverns Left": EntranceData("Halloween Hill", "Creepy Caverns Left", True),
    "Vampy Land -> Castle Vampy": EntranceData("Vampy Land", "Castle Vampy", True),
    "Halloween Hill -> Cabin In The Woods": EntranceData("Halloween Hill", "Cabin In The Woods", True),
    "Halloween Hill -> A Cabin Collector": EntranceData("Halloween Hill", "A Cabin Collector", True),
    "Halloween Hill -> A Hidey-Hole": EntranceData("Halloween Hill", "A Hidey-Hole", True),
    "Halloween Hill -> Creepy Caverns Right": EntranceData("Halloween Hill", "Creepy Caverns", True),
    "Halloween Hill -> Swampdog Lair": EntranceData("Halloween Hill", "Swampdog Lair", True),
    "A Cabin -> Halloween Hill": EntranceData("A Cabin", "Halloween Hill", True),
    "The Witch's Cabin Front -> Halloween Hill": EntranceData("The Witch's Cabin Front", "Halloween Hill", True),
    "The Witch's Cabin Back -> Halloween Hill": EntranceData("The Witch's Cabin Back", "Halloween Hill", True),
    "Bonita's Cabin -> Halloween Hill": EntranceData("Bonita's Cabin", "Halloween Hill", True),
    "The Bog Pit -> Halloween Hill": EntranceData("The Bog Pit", "Halloween Hill", True),
    "Underground Tunnel Top -> Halloween Hill": EntranceData("Underground Tunnel Top", "Halloween Hill", True),
    "Underground Tunnel Zombie -> Benny's Cocktails": EntranceData("Underground Tunnel Zombie", "Benny's Cocktails", True),
    "Swamp Gas Cavern Front -> Slurpy Swamp Mud": EntranceData("Swamp Gas Cavern Front", "Slurpy Swamp Mud", True),
    "Swamp Gas Cavern Back -> Slurpy Swamp Mud": EntranceData("Swamp Gas Cavern Back", "Slurpy Swamp Mud", True),
    "A Tiny Cabin -> Halloween Hill": EntranceData("A Tiny Cabin", "Halloween Hill", True),
    "A Cabin Seer -> Zombiton": EntranceData("A Cabin Seer", "Zombiton", True),
    "Benny's Cocktails -> Zombiton": EntranceData("Benny's Cocktails", "Zombiton", True),
    "Benny's Cocktails -> Underground Tunnel Zombie": EntranceData("Benny's Cocktails", "Underground Tunnel Zombie", True),
    "Dusty Crypt -> Halloween Hill": EntranceData("Dusty Crypt", "Halloween Hill", True),
    "Musty Crypt -> Zombiton": EntranceData("Musty Crypt", "Zombiton", True),
    "Rusty Crypt -> Halloween Hill": EntranceData("Rusty Crypt", "Halloween Hill", True),
    "A Messy Cabin -> Zombiton": EntranceData("A Messy Cabin", "Zombiton", True),
    "Under The Lake -> Halloween Hill": EntranceData("Under The Lake", "Halloween Hill", True),
    "Under The Lake -> Deeper Under The Lake": EntranceData("Under The Lake", "Deeper Under The Lake", True),
    "Deeper Under The Lake -> Under The Lake": EntranceData("Deeper Under The Lake", "Under The Lake", True),
    "Deeper Under The Lake -> Frankenjulie's Laboratory": EntranceData("Deeper Under The Lake", "Frankenjulie's Laboratory", True),
    "Frankenjulie's Laboratory -> Deeper Under The Lake": EntranceData("Frankenjulie's Laboratory", "Deeper Under The Lake", True),
    "Frankenjulie's Laboratory -> Halloween Hill": EntranceData("Frankenjulie's Laboratory", "Halloween Hill", True),
    "Haunted Tower -> Halloween Hill": EntranceData("Haunted Tower", "Halloween Hill", True),
    "Haunted Tower -> Haunted Tower, Floor 2": EntranceData("Haunted Tower", "Haunted Tower, Floor 2", True),
    "Haunted Tower -> Haunted Basement": EntranceData("Haunted Tower", "Haunted Basement", True),
    "Haunted Tower, Floor 2 -> Haunted Tower": EntranceData("Haunted Tower, Floor 2", "Haunted Tower", True),
    "Haunted Tower, Floor 2 -> Haunted Tower, Floor 3": EntranceData("Haunted Tower, Floor 2", "Haunted Tower, Floor 3", True),
    "Haunted Tower, Floor 3 -> Haunted Tower, Floor 2": EntranceData("Haunted Tower, Floor 3", "Haunted Tower, Floor 2", True),
    "Haunted Tower, Floor 3 -> Haunted Tower Roof": EntranceData("Haunted Tower, Floor 3", "Haunted Tower Roof", True),
    "Haunted Tower Roof -> Halloween Hill": EntranceData("Haunted Tower Roof", "Halloween Hill", True),
    "Haunted Tower Roof -> Haunted Tower, Floor 3": EntranceData("Haunted Tower Roof", "Haunted Tower, Floor 3", True),
    "Haunted Basement -> Haunted Tower": EntranceData("Haunted Basement", "Haunted Tower", True),
    "Abandoned Mines -> Halloween Hill": EntranceData("Abandoned Mines", "Halloween Hill", True),
    "The Shrine Of Bombulus -> Halloween Hill": EntranceData("The Shrine Of Bombulus", "Halloween Hill", True),
    "A Gloomy Cavern -> Halloween Hill": EntranceData("A Gloomy Cavern", "Halloween Hill", True),
    "Happy Stick Woods -> Halloween Hill": EntranceData("Happy Stick Woods", "Halloween Hill", True),
    "The Wolf Den -> Halloween Hill": EntranceData("The Wolf Den", "Halloween Hill", True),
    "The Wolf Den -> Larry's Lair": EntranceData("The Wolf Den", "Larry's Lair", True),
    "A Cabin Larry -> Zombiton": EntranceData("A Cabin Larry", "Zombiton", True),
    "Upper Creepy Caverns -> Halloween Hill": EntranceData("Upper Creepy Caverns", "Halloween Hill", True),
    "Upper Creepy Caverns -> Creepy Caverns Left": EntranceData("Upper Creepy Caverns", "Creepy Caverns Left", True),
    "Upper Creepy Caverns -> Creepy Caverns Middle": EntranceData("Upper Creepy Caverns", "Creepy Caverns Middle", True),
    "Under The Ravine -> Creepy Caverns Middle": EntranceData("Under The Ravine", "Creepy Caverns Middle", True),
    "Under The Ravine -> Creepy Caverns Right": EntranceData("Under The Ravine", "Creepy Caverns Right", True),
    "Creepy Caverns Left -> Halloween Hill": EntranceData("Creepy Caverns Left", "Halloween Hill", True),
    "Creepy Caverns Left -> Upper Creepy Caverns": EntranceData("Creepy Caverns Left", "Upper Creepy Caverns", True),
    "Creepy Caverns Middle -> Upper Creepy Caverns": EntranceData("Creepy Caverns Middle", "Upper Creepy Caverns", True),
    "Creepy Caverns Middle -> Under The Ravine": EntranceData("Creepy Caverns Middle", "Under The Ravine", True),
    "Creepy Caverns Right -> Under The Ravine": EntranceData("Creepy Caverns Right", "Under The Ravine", True),
    "Creepy Caverns Right -> Vampy Land": EntranceData("Creepy Caverns Right", "Vampy Land", True),
    "Castle Vampy -> Halloween Hill": EntranceData("Castle Vampy", "Halloween Hill", True),
    "Castle Vampy -> Castle Vampy II": EntranceData("Castle Vampy", "Castle Vampy II", True),
    "Castle Vampy -> Castle Vampy II NE": EntranceData("Castle Vampy", "Castle Vampy II NE", True),
    "Castle Vampy -> Castle Vampy II SE": EntranceData("Castle Vampy", "Castle Vampy II SE", True),
    "Castle Vampy -> Castle Vampy II SW": EntranceData("Castle Vampy", "Castle Vampy II SW", True),
    "Castle Vampy -> Castle Vampy II NW": EntranceData("Castle Vampy", "Castle Vampy II NW", True),
    "Castle Vampy II Main -> Castle Vampy": EntranceData("Castle Vampy II", "Castle Vampy", True),
    "Castle Vampy II Main -> Castle Vampy III Main": EntranceData("Castle Vampy II Main", "Castle Vampy III Main", True),
    "Castle Vampy II NE -> Castle Vampy": EntranceData("Castle Vampy II NE", "Castle Vampy", True),
    "Castle Vampy II NE -> Castle Vampy III NE": EntranceData("Castle Vampy II NE", "Castle Vampy III NE", True),
    "Castle Vampy II SE -> Castle Vampy": EntranceData("Castle Vampy II SE", "Castle Vampy", True),
    "Castle Vampy II SE -> Castle Vampy III SE": EntranceData("Castle Vampy II SE", "Castle Vampy III SE", True),
    "Castle Vampy II SW -> Castle Vampy": EntranceData("Castle Vampy II SW", "Castle Vampy", True),
    "Castle Vampy II SW -> Castle Vampy III SW": EntranceData("Castle Vampy II SW", "Castle Vampy III SW", True),
    "Castle Vampy II NW -> Castle Vampy": EntranceData("Castle Vampy II NW", "Castle Vampy", True),
    "Castle Vampy II NW -> Castle Vampy III NW": EntranceData("Castle Vampy II NW", "Castle Vampy III NW", True),
    "Cabin In The Woods -> Halloween Hill": EntranceData("Cabin In The Woods", "Halloween Hill", True),
    "Castle Vampy III -> Castle Vampy II": EntranceData("Castle Vampy III", "Castle Vampy II", True),
    "Castle Vampy III -> Castle Vampy IV": EntranceData("Castle Vampy III", "Castle Vampy IV", True),
    "Castle Vampy III NE -> Castle Vampy II NE": EntranceData("Castle Vampy III NE", "Castle Vampy II NE", True),
    "Castle Vampy III NE -> Castle Vampy IV NE": EntranceData("Castle Vampy III NE", "Castle Vampy IV NE", True),
    "Castle Vampy III SE -> Castle Vampy II SE": EntranceData("Castle Vampy III SE", "Castle Vampy II SE", True),
    "Castle Vampy III SE -> Castle Vampy IV SE": EntranceData("Castle Vampy III SE", "Castle Vampy IV SE", True),
    "Castle Vampy III SW -> Castle Vampy II SW": EntranceData("Castle Vampy III SW", "Castle Vampy II SW", True),
    "Castle Vampy III SW -> Castle Vampy IV SW": EntranceData("Castle Vampy III SW", "Castle Vampy IV SW", True),
    "Castle Vampy III NW -> Castle Vampy II NW": EntranceData("Castle Vampy III NW", "Castle Vampy II NW", True),
    "Castle Vampy III NW -> Castle Vampy IV NW": EntranceData("Castle Vampy III NW", "Castle Vampy IV NW", True),
    "Castle Vampy IV -> Castle Vampy III": EntranceData("Castle Vampy IV", "Castle Vampy III", True),
    "Castle Vampy IV -> The Heart Of Terror": EntranceData("Castle Vampy IV", "The Heart Of Terror", True),
    "Castle Vampy IV NE -> Castle Vampy III NE": EntranceData("Castle Vampy IV NE", "Castle Vampy III NE", True),
    "Castle Vampy IV NE -> Castle Vampy Roof NE": EntranceData("Castle Vampy IV NE", "Castle Vampy Roof NE", True),
    "Castle Vampy IV SE -> Castle Vampy III SE": EntranceData("Castle Vampy IV SE", "Castle Vampy III SE", True),
    "Castle Vampy IV SE -> Castle Vampy Roof SE": EntranceData("Castle Vampy IV SE", "Castle Vampy Roof SE", True),
    "Castle Vampy IV SW -> Castle Vampy III SW": EntranceData("Castle Vampy IV SW", "Castle Vampy III SW", True),
    "Castle Vampy IV SW -> Castle Vampy Roof SW": EntranceData("Castle Vampy IV SW", "Castle Vampy Roof SW", True),
    "Castle Vampy IV NW -> Castle Vampy III NW": EntranceData("Castle Vampy IV NW", "Castle Vampy III NW", True),
    "Castle Vampy IV Nw -> Castle Vampy Roof NW": EntranceData("Castle Vampy IV NW", "Castle Vampy Roof NW", True),
    "A Cabin Collector -> Halloween Hill": EntranceData("A Cabin Collector", "Halloween Hill", True),
    "Castle Vampy Roof NE -> Castle Vampy IV NE": EntranceData("Castle Vampy Roof", "Castle Vampy IV", True),
    "Castle Vampy Roof SE -> Castle Vampy IV SE": EntranceData("Castle Vampy Roof", "Castle Vampy IV", True),
    "Castle Vampy Roof SW -> Castle Vampy IV SW": EntranceData("Castle Vampy Roof", "Castle Vampy IV", True),
    "Castle Vampy Roof NW -> Castle Vampy IV NW": EntranceData("Castle Vampy Roof", "Castle Vampy IV", True),
    "The Evilizer -> Halloween Hill": EntranceData("The Evilizer", "Halloween Hill", True),
    "The Heart Of Terror -> The Evilizer": EntranceData("The Heart Of Terror", "The Evilizer", True),
    "A Hidey-Hole -> Halloween Hill": EntranceData("A Hidey-Hole", "Halloween Hill", True),
    "Empty Rooftop -> Halloween Hill": EntranceData("Empty Rooftop", "Halloween Hill", True),
    "Swampdog Lair -> Halloween Hill": EntranceData("Swampdog Lair", "Halloween Hill", True),
    "Larry's Lair -> Halloween Hill": EntranceData("Larry's Lair", "Halloween Hill", True),

    #logical zone connections, cant be randomized

    "Halloween Hill -> Slurpy Swamp Mud": EntranceData("Halloween Hill", "Slurpy Swamp Mud", False),
    "Slurpy Swamp Mud -> Halloween Hill": EntranceData("Slurpy Swamp Mud", "Halloween Hill", False),

    "Zombiton -> Halloween Hill": EntranceData("Zombiton", "Halloween Hill", False), #one way
    #"Halloween Hill -> Zombiton": EntranceData("Halloween Hill", "Zombiton ", False), todo possible with badges

    "Halloween Hill -> Rocky Cliffs": EntranceData("Halloween Hill", "Rocky Cliffs", False),
    "Rocky Cliffs -> Halloween Hill": EntranceData("Rocky Cliffs", "Halloween Hill", False),

    "Vampy Land -> Halloween Hill": EntranceData("Vampy Land", "Halloween Hill", False), #one way
    #"Halloween Hill -> Vampy Land": EntranceData("Halloween Hill", "Vampy Land", False), TODO possible with badges/rando

    "Underground Tunnel Top -> Underground Tunnel Mud":
        EntranceData("Underground Tunnel Top", "Underground Tunnel Mud", False),
    "Underground Tunnel Mud -> Underground Tunnel Top":
        EntranceData("Underground Tunnel Mud", "Underground Tunnel Top", False),
    "Underground Tunnel Mud -> Underground Tunnel Zombie":
        EntranceData("Underground Tunnel Mud", "Underground Tunnel Zombie", False), #one way
    #"Underground Tunnel Zombie -> Underground Tunnel Mud":
    #    EntranceData("Underground Tunnel Mud", "Underground Tunnel Zombie", False),  # TODO possible with badges/bridge rando

    "Swamp Gas Cavern Front -> Swamp Gas Cavern Back":
        EntranceData("Swamp Gas Cavern Front", "Swamp Gas Cavern Back", False),  # one way
    #"Swamp Gas Cavern Back -> Swamp Gas Cavern Front":
    #    EntranceData("Swamp Gas Cavern Back", "Swamp Gas Cavern Front", False),  # TODO possible with badges


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



}