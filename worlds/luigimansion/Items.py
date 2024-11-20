from enum import Enum
from typing import NamedTuple, Dict, Set, Optional

from BaseClasses import Item
from BaseClasses import ItemClassification as IC


class LMItemData(NamedTuple):
    type: str
    code: Optional[int]
    classification: IC
    quantity: int = 1
    doorid: Optional[int] = None
    DME_item_id: Optional[int] = None  # potentially use when we figure out how to receive items in game


class LMItem(Item):
    game: str = "Luigi's Mansion"

    def __init__(self, name: str, player: int, data: LMItemData, force_nonprogress: bool):
        adjusted_classification = IC.filler if force_nonprogress else data.classification
        super(LMItem, self).__init__(name, adjusted_classification, LMItem.get_apid(data.code), player)

        self.type = data.type
        self.item_id = data.code

    @staticmethod
    def get_apid(code: int):
        base_id: int = 8000
        return base_id + code if code is not None else None


# class LMRandoItems(Enum):
#     HeartKey = "Heart Key"


ITEM_TABLE: dict[str, LMItemData] = {
    "Heart Key": LMItemData("Door Key", 0, IC.progression, doorid=3),
    "Club Key": LMItemData("Door Key", 1, IC.progression, doorid=42),
    "Diamond Key": LMItemData("Door Key", 2, IC.progression, doorid=59),
    "Spade Key": LMItemData("Door Key", 3, IC.progression, doorid=72),
    "Parlor Key": LMItemData("Door Key", 4, IC.progression),
    "Anteroom Key": LMItemData("Door Key", 5, IC.progression, doorid=38),
    # "Wardrobe Key":        LMItemData("Door Key",   06), does not actually exist
    "Front Hallway Key": LMItemData("Door Key", 7, IC.progression, doorid=33),
    "Master Bedroom Key": LMItemData("Door Key", 8, IC.progression, doorid=31),
    "Nursery Key": LMItemData("Door Key", 9, IC.progression, doorid=27),
    "Twins Bedroom Key": LMItemData("Door Key", 10, IC.progression, doorid=28),
    "Ballroom Key": LMItemData("Door Key", 11, IC.progression, doorid=15),
    "Storage Room Key": LMItemData("Door Key", 12, IC.progression, doorid=16),
    "Fortune Teller Key": LMItemData("Door Key", 13, IC.progression, doorid=4),
    "Laundry Key": LMItemData("Door Key", 14, IC.progression, doorid=7),
    "2F Stairwell Key": LMItemData("Door Key", 15, IC.progression, doorid=74),
    "Conservatory Key": LMItemData("Door Key", 16, IC.progression, doorid=14),
    "Dining Room Key": LMItemData("Door Key", 17, IC.progression, doorid=14),
    "Rec Room Key": LMItemData("Door Key", 18, IC.progression, doorid=25),
    "Billiards Key": LMItemData("Door Key", 19, IC.progression, doorid=17),
    "Safari Key": LMItemData("Door Key", 20, IC.progression, doorid=56),
    "Balcony Key": LMItemData("Door Key", 21, IC.progression, doorid=62),
    "Breaker Key": LMItemData("Door Key", 22, IC.progression, doorid=71),
    "Cellar Key": LMItemData("Door Key", 23, IC.progression, doorid=68),
    "Clockwork Key": LMItemData("Door Key", 24, IC.progression, doorid=53),
    "Armory Key": LMItemData("Door Key", 25, IC.progression, doorid=51),
    "Sitting Room Key": LMItemData("Door Key", 26, IC.progression, doorid=29),
    "Pipe Room Key": LMItemData("Door Key", 27, IC.progression, doorid=69),
    "Cold Storage Key": LMItemData("Door Key", 28, IC.progression, doorid=65),
    "Art Studio Key": LMItemData("Door Key", 29, IC.progression, doorid=63),
    "Fire Element Medal": LMItemData("Medal", 30, IC.progression),
    "Water Element Medal": LMItemData("Medal", 31, IC.progression),
    "Ice Element Medal": LMItemData("Medal", 32, IC.progression),
    "Mario's Glove": LMItemData("Mario Item", 33, IC.progression),
    "Mario's Hat": LMItemData("Mario Item", 34, IC.progression),
    "Mario's Letter": LMItemData("Mario Item", 35, IC.progression),
    "Mario's Star": LMItemData("Mario Item", 36, IC.progression),
    "Mario's Shoe": LMItemData("Mario Item", 37, IC.progression),
    "Boo": LMItemData("Boo Item", 38, IC.progression, 35),
    "Boo Radar": LMItemData("Upgrade", 39, IC.progression),
    "Poltergust 4000": LMItemData("Upgrade", 40, IC.useful),
    "Gold Diamond": LMItemData("Filler", 49, IC.progression, 5),
}

filler_items: Dict[str, LMItemData] = {
    "Money Bundle": LMItemData("Filler", 41, IC.filler),
    "Poison Mushroom": LMItemData("Trap", 42, IC.trap),
    "Ghost": LMItemData("Trap", 43, IC.trap),
    "Nothing": LMItemData("Filler", 44, IC.filler),
    "Small Heart": LMItemData("Filler", 45, IC.filler),
    "Medium Heart": LMItemData("Filler", 46, IC.filler),
    "Large Heart": LMItemData("Filler", 47, IC.filler)
}

ALL_ITEMS_TABLE = {**ITEM_TABLE,
                   **filler_items}

LOOKUP_ID_TO_NAME: dict[int, str] = {
    LMItem.get_apid(data.code): item for item, data in ALL_ITEMS_TABLE.items() if data.code is not None
}


def get_item_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in ALL_ITEMS_TABLE.items():
        categories.setdefault(data.type, set()).add(name)

    return categories
