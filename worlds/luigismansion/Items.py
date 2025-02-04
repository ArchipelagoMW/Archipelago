from typing import NamedTuple, Dict, Set, Optional

from BaseClasses import Item
from BaseClasses import ItemClassification as IC


class LMItemData(NamedTuple):
    type: str
    code: Optional[int]
    classification: IC
    doorid: Optional[int] = None
    ram_addr: Optional[int] = None
    itembit: Optional[int] = None
    pointer_offset: Optional[int] = None
    ram_byte_size: Optional[int] = None


class LMItem(Item):
    game: str = "Luigi's Mansion"
    doorid: Optional[int] = None

    def __init__(self, name: str, player: int, data: LMItemData, force_nonprogress: bool = False):
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
    "Heart Key": LMItemData("Door Key", 0, IC.progression, 3, ram_addr=0x803D5E14, itembit=3),
    "Club Key": LMItemData("Door Key", 1, IC.progression, 42, ram_addr=0x803D5E19, itembit=2),
    "Diamond Key": LMItemData("Door Key", 2, IC.progression, 59, ram_addr=0x803D5E1B, itembit=3),
    "Spade Key": LMItemData("Door Key", 3, IC.progression, 72, ram_addr=0x803D5E1D, itembit=0),
    "Parlor Key": LMItemData("Door Key", 4, IC.progression, 34, ram_addr=0x803D5E18, itembit=2),
    "Anteroom Key": LMItemData("Door Key", 5, IC.progression, 38, ram_addr=0x803D5E18, itembit=6),
    "Wardrobe Key": LMItemData("Door Key", 6, IC.progression, 43, ram_addr=0x803D5E19, itembit=3),
    "Family Hallway Key": LMItemData("Door Key", 7, IC.progression, 33, ram_addr=0x803D5E18, itembit=1),
    "Master Bedroom Key": LMItemData("Door Key", 8, IC.progression, 31, ram_addr=0x803D5E17, itembit=7),
    "Nursery Key": LMItemData("Door Key", 9, IC.progression, 27, ram_addr=0x803D5E17, itembit=3),
    "Twins Bedroom Key": LMItemData("Door Key", 10, IC.progression, 28, ram_addr=0x803D5E17, itembit=4),
    "Ballroom Key": LMItemData("Door Key", 11, IC.progression, 15, ram_addr=0x803D5E15, itembit=7),
    "Storage Room Key": LMItemData("Door Key", 12, IC.progression, 16, ram_addr=0x803D5E16, itembit=0),
    "Fortune Teller Key": LMItemData("Door Key", 13, IC.progression, 4, ram_addr=0x803D5E14, itembit=4),
    "Laundry Key": LMItemData("Door Key", 14, IC.progression, 7, ram_addr=0x803D5E14, itembit=7),
    "Lower 2F Stairwell Key": LMItemData("Door Key", 15, IC.progression, 74, ram_addr=0x803D5E1D, itembit=2), # TODO 1F - 2F Stairwell (Lower Door) Key
    "Conservatory Key": LMItemData("Door Key", 16, IC.progression, 21, ram_addr=0x803D5E16, itembit=5),
    "Dining Room Key": LMItemData("Door Key", 17, IC.progression, 14, ram_addr=0x803D5E15, itembit=6),
    "North Rec Room Key": LMItemData("Door Key", 18, IC.progression, 25, ram_addr=0x803D5E17, itembit=1),
    "Billiards Key": LMItemData("Door Key", 19, IC.progression, 17, ram_addr=0x803D5E16, itembit=1),
    "Safari Key": LMItemData("Door Key", 20, IC.progression, 56, ram_addr=0x803D5E1B, itembit=0), #TODO North Safari Key
    "Balcony Key": LMItemData("Door Key", 21, IC.progression, 62, ram_addr=0x803D5E1B, itembit=6), #TODO Boolossus Balcony East Side Key
    "Cellar Key": LMItemData("Door Key", 23, IC.progression, 68, ram_addr=0x803D5E1C, itembit=4),
    "Clockwork Key": LMItemData("Door Key", 24, IC.progression, 53, ram_addr=0x803D5E1A, itembit=5),
    "Armory Key": LMItemData("Door Key", 25, IC.progression, 51, ram_addr=0x803D5E1A, itembit=3),
    "Sitting Room Key": LMItemData("Door Key", 26, IC.progression, 29, ram_addr=0x803D5E17, itembit=5),
    "Pipe Room Key": LMItemData("Door Key", 27, IC.progression, 69, ram_addr=0x803D5E1C, itembit=5),
    "Cold Storage Key": LMItemData("Door Key", 28, IC.progression, 65, ram_addr=0x803D5E1C, itembit=1),
    "Artist's Studio Key": LMItemData("Door Key", 29, IC.progression, 63, ram_addr=0x803D5E1B, itembit=7),
    "Wardrobe Balcony Key": LMItemData("Door Key", 30, IC.progression, 41, ram_addr=0x803D5E19, itembit=1),
    "Study Key": LMItemData("Door Key", 31, IC.progression, 32, ram_addr=0x803D5E18, itembit=0),
    "Basement Stairwell Key": LMItemData("Door Key", 32, IC.progression, 9, ram_addr=0x803D5E15, itembit=1),
    "1F Bathroom Key": LMItemData("Door Key", 33, IC.progression, 23, ram_addr=0x803D5E16, itembit=7),
    "1F Washroom Key": LMItemData("Door Key", 34, IC.progression, 20, ram_addr=0x803D5E16, itembit=4),
    "Kitchen Key": LMItemData("Door Key", 35, IC.progression, 11, ram_addr=0x803D5E15, itembit=3),
    "Boneyard Key": LMItemData("Door Key", 36, IC.progression, 10, ram_addr=0x803D5E15, itembit=2),
    "Projection Room Key": LMItemData("Door Key", 37, IC.progression, 18, ram_addr=0x803D5E16, itembit=2),
    "Mirror Room Key": LMItemData("Door Key", 38, IC.progression, 5, ram_addr=0x803D5E14, itembit=5),
    "Butler's Room Key": LMItemData("Door Key", 39, IC.progression, 1, ram_addr=0x803D5E14, itembit=1),
    "Tea Room Key": LMItemData("Door Key", 40, IC.progression, 47, ram_addr=0x803D5E19, itembit=7),
    "South Rec Room Key": LMItemData("Door Key", 41, IC.progression, 24, ram_addr=0x803D5E17, itembit=0),
    "Upper 2F Stairwell Key": LMItemData("Door Key", 42, IC.progression, 75, ram_addr=0x803D5E1D, itembit=3), #TODO 1F - 2F Stairwell (Upper Door) Key
    "2F Bathroom Key": LMItemData("Door Key", 43, IC.progression, 48, ram_addr=0x803D5E1A, itembit=0),
    "2F Washroom Key": LMItemData("Door Key", 44, IC.progression, 45, ram_addr=0x803D5E19, itembit=5),
    "Nana's Room Key": LMItemData("Door Key", 45, IC.progression, 49, ram_addr=0x803D5E1A, itembit=1),
    "Astral Hall Key": LMItemData("Door Key", 46, IC.progression, 44, ram_addr=0x803D5E19, itembit=4),
    "Observatory Key": LMItemData("Door Key", 47, IC.progression, 40, ram_addr=0x803D5E19, itembit=0),
    "Guest Room Key": LMItemData("Door Key", 48, IC.progression, 30, ram_addr=0x803D5E17, itembit=6),
    "East Attic Hallway Key": LMItemData("Door Key", 49, IC.progression, 55, ram_addr=0x803D5E1A, itembit=7), #TODO West Safari Hallway Key
    "Telephone Room Key": LMItemData("Door Key", 50, IC.progression, 52, ram_addr=0x803D5E1A, itembit=4),
    "Ceramics Studio Key": LMItemData("Door Key", 51, IC.progression, 50, ram_addr=0x803D5E1A, itembit=2),
    "Breaker Room Key": LMItemData("Door Key", 52, IC.progression, 71, ram_addr=0x803D5E1C, itembit=7),
    "Basement Hallway Key": LMItemData("Door Key", 53, IC.progression, 67, ram_addr=0x803D5E1C, itembit=3),
    "Spade Hallway Key": LMItemData("Door Key", 54, IC.progression, 70, ram_addr=0x803D5E1C, itembit=6),
    "Fire Element Medal": LMItemData("Medal", 55, IC.progression, ram_addr=0x803D5DB2, itembit=5),
    "Water Element Medal": LMItemData("Medal", 56, IC.progression, ram_addr=0x803D5DB2, itembit=7),
    "Ice Element Medal": LMItemData("Medal", 57, IC.progression, ram_addr=0x803D5DB2, itembit=6),
    "Mario's Glove": LMItemData("Mario Item", 58, IC.progression, ram_addr=0x803D5DBB, itembit=6),
    "Mario's Hat": LMItemData("Mario Item", 59, IC.progression, ram_addr=0x803D5DBB, itembit=4),
    "Mario's Letter": LMItemData("Mario Item", 60, IC.progression, ram_addr=0x803D5DBC, itembit=0),
    "Mario's Star": LMItemData("Mario Item", 61, IC.progression, ram_addr=0x803D5DBB, itembit=5),
    "Mario's Shoe": LMItemData("Mario Item", 62, IC.progression, ram_addr=0x803D5DBB, itembit=7),
    "Boo Radar": LMItemData("Upgrade", 63, IC.progression, ram_addr=0x803D33A2, pointer_offset=0),
    "Poltergust 4000": LMItemData("Upgrade", 64, IC.useful, ram_addr=0x80081CC8, pointer_offset=0),
    "Gold Diamond": LMItemData("Money", 65, IC.progression,
                               ram_addr=0x803D8B7C, pointer_offset=0x344, ram_byte_size=4),
}

BOO_ITEM_TABLE: dict[str, LMItemData] = {
    "Butler's Room Boo (PeekaBoo)": LMItemData("Boo", 66, IC.progression, ram_addr=0x803D5E04, itembit=0),
    "Hidden Room Boo (GumBoo)": LMItemData("Boo", 67, IC.progression, ram_addr=0x803D5E04, itembit=1),
    "Fortune Teller Boo (Booigi)": LMItemData("Boo", 68, IC.progression, ram_addr=0x803D5E04, itembit=2),
    "Mirror Room Boo (Kung Boo)": LMItemData("Boo", 69, IC.progression, ram_addr=0x803D5E04, itembit=3),
    "Laundry Room Boo (Boogie)": LMItemData("Boo", 70, IC.progression, ram_addr=0x803D5E04, itembit=4),
    "Kitchen Boo (Booligan)": LMItemData("Boo", 71, IC.progression, ram_addr=0x803D5E04, itembit=5),
    "Dining Room Boo (Boodacious)": LMItemData("Boo", 72, IC.progression, ram_addr=0x803D5E04, itembit=6),
    "Ball Room Boo (Boo La La)": LMItemData("Boo", 73, IC.progression, ram_addr=0x803D5E04, itembit=7),
    "Billiards Boo (Boohoo)": LMItemData("Boo", 74, IC.progression, ram_addr=0x803D5E05, itembit=0),
    "Projection Room Boo (ShamBoo)": LMItemData("Boo", 75, IC.progression, ram_addr=0x803D5E05, itembit=1),
    "Storage Room Boo (Game Boo)": LMItemData("Boo", 76, IC.progression, ram_addr=0x803D5E05, itembit=2),
    "Conservatory Boo (Boomeo)": LMItemData("Boo", 77, IC.progression, ram_addr=0x803D5E05, itembit=3),
    "Rec Room Boo (Booregard)": LMItemData("Boo", 78, IC.progression, ram_addr=0x803D5E05, itembit=4),
    "Nursery Boo (TurBoo)": LMItemData("Boo", 79, IC.progression, ram_addr=0x803D5E05, itembit=5),
    "Twin's Room Boo (Booris)": LMItemData("Boo", 80, IC.progression, ram_addr=0x803D5E05, itembit=6),
    "Sitting Room Boo (Boolivia)": LMItemData("Boo", 81, IC.progression, ram_addr=0x803D5E05, itembit=7),
    "Guest Room Boo (Boonita)": LMItemData("Boo", 82, IC.progression, ram_addr=0x803D5E06, itembit=0),
    "Master Bedroom Boo (Boolicious)": LMItemData("Boo", 83, IC.progression, ram_addr=0x803D5E06, itembit=1),
    "Study Boo (TaBoo)": LMItemData("Boo", 84, IC.progression, ram_addr=0x803D5E06, itembit=2),
    "Parlor Boo (BamBoo)": LMItemData("Boo", 85, IC.progression, ram_addr=0x803D5E06, itembit=3),
    "Wardrobe Boo (GameBoo Advance)": LMItemData("Boo", 86, IC.progression, ram_addr=0x803D5E06, itembit=4),
    "Anteroom Boo (Bootha)": LMItemData("Boo", 87, IC.progression, ram_addr=0x803D5E06, itembit=5),
    "Astral Boo (Boonswoggle)": LMItemData("Boo", 88, IC.progression, ram_addr=0x803D5E06, itembit=6),
    "Nana's Room (LamBooger)": LMItemData("Boo", 89, IC.progression, ram_addr=0x803D5E06, itembit=7),
    "Tea Room Boo (Mr. Boojangles)": LMItemData("Boo", 90, IC.progression, ram_addr=0x803D5E07, itembit=0),
    "Armory Boo (Underboo)": LMItemData("Boo", 91, IC.progression, ram_addr=0x803D5E07, itembit=1),
    "Telephone Room Boo (Boomerang)": LMItemData("Boo", 92, IC.progression, ram_addr=0x803D5E07, itembit=2),
    "Safari Room Boo (Little Boo Peep)": LMItemData("Boo", 93, IC.progression, ram_addr=0x803D5E07, itembit=3),
    "Ceramics Studio Boo (TamBoorine)": LMItemData("Boo", 94, IC.progression, ram_addr=0x803D5E07, itembit=4),
    "Clockwork Room Boo (Booscaster)": LMItemData("Boo", 95, IC.progression, ram_addr=0x803D5E07, itembit=5),
    "Artist's Studio Boo (Bootique)": LMItemData("Boo", 96, IC.progression, ram_addr=0x803D5E07, itembit=6),
    "Cold Storage Boo (Boolderdash)": LMItemData("Boo", 97, IC.progression, ram_addr=0x803D5E07, itembit=7),
    "Cellar Boo (Booripedes)": LMItemData("Boo", 98, IC.progression, ram_addr=0x803D5E08, itembit=0),
    "Pipe Room Boo (Booffant)": LMItemData("Boo", 99, IC.progression, ram_addr=0x803D5E08, itembit=1),
    "Breaker Room Boo (Boo B. Hatch)": LMItemData("Boo", 100, IC.progression, ram_addr=0x803D5E08, itembit=2),
    "Boolossus Boo 1": LMItemData("Boo", 101, IC.progression, ram_addr=0x803D5E08, itembit=3),
    "Boolossus Boo 2": LMItemData("Boo", 102, IC.progression, ram_addr=0x803D5E08, itembit=4),
    "Boolossus Boo 3": LMItemData("Boo", 103, IC.progression, ram_addr=0x803D5E08, itembit=5),
    "Boolossus Boo 4": LMItemData("Boo", 104, IC.progression, ram_addr=0x803D5E08, itembit=6),
    "Boolossus Boo 5": LMItemData("Boo", 105, IC.progression, ram_addr=0x803D5E08, itembit=7),
    "Boolossus Boo 6": LMItemData("Boo", 107, IC.progression, ram_addr=0x803D5E09, itembit=0),
    "Boolossus Boo 7": LMItemData("Boo", 108, IC.progression, ram_addr=0x803D5E09, itembit=1),
    "Boolossus Boo 8": LMItemData("Boo", 109, IC.progression, ram_addr=0x803D5E09, itembit=2),
    "Boolossus Boo 9": LMItemData("Boo", 110, IC.progression, ram_addr=0x803D5E09, itembit=3),
    "Boolossus Boo 10": LMItemData("Boo", 111, IC.progression, ram_addr=0x803D5E09, itembit=4),
    "Boolossus Boo 11": LMItemData("Boo", 112, IC.progression, ram_addr=0x803D5E09, itembit=5),
    "Boolossus Boo 12": LMItemData("Boo", 113, IC.progression, ram_addr=0x803D5E09, itembit=6),
    "Boolossus Boo 13": LMItemData("Boo", 114, IC.progression, ram_addr=0x803D5E09, itembit=7),
    "Boolossus Boo 14": LMItemData("Boo", 115, IC.progression, ram_addr=0x803D5E0A, itembit=0),
    "Boolossus Boo 15": LMItemData("Boo", 116, IC.progression, ram_addr=0x803D5E0A, itembit=1),
}

filler_items: Dict[str, LMItemData] = {
    "20 Coins & Bills": LMItemData("Money", 119, IC.filler, ram_addr=0x803D8B7C, pointer_offset=0x324, ram_byte_size=4),
    "Sapphire": LMItemData("Money", 121, IC.filler, ram_addr=0x803D8B7C, pointer_offset=0x330, ram_byte_size=4),
    "Emerald": LMItemData("Money", 122, IC.filler, ram_addr=0x803D8B7C, pointer_offset=0x334, ram_byte_size=4),
    "Ruby": LMItemData("Money", 123, IC.filler, ram_addr=0x803D8B7C, pointer_offset=0x338, ram_byte_size=4),
    "Diamond": LMItemData("Money", 124, IC.filler, ram_addr=0x803D8B7C, pointer_offset=0x33C, ram_byte_size=4),
    "Poison Mushroom": LMItemData("Trap", 125, IC.trap),
    # "Ghost": LMItemData("Trap", 126, IC.trap),
    "Nothing": LMItemData("Nothing Item", 127, IC.filler),
    "Small Heart": LMItemData("Heart", 128, IC.filler, ram_addr=0x803D8B40, pointer_offset=0xB8, ram_byte_size=2),
    "Large Heart": LMItemData("Heart", 129, IC.filler, ram_addr=0x803D8B40, pointer_offset=0xB8, ram_byte_size=2),
    "Bomb": LMItemData("Trap", 130, IC.trap),
    "Ice Trap": LMItemData("Trap", 131, IC.trap),
    "Banana Trap": LMItemData("Trap", 132, IC.trap),
    "10 Coins": LMItemData("Money", 133, IC.filler, ram_addr=0x803D8B7C, pointer_offset=0x324, ram_byte_size=4),
    "20 Coins": LMItemData("Money", 134, IC.filler, ram_addr=0x803D8B7C, pointer_offset=0x324, ram_byte_size=4),
    "30 Coins": LMItemData("Money", 135, IC.filler, ram_addr=0x803D8B7C, pointer_offset=0x324, ram_byte_size=4),
    "15 Bills": LMItemData("Money", 136, IC.filler, ram_addr=0x803D8B7C, pointer_offset=0x328, ram_byte_size=4),
    "25 Bills": LMItemData("Money", 137, IC.filler, ram_addr=0x803D8B7C, pointer_offset=0x328, ram_byte_size=4),
    "1 Gold Bars": LMItemData("Money", 138, IC.filler, ram_addr=0x803D8B7C, pointer_offset=0x32C, ram_byte_size=4),
    "2 Gold Bars": LMItemData("Money", 139, IC.filler, ram_addr=0x803D8B7C, pointer_offset=0x32C, ram_byte_size=4)
}

ALL_ITEMS_TABLE = {**ITEM_TABLE,
                   **BOO_ITEM_TABLE,
                   **filler_items}


def get_item_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in ALL_ITEMS_TABLE.items():
        categories.setdefault(data.type, set()).add(name)

    return categories
