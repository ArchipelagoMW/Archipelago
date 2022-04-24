"""
Defines progression, junk and event items for The Witness
"""

from typing import Dict, NamedTuple, Optional

from BaseClasses import Item
from worlds.witness.Options import is_option_enabled
from worlds.witness.locations import WitnessLocations
from worlds.witness.rules import WitnessLogic


class ItemData(NamedTuple):
    """
    ItemData for an item in The Witness
    """
    code: Optional[int]
    progression: bool
    event: bool = False
    trap: bool = False


class WitnessItem(Item):
    """
    Item from the game The Witness
    """
    game: str = "The Witness"


class WitnessItems():
    """Class that handles Witness items"""
    def __init__(self, early_logic: WitnessLogic):
        self.ITEM_TABLE: Dict[str, ItemData] = {
        }
        self.locat = None

        self.EVENT_ITEM_TABLE = dict()

        self.JUNK_WEIGHTS = {
            "Speed Boost": 1,
            "Slowness": 0.8,
            "Power Surge": 0.2,
        }

        self.logic = early_logic

        for item in self.logic.ALL_ITEMS:
            if item[0] == "11 Lasers" or item == "7 Lasers":
                continue

            self.ITEM_TABLE[item[0]] = ItemData(158000 + item[1], True, False)

        for item in self.logic.ALL_TRAPS:
            self.ITEM_TABLE[item[0]] = ItemData(
                158000 + item[1], False, False, True
            )

        for item in self.logic.ALL_BOOSTS:
            self.ITEM_TABLE[item[0]] = ItemData(158000 + item[1], False, False)
            
        self.ITEM_TABLE = dict(sorted(self.ITEM_TABLE.items(),
                                      key=lambda item: item[1].code
                                      if isinstance(item[1].code, int) else 0))
        
    def adjust_after_options(self, locat, world, player):
        """Adds event items after logic changes due to options"""

        self.GOOD_ITEMS = [
            "Dots", "Black/White Squares", "Stars",
            "Shapers", "Symmetry"
        ]

        if is_option_enabled(
            world, player, "shuffle_discarded_panels"
        ):
            self.GOOD_ITEMS.append("Triangles")
        if not is_option_enabled(
            world, player, "disable_non_randomized_puzzles"
        ):
            self.GOOD_ITEMS.append("Colored Squares")

        self.locat = locat

        for event_location in self.locat.EVENT_LOCATION_TABLE:
            location = self.logic.EVENT_ITEM_PAIRS[event_location]
            self.EVENT_ITEM_TABLE[location] = ItemData(None, True, True)
            self.ITEM_TABLE[location] = ItemData(None, True, True)

        self.JUNK_WEIGHTS = {key: value for (key, value)
                             in self.JUNK_WEIGHTS.items()
                             if key in self.ITEM_TABLE.keys()}
