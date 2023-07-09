from BaseClasses import Item, Location
from typing import NamedTuple, Dict
from .Constants import *
from .Items import *
from .Options import *
import random

#print(OpenRCT2Options["difficulty"])
NoPrereqs = []
openRCT2_locations = []

class OpenRCT2Location(Location):
    game = "OpenRCT2"

for index, item in enumerate(item_table):
    #if self.Options["difficulty"] == 0:
        #pass
    openRCT2_locations.append("OpenRCT2_" + str(index))


