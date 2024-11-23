from typing import NamedTuple, Dict, Set, Optional

from BaseClasses import Item
from BaseClasses import ItemClassification as IC


class LMItemData(NamedTuple):
    type: str
    code: Optional[int]
    classification: IC
    quantity: int = 1
    doorid: Optional[int] = None


class LMItem(Item):
    game: str = "Luigi's Mansion"
    doorid: Optional[int] = None

    def __init__(self, name: str, player: int, data: LMItemData, force_nonprogress: bool):
        adjusted_classification = IC.filler if force_nonprogress else data.classification
        super(LMItem, self).__init__(name, adjusted_classification, LMItem.get_apid(data.code), player)

        self.type = data.type
        self.item_id = data.code
        self.doorid = data.doorid

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
    "Parlor Key": LMItemData("Door Key", 4, IC.progression, doorid=34),
    "Anteroom Key": LMItemData("Door Key", 5, IC.progression, doorid=38),
    "Wardrobe Key": LMItemData("Door Key", 6, IC.progression, doorid=43),
    "Front Hallway Key": LMItemData("Door Key", 7, IC.progression, doorid=33),
    "Master Bedroom Key": LMItemData("Door Key", 8, IC.progression, doorid=31),
    "Nursery Key": LMItemData("Door Key", 9, IC.progression, doorid=27),
    "Twins Bedroom Key": LMItemData("Door Key", 10, IC.progression, doorid=28),
    "Ballroom Key": LMItemData("Door Key", 11, IC.progression, doorid=15),
    "Storage Room Key": LMItemData("Door Key", 12, IC.progression, doorid=16),
    "Fortune Teller Key": LMItemData("Door Key", 13, IC.progression, doorid=4),
    "Laundry Key": LMItemData("Door Key", 14, IC.progression, doorid=7),
    "Lower 2F Stairwell Key": LMItemData("Door Key", 15, IC.progression, doorid=74),
    "Conservatory Key": LMItemData("Door Key", 16, IC.progression, doorid=21),
    "Dining Room Key": LMItemData("Door Key", 17, IC.progression, doorid=14),
    "North Rec Room Key": LMItemData("Door Key", 18, IC.progression, doorid=25),
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
    "Wardrobe Balcony Key": LMItemData("Door Key", 54, IC.progression, doorid=41),
    "2F Front Hallway Key": LMItemData("Door Key", 55, IC.progression, doorid=33),
    "Study Key": LMItemData("Door Key", 57, IC.progression, doorid=32),
    "Basement Stairwell Key": LMItemData("Door Key", 61, IC.progression, doorid=9),
    "1F Bathroom Key": LMItemData("Door Key", 64, IC.progression, doorid=23),
    "1F Washroom Key": LMItemData("Door Key", 67, IC.progression, doorid=20),
    "Kitchen Key": LMItemData("Door Key", 75, IC.progression, doorid=11),
    "Boneyard Key": LMItemData("Door Key", 76, IC.progression, doorid=10),
    "Projection Room Key": LMItemData("Door Key", 77, IC.progression, doorid=18),
    "Mirror Room Key": LMItemData("Door Key", 78, IC.progression, doorid=5),
    "Butler's Room Key": LMItemData("Door Key", 79, IC.progression, doorid=1),
    "Tea Room Key": LMItemData("Door Key", 81, IC.progression, doorid=47),
    "South Rec Room Key": LMItemData("Door Key", 82, IC.progression, doorid=24),
    "Upper 2F Stairwell Key": LMItemData("Door Key", 83, IC.progression, doorid=75),
    "2F Bathroom Key": LMItemData("Door Key", 84, IC.progression, doorid=48),
    "2F Washroom Key": LMItemData("Door Key", 85, IC.progression, doorid=45),
    "Nana's Room Key": LMItemData("Door Key", 86, IC.progression, doorid=49),
    "Astral Hall Key": LMItemData("Door Key", 87, IC.progression, doorid=44),
    "Observatory Key": LMItemData("Door Key", 90, IC.progression, doorid=40),
    "Guest Room": LMItemData("Door Key", 91, IC.progression, doorid=30),
    "3F Right Hallway Key": LMItemData("Door Key", 92, IC.progression, doorid=55),
    "Telephone Room Key": LMItemData("Door Key", 97, IC.progression, doorid=52),
    "Ceramics Studio Key": LMItemData("Door Key", 99, IC.progression, doorid=50),
    "Breaker Room Key": LMItemData("Door Key", 100, IC.progression, doorid=71),
    "Basement Hallway Key": LMItemData("Door Key", 102, IC.progression, doorid=67),
    "Spade Hallway Key": LMItemData("Door Key", 105, IC.progression, doorid=70),
}

filler_items: Dict[str, LMItemData] = {
    # "10 Coins": LMItemData("Filler", 52, IC.filler),
    # "10 Bills": LMItemData("Filler", 53, IC.filler),
    "Money Bundle": LMItemData("Filler", 41, IC.filler),
    # "Gold Bar": LMItemData("Filler", 56, IC.filler),
    # "Sapphire": LMItemData("Filler", 58, IC.filler),
    # "Emerald": LMItemData("Filler", 59, IC.filler),
    # "Ruby": LMItemData("Filler", 60, IC.filler),
    # "Diamond": LMItemData("Filler", 62, IC.filler),
    "Poison Mushroom": LMItemData("Trap", 42, IC.trap),
    #"Ghost": LMItemData("Trap", 43, IC.trap),
    "Nothing": LMItemData("Filler", 44, IC.filler),
    "Small Heart": LMItemData("Filler", 45, IC.filler),
    "Large Heart": LMItemData("Filler", 47, IC.filler),
    "Bomb": LMItemData("Trap", 50, IC.trap)
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
