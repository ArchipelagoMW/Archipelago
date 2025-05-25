from typing import NamedTuple, Dict, Set, Optional

from BaseClasses import Item
from BaseClasses import ItemClassification as IC
from .Helper_Functions import LMRamData


class LMItemData(NamedTuple):
    type: str
    code: Optional[int]
    classification: IC
    doorid: Optional[int] = None
    update_ram_addr: Optional[list[LMRamData]] = None


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


def get_item_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in ALL_ITEMS_TABLE.items():
        categories.setdefault(data.type, set()).add(name)

    return categories


ITEM_TABLE: dict[str, LMItemData] = {
    "Heart Key": LMItemData("Door Key", 0, IC.progression, 3, [LMRamData(0x803D5E14, bit_position=3)]),
    "Club Key": LMItemData("Door Key", 1, IC.progression, 42, [LMRamData(0x803D5E19, bit_position=2)]),
    "Diamond Key": LMItemData("Door Key", 2, IC.progression, 59, [LMRamData(0x803D5E1B, bit_position=3)]),
    "Spade Key": LMItemData("Door Key", 3, IC.progression, 72, [LMRamData(0x803D5E1D, bit_position=0)]),
    "Parlor Key": LMItemData("Door Key", 4, IC.progression, 34, [LMRamData(0x803D5E18, bit_position=2)]),
    "Anteroom Key": LMItemData("Door Key", 5, IC.progression, 38, [LMRamData(0x803D5E18, bit_position=6)]),
    "Wardrobe Key": LMItemData("Door Key", 6, IC.progression, 43, [LMRamData(0x803D5E19, bit_position=3)]),
    "Family Hallway Key": LMItemData("Door Key", 7, IC.progression, 33, [LMRamData(0x803D5E18, bit_position=1)]),
    "Master Bedroom Key": LMItemData("Door Key", 8, IC.progression, 31, [LMRamData(0x803D5E17, bit_position=7)]),
    "Nursery Key": LMItemData("Door Key", 9, IC.progression, 27, [LMRamData(0x803D5E17, bit_position=3)]),
    "Twins Bedroom Key": LMItemData("Door Key", 10, IC.progression, 28, [LMRamData(0x803D5E17, bit_position=4)]),
    "Ballroom Key": LMItemData("Door Key", 11, IC.progression, 15, [LMRamData(0x803D5E15, bit_position=7)]),
    "Storage Room Key": LMItemData("Door Key", 12, IC.progression, 16, [LMRamData(0x803D5E16, bit_position=0)]),
    "Fortune Teller Key": LMItemData("Door Key", 13, IC.progression, 4, [LMRamData(0x803D5E14, bit_position=4)]),
    "Laundry Room Key": LMItemData("Door Key", 14, IC.progression, 7, [LMRamData(0x803D5E14, bit_position=7)]),
    "Lower 2F Stairwell Key": LMItemData("Door Key", 15, IC.progression, 74, [LMRamData(0x803D5E1D, bit_position=2)]),
    "Conservatory Key": LMItemData("Door Key", 16, IC.progression, 21, [LMRamData(0x803D5E16, bit_position=5)]),
    "Dining Room Key": LMItemData("Door Key", 17, IC.progression, 14, [LMRamData(0x803D5E15, bit_position=6)]),
    "North Rec Room Key": LMItemData("Door Key", 18, IC.progression, 25, [LMRamData(0x803D5E17, bit_position=1)]),
    "Billiards Key": LMItemData("Door Key", 19, IC.progression, 17, [LMRamData(0x803D5E16, bit_position=1)]),
    "Safari Room Key": LMItemData("Door Key", 20, IC.progression, 56, [LMRamData(0x803D5E1B, bit_position=0)]),
    "Balcony Key": LMItemData("Door Key", 21, IC.progression, 62, [LMRamData(0x803D5E1B, bit_position=6)]),
    "Cellar Key": LMItemData("Door Key", 23, IC.progression, 68, [LMRamData(0x803D5E1C, bit_position=4)]),
    "Clockwork Key": LMItemData("Door Key", 24, IC.progression, 53, [LMRamData(0x803D5E1A, bit_position=5)]),
    "Armory Key": LMItemData("Door Key", 25, IC.progression, 51, [LMRamData(0x803D5E1A, bit_position=3)]),
    "Sitting Room Key": LMItemData("Door Key", 26, IC.progression, 29, [LMRamData(0x803D5E17, bit_position=5)]),
    "Pipe Room Key": LMItemData("Door Key", 27, IC.progression, 69, [LMRamData(0x803D5E1C, bit_position=5)]),
    "Cold Storage Key": LMItemData("Door Key", 28, IC.progression, 65, [LMRamData(0x803D5E1C, bit_position=1)]),
    "Artist's Studio Key": LMItemData("Door Key", 29, IC.progression, 63, [LMRamData(0x803D5E1B, bit_position=7)]),
    "Wardrobe Balcony Key": LMItemData("Door Key", 30, IC.progression, 41, [LMRamData(0x803D5E19, bit_position=1)]),
    "Study Key": LMItemData("Door Key", 31, IC.progression, 32, [LMRamData(0x803D5E18, bit_position=0)]),
    "Basement Stairwell Key": LMItemData("Door Key", 32, IC.progression, 9, [LMRamData(0x803D5E15, bit_position=1)]),
    "1F Bathroom Key": LMItemData("Door Key", 33, IC.progression, 23, [LMRamData(0x803D5E16, bit_position=7)]),
    "1F Washroom Key": LMItemData("Door Key", 34, IC.progression, 20, [LMRamData(0x803D5E16, bit_position=4)]),
    "Kitchen Key": LMItemData("Door Key", 35, IC.progression, 11, [LMRamData(0x803D5E15, bit_position=3)]),
    "Boneyard Key": LMItemData("Door Key", 36, IC.progression, 10, [LMRamData(0x803D5E15, bit_position=2)]),
    "Projection Room Key": LMItemData("Door Key", 37, IC.progression, 18, [LMRamData(0x803D5E16, bit_position=2)]),
    "Mirror Room Key": LMItemData("Door Key", 38, IC.progression, 5, [LMRamData(0x803D5E14, bit_position=5)]),
    "Butler's Room Key": LMItemData("Door Key", 39, IC.progression, 1, [LMRamData(0x803D5E14, bit_position=1)]),
    "Tea Room Key": LMItemData("Door Key", 40, IC.progression, 47, [LMRamData(0x803D5E19, bit_position=7)]),
    "South Rec Room Key": LMItemData("Door Key", 41, IC.progression, 24, [LMRamData(0x803D5E17, bit_position= 0)]),
    "Upper 2F Stairwell Key": LMItemData("Door Key", 42, IC.progression, 75, [LMRamData(0x803D5E1D, bit_position=3)]),
    "2F Bathroom Key": LMItemData("Door Key", 43, IC.progression, 48, [LMRamData(0x803D5E1A, bit_position=0)]),
    "2F Washroom Key": LMItemData("Door Key", 44, IC.progression, 45, [LMRamData(0x803D5E19, bit_position=5)]),
    "Nana's Room Key": LMItemData("Door Key", 45, IC.progression, 49, [LMRamData(0x803D5E1A, bit_position=1)]),
    "Astral Hall Key": LMItemData("Door Key", 46, IC.progression, 44, [LMRamData(0x803D5E19, bit_position=4)]),
    "Observatory Key": LMItemData("Door Key", 47, IC.progression, 40, [LMRamData(0x803D5E19, bit_position=0)]),
    "Guest Room Key": LMItemData("Door Key", 48, IC.progression, 30, [LMRamData(0x803D5E17, bit_position=6)]),
    "East Attic Hallway Key": LMItemData("Door Key", 49, IC.progression, 55, [LMRamData(0x803D5E1A, bit_position=7)]),
    "Telephone Room Key": LMItemData("Door Key", 50, IC.progression, 52, [LMRamData(0x803D5E1A, bit_position=4)]),
    "Ceramics Studio Key": LMItemData("Door Key", 51, IC.progression, 50, [LMRamData(0x803D5E1A, bit_position=2)]),
    "Breaker Room Key": LMItemData("Door Key", 52, IC.progression, 71, [LMRamData(0x803D5E1C, bit_position=7)]),
    "Basement Hallway Key": LMItemData("Door Key", 53, IC.progression, 67, [LMRamData(0x803D5E1C, bit_position=3)]),
    "Altar Hallway Key": LMItemData("Door Key", 54, IC.progression, 70, [LMRamData(0x803D5E1C, bit_position=6)]),
    "Fire Element Medal": LMItemData("Medal", 55, IC.progression,
        update_ram_addr=[LMRamData(0x803D5DB2, bit_position=5), LMRamData(0x803D339E, bit_position=3)]),
    "Water Element Medal": LMItemData("Medal", 56, IC.progression,
        update_ram_addr=[LMRamData(0x803D5DB2, bit_position=7), LMRamData(0x803D339E, bit_position=4)]),
    "Ice Element Medal": LMItemData("Medal", 57, IC.progression, # Flag 45
        update_ram_addr=[LMRamData(0x803D5DB2, bit_position=6), LMRamData(0x803D339E, bit_position=5)]),
    "Mario's Glove": LMItemData("Mario Item", 58, IC.progression, # Flag 21
        update_ram_addr=[LMRamData(0x803D5DBB, bit_position=6), LMRamData(0x803D339B, bit_position=5)]),
    "Mario's Hat": LMItemData("Mario Item", 59, IC.progression, # Flag 24
        update_ram_addr=[LMRamData(0x803D5DBB, bit_position=4), LMRamData(0x803D339D, bit_position=1)]),
    "Mario's Letter": LMItemData("Mario Item", 60, IC.progression, # Flag 27
        update_ram_addr=[LMRamData(0x803D5DBC, bit_position=0), LMRamData(0x803D339C, bit_position=3)]),
    "Mario's Star": LMItemData("Mario Item", 61, IC.progression, # Flag 30
        update_ram_addr=[LMRamData(0x803D5DBB, bit_position=5), LMRamData(0x803D339C, bit_position=6)]),
    "Mario's Shoe": LMItemData("Mario Item", 62, IC.progression, # Flag 33
        update_ram_addr=[LMRamData(0x803D5DBB, bit_position=7), LMRamData(0x803D339C, bit_position=0)]),
    "Boo Radar": LMItemData("Upgrade", 63, IC.progression,
        update_ram_addr=[LMRamData(0x803D33A2, bit_position=1), LMRamData(0x803D33A2, bit_position=3)]),
    "Poltergust 4000": LMItemData("Upgrade", 64, IC.useful, update_ram_addr=[LMRamData(0x80081CC8, item_count=0)]),
    "Gold Diamond": LMItemData("Money", 65, IC.progression,
        update_ram_addr=[LMRamData(0x803D8B7C, pointer_offset=0x344, ram_byte_size=4, item_count=1)]),
    "Progressive Flower": LMItemData("Flower Stage", 140, IC.progression,
        update_ram_addr=[LMRamData(0x80338fc0, ram_byte_size=4)])
}

BOO_ITEM_TABLE: dict[str, LMItemData] = {
    "Butler's Room Boo (PeekaBoo)": LMItemData("Boo", 66, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF08, bit_position=0)]),
    "Hidden Room Boo (GumBoo)": LMItemData("Boo", 67, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF08, bit_position=1)]),
    "Fortune Teller Boo (Booigi)": LMItemData("Boo", 68, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF08, bit_position=2)]),
    "Mirror Room Boo (Kung Boo)": LMItemData("Boo", 69, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF08, bit_position=3)]),
    "Laundry Room Boo (Boogie)": LMItemData("Boo", 70, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF08, bit_position=4)]),
    "Kitchen Boo (Booligan)": LMItemData("Boo", 71, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF08, bit_position=5)]),
    "Dining Room Boo (Boodacious)": LMItemData("Boo", 72, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF08, bit_position=6)]),
    "Ball Room Boo (Boo La La)": LMItemData("Boo", 73, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF08, bit_position=7)]),
    "Billiards Boo (Boohoo)": LMItemData("Boo", 74, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF09, bit_position=0)]),
    "Projection Room Boo (ShamBoo)": LMItemData("Boo", 75, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF09, bit_position=1)]),
    "Storage Room Boo (Game Boo)": LMItemData("Boo", 76, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF09, bit_position=2)]),
    "Conservatory Boo (Boomeo)": LMItemData("Boo", 77, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF09, bit_position=3)]),
    "Rec Room Boo (Booregard)": LMItemData("Boo", 78, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF09, bit_position=4)]),
    "Nursery Boo (TurBoo)": LMItemData("Boo", 79, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF09, bit_position=5)]),
    "Twin's Room Boo (Booris)": LMItemData("Boo", 80, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF09, bit_position=6)]),
    "Sitting Room Boo (Boolivia)": LMItemData("Boo", 81, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF09, bit_position=7)]),
    "Guest Room Boo (Boonita)": LMItemData("Boo", 82, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0A, bit_position=0)]),
    "Master Bedroom Boo (Boolicious)": LMItemData("Boo", 83, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0A, bit_position=1)]),
    "Study Boo (TaBoo)": LMItemData("Boo", 84, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0A, bit_position=2)]),
    "Parlor Boo (BamBoo)": LMItemData("Boo", 85, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0A, bit_position=3)]),
    "Wardrobe Boo (GameBoo Advance)": LMItemData("Boo", 86, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0A, bit_position=4)]),
    "Anteroom Boo (Bootha)": LMItemData("Boo", 87, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0A, bit_position=5)]),
    "Astral Boo (Boonswoggle)": LMItemData("Boo", 88, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0A, bit_position=6)]),
    "Nana's Room Boo (LimBooger)": LMItemData("Boo", 89, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0A, bit_position=7)]),
    "Tea Room Boo (Mr. Boojangles)": LMItemData("Boo", 90, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0B, bit_position=0)]),
    "Armory Boo (Underboo)": LMItemData("Boo", 91, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0B, bit_position=1)]),
    "Telephone Room Boo (Boomerang)": LMItemData("Boo", 92, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0B, bit_position=2)]),
    "Safari Room Boo (Little Boo Peep)": LMItemData("Boo", 93, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0B, bit_position=3)]),
    "Ceramics Studio Boo (TamBoorine)": LMItemData("Boo", 94, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0B, bit_position=4)]),
    "Clockwork Room Boo (Booscaster)": LMItemData("Boo", 95, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0B, bit_position=5)]),
    "Artist's Studio Boo (Bootique)": LMItemData("Boo", 96, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0B, bit_position=6)]),
    "Cold Storage Boo (Boolderdash)": LMItemData("Boo", 97, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0B, bit_position=7)]),
    "Cellar Boo (Booripedes)": LMItemData("Boo", 98, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0C, bit_position=0)]),
    "Pipe Room Boo (Booffant)": LMItemData("Boo", 99, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0C, bit_position=1)]),
    "Breaker Room Boo (Boo B. Hatch)": LMItemData("Boo", 100, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0C, bit_position=2)]),
    "Boolossus MiniBoo 1": LMItemData("Boo", 101, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0C, bit_position=3)]),
    "Boolossus MiniBoo 2": LMItemData("Boo", 102, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0C, bit_position=4)]),
    "Boolossus MiniBoo 3": LMItemData("Boo", 103, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0C, bit_position=5)]),
    "Boolossus MiniBoo 4": LMItemData("Boo", 104, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0C, bit_position=6)]),
    "Boolossus MiniBoo 5": LMItemData("Boo", 105, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0C, bit_position=7)]),
    "Boolossus MiniBoo 6": LMItemData("Boo", 107, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0D, bit_position=0)]),
    "Boolossus MiniBoo 7": LMItemData("Boo", 108, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0D, bit_position=1)]),
    "Boolossus MiniBoo 8": LMItemData("Boo", 109, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0D, bit_position=2)]),
    "Boolossus MiniBoo 9": LMItemData("Boo", 110, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0D, bit_position=3)]),
    "Boolossus MiniBoo 10": LMItemData("Boo", 111, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0D, bit_position=4)]),
    "Boolossus MiniBoo 11": LMItemData("Boo", 112, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0D, bit_position=5)]),
    "Boolossus MiniBoo 12": LMItemData("Boo", 113, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0D, bit_position=6)]),
    "Boolossus MiniBoo 13": LMItemData("Boo", 114, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0D, bit_position=7)]),
    "Boolossus MiniBoo 14": LMItemData("Boo", 115, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0E, bit_position=0)]),
    "Boolossus MiniBoo 15": LMItemData("Boo", 116, IC.progression,
        update_ram_addr=[LMRamData(0x804DDF0E, bit_position=1)]),
}

other_filler_items: Dict[str, LMItemData] = {
    "20 Coins & Bills": LMItemData("Money", 119, IC.filler,
        update_ram_addr=[LMRamData(0x803D8B7C, pointer_offset=0x324, ram_byte_size=4, item_count=20),
                         LMRamData(0x803D8B7C, pointer_offset=0x328, ram_byte_size=4, item_count=20)]),
    "Sapphire": LMItemData("Money", 121, IC.filler,
        update_ram_addr=[LMRamData(0x803D8B7C, pointer_offset=0x330, ram_byte_size=4, item_count=1)]),
    "Emerald": LMItemData("Money", 122, IC.filler,
        update_ram_addr=[LMRamData(0x803D8B7C, pointer_offset=0x334, ram_byte_size=4, item_count=1)]),
    "Ruby": LMItemData("Money", 123, IC.filler,
        update_ram_addr=[LMRamData(0x803D8B7C, pointer_offset=0x338, ram_byte_size=4, item_count=1)]),
    "Diamond": LMItemData("Money", 124, IC.filler,
        update_ram_addr=[LMRamData(0x803D8B7C, pointer_offset=0x33C, ram_byte_size=4, item_count=1)]),
    "Nothing": LMItemData("Nothing Item", 127, IC.filler),
    "Small Heart": LMItemData("Heart", 128, IC.filler,
        update_ram_addr=[LMRamData(0x803D8B40, pointer_offset=0xB8, ram_byte_size=2, item_count=20)]),
    "Large Heart": LMItemData("Heart", 129, IC.filler,
        update_ram_addr=[LMRamData(0x803D8B40, pointer_offset=0xB8, ram_byte_size=2, item_count=50)]),
    "10 Coins": LMItemData("Money", 133, IC.filler,
        update_ram_addr=[LMRamData(0x803D8B7C, pointer_offset=0x324, ram_byte_size=4, item_count=10)]),
    "20 Coins": LMItemData("Money", 134, IC.filler,
        update_ram_addr=[LMRamData(0x803D8B7C, pointer_offset=0x324, ram_byte_size=4, item_count=20)]),
    "30 Coins": LMItemData("Money", 135, IC.filler,
        update_ram_addr=[LMRamData(0x803D8B7C, pointer_offset=0x324, ram_byte_size=4, item_count=30)]),
    "15 Bills": LMItemData("Money", 136, IC.filler,
        update_ram_addr=[LMRamData(0x803D8B7C, pointer_offset=0x328, ram_byte_size=4, item_count=15)]),
    "25 Bills": LMItemData("Money", 137, IC.filler,
        update_ram_addr=[LMRamData(0x803D8B7C, pointer_offset=0x328, ram_byte_size=4, item_count=25)]),
    "1 Gold Bar": LMItemData("Money", 138, IC.filler,
        update_ram_addr=[LMRamData(0x803D8B7C, pointer_offset=0x32C, ram_byte_size=4, item_count=1)]),
    "2 Gold Bars": LMItemData("Money", 139, IC.filler,
        update_ram_addr=[LMRamData(0x803D8B7C, pointer_offset=0x32C, ram_byte_size=4, item_count=2)]),
}

trap_filler_items: Dict[str, LMItemData] = {
    "Possession Trap": LMItemData("Trap", 141, IC.trap,
        update_ram_addr=[LMRamData(0x804DDD4C, ram_byte_size=4, item_count=5)]),
    "Bonk Trap": LMItemData("Trap", 142, IC.trap,
        update_ram_addr=[LMRamData(0x804DDD4C, ram_byte_size=4, item_count=4)]),
    "Bomb": LMItemData("Trap", 130, IC.trap,
        update_ram_addr=[LMRamData(0x804DDD4C, ram_byte_size=4, item_count=1)]), # value of 1
    "Ice Trap": LMItemData("Trap", 131, IC.trap,
        update_ram_addr=[LMRamData(0x804DDD4C, ram_byte_size=4, item_count=3)]), # value of 3
    "Banana Trap": LMItemData("Trap", 132, IC.trap,
        update_ram_addr=[LMRamData(0x804DDD4C, ram_byte_size=4, item_count=2)]), # value of 2
    "Poison Mushroom": LMItemData("Trap", 125, IC.trap,
        update_ram_addr=[LMRamData(0x804DDD4C, ram_byte_size=4, item_count=6)]), # value of 6
    "Ghost": LMItemData("Trap", 126, IC.trap,
        update_ram_addr=[LMRamData(0x804DD940, ram_byte_size=4, item_count=1)]),

}

filler_items = {**other_filler_items,
                **trap_filler_items}

ALL_ITEMS_TABLE = {**ITEM_TABLE,
                   **BOO_ITEM_TABLE,
                   **filler_items}


BOO_AP_ID_LIST: list[int] = [LMItem.get_apid(value.code) for value in BOO_ITEM_TABLE.values()]
IMPORTANT_ITEM_AP_LIST: list[int] = [LMItem.get_apid(value.code) for value in ITEM_TABLE.values() if
    not value.code == 65]

# Mario items + Elemental Medals + Traps + Boo Radar + Super Vac + Progressive Flower + Certain Traps
RECV_OWN_GAME_ITEMS: list[int] = BOO_AP_ID_LIST + IMPORTANT_ITEM_AP_LIST + [8126, 8141, 8142]

# List of received items to ignore because they are handled elsewhere
RECV_ITEMS_IGNORE: list[int] = [8127]

# List of health related items, which are used to not exceed max health
HEALTH_RELATED_ITEMS: list[int] = [8128, 8129]

ICE_TRAP_EQUIV = ["Freeze Trap", "Frozen Trap", "Ice Trap"]
BOMB_EQUIV = ["TNT Barrel Trap", "Bomb", "Fire Trap"]
BANANA_TRAP_EQUIV = ["Stun Trap", "Banana Trap", "Thwimp Trap", "Hiccup Trap"]
GHOST_EQUIV = ["OmoTrap", "Ghost", "Bee Trap", "Police Trap", "Nut Trap", "Army Trap"]
POISON_MUSH_EQUIV = [ "Tiny Trap", "Poison Mushroom"]
BONK_EQUIV = ["Spring Trap", "Damage Trap", "Bonk Trap"]
POSSESION_EQUIV = ["Poison Trap", "Possession Trap", "Laughter Trap"]

trap_id_list = [8125, 8126, 8130, 8131, 8132, 8141, 8142]
ACCEPTED_TRAPS = ICE_TRAP_EQUIV+BOMB_EQUIV+BANANA_TRAP_EQUIV+GHOST_EQUIV+POISON_MUSH_EQUIV+BONK_EQUIV+POSSESION_EQUIV