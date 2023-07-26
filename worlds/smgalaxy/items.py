from BaseClasses import Item
from typing import Dict
from .locations import SMGLocationData

# this lets us use these items by using SMGItem.
class SMGItem(Item):
    game: str = "Super Mario Galaxy"
# This is all the items that are used by the game we define them here so the they can be used.

item_table: Dict[str, SMGLocationData] = {
  "Power Star": 170000004, # rom address  0x007ACCA0F2FF8760
  "Progressive Grand Star": 170000005,
  "Green Star": 170000006,
  "Nothing": 170000007,
  "Peach": 170000008
}
