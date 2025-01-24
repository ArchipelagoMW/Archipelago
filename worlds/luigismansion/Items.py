from typing import NamedTuple, Dict, Set, Optional

from BaseClasses import Item
from BaseClasses import ItemClassification as IC


class LMItemData(NamedTuple):
    type: str
    code: Optional[int]
    classification: IC
    doorid: Optional[int] = None
    address: Optional[int] = None
    itembit: Optional[int] = None


class LMItem(Item):
    game: str = "Luigi's Mansion"

    def __init__(self, name: str, player: int, data: LMItemData, force_nonprogress: bool = False):
        adjusted_classification = IC.filler if force_nonprogress else data.classification
        super(LMItem, self).__init__(name, adjusted_classification, LMItem.get_apid(data.code), player)

        self.type = data.type
        self.item_id = data.code

    @staticmethod
    def get_apid(code: int):
        base_id: int = 8000
        return base_id + code if code is not None else None


ITEM_TABLE: dict[str, LMItemData] = {
    "Heart Key": LMItemData("Door Key", 0, IC.progression, 3, 0x803D5E14, 3),
    "Club Key": LMItemData("Door Key", 1, IC.progression, 42, 0x803D5E19, 2),
    "Diamond Key": LMItemData("Door Key", 2, IC.progression, 59, 0x803D5E1B, 3),
    "Spade Key": LMItemData("Door Key", 3, IC.progression, 72, 0x803D5E1D, 0),
    "Parlor Key": LMItemData("Door Key", 4, IC.progression, 34, 0x803D5E18, 2),
    "Anteroom Key": LMItemData("Door Key", 5, IC.progression, 38, 0x803D5E18, 6),
    "Wardrobe Key": LMItemData("Door Key", 6, IC.progression, 43, 0x803D5E19, 3),
    "Family Hallway Key": LMItemData("Door Key", 7, IC.progression, 33, 0x803D5E18, 1),
    "Master Bedroom Key": LMItemData("Door Key", 8, IC.progression, 31, 0x803D5E17, 7),
    "Nursery Key": LMItemData("Door Key", 9, IC.progression, 27, 0x803D5E17, 3),
    "Twins Bedroom Key": LMItemData("Door Key", 10, IC.progression, 28, 0x803D5E17, 4),
    "Ballroom Key": LMItemData("Door Key", 11, IC.progression, 15, 0x803D5E15, 7),
    "Storage Room Key": LMItemData("Door Key", 12, IC.progression, 16, 0x803D5E16, 0),
    "Fortune Teller Key": LMItemData("Door Key", 13, IC.progression, 4, 0x803D5E14, 4),
    "Laundry Key": LMItemData("Door Key", 14, IC.progression, 7, 0x803D5E14, 7),
    "1F - 2F Stairwell (Lower Door) Key": LMItemData("Door Key", 15, IC.progression, 74, 0x803D5E1D, 2),
    "Conservatory Key": LMItemData("Door Key", 16, IC.progression, 21, 0x803D5E16, 5),
    "Dining Room Key": LMItemData("Door Key", 17, IC.progression, 14, 0x803D5E15, 6),
    "North Rec Room Key": LMItemData("Door Key", 18, IC.progression, 25, 0x803D5E17, 1),
    "Billiards Key": LMItemData("Door Key", 19, IC.progression, 17, 0x803D5E16, 1),
    "North Safari Key": LMItemData("Door Key", 20, IC.progression, 56, 0x803D5E1B, 0),
    "Boolossus Balcony (East Side) Key": LMItemData("Door Key", 21, IC.progression, 62, 0x803D5E1B, 6),
    "Breaker Key": LMItemData("Door Key", 22, IC.progression, 71, 0x803D5E1C, 7),
    "Cellar Key": LMItemData("Door Key", 23, IC.progression, 68, 0x803D5E1C, 4),
    "Clockwork Key": LMItemData("Door Key", 24, IC.progression, 53, 0x803D5E1A, 5),
    "Armory Key": LMItemData("Door Key", 25, IC.progression, 51, 0x803D5E1A, 3),
    "Sitting Room Key": LMItemData("Door Key", 26, IC.progression, 29, 0x803D5E17, 5),
    "Pipe Room Key": LMItemData("Door Key", 27, IC.progression, 69, 0x803D5E1C, 5),
    "Cold Storage Key": LMItemData("Door Key", 28, IC.progression, 65, 0x803D5E1C, 1),
    "Artist's Studio Key": LMItemData("Door Key", 29, IC.progression, 63, 0x803D5E1B, 7),
    "Wardrobe Balcony Key": LMItemData("Door Key", 30, IC.progression, 41, 0x803D5E19, 1),
    "Study Key": LMItemData("Door Key", 31, IC.progression, 32, 0x803D5E18, 0),
    "Basement Stairwell Key": LMItemData("Door Key", 32, IC.progression, 9, 0x803D5E15, 1),
    "1F Bathroom Key": LMItemData("Door Key", 33, IC.progression, 23, 0x803D5E16, 7),
    "1F Washroom Key": LMItemData("Door Key", 34, IC.progression, 20, 0x803D5E16, 4),
    "Kitchen Key": LMItemData("Door Key", 35, IC.progression, 11, 0x803D5E15, 3),
    "Boneyard Key": LMItemData("Door Key", 36, IC.progression, 10, 0x803D5E15, 2),
    "Projection Room Key": LMItemData("Door Key", 37, IC.progression, 18, 0x803D5E16, 2),
    "Mirror Room Key": LMItemData("Door Key", 38, IC.progression, 5, 0x803D5E14, 5),
    "Butler's Room Key": LMItemData("Door Key", 39, IC.progression, 1, 0x803D5E14, 1),
    "Tea Room Key": LMItemData("Door Key", 40, IC.progression, 47, 0x803D5E19, 7),
    "South Rec Room Key": LMItemData("Door Key", 41, IC.progression, 24, 0x803D5E17, 0),
    "1F - 2F Stairwell (Upper Door) Key": LMItemData("Door Key", 42, IC.progression, 75),
    "2F Bathroom Key": LMItemData("Door Key", 43, IC.progression, 48, 0x803D5E1A, 0),
    "2F Washroom Key": LMItemData("Door Key", 44, IC.progression, 45, 0x803D5E19, 5),
    "Nana's Room Key": LMItemData("Door Key", 45, IC.progression, 49, 0x803D5E1A, 1),
    "Astral Hall Key": LMItemData("Door Key", 46, IC.progression, 44, 0x803D5E19, 4),
    "Observatory Key": LMItemData("Door Key", 47, IC.progression, 40, 0x803D5E19, 0),
    "Guest Room Key": LMItemData("Door Key", 48, IC.progression, 30, 0x803D5E17, 6),
    "West Safari Hallway Key": LMItemData("Door Key", 49, IC.progression, 55, 0x803D5E1A, 7),
    "Telephone Room Key": LMItemData("Door Key", 50, IC.progression, 52, 0x803D5E1A, 4),
    "Ceramics Studio Key": LMItemData("Door Key", 51, IC.progression, 50, 0x803D5E1A, 2),
    "Breaker Room Key": LMItemData("Door Key", 52, IC.progression, 71, 0x803D5E1C, 7),
    "Basement Hallway Key": LMItemData("Door Key", 53, IC.progression, 67, 0x803D5E1C, 3),
    "Secret Altar Hallway Key": LMItemData("Door Key", 54, IC.progression, 70, 0x803D5E1C, 6),
    "Fire Element Medal": LMItemData("Medal", 55, IC.progression, 0, 0x803D5DB2, 5),
    "Water Element Medal": LMItemData("Medal", 56, IC.progression, 0, 0x803D5DB2, 7),
    "Ice Element Medal": LMItemData("Medal", 57, IC.progression, 0, 0x803D5DB2, 6),
    "Mario's Glove": LMItemData("Mario Item", 58, IC.progression, 0, 0x803D5DBB, 6),
    "Mario's Hat": LMItemData("Mario Item", 59, IC.progression, 0, 0x803D5DBB, 4),
    "Mario's Letter": LMItemData("Mario Item", 60, IC.progression, 0, 0x803D5DBC, 0),
    "Mario's Star": LMItemData("Mario Item", 61, IC.progression, 0, 0x803D5DBB, 5),
    "Mario's Shoe": LMItemData("Mario Item", 62, IC.progression, 0, 0x803D5DBB, 7),
    "Boo Radar": LMItemData("Upgrade", 63, IC.progression, 0), #TODO
    "Poltergust 4000": LMItemData("Upgrade", 64, IC.useful, 0), #TODO
    "Gold Diamond": LMItemData("Money", 65, IC.progression, 0), #TODO
}

BOO_ITEM_TABLE: dict[str, LMItemData] = {
    "Butler's Room Boo (PeekaBoo)": LMItemData("Boo", 66, IC.progression, 0, 0x803D5E04, 0),
    "Hidden Room Boo (GumBoo)": LMItemData("Boo", 67, IC.progression, 0, 0x803D5E04, 1),
    "Fortune Teller Boo (Booigi)": LMItemData("Boo", 68, IC.progression, 0, 0x803D5E04, 2),
    "Mirror Room Boo (Kung Boo)": LMItemData("Boo", 69, IC.progression, 0, 0x803D5E04, 3),
    "Laundry Room Boo (Boogie)": LMItemData("Boo", 70, IC.progression, 0, 0x803D5E04, 4),
    "Kitchen Boo (Booligan)": LMItemData("Boo", 71, IC.progression, 0, 0x803D5E04, 5),
    "Dining Room Boo (Boodacious)": LMItemData("Boo", 72, IC.progression, 0, 0x803D5E04, 6),
    "Ball Room Boo (Boo La La)": LMItemData("Boo", 73, IC.progression, 0, 0x803D5E04, 7),
    "Billiards Boo (Boohoo)": LMItemData("Boo", 74, IC.progression, 0, 0x803D5E05, 0),
    "Projection Room Boo (ShamBoo)": LMItemData("Boo", 75, IC.progression, 0, 0x803D5E05, 1),
    "Storage Room Boo (Game Boo)": LMItemData("Boo", 76, IC.progression, 0, 0x803D5E05, 2),
    "Conservatory Boo (Boomeo)": LMItemData("Boo", 77, IC.progression, 0, 0x803D5E05, 3),
    "Rec Room Boo (Booregard)": LMItemData("Boo", 78, IC.progression, 0, 0x803D5E05, 4),
    "Nursery Boo (TurBoo)": LMItemData("Boo", 79, IC.progression, 0, 0x803D5E05, 5),
    "Twin's Room Boo (Booris)": LMItemData("Boo", 80, IC.progression, 0, 0x803D5E05, 6),
    "Sitting Room Boo (Boolivia)": LMItemData("Boo", 81, IC.progression, 0, 0x803D5E05, 7),
    "Guest Room (Boonita)": LMItemData("Boo", 82, IC.progression, 0, 0x803D5E06, 0),
    "Master Bedroom Boo (Boolicious)": LMItemData("Boo", 83, IC.progression, 0, 0x803D5E06, 1),
    "Study Boo (TaBoo)": LMItemData("Boo", 84, IC.progression, 0, 0x803D5E06, 2),
    "Parlor Boo (BamBoo)": LMItemData("Boo", 85, IC.progression, 0, 0x803D5E06, 3),
    "Wardrobe Boo (GameBoo Advance)": LMItemData("Boo", 86, IC.progression, 0, 0x803D5E06, 4),
    "Anteroom  Boo (Bootha)": LMItemData("Boo", 87, IC.progression, 0, 0x803D5E06, 5),
    "Astral Boo (Boonswoggle)": LMItemData("Boo", 88, IC.progression, 0, 0x803D5E06, 6),
    "Nana's Room (LamBooger)": LMItemData("Boo", 89, IC.progression, 0, 0x803D5E06, 7),
    "Tea Room (Mr. Boojangles)": LMItemData("Boo", 90, IC.progression, 0, 0x803D5E07, 0),
    "Armory Boo (Underboo)": LMItemData("Boo", 91, IC.progression, 0, 0x803D5E07, 1),
    "Telephone Room Boo (Boomerang)": LMItemData("Boo", 92, IC.progression, 0, 0x803D5E07, 2),
    "Safari Room Boo (Little Boo Peep)": LMItemData("Boo", 93, IC.progression, 0, 0x803D5E07, 3),
    "Ceramics Studio (TamBoorine)": LMItemData("Boo", 94, IC.progression, 0, 0x803D5E07, 4),
    "Clockwork Room Boo (Booscaster)": LMItemData("Boo", 95, IC.progression, 0, 0x803D5E07, 5),
    "Artist's Studio Boo (Bootique)": LMItemData("Boo", 96, IC.progression, 0, 0x803D5E07, 6),
    "Cold Storage Boo (Boolderdash)": LMItemData("Boo", 97, IC.progression, 0, 0x803D5E07, 7),
    "Cellar Boo (Booripedes)": LMItemData("Boo", 98, IC.progression, 0, 0x803D5E08, 0),
    "Pipe Room  Boo (Booffant)": LMItemData("Boo", 99, IC.progression, 0, 0x803D5E08, 1),
    "Breaker Room Boo (Boo B. Hatch)": LMItemData("Boo", 100, IC.progression, 0, 0x803D5E08, 2),
    "Boolossus Boo 1": LMItemData("Boo", 101, IC.progression, 0, 0x803D5E08, 3),
    "Boolossus Boo 2": LMItemData("Boo", 102, IC.progression, 0, 0x803D5E08, 4),
    "Boolossus Boo 3": LMItemData("Boo", 103, IC.progression, 0, 0x803D5E08, 5),
    "Boolossus Boo 4": LMItemData("Boo", 104, IC.progression, 0, 0x803D5E08, 6),
    "Boolossus Boo 5": LMItemData("Boo", 105, IC.progression, 0, 0x803D5E08, 7),
    "Boolossus Boo 6": LMItemData("Boo", 107, IC.progression, 0, 0x803D5E09, 0),
    "Boolossus Boo 7": LMItemData("Boo", 108, IC.progression, 0, 0x803D5E09, 1),
    "Boolossus Boo 8": LMItemData("Boo", 109, IC.progression, 0, 0x803D5E09, 2),
    "Boolossus Boo 9": LMItemData("Boo", 110, IC.progression, 0, 0x803D5E09, 3),
    "Boolossus Boo 10": LMItemData("Boo", 111, IC.progression, 0, 0x803D5E09, 4),
    "Boolossus Boo 11": LMItemData("Boo", 112, IC.progression, 0, 0x803D5E09, 5),
    "Boolossus Boo 12": LMItemData("Boo", 113, IC.progression, 0, 0x803D5E09, 6),
    "Boolossus Boo 13": LMItemData("Boo", 114, IC.progression, 0, 0x803D5E09, 7),
    "Boolossus Boo 14": LMItemData("Boo", 115, IC.progression, 0, 0x803D5E0A, 0),
    "Boolossus Boo 15": LMItemData("Boo", 116, IC.progression, 0, 0x803D5E0A, 1),
}

filler_items: Dict[str, LMItemData] = {
    # "10 Coins": LMItemData("Money", 117, IC.filler),
    # "10 Bills": LMItemData("Money", 118, IC.filler),
    "Money Bundle": LMItemData("Money", 119, IC.filler),
    # "Gold Bar": LMItemData("Money", 120, IC.filler),
    # "Sapphire": LMItemData("Money", 121, IC.filler),
    # "Emerald": LMItemData("Money", 122, IC.filler),
    # "Ruby": LMItemData("Money", 123, IC.filler),
    # "Diamond": LMItemData("Money", 124, IC.filler),
    "Poison Mushroom": LMItemData("Trap", 125, IC.trap),
    # "Ghost": LMItemData("Trap", 126, IC.trap),
    "Nothing": LMItemData("Nothing", 127, IC.filler),
    "Small Heart": LMItemData("Heart", 128, IC.filler),
    "Large Heart": LMItemData("Heart", 129, IC.filler),
    "Bomb": LMItemData("Trap", 130, IC.trap),
    "Ice Trap": LMItemData("Trap", 131, IC.trap),
    "Banana Trap": LMItemData("Trap", 132, IC.trap)
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
