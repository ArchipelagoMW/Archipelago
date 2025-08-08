# Look at init or Items.py for more information on imports
from typing import Dict, TYPE_CHECKING
import logging

from .Types import LocData

if TYPE_CHECKING:
    from . import HexcellsInfiniteWorld

# This is technique in programming to make things more readable for booleans
# A boolean is true or false
# def did_include_extra_locations(world: "HexcellsInfiniteWorld") -> bool:
#     return bool(world.options.ExtraLocations)

# This is used by ap and in Items.py
# Theres a multitude of reasons to need to grab how many locations there are
def get_total_locations(world: "HexcellsInfiniteWorld") -> int:
    # This is the total that we'll keep updating as we count how many locations there are
    total = 0
    for name in location_table:
        # If we did not turn on extra locations (see how readable it is with that thing from the top)
        # AND the name of it is found in our extra locations table, then that means we dont want to count it
        # So continue moves onto the next name in the table
        # if not did_include_extra_locations(world) and name in extra_locations:
        #     continue

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
    # if not did_include_extra_locations(world) and name in extra_locations:
    #     return False
    # if not did_include_extra_locations(world):
    #     return False
    
    return True

# You might need more functions as well so be liberal with them
# My advice, if you are about to type the same thing in a second time, turn it into a function
# Even if you only do it once you can turn it into a function too for organization

# Heres where you do the next fun part of listing out all those locations
# Its a lot
# My advice, zone out for half an hour listening to music and hope you wake up to a completed list
hexcells_infinite_locations = {
    # You can take a peak at Types.py for more information but,
    # LocData is code, region in this instance
    # Regions will be explained more in Regions.py
    # But just know that it's mostly about organization
    # Place locations together based on where they are in the game and what is needed to get there
    # "A Fake Location Name": LocData(20050100, "Bucharest"),
    # "A really good restaurant": LocData(20050101, "Brașov"),
    # "Nuketown": LocData(20050103, "Green Hill Zone - Act 1"),
    # "Nuketown 2": LocData(20050104, "Green Hill Zone - Act 1"),
    # "Talk to Sonic": LocData(20050105, "Green Hill Zone - Act 2"),
    # "Talk to Captain Price": LocData(20050106, "Green Hill Zone - Act 3"),
    # "TMNT Hangout Spot": LocData(20050107, "The Sewer"),
    # "Above TMNT Hangout Spot": LocData(20050108, "The Sewer"),
    # "Coughing Baby Pickup": LocData(20050109, "The Sewer"), 
    "Level 1": LocData(75001, "Level Group 1"),
    "Level 2": LocData(75002, "Level Group 1"),
    "Level 3": LocData(75003, "Level Group 1"),
    "Level 4": LocData(75004, "Level Group 1"),
    "Level 5": LocData(75005, "Level Group 1"),
    "Level 6": LocData(75006, "Level Group 1"),

    "Level 7": LocData(75007, "Level Group 2"),
    "Level 8": LocData(75008, "Level Group 2"),
    "Level 9": LocData(75009, "Level Group 2"),
    "Level 10": LocData(75010, "Level Group 2"),
    "Level 11": LocData(75011, "Level Group 2"),
    "Level 12": LocData(75012, "Level Group 2"),

    "Level 13": LocData(75013, "Level Group 3"),
    "Level 14": LocData(75014, "Level Group 3"),
    "Level 15": LocData(75015, "Level Group 3"), 
    "Level 16": LocData(75016, "Level Group 3"),
    "Level 17": LocData(75017, "Level Group 3"),
    "Level 18": LocData(75018, "Level Group 3"),

    "Level 19": LocData(75019, "Level Group 4"),
    "Level 20": LocData(75020, "Level Group 4"),
    "Level 21": LocData(75021, "Level Group 4"),
    "Level 22": LocData(75022, "Level Group 4"),
    "Level 23": LocData(75023, "Level Group 4"),
    "Level 24": LocData(75024, "Level Group 4"),

    "Level 25": LocData(75025, "Level Group 5"),
    "Level 26": LocData(75026, "Level Group 5"),
    "Level 27": LocData(75027, "Level Group 5"),
    "Level 28": LocData(75028, "Level Group 5"),
    "Level 29": LocData(75029, "Level Group 5"),
    "Level 30": LocData(75030, "Level Group 5"),

    "Level 31": LocData(75031, "Level Group 6"),
    "Level 32": LocData(75032, "Level Group 6"),
    "Level 33": LocData(75033, "Level Group 6"),
    "Level 34": LocData(75034, "Level Group 6"),
    "Level 35": LocData(75035, "Level Group 6"),
    "Level 36": LocData(75036, "Level Group 6")

}

# extra_locations = {
#     "ml7's house": LocData(20050102, "Sibiu"),
# }

# Like in Items.py, breaking up the different locations to help with organization and if something special needs to happen to them
# event_locations = {
#     "Beat Final Boss": LocData(20050110, "Big Hole in the Floor")
# }

# Also like in Items.py, this collects all the dictionaries together
# Its important to note that locations MUST be bigger than progressive item count and should be bigger than total item count
# Its not here because this is an example and im not funny enough to think of more locations
# But important to note
location_table = {
    **hexcells_infinite_locations,
    # **extra_locations,
    # **event_locations
}