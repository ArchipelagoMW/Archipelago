from typing import NamedTuple, Dict, Set, Optional

from BaseClasses import Item
from BaseClasses import ItemClassification as IC


class LMItemData(NamedTuple):
    type: str
    code: Optional[int]
    classification: IC
    doorid: Optional[int] = None
    itembit: Optional[int] = None
    address: Optional[int] = None


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


ITEM_TABLE: dict[str, LMItemData] = {
    "Heart Key": LMItemData("Door Key", 0, IC.progression,  3),
    "Club Key": LMItemData("Door Key", 1, IC.progression,  42),
    "Diamond Key": LMItemData("Door Key", 2, IC.progression,  59),
    "Spade Key": LMItemData("Door Key", 3, IC.progression,  72),
    "Parlor Key": LMItemData("Door Key", 4, IC.progression,  34),
    "Anteroom Key": LMItemData("Door Key", 5, IC.progression,  38),
    "Wardrobe Key": LMItemData("Door Key", 6, IC.progression,  43),
    "2F Front Hallway Key": LMItemData("Door Key", 7, IC.progression,  33),
    "Master Bedroom Key": LMItemData("Door Key", 8, IC.progression,  31),
    "Nursery Key": LMItemData("Door Key", 9, IC.progression,  27),
    "Twins Bedroom Key": LMItemData("Door Key", 10, IC.progression,  28),
    "Ballroom Key": LMItemData("Door Key", 11, IC.progression,  15),
    "Storage Room Key": LMItemData("Door Key", 12, IC.progression,  16),
    "Fortune Teller Key": LMItemData("Door Key", 13, IC.progression,  4),
    "Laundry Key": LMItemData("Door Key", 14, IC.progression,  7),
    "Lower 2F Stairwell Key": LMItemData("Door Key", 15, IC.progression,  74),
    "Conservatory Key": LMItemData("Door Key", 16, IC.progression,  21),
    "Dining Room Key": LMItemData("Door Key", 17, IC.progression,  14),
    "North Rec Room Key": LMItemData("Door Key", 18, IC.progression,  25),
    "Billiards Key": LMItemData("Door Key", 19, IC.progression,  17),
    "Safari Key": LMItemData("Door Key", 20, IC.progression,  56),
    "Balcony Key": LMItemData("Door Key", 21, IC.progression,  62),
    "Breaker Key": LMItemData("Door Key", 22, IC.progression,  71),
    "Cellar Key": LMItemData("Door Key", 23, IC.progression,  68),
    "Clockwork Key": LMItemData("Door Key", 24, IC.progression,  53),
    "Armory Key": LMItemData("Door Key", 25, IC.progression,  51),
    "Sitting Room Key": LMItemData("Door Key", 26, IC.progression,  29),
    "Pipe Room Key": LMItemData("Door Key", 27, IC.progression,  69),
    "Cold Storage Key": LMItemData("Door Key", 28, IC.progression,  65),
    "Art Studio Key": LMItemData("Door Key", 29, IC.progression,  63),
    "Wardrobe Balcony Key": LMItemData("Door Key", 54, IC.progression,  41),
    "Study Key": LMItemData("Door Key", 57, IC.progression,  32),
    "Basement Stairwell Key": LMItemData("Door Key", 61, IC.progression,  9),
    "1F Bathroom Key": LMItemData("Door Key", 64, IC.progression,  23),
    "1F Washroom Key": LMItemData("Door Key", 67, IC.progression,  20),
    "Kitchen Key": LMItemData("Door Key", 75, IC.progression,  11),
    "Boneyard Key": LMItemData("Door Key", 76, IC.progression,  10),
    "Projection Room Key": LMItemData("Door Key", 77, IC.progression,  18),
    "Mirror Room Key": LMItemData("Door Key", 78, IC.progression,  5),
    "Butler's Room Key": LMItemData("Door Key", 79, IC.progression,  1),
    "Tea Room Key": LMItemData("Door Key", 81, IC.progression,  47),
    "South Rec Room Key": LMItemData("Door Key", 82, IC.progression,  24),
    "Upper 2F Stairwell Key": LMItemData("Door Key", 83, IC.progression,  75),
    "2F Bathroom Key": LMItemData("Door Key", 84, IC.progression,  48),
    "2F Washroom Key": LMItemData("Door Key", 85, IC.progression,  45),
    "Nana's Room Key": LMItemData("Door Key", 86, IC.progression,  49),
    "Astral Hall Key": LMItemData("Door Key", 87, IC.progression,  44),
    "Observatory Key": LMItemData("Door Key", 90, IC.progression,  40),
    "Guest Room": LMItemData("Door Key", 91, IC.progression,  30),
    "3F Right Hallway Key": LMItemData("Door Key", 92, IC.progression,  55),
    "Telephone Room Key": LMItemData("Door Key", 97, IC.progression,  52),
    "Ceramics Studio Key": LMItemData("Door Key", 99, IC.progression,  50),
    "Breaker Room Key": LMItemData("Door Key", 100, IC.progression,  71),
    "Basement Hallway Key": LMItemData("Door Key", 102, IC.progression,  67),
    "Spade Hallway Key": LMItemData("Door Key", 105, IC.progression,  70),
    "Fire Element Medal": LMItemData("Medal", 30, IC.progression),
    "Water Element Medal": LMItemData("Medal", 31, IC.progression),
    "Ice Element Medal": LMItemData("Medal", 32, IC.progression),
    "Mario's Glove": LMItemData("Mario Item", 33, IC.progression),
    "Mario's Hat": LMItemData("Mario Item", 34, IC.progression),
    "Mario's Letter": LMItemData("Mario Item", 35, IC.progression),
    "Mario's Star": LMItemData("Mario Item", 36, IC.progression),
    "Mario's Shoe": LMItemData("Mario Item", 37, IC.progression),
    "Boo Radar": LMItemData("Upgrade", 39, IC.progression),
    "Poltergust 4000": LMItemData("Upgrade", 40, IC.useful),
    "Gold Diamond": LMItemData("Money", 49, IC.progression),
}

BOO_ITEM_TABLE: dict[str, LMItemData] = {
    "Butler's Room Boo (PeekaBoo)": LMItemData("Boo", 38, IC.progression),
    "Hidden Room Boo (GumBoo)": LMItemData("Boo", 64, IC.progression),
    "Fortune Teller Boo (Booigi)": LMItemData("Boo", 65, IC.progression),
    "Mirror Room Boo (Kung Boo)": LMItemData("Boo", 66, IC.progression),
    "Laundry Room Boo (Boogie)": LMItemData("Boo", 67, IC.progression),
    "Kitchen Boo (Booligan)": LMItemData("Boo", 68, IC.progression),
    "Dining Room Boo (Boodacious)": LMItemData("Boo", 69, IC.progression),
    "Ball Room Boo (Boo La La)": LMItemData("Boo", 70, IC.progression),
    "Billiards Boo (Boohoo)": LMItemData("Boo", 71, IC.progression),
    "Projection Room Boo (ShamBoo)": LMItemData("Boo", 72, IC.progression),
    "Storage Room Boo (Game Boo)": LMItemData("Boo", 73, IC.progression),
    "Conservatory Boo (Boomeo)": LMItemData("Boo", 74, IC.progression),
    "Rec Room Boo (Booregard)": LMItemData("Boo", 75, IC.progression),
    "Nursery Boo (TurBoo)": LMItemData("Boo", 76, IC.progression),
    "Twin's Room Boo (Booris)": LMItemData("Boo", 77, IC.progression),
    "Sitting Room Boo (Boolivia)": LMItemData("Boo", 78, IC.progression),
    "Guest Room (Boonita)": LMItemData("Boo", 79, IC.progression),
    "Master Bedroom Boo (Boolicious)": LMItemData("Boo", 80, IC.progression),
    "Study Boo (TaBoo)": LMItemData("Boo", 81, IC.progression),
    "Parlor Boo (BamBoo)": LMItemData("Boo", 82, IC.progression),
    "Wardrobe Boo (GameBoo Advance)": LMItemData("Boo", 83, IC.progression),
    "Anteroom  Boo (Bootha)": LMItemData("Boo", 84, IC.progression),
    "Astral Boo (Boonswoggle)": LMItemData("Boo", 85, IC.progression),
    "Nana's Room (LamBooger)": LMItemData("Boo", 86, IC.progression),
    "Tea Room (Mr. Boojangles)": LMItemData("Boo", 87, IC.progression),
    "Armory Boo (Underboo)": LMItemData("Boo", 88, IC.progression),
    "Telephone Room Boo (Boomerang)": LMItemData("Boo", 89, IC.progression),
    "Safari Room Boo (Little Boo Peep)": LMItemData("Boo", 90, IC.progression),
    "Ceramics Studio (TamBoorine)": LMItemData("Boo", 91, IC.progression),
    "Clockwork Room Boo (Booscaster)": LMItemData("Boo", 92, IC.progression),
    "Artist's Studio Boo (Bootique)": LMItemData("Boo", 93, IC.progression),
    "Cold Storage Boo (Boolderdash)": LMItemData("Boo", 94, IC.progression),
    "Cellar Boo (Booripedes)": LMItemData("Boo", 95, IC.progression),
    "Pipe Room  Boo (Booffant)": LMItemData("Boo", 96, IC.progression),
    "Breaker Room Boo (Boo B. Hatch)": LMItemData("Boo", 97, IC.progression),
    "Boolossus Boo 1": LMItemData("Boo", 98, IC.progression),
    "Boolossus Boo 2": LMItemData("Boo", 99, IC.progression),
    "Boolossus Boo 3": LMItemData("Boo", 100, IC.progression),
    "Boolossus Boo 4": LMItemData("Boo", 101, IC.progression),
    "Boolossus Boo 5": LMItemData("Boo", 102, IC.progression),
    "Boolossus Boo 6": LMItemData("Boo", 103, IC.progression),
    "Boolossus Boo 7": LMItemData("Boo", 104, IC.progression),
    "Boolossus Boo 8": LMItemData("Boo", 105, IC.progression),
    "Boolossus Boo 9": LMItemData("Boo", 107, IC.progression),
    "Boolossus Boo 10": LMItemData("Boo", 108, IC.progression),
    "Boolossus Boo 11": LMItemData("Boo", 109, IC.progression),
    "Boolossus Boo 12": LMItemData("Boo", 110, IC.progression),
    "Boolossus Boo 13": LMItemData("Boo", 111, IC.progression),
    "Boolossus Boo 14": LMItemData("Boo", 112, IC.progression),
    "Boolossus Boo 15": LMItemData("Boo", 113, IC.progression)
}

filler_items: Dict[str, LMItemData] = {
    # "10 Coins": LMItemData("Money", 52, IC.filler),
    # "10 Bills": LMItemData("Money", 53, IC.filler),
    "Money Bundle": LMItemData("Money", 41, IC.filler),
    # "Gold Bar": LMItemData("Money", 56, IC.filler),
    # "Sapphire": LMItemData("Money", 58, IC.filler),
    # "Emerald": LMItemData("Money", 59, IC.filler),
    # "Ruby": LMItemData("Money", 60, IC.filler),
    # "Diamond": LMItemData("Money", 62, IC.filler),
    "Poison Mushroom": LMItemData("Trap", 42, IC.trap),
    # "Ghost": LMItemData("Trap", 43, IC.trap),
    "Nothing": LMItemData("Nothing", 44, IC.filler),
    "Small Heart": LMItemData("Heart", 45, IC.filler),
    "Large Heart": LMItemData("Heart", 47, IC.filler),
    "Bomb": LMItemData("Trap", 50, IC.trap),
    "Ice Trap": LMItemData("Trap", 106, IC.trap),
    "Banana Trap": LMItemData("Trap", 63, IC.trap)
}

ALL_ITEMS_TABLE = {**ITEM_TABLE,
                   **BOO_ITEM_TABLE,
                   **filler_items}

LOOKUP_ID_TO_NAME: dict[int, str] = {
    LMItem.get_apid(data.code): item for item, data in ALL_ITEMS_TABLE.items() if data.code is not None
}


def get_item_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in ALL_ITEMS_TABLE.items():
        categories.setdefault(data.type, set()).add(name)

    return categories
