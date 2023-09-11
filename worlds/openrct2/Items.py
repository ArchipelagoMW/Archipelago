from BaseClasses import Item
from typing import NamedTuple, Dict
from .Constants import *
from .Options import *


class OpenRCT2Item(Item):
    game: str = "OpenRCT2"



openRCT2_items = ForestFrontiers
item_table = {name: [base_id + count, True] for count, name in enumerate(openRCT2_items)}
item_frequency = {}
for ride in openRCT2_items:
    found = False
    for item in item_frequency:
        if ride == item:
            item_frequency[item] += 1
            found = True
            break
    if not found:
        item_frequency[ride] = 1
