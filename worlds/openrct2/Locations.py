from BaseClasses import Item, Location
from typing import NamedTuple, Dict
from .Constants import *
from .Items import *
from .Options import *
import random

#print(OpenRCT2Options["difficulty"])


class OpenRCT2Location(Location):
    game = "OpenRCT2"

def create_locations():
    NoPrereqs = []
    locations = []
    num_items = 0
    for item in item_frequency:
        num_items += item_frequency[item]

    counter = 0

    while counter != num_items:
        locations.append("OpenRCT2_" + str(counter))
        counter += 1
    return locations
# for index, item in enumerate(item_table):
#     #if self.Options["difficulty"] == 0:
#         #pass
#     openRCT2_locations.append("OpenRCT2_" + str(index))


