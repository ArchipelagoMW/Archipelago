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

# You might need more functions as well so be liberal with them
# My advice, if you are about to type the same thing in a second time, turn it into a function
# Even if you only do it once you can turn it into a function too for organization

# Heres where you do the next fun part of listing out all those locations
# Its a lot
# My advice, zone out for half an hour listening to music and hope you wake up to a completed list

hexcells_infinite_locations = {}


for worldNum in range(1, 7):
    for levelNum in range(1, 7):
        name = f"Hexcells {worldNum}-{levelNum}"
        hexcells_infinite_locations[name] = LocData(len(hexcells_infinite_locations)+1, f"Level Group {worldNum}")


for worldNum in range(1, 7):
    for levelNum in range(1, 7):
        name = f"Hexcells Level {worldNum}-{levelNum}"
        hexcells_infinite_locations[name] = LocData(len(hexcells_infinite_locations)+1, f"{name}")


# Also like in Items.py, this collects all the dictionaries together
# It's important to note that locations MUST be bigger than progressive item count and should be greater or equal to the total item count
# It's not here because this is an example and I'm not funny enough to think of more locations
# But important to note
location_table = {
    **hexcells_infinite_locations,
}
