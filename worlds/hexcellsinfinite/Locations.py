# Look at init or Items.py for more information on imports
from typing import Dict, TYPE_CHECKING
import logging
from . import Options

from .Types import LocData

if TYPE_CHECKING:
    from . import HexcellsInfiniteWorld


# This is used by ap and in Items.py
# Theres a multitude of reasons to need to grab how many locations there are
def get_total_locations(world: "HexcellsInfiniteWorld") -> int:
    # This is the total that we'll keep updating as we count how many locations there are
    total = 0
    for name in location_table:
        # If the location is valid though, count it
        if is_valid_location(world, name):
            total += 1

    return total

def get_location_names() -> Dict[str, int]:
    # This is just a fancy way of getting all the names and data in the location table and making a dictionary thats {name, code}
    # If you have dynamic locations then you want to add them to the dictionary as well
    names = {name: data.ap_code for name, data in location_table.items()}

    return names

# The check to make sure the location is valid
# I know it looks like the same as when we counted it but thats because this is an example
# Things get complicated fast so having a back up is nice
def is_valid_location(world: "HexcellsInfiniteWorld", name) -> bool:
    return True

# You might need more functions as well so be liberal with them
# My advice, if you are about to type the same thing in a second time, turn it into a function
# Even if you only do it once you can turn it into a function too for organization

# Heres where you do the next fun part of listing out all those locations
# Its a lot
# My advice, zone out for half an hour listening to music and hope you wake up to a completed list
# if(HexcellsInfiniteWorld.options.LevelUnlockType == Options.LevelUnlockType.option_vanilla):

hexcells_infinite_locations = {}


for world in range(1, 7):
    for level in range(1, 7):
        name = f"Hexcells {world}-{level}"
        hexcells_infinite_locations[name] = LocData(len(hexcells_infinite_locations)+1, f"{name}")



# elif(HexcellsInfiniteWorld.options.LevelUnlockType == Options.LevelUnlockType.option_individual):
#     hexcells_infinite_locations = {
#         # You can take a peak at Types.py for more information but,
#         # LocData is code, region in this instance
#         # Regions will be explained more in Regions.py
#         # But just know that it's mostly about organization
#         # Place locations together based on where they are in the game and what is needed to get there
#         "1-1": LocData(1, "1-1"),
#         "1-2": LocData(2, "1-2"),
#         "1-3": LocData(3, "1-3"),
#         "1-4": LocData(4, "1-4"),
#         "1-5": LocData(5, "1-5"),
#         "1-6": LocData(6, "1-6"),

#         "2-1": LocData(7, "2-1"),
#         "2-2": LocData(8, "2-2"),
#         "2-3": LocData(9, "2-3"),
#         "2-4": LocData(10, "2-4"),
#         "2-5": LocData(11, "2-5"),
#         "2-6": LocData(12, "2-6"),

#         "3-1": LocData(13, "3-1"),
#         "3-2": LocData(14, "3-2"),
#         "3-3": LocData(15, "3-3"), 
#         "3-4": LocData(16, "3-4"),
#         "3-5": LocData(17, "3-5"),
#         "3-6": LocData(18, "3-6"),

#         "4-1": LocData(19, "4-1"),
#         "4-2": LocData(20, "4-2"),
#         "4-3": LocData(21, "4-3"),
#         "4-4": LocData(22, "4-4"),
#         "4-5": LocData(23, "4-5"),
#         "4-6": LocData(24, "4-6"),

#         "5-1": LocData(25, "5-1"),
#         "5-2": LocData(26, "5-2"),
#         "5-3": LocData(27, "5-3"),
#         "5-4": LocData(28, "5-4"),
#         "5-5": LocData(29, "5-5"),
#         "5-6": LocData(30, "5-6"),

#         "6-1": LocData(31, "6-1"),
#         "6-2": LocData(32, "6-2"),
#         "6-3": LocData(33, "6-3"),
#         "6-4": LocData(34, "6-4"),
#         "6-5": LocData(35, "6-5"),
#         "6-6": LocData(36, "6-6")
#     }

# Also like in Items.py, this collects all the dictionaries together
# Its important to note that locations MUST be bigger than progressive item count and should be bigger than total item count
# Its not here because this is an example and im not funny enough to think of more locations
# But important to note
location_table = {
    **hexcells_infinite_locations,
}