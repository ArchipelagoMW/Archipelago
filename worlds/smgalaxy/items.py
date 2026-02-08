from BaseClasses import Item
from BaseClasses import ItemClassification as IC
from typing import NamedTuple, Optional

class SMGItemData(NamedTuple):
    type: str
    code: Optional[int]
    classification: IC
    other_variable: Optional[int] = None

# this lets us use these items by using SMGItem.
class SMGItem(Item):
    game: str = "Super Mario Galaxy"

    def __init__(self, name: str, player: int, data: SMGItemData):
        super(SMGItem, self).__init__(name, data.classification, data.code, player)

        self.type = data.type
        self.item_id = data.code
# This is all the items that are used by the game we define them here so they can be used.


item_table: dict[str, SMGItemData] = {
  "Power Star": SMGItemData("Power Star", 170000004, IC.progression_deprioritized_skip_balancing),# rom address  0x007ACCA0F2FF8760 don't remeber how i found this or if it's acurate so could use double check.
  "Progressive Grand Star": SMGItemData("Grand Star", 170000005, IC.progression),
  "Green Star": SMGItemData("Green Star", 170000006, IC.progression),
  "Nothing": SMGItemData("Nothing Item", 170000007, IC.filler),
  "Progressive Comets": SMGItemData("Comet", 170000008, IC.progression),
  "Peach": SMGItemData("Victory", None, IC.progression)
}

ITEM_NAME_TO_ID: dict[str, int] =  {
    name: SMGItem.code for name, data in item_table.items() if data.code is not None}