"""
Defines progression, junk and event items for The Witness
"""

from typing import Dict, NamedTuple, Optional

from BaseClasses import Item
from worlds.witness.locations import WitnessLocations
from worlds.witness.rules import WitnessLogic


class ItemData(NamedTuple):
    """
    ItemData for an item in The Witness
    """
    code: Optional[int]
    progression: bool
    event: bool = False


class WitnessItem(Item):
    """
    Item from the game The Witness
    """

    game: str = "The Witness"


class WitnessItems():
    """Class that handles Witness items"""
    def __init__(self, early_logic: WitnessLogic):
        self.ITEM_TABLE: Dict[str, ItemData] = {
            # Event Items
            'Victory': ItemData(158700, True, True)
        }
        self.locat = None

        self.EVENT_ITEM_TABLE = dict()

        self.JUNK_WEIGHTS = {
            "Speed Boost": 1,
            "Slowness Trap": 0.8,
            "Power Surge Trap": 0.2,
        }

        self.logic = early_logic

        for item in self.logic.ALL_ITEMS:
            if item[0] == "11 Lasers" or item == "7 Lasers":
                continue

            self.ITEM_TABLE[item[0]] = ItemData(158000 + item[1], True, False)

        for item in self.logic.ALL_TRAPS:
            self.ITEM_TABLE[item[0]] = ItemData(158000 + item[1], False, False)

        for item in self.logic.ALL_BOOSTS:
            self.ITEM_TABLE[item[0]] = ItemData(158000 + item[1], False, False)
            
        self.ITEM_TABLE = dict(sorted(self.ITEM_TABLE.items(),
                                      key=lambda item: item[1].code
                                      if isinstance(item[1].code, int) else 0))
        
    def adjust_after_options(self, locat):
        """Adds event items after logic changes due to options"""

        self.locat = locat

        for event_location in self.locat.EVENT_LOCATION_TABLE:
            location = self.logic.EVENT_ITEM_PAIRS[event_location]
            self.EVENT_ITEM_TABLE[location] = ItemData(None, True, True)
            self.ITEM_TABLE[location] = ItemData(None, True, True)

        self.JUNK_WEIGHTS = {key: value for (key, value)
                             in self.JUNK_WEIGHTS.items()
                             if key in self.ITEM_TABLE.keys()}
