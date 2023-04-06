from BaseClasses import Item
from typing import Dict
from .locations import SMGLocationData

# this lets us use these items by using SMGItem.
class SMGItem(Item):
    game: str = "Super Mario Galaxy"
# This is all the items that are used by the game we define them here so the they can be used.

item_table: Dict[str, SMGLocationData] = {
  "Power Star": 170000000, # rom address  0x007ACCA0F2FF8760
  "Grand Star Terrace": 170000001,
  "Grand Star Fountain": 170000002,
  "Grand Star Kitchen": 170000003,
  "Grand Star Bedroom": 170000004,
  "Grand Star Engine Room": 170000005,
  "Green Star": 170000006,
  "Nothing": 170000007,
  "Peach": 170000008
}
