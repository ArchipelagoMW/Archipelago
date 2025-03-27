from collections.abc import Iterable
from typing import TYPE_CHECKING, NamedTuple, Optional

from BaseClasses import Item
from BaseClasses import ItemClassification as IC
from worlds.AutoWorld import World

if TYPE_CHECKING:
    from .randomizers.Dungeons import Dungeon


def item_factory(items: str | Iterable[str], world: World) -> Item | list[Item]:
    """
    Create items based on their names.
    Depending on the input, this function can return a single item or a list of items.

    :param items: The name or names of the items to create.
    :param world: The game world.
    :raises KeyError: If an unknown item name is provided.
    :return: A single item or a list of items.
    """
    ret: list[Item] = []
    singleton = False
    if isinstance(items, str):
        items = [items]
        singleton = True
    for item in items:
        if item in ITEM_TABLE:
            ret.append(world.create_item(item))
        else:
            raise KeyError(f"Unknown item {item}")

    return ret[0] if singleton else ret


class TWWItemData(NamedTuple):
    """
    This class represents the data for an item in The Wind Waker.

    :param type: The type of the item (e.g., "Item", "Dungeon Item").
    :param classification: The item's classification (progression, useful, filler).
    :param code: The unique code identifier for the item.
    :param quantity: The number of this item available.
    :param item_id: The ID used to represent the item in-game.
    """

    type: str
    classification: IC
    code: Optional[int]
    quantity: int
    item_id: Optional[int]


class TWWItem(Item):
    """
    This class represents an item in The Wind Waker.

    :param name: The item's name.
    :param player: The ID of the player who owns the item.
    :param data: The data associated with this item.
    :param classification: Optional classification to override the default.
    """

    game: str = "The Wind Waker"
    type: Optional[str]
    dungeon: Optional["Dungeon"] = None

    def __init__(self, name: str, player: int, data: TWWItemData, classification: Optional[IC] = None) -> None:
        super().__init__(
            name,
            data.classification if classification is None else classification,
            None if data.code is None else TWWItem.get_apid(data.code),
            player,
        )

        self.type = data.type
        self.item_id = data.item_id

    @staticmethod
    def get_apid(code: int) -> int:
        """
        Compute the Archipelago ID for the given item code.

        :param code: The unique code for the item.
        :return: The computed Archipelago ID.
        """
        base_id: int = 2322432
        return base_id + code

    @property
    def dungeon_item(self) -> Optional[str]:
        """
        Determine if the item is a dungeon item and, if so, returns its type.

        :return: The type of dungeon item, or `None` if it is not a dungeon item.
        """
        if self.type in ("Small Key", "Big Key", "Map", "Compass"):
            return self.type
        return None


ITEM_TABLE: dict[str, TWWItemData] = {
    "Telescope":                 TWWItemData("Item",      IC.useful,                       0,  1, 0x20),
  # "Boat's Sail":               TWWItemData("Item",      IC.progression,                  1,  1, 0x78),  # noqa: E131
    "Wind Waker":                TWWItemData("Item",      IC.progression,                  2,  1, 0x22),
    "Grappling Hook":            TWWItemData("Item",      IC.progression,                  3,  1, 0x25),
    "Spoils Bag":                TWWItemData("Item",      IC.progression,                  4,  1, 0x24),
    "Boomerang":                 TWWItemData("Item",      IC.progression,                  5,  1, 0x2D),
    "Deku Leaf":                 TWWItemData("Item",      IC.progression,                  6,  1, 0x34),
    "Tingle Tuner":              TWWItemData("Item",      IC.progression,                  7,  1, 0x21),
    "Iron Boots":                TWWItemData("Item",      IC.progression,                  8,  1, 0x29),
    "Magic Armor":               TWWItemData("Item",      IC.progression,                  9,  1, 0x2A),
    "Bait Bag":                  TWWItemData("Item",      IC.progression,                 10,  1, 0x2C),
    "Bombs":                     TWWItemData("Item",      IC.progression,                 11,  1, 0x31),
    "Delivery Bag":              TWWItemData("Item",      IC.progression,                 12,  1, 0x30),
    "Hookshot":                  TWWItemData("Item",      IC.progression,                 13,  1, 0x2F),
    "Skull Hammer":              TWWItemData("Item",      IC.progression,                 14,  1, 0x33),
    "Power Bracelets":           TWWItemData("Item",      IC.progression,                 15,  1, 0x28),

    "Hero's Charm":              TWWItemData("Item",      IC.useful,                      16,  1, 0x43),
    "Hurricane Spin":            TWWItemData("Item",      IC.useful,                      17,  1, 0xAA),
    "Dragon Tingle Statue":      TWWItemData("Item",      IC.progression,                 18,  1, 0xA3),
    "Forbidden Tingle Statue":   TWWItemData("Item",      IC.progression,                 19,  1, 0xA4),
    "Goddess Tingle Statue":     TWWItemData("Item",      IC.progression,                 20,  1, 0xA5),
    "Earth Tingle Statue":       TWWItemData("Item",      IC.progression,                 21,  1, 0xA6),
    "Wind Tingle Statue":        TWWItemData("Item",      IC.progression,                 22,  1, 0xA7),

    "Wind's Requiem":            TWWItemData("Item",      IC.progression,                 23,  1, 0x6D),
    "Ballad of Gales":           TWWItemData("Item",      IC.progression,                 24,  1, 0x6E),
    "Command Melody":            TWWItemData("Item",      IC.progression,                 25,  1, 0x6F),
    "Earth God's Lyric":         TWWItemData("Item",      IC.progression,                 26,  1, 0x70),
    "Wind God's Aria":           TWWItemData("Item",      IC.progression,                 27,  1, 0x71),
    "Song of Passing":           TWWItemData("Item",      IC.progression,                 28,  1, 0x72),

    "Triforce Shard 1":          TWWItemData("Item",      IC.progression,                 29,  1, 0x61),
    "Triforce Shard 2":          TWWItemData("Item",      IC.progression,                 30,  1, 0x62),
    "Triforce Shard 3":          TWWItemData("Item",      IC.progression,                 31,  1, 0x63),
    "Triforce Shard 4":          TWWItemData("Item",      IC.progression,                 32,  1, 0x64),
    "Triforce Shard 5":          TWWItemData("Item",      IC.progression,                 33,  1, 0x65),
    "Triforce Shard 6":          TWWItemData("Item",      IC.progression,                 34,  1, 0x66),
    "Triforce Shard 7":          TWWItemData("Item",      IC.progression,                 35,  1, 0x67),
    "Triforce Shard 8":          TWWItemData("Item",      IC.progression,                 36,  1, 0x68),

    "Skull Necklace":            TWWItemData("Item",      IC.filler,                      37,  9, 0x45),
    "Boko Baba Seed":            TWWItemData("Item",      IC.filler,                      38,  1, 0x46),
    "Golden Feather":            TWWItemData("Item",      IC.filler,                      39,  9, 0x47),
    "Knight's Crest":            TWWItemData("Item",      IC.filler,                      40,  3, 0x48),
    "Red Chu Jelly":             TWWItemData("Item",      IC.filler,                      41,  1, 0x49),
    "Green Chu Jelly":           TWWItemData("Item",      IC.filler,                      42,  1, 0x4A),
    "Joy Pendant":               TWWItemData("Item",      IC.filler,                      43, 20, 0x1F),
    "All-Purpose Bait":          TWWItemData("Item",      IC.filler,                      44,  1, 0x82),
    "Hyoi Pear":                 TWWItemData("Item",      IC.filler,                      45,  4, 0x83),

    "Note to Mom":               TWWItemData("Item",      IC.progression,                 46,  1, 0x99),
    "Maggie's Letter":           TWWItemData("Item",      IC.progression,                 47,  1, 0x9A),
    "Moblin's Letter":           TWWItemData("Item",      IC.progression,                 48,  1, 0x9B),
    "Cabana Deed":               TWWItemData("Item",      IC.progression,                 49,  1, 0x9C),
    "Fill-Up Coupon":            TWWItemData("Item",      IC.useful,                      50,  1, 0x9E),

    "Nayru's Pearl":             TWWItemData("Item",      IC.progression,                 51,  1, 0x69),
    "Din's Pearl":               TWWItemData("Item",      IC.progression,                 52,  1, 0x6A),
    "Farore's Pearl":            TWWItemData("Item",      IC.progression,                 53,  1, 0x6B),

    "Progressive Sword":         TWWItemData("Item",      IC.progression,                 54,  4, 0x38),
    "Progressive Shield":        TWWItemData("Item",      IC.progression,                 55,  2, 0x3B),
    "Progressive Picto Box":     TWWItemData("Item",      IC.progression,                 56,  2, 0x23),
    "Progressive Bow":           TWWItemData("Item",      IC.progression,                 57,  3, 0x27),
    "Progressive Magic Meter":   TWWItemData("Item",      IC.progression,                 58,  2, 0xB1),
    "Quiver Capacity Upgrade":   TWWItemData("Item",      IC.progression,                 59,  2, 0xAF),
    "Bomb Bag Capacity Upgrade": TWWItemData("Item",      IC.useful,                      60,  2, 0xAD),
    "Wallet Capacity Upgrade":   TWWItemData("Item",      IC.progression,                 61,  2, 0xAB),
    "Empty Bottle":              TWWItemData("Item",      IC.progression,                 62,  4, 0x50),

    "Triforce Chart 1":          TWWItemData("Item",      IC.progression_skip_balancing,  63,  1, 0xFE),
    "Triforce Chart 2":          TWWItemData("Item",      IC.progression_skip_balancing,  64,  1, 0xFD),
    "Triforce Chart 3":          TWWItemData("Item",      IC.progression_skip_balancing,  65,  1, 0xFC),
    "Triforce Chart 4":          TWWItemData("Item",      IC.progression_skip_balancing,  66,  1, 0xFB),
    "Triforce Chart 5":          TWWItemData("Item",      IC.progression_skip_balancing,  67,  1, 0xFA),
    "Triforce Chart 6":          TWWItemData("Item",      IC.progression_skip_balancing,  68,  1, 0xF9),
    "Triforce Chart 7":          TWWItemData("Item",      IC.progression_skip_balancing,  69,  1, 0xF8),
    "Triforce Chart 8":          TWWItemData("Item",      IC.progression_skip_balancing,  70,  1, 0xF7),
    "Treasure Chart 1":          TWWItemData("Item",      IC.progression_skip_balancing,  71,  1, 0xE7),
    "Treasure Chart 2":          TWWItemData("Item",      IC.progression_skip_balancing,  72,  1, 0xEE),
    "Treasure Chart 3":          TWWItemData("Item",      IC.progression_skip_balancing,  73,  1, 0xE0),
    "Treasure Chart 4":          TWWItemData("Item",      IC.progression_skip_balancing,  74,  1, 0xE1),
    "Treasure Chart 5":          TWWItemData("Item",      IC.progression_skip_balancing,  75,  1, 0xF2),
    "Treasure Chart 6":          TWWItemData("Item",      IC.progression_skip_balancing,  76,  1, 0xEA),
    "Treasure Chart 7":          TWWItemData("Item",      IC.progression_skip_balancing,  77,  1, 0xCC),
    "Treasure Chart 8":          TWWItemData("Item",      IC.progression_skip_balancing,  78,  1, 0xD4),
    "Treasure Chart 9":          TWWItemData("Item",      IC.progression_skip_balancing,  79,  1, 0xDA),
    "Treasure Chart 10":         TWWItemData("Item",      IC.progression_skip_balancing,  80,  1, 0xDE),
    "Treasure Chart 11":         TWWItemData("Item",      IC.progression_skip_balancing,  81,  1, 0xF6),
    "Treasure Chart 12":         TWWItemData("Item",      IC.progression_skip_balancing,  82,  1, 0xE9),
    "Treasure Chart 13":         TWWItemData("Item",      IC.progression_skip_balancing,  83,  1, 0xCF),
    "Treasure Chart 14":         TWWItemData("Item",      IC.progression_skip_balancing,  84,  1, 0xDD),
    "Treasure Chart 15":         TWWItemData("Item",      IC.progression_skip_balancing,  85,  1, 0xF5),
    "Treasure Chart 16":         TWWItemData("Item",      IC.progression_skip_balancing,  86,  1, 0xE3),
    "Treasure Chart 17":         TWWItemData("Item",      IC.progression_skip_balancing,  87,  1, 0xD7),
    "Treasure Chart 18":         TWWItemData("Item",      IC.progression_skip_balancing,  88,  1, 0xE4),
    "Treasure Chart 19":         TWWItemData("Item",      IC.progression_skip_balancing,  89,  1, 0xD1),
    "Treasure Chart 20":         TWWItemData("Item",      IC.progression_skip_balancing,  90,  1, 0xF3),
    "Treasure Chart 21":         TWWItemData("Item",      IC.progression_skip_balancing,  91,  1, 0xCE),
    "Treasure Chart 22":         TWWItemData("Item",      IC.progression_skip_balancing,  92,  1, 0xD9),
    "Treasure Chart 23":         TWWItemData("Item",      IC.progression_skip_balancing,  93,  1, 0xF1),
    "Treasure Chart 24":         TWWItemData("Item",      IC.progression_skip_balancing,  94,  1, 0xEB),
    "Treasure Chart 25":         TWWItemData("Item",      IC.progression_skip_balancing,  95,  1, 0xD6),
    "Treasure Chart 26":         TWWItemData("Item",      IC.progression_skip_balancing,  96,  1, 0xD3),
    "Treasure Chart 27":         TWWItemData("Item",      IC.progression_skip_balancing,  97,  1, 0xCD),
    "Treasure Chart 28":         TWWItemData("Item",      IC.progression_skip_balancing,  98,  1, 0xE2),
    "Treasure Chart 29":         TWWItemData("Item",      IC.progression_skip_balancing,  99,  1, 0xE6),
    "Treasure Chart 30":         TWWItemData("Item",      IC.progression_skip_balancing, 100,  1, 0xF4),
    "Treasure Chart 31":         TWWItemData("Item",      IC.progression_skip_balancing, 101,  1, 0xF0),
    "Treasure Chart 32":         TWWItemData("Item",      IC.progression_skip_balancing, 102,  1, 0xD0),
    "Treasure Chart 33":         TWWItemData("Item",      IC.progression_skip_balancing, 103,  1, 0xEF),
    "Treasure Chart 34":         TWWItemData("Item",      IC.progression_skip_balancing, 104,  1, 0xE5),
    "Treasure Chart 35":         TWWItemData("Item",      IC.progression_skip_balancing, 105,  1, 0xE8),
    "Treasure Chart 36":         TWWItemData("Item",      IC.progression_skip_balancing, 106,  1, 0xD8),
    "Treasure Chart 37":         TWWItemData("Item",      IC.progression_skip_balancing, 107,  1, 0xD5),
    "Treasure Chart 38":         TWWItemData("Item",      IC.progression_skip_balancing, 108,  1, 0xED),
    "Treasure Chart 39":         TWWItemData("Item",      IC.progression_skip_balancing, 109,  1, 0xEC),
    "Treasure Chart 40":         TWWItemData("Item",      IC.progression_skip_balancing, 110,  1, 0xDF),
    "Treasure Chart 41":         TWWItemData("Item",      IC.progression_skip_balancing, 111,  1, 0xD2),

    "Tingle's Chart":            TWWItemData("Item",      IC.filler,                     112,  1, 0xDC),
    "Ghost Ship Chart":          TWWItemData("Item",      IC.progression,                113,  1, 0xDB),
    "Octo Chart":                TWWItemData("Item",      IC.filler,                     114,  1, 0xCA),
    "Great Fairy Chart":         TWWItemData("Item",      IC.filler,                     115,  1, 0xC9),
    "Secret Cave Chart":         TWWItemData("Item",      IC.filler,                     116,  1, 0xC6),
    "Light Ring Chart":          TWWItemData("Item",      IC.filler,                     117,  1, 0xC5),
    "Platform Chart":            TWWItemData("Item",      IC.filler,                     118,  1, 0xC4),
    "Beedle's Chart":            TWWItemData("Item",      IC.filler,                     119,  1, 0xC3),
    "Submarine Chart":           TWWItemData("Item",      IC.filler,                     120,  1, 0xC2),

    "Green Rupee":               TWWItemData("Item",      IC.filler,                     121,  1, 0x01),
    "Blue Rupee":                TWWItemData("Item",      IC.filler,                     122,  2, 0x02),
    "Yellow Rupee":              TWWItemData("Item",      IC.filler,                     123,  3, 0x03),
    "Red Rupee":                 TWWItemData("Item",      IC.filler,                     124,  8, 0x04),
    "Purple Rupee":              TWWItemData("Item",      IC.filler,                     125, 10, 0x05),
    "Orange Rupee":              TWWItemData("Item",      IC.useful,                     126, 15, 0x06),
    "Silver Rupee":              TWWItemData("Item",      IC.useful,                     127, 20, 0x0F),
    "Rainbow Rupee":             TWWItemData("Item",      IC.useful,                     128,  1, 0xB8),

    "Piece of Heart":            TWWItemData("Item",      IC.useful,                     129, 44, 0x07),
    "Heart Container":           TWWItemData("Item",      IC.useful,                     130,  6, 0x08),

    "DRC Big Key":               TWWItemData("Big Key",   IC.progression,                131,  1, 0x14),
    "DRC Small Key":             TWWItemData("Small Key", IC.progression,                132,  4, 0x13),
    "FW Big Key":                TWWItemData("Big Key",   IC.progression,                133,  1, 0x40),
    "FW Small Key":              TWWItemData("Small Key", IC.progression,                134,  1, 0x1D),
    "TotG Big Key":              TWWItemData("Big Key",   IC.progression,                135,  1, 0x5C),
    "TotG Small Key":            TWWItemData("Small Key", IC.progression,                136,  2, 0x5B),
    "ET Big Key":                TWWItemData("Big Key",   IC.progression,                138,  1, 0x74),
    "ET Small Key":              TWWItemData("Small Key", IC.progression,                139,  3, 0x73),
    "WT Big Key":                TWWItemData("Big Key",   IC.progression,                140,  1, 0x81),
    "WT Small Key":              TWWItemData("Small Key", IC.progression,                141,  2, 0x77),
    "DRC Dungeon Map":           TWWItemData("Map",       IC.filler,                     142,  1, 0x1B),
    "DRC Compass":               TWWItemData("Compass",   IC.filler,                     143,  1, 0x1C),
    "FW Dungeon Map":            TWWItemData("Map",       IC.filler,                     144,  1, 0x41),
    "FW Compass":                TWWItemData("Compass",   IC.filler,                     145,  1, 0x5A),
    "TotG Dungeon Map":          TWWItemData("Map",       IC.filler,                     146,  1, 0x5D),
    "TotG Compass":              TWWItemData("Compass",   IC.filler,                     147,  1, 0x5E),
    "FF Dungeon Map":            TWWItemData("Map",       IC.filler,                     148,  1, 0x5F),
    "FF Compass":                TWWItemData("Compass",   IC.filler,                     149,  1, 0x60),
    "ET Dungeon Map":            TWWItemData("Map",       IC.filler,                     150,  1, 0x75),
    "ET Compass":                TWWItemData("Compass",   IC.filler,                     151,  1, 0x76),
    "WT Dungeon Map":            TWWItemData("Map",       IC.filler,                     152,  1, 0x84),
    "WT Compass":                TWWItemData("Compass",   IC.filler,                     153,  1, 0x85),

    "Victory":                   TWWItemData("Event",     IC.progression,               None,  1, None),
}

ISLAND_NUMBER_TO_CHART_NAME = {
    1: "Treasure Chart 25",
    2: "Treasure Chart 7",
    3: "Treasure Chart 24",
    4: "Triforce Chart 2",
    5: "Treasure Chart 11",
    6: "Triforce Chart 7",
    7: "Treasure Chart 13",
    8: "Treasure Chart 41",
    9: "Treasure Chart 29",
    10: "Treasure Chart 22",
    11: "Treasure Chart 18",
    12: "Treasure Chart 30",
    13: "Treasure Chart 39",
    14: "Treasure Chart 19",
    15: "Treasure Chart 8",
    16: "Treasure Chart 2",
    17: "Treasure Chart 10",
    18: "Treasure Chart 26",
    19: "Treasure Chart 3",
    20: "Treasure Chart 37",
    21: "Treasure Chart 27",
    22: "Treasure Chart 38",
    23: "Triforce Chart 1",
    24: "Treasure Chart 21",
    25: "Treasure Chart 6",
    26: "Treasure Chart 14",
    27: "Treasure Chart 34",
    28: "Treasure Chart 5",
    29: "Treasure Chart 28",
    30: "Treasure Chart 35",
    31: "Triforce Chart 3",
    32: "Triforce Chart 6",
    33: "Treasure Chart 1",
    34: "Treasure Chart 20",
    35: "Treasure Chart 36",
    36: "Treasure Chart 23",
    37: "Treasure Chart 12",
    38: "Treasure Chart 16",
    39: "Treasure Chart 4",
    40: "Treasure Chart 17",
    41: "Treasure Chart 31",
    42: "Triforce Chart 5",
    43: "Treasure Chart 9",
    44: "Triforce Chart 4",
    45: "Treasure Chart 40",
    46: "Triforce Chart 8",
    47: "Treasure Chart 15",
    48: "Treasure Chart 32",
    49: "Treasure Chart 33",
}


LOOKUP_ID_TO_NAME: dict[int, str] = {
    TWWItem.get_apid(data.code): item for item, data in ITEM_TABLE.items() if data.code is not None
}

item_name_groups = {
    "Songs": {
        "Wind's Requiem",
        "Ballad of Gales",
        "Command Melody",
        "Earth God's Lyric",
        "Wind God's Aria",
        "Song of Passing",
    },
    "Mail": {
        "Note to Mom",
        "Maggie's Letter",
        "Moblin's Letter",
    },
    "Special Charts": {
        "Tingle's Chart",
        "Ghost Ship Chart",
        "Octo Chart",
        "Great Fairy Chart",
        "Secret Cave Chart",
        "Light Ring Chart",
        "Platform Chart",
        "Beedle's Chart",
        "Submarine Chart",
    },
}
# generic groups, (Name, substring)
_simple_groups = {
    ("Tingle Statues", "Tingle Statue"),
    ("Shards", "Shard"),
    ("Pearls", "Pearl"),
    ("Triforce Charts", "Triforce Chart"),
    ("Treasure Charts", "Treasure Chart"),
    ("Small Keys", "Small Key"),
    ("Big Keys", "Big Key"),
    ("Rupees", "Rupee"),
    ("Dungeon Items", "Compass"),
    ("Dungeon Items", "Map"),
}
for basename, substring in _simple_groups:
    if basename not in item_name_groups:
        item_name_groups[basename] = set()
    for itemname in ITEM_TABLE:
        if substring in itemname:
            item_name_groups[basename].add(itemname)
