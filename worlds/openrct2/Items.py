from BaseClasses import Item
from typing import NamedTuple, Dict
from .Constants import *

class OpenRCT2Item(Item):
    game: str = "OpenRCT2"
    

openRCT2_items = ForestFrontiers
item_table = {name: [base_id + count, True] for count, name in enumerate(openRCT2_items)}



