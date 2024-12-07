from typing import NamedTuple, Dict, List

from BaseClasses import Region


class LoonylandRegion(Region):
    game = "Loonyland"


class LoonylandRegionData(NamedTuple):
    id: int
    real: bool
    map: str

loonyland_region_table: Dict[str, LoonylandRegionData] = {
    "Menu": LoonylandRegionData(0, False, ""),
        "Halloween Hill": LoonylandRegionData(0, False, "Halloween Hill"),
        "Slurpy Swamp Mud": LoonylandRegionData(0, False, "Halloween Hill"),
        "Zombiton": LoonylandRegionData(0, False, "Halloween Hill"),
        "Rocky Cliffs": LoonylandRegionData(0, False, "Halloween Hill"),
        "Vampy Land": LoonylandRegionData(0, False, "Halloween Hill"),
    "A Cabin Trees": LoonylandRegionData(0, True, "A Cabin"),
        "The Witch's Cabin Front": LoonylandRegionData(0, False, "The Witch's Cabin"),
        "The Witch's Cabin Back": LoonylandRegionData(0, False, "The Witch's Cabin"),
    "Bonita's Cabin": LoonylandRegionData(0, True, ""),
    "The Bog Pit": LoonylandRegionData(0, True, ""),
    "Underground Tunnel Top": LoonylandRegionData(0, True, ""),
        "Underground Tunnel Mud": LoonylandRegionData(0, False, "Underground Tunnel"),
        "Underground Tunnel Zombie": LoonylandRegionData(0, False, "Underground Tunnel"),
        "Swamp Gas Cavern Front": LoonylandRegionData(0, False, "Swamp Gas Cavern"),
        "Swamp Gas Cavern Back": LoonylandRegionData(0, False, "Swamp Gas Cavern"),
    "A Tiny Cabin": LoonylandRegionData(0, True, ""),
    "A Cabin Seer": LoonylandRegionData(0, True, ""),
    "Benny's Cocktails": LoonylandRegionData(0, True, ""),
    "Dusty Crypt": LoonylandRegionData(0, True, ""),
    "Musty Crypt": LoonylandRegionData(0, True, ""),
    "Rusty Crypt": LoonylandRegionData(0, True, ""),
    "A Messy Cabin": LoonylandRegionData(0, True, ""),
    "Under the Lake": LoonylandRegionData(0, True, ""),
    "Deeper Under the Lake": LoonylandRegionData(0, True, ""),
    "Frankenjulie's Laboratory": LoonylandRegionData(0, True, ""),
    "Haunted Tower": LoonylandRegionData(0, True, ""),
    "Haunted Tower, Floor 2": LoonylandRegionData(0, True, ""),
    "Haunted Tower, Floor 3": LoonylandRegionData(0, True, ""),
    "Haunted Tower Roof": LoonylandRegionData(0, True, ""),
    "Haunted Basement": LoonylandRegionData(0, True, ""),
    "Abandoned Mines": LoonylandRegionData(0, True, ""),
    "The Shrine of Bombulus": LoonylandRegionData(0, True, ""),
    "A Gloomy Cavern": LoonylandRegionData(0, True, ""),
    "Happy Stick Woods": LoonylandRegionData(0, True, ""),
    "The Wolf Den": LoonylandRegionData(0, True, ""),
    "A Cabin Larry": LoonylandRegionData(0, True, ""),
    "Upper Creepy Cavern": LoonylandRegionData(0, True, ""),
    "Under the Ravine": LoonylandRegionData(0, True, ""),
        "Creepy Caverns Left": LoonylandRegionData(0, False, "Creepy Caverns Left"),
        "Creepy Caverns Middle": LoonylandRegionData(0, False, "Creepy Caverns Middle"),
        "Creepy Caverns Right": LoonylandRegionData(0, False, "Creepy Caverns Right"),
    "Castle Vampy": LoonylandRegionData(0, True, ""),
        "Castle Vampy II Main": LoonylandRegionData(0, False, "Castle Vampy II"),
        "Castle Vampy II NW": LoonylandRegionData(0, False, "Castle Vampy II"),
        "Castle Vampy II NE": LoonylandRegionData(0, False, "Castle Vampy II"),
        "Castle Vampy II SW": LoonylandRegionData(0, False, "Castle Vampy II"),
        "Castle Vampy II SE": LoonylandRegionData(0, False, "Castle Vampy II"),
    "Cabin in the woods": LoonylandRegionData(0, True, ""),
        "Castle Vampy III Main": LoonylandRegionData(0, False, "Castle Vampy III"),
        "Castle Vampy III NW": LoonylandRegionData(0, False, "Castle Vampy III"),
        "Castle Vampy III NE": LoonylandRegionData(0, False, "Castle Vampy III"),
        "Castle Vampy III SW": LoonylandRegionData(0, False, "Castle Vampy III"),
        "Castle Vampy III SE": LoonylandRegionData(0, False, "Castle Vampy III"),
        "Castle Vampy IV Main": LoonylandRegionData(0, False, "Castle Vampy IV"),
        "Castle Vampy IV NW": LoonylandRegionData(0, False, "Castle Vampy IV"),
        "Castle Vampy IV NE": LoonylandRegionData(0, False, "Castle Vampy IV"),
        "Castle Vampy IV SW": LoonylandRegionData(0, False, "Castle Vampy IV"),
        "Castle Vampy IV SE": LoonylandRegionData(0, False, "Castle Vampy IV"),
    "A Cabin Collector": LoonylandRegionData(0, True, ""),
    "Castle Vampy Roof NE": LoonylandRegionData(0, True, ""),
    "Castle Vampy Roof SE": LoonylandRegionData(0, True, ""),
    "Castle Vampy Roof SW": LoonylandRegionData(0, True, ""),
    "Castle Vampy Roof NW": LoonylandRegionData(0, True, ""),
    "The Evilizer": LoonylandRegionData(0, True, ""),
    "Heart of Terror": LoonylandRegionData(0, True, ""),
    "A Hidey Hole": LoonylandRegionData(0, True, ""),
    "Empty Rooftop": LoonylandRegionData(0, True, ""),
    "Swampdog Lair": LoonylandRegionData(0, True, ""),
    "Larry's Lair": LoonylandRegionData(0, True, ""),

    #gamemodes
        "Bowling": LoonylandRegionData(0, False, ""),
        "Survival": LoonylandRegionData(0, False, ""),
        "Boss Bash": LoonylandRegionData(0, False, ""),
        "Loony Ball": LoonylandRegionData(0, False, ""),
        "Remix": LoonylandRegionData(0, False, ""),
    #"Bowling",
    #"Survival",
    #"Boss Bash",
    #"Loony Ball",
    #"Remix"
}
