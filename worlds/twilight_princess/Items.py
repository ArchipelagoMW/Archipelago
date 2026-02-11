from collections.abc import Iterable
from typing import TYPE_CHECKING, NamedTuple, Optional, Union

from BaseClasses import Item, Item
from BaseClasses import ItemClassification as IC
from worlds.AutoWorld import World

# from .Randomizer.Dungeons import Dungeon


# Events / Items to add
# DiababaDefeated
# FyrusDefeated
# MorpheelDefeated
# StallordDefeated
# BlizzetaDefeated
# ArmogohmaDefeated
# ArgorokDefeated
# ZantDefeated


class TPItemData(NamedTuple):
    """
    This class represents the data for an item in Twilight Princess

    :param type: The type of the item (e.g., "Item", "Poe").
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
    game: str = "Twilight Princess"


class TPItem(Item):
    """
    This class represents an item in Twilight Princess

    :param name: The item's name.
    :param player: The ID of the player who owns the item.
    :param data: The data associated with this item.
    :param classification: Optional classification to override the default.
    """

    game: str = "Twilight Princess"
    type: Optional[str]

    def __init__(
        self,
        name: str,
        player: int,
        data: TPItemData,
        classification: Optional[IC] = None,
        # dungeon: Optional[Dungeon] = None,
    ) -> None:
        super().__init__(
            name,
            data.classification if classification is None else classification,
            None if data.code is None else TPItem.get_apid(data.code),
            player,
        )
        # self.dungeon = dungeon
        self.type = data.type
        self.item_id = data.item_id

    @staticmethod
    def get_apid(code: int) -> int:
        """
        Compute the Archipelago ID for the given item code.

        :param code: The unique code for the item.
        :return: The computed Archipelago ID.
        """
        base_id: int = 2320000
        return base_id + code


def item_factory(
    items: Union[str, Iterable[str]], world: World
) -> Union[TPItem, list[TPItem]]:
    """
    Create items based on their names.
    Depending on the input, this function can return a single item or a list of items.

    :param items: The name or names of the items to create.
    :param world: The game world.
    :raises KeyError: If an unknown item name is provided.
    :return: A single item or a list of items.
    """
    ret: list[TPItem] = []
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


VERY_USEFUL = IC.progression | IC.useful
ITEM_TABLE: dict[str, TPItemData] = {
    "Green Rupee": TPItemData("Rupee", IC.filler, 0, 1, 0x01),
    "Blue Rupee": TPItemData("Rupee", IC.filler, 1, 1, 0x02),
    "Yellow Rupee": TPItemData("Rupee", IC.filler, 2, 1, 0x03),
    "Red Rupee": TPItemData("Rupee", IC.filler, 3, 1, 0x04),
    "Purple Rupee": TPItemData("Rupee", IC.filler, 4, 1, 0x05),
    "Orange Rupee": TPItemData("Rupee", IC.filler, 5, 1, 0x06),
    "Silver Rupee": TPItemData("Rupee", IC.filler, 6, 1, 0x07),
    "Links Purple Rupee": TPItemData("Rupee", IC.filler, 7, 1, 0xED),
    "Bombs (5)": TPItemData("Ammo", IC.filler, 8, 1, 0x0A),
    "Bombs (10)": TPItemData("Ammo", IC.filler, 9, 1, 0x0B),
    "Bombs (20)": TPItemData("Ammo", IC.filler, 10, 1, 0x0C),
    "Bombs (30)": TPItemData("Ammo", IC.filler, 11, 1, 0x0D),
    "Arrows (10)": TPItemData("Ammo", IC.filler, 12, 1, 0x0E),
    "Arrows (20)": TPItemData("Ammo", IC.filler, 13, 1, 0x0F),
    "Arrows (30)": TPItemData("Ammo", IC.filler, 14, 1, 0x10),
    "Seeds (50)": TPItemData("Ammo", IC.filler, 15, 1, 0x12),
    "Water Bombs (3)": TPItemData("Ammo", IC.filler, 16, 1, 0x19),
    "Water Bombs (5)": TPItemData("Ammo", IC.filler, 17, 1, 0x16),
    "Water Bombs (10)": TPItemData("Ammo", IC.filler, 18, 1, 0x17),
    "Water Bombs (15)": TPItemData("Ammo", IC.filler, 19, 1, 0x18),
    "Bomblings (3)": TPItemData("Ammo", IC.filler, 20, 1, 0x1C),
    "Bomblings (5)": TPItemData("Ammo", IC.filler, 21, 1, 0x1A),
    "Bomblings (10)": TPItemData("Ammo", IC.filler, 22, 1, 0x1B),
    "Piece of Heart": TPItemData("Heart", IC.useful, 23, 45, 0x21),
    "Heart Container": TPItemData("Heart", IC.useful, 24, 8, 0x22),
    "Progressive Master Sword": TPItemData("Item", VERY_USEFUL, 25, 4, 0x29),
    "Ordon Shield": TPItemData("Item", IC.progression, 26, 1, 0x2A),
    "Hylian Shield": TPItemData("Item", IC.progression, 27, 1, 0x2C),
    "Magic Armor": TPItemData("Item", IC.progression, 28, 1, 0x30),
    "Zora Armor": TPItemData("Item", IC.progression, 29, 1, 0x31),
    "Shadow Crystal": TPItemData("Item", VERY_USEFUL, 30, 1, 0x32),
    "Progressive Wallet": TPItemData("Item", IC.progression, 31, 2, 0x36),
    "Hawkeye": TPItemData("Item", IC.progression, 32, 1, 0x3E),
    "Gale Boomerang": TPItemData("Item", VERY_USEFUL, 33, 1, 0x40),
    "Spinner": TPItemData("Item", VERY_USEFUL, 34, 1, 0x41),
    "Ball and Chain": TPItemData("Item", VERY_USEFUL, 35, 1, 0x42),
    "Progressive Hero's Bow": TPItemData("Item", VERY_USEFUL, 36, 3, 0x43),
    "Progressive Clawshot": TPItemData("Item", VERY_USEFUL, 37, 2, 0x44),
    "Iron Boots": TPItemData("Item", VERY_USEFUL, 38, 1, 0x45),
    "Progressive Dominion Rod": TPItemData("Item", IC.progression, 39, 2, 0x46),
    "Lantern": TPItemData("Item", VERY_USEFUL, 40, 1, 0x48),
    "Progressive Fishing Rod": TPItemData("Item", IC.progression, 41, 2, 0x4A),
    "Slingshot": TPItemData("Item", IC.progression, 44, 1, 0x4B),
    "Bomb Bag": TPItemData("Item", IC.progression, 45, 3, 0x51),
    "Empty Bottle (Fishing Hole)": TPItemData("Bottle", IC.progression, 46, 1, 0x60),
    "Milk (half) (Sera Bottle)": TPItemData("Bottle", IC.progression, 47, 1, 0x65),
    "Lantern Oil (Coro Bottle)": TPItemData("Bottle", IC.progression, 48, 1, 0x9D),
    "Great Fairy Tears (Jovani)": TPItemData("Bottle", IC.progression, 49, 1, 0x75),
    # Story Items fit here (useful if randomized eventually)
    "Horse Call": TPItemData("Item", VERY_USEFUL, 53, 1, 0x84),
    "Forest Temple Small Key": TPItemData("Small key", IC.progression, 54, 4, 0x85),
    "Goron Mines Small Key": TPItemData("Small key", IC.progression, 55, 3, 0x86),
    "Lakebed Temple Small Key": TPItemData("Small key", IC.progression, 56, 3, 0x87),
    "Arbiters Grounds Small Key": TPItemData("Small key", IC.progression, 57, 5, 0x88),
    "Snowpeak Ruins Small Key": TPItemData("Small key", IC.progression, 58, 4, 0x89),
    "Temple of Time Small Key": TPItemData("Small key", IC.progression, 59, 3, 0x8A),
    "City in The Sky Small Key": TPItemData("Small key", IC.progression, 60, 1, 0x8B),
    "Palace of Twilight Small Key": TPItemData(
        "Small key", IC.progression, 61, 7, 0x8C
    ),
    "Hyrule Castle Small Key": TPItemData("Small key", IC.progression, 62, 3, 0x8D),
    # "Small Key (North Faron Gate)": TPItemData(
    #     "Small key", IC.progression, 63, 1, 0xEE
    # ),
    # "Small Key (Coro)": TPItemData("Small key", IC.progression, 64, 1, 0xFE),
    "Gate Keys": TPItemData("Small key", IC.progression, 65, 1, 0xF3),
    "Gerudo Desert Bublin Camp Key": TPItemData(
        "Small key", IC.progression, 66, 1, 0x8E
    ),
    "Auru's Memo": TPItemData("Item", IC.progression, 67, 1, 0x90),
    "Ashei's Sketch": TPItemData("Item", IC.progression, 68, 1, 0x91),
    "Forest Temple Big Key": TPItemData("Big Key", IC.progression, 69, 1, 0x92),
    "Lakebed Temple Big Key": TPItemData("Big Key", IC.progression, 70, 1, 0x93),
    "Goron Mines Key Shard": TPItemData("Big Key", IC.progression, 71, 3, 0xF9),
    "Arbiters Grounds Big Key": TPItemData("Big Key", IC.progression, 72, 1, 0x94),
    "Bedroom Key": TPItemData("Big Key", IC.progression, 73, 1, 0xF6),
    "Temple of Time Big Key": TPItemData("Big Key", IC.progression, 74, 1, 0x95),
    "City in The Sky Big Key": TPItemData("Big Key", IC.progression, 75, 1, 0x96),
    "Palace of Twilight Big Key": TPItemData("Big Key", IC.progression, 76, 1, 0x97),
    "Hyrule Castle Big Key": TPItemData("Big Key", IC.progression, 77, 1, 0x98),
    "Forest Temple Compass": TPItemData("Compass", IC.useful, 78, 1, 0x99),
    "Goron Mines Compass": TPItemData("Compass", IC.useful, 79, 1, 0x9A),
    "Lakebed Temple Compass": TPItemData("Compass", IC.useful, 80, 1, 0x9B),
    "Arbiters Grounds Compass": TPItemData("Compass", IC.useful, 81, 1, 0xA8),
    "Snowpeak Ruins Compass": TPItemData("Compass", IC.useful, 82, 1, 0xA9),
    "Temple of Time Compass": TPItemData("Compass", IC.useful, 83, 1, 0xAA),
    "City in The Sky Compass": TPItemData("Compass", IC.useful, 84, 1, 0xAB),
    "Palace of Twilight Compass": TPItemData("Compass", IC.useful, 85, 1, 0xAC),
    "Hyrule Castle Compass": TPItemData("Compass", IC.useful, 86, 1, 0xAD),
    "Forest Temple Map": TPItemData("Map", IC.useful, 87, 1, 0xB6),
    "Goron Mines Map": TPItemData("Map", IC.useful, 88, 1, 0xB7),
    "Lakebed Temple Map": TPItemData("Map", IC.useful, 89, 1, 0xB8),
    "Arbiters Grounds Map": TPItemData("Map", IC.useful, 90, 1, 0xB9),
    "Snowpeak Ruins Map": TPItemData("Map", IC.useful, 91, 1, 0xBA),
    "Temple of Time Map": TPItemData("Map", IC.useful, 92, 1, 0xBB),
    "City in The Sky Map": TPItemData("Map", IC.useful, 93, 1, 0xBC),
    "Palace of Twilight Map": TPItemData("Map", IC.useful, 94, 1, 0xBD),
    "Hyrule Castle Map": TPItemData("Map", IC.useful, 95, 1, 0xBE),
    "Male Beetle": TPItemData("Bug", IC.progression, 96, 1, 0xC0),
    "Female Beetle": TPItemData("Bug", IC.progression, 97, 1, 0xC1),
    "Male Butterfly": TPItemData("Bug", IC.progression, 98, 1, 0xC2),
    "Female Butterfly": TPItemData("Bug", IC.progression, 99, 1, 0xC3),
    "Male Stag Beetle": TPItemData("Bug", IC.progression, 100, 1, 0xC4),
    "Female Stag Beetle": TPItemData("Bug", IC.progression, 101, 1, 0xC5),
    "Male Grasshopper": TPItemData("Bug", IC.progression, 102, 1, 0xC6),
    "Female Grasshopper": TPItemData("Bug", IC.progression, 103, 1, 0xC7),
    "Male Phasmid": TPItemData("Bug", IC.progression, 104, 1, 0xC8),
    "Female Phasmid": TPItemData("Bug", IC.progression, 105, 1, 0xC9),
    "Male Pill Bug": TPItemData("Bug", IC.progression, 106, 1, 0xCA),
    "Female Pill Bug": TPItemData("Bug", IC.progression, 107, 1, 0xCB),
    "Male Mantis": TPItemData("Bug", IC.progression, 108, 1, 0xCC),
    "Female Mantis": TPItemData("Bug", IC.progression, 109, 1, 0xCD),
    "Male Ladybug": TPItemData("Bug", IC.progression, 110, 1, 0xCE),
    "Female Ladybug": TPItemData("Bug", IC.progression, 111, 1, 0xCF),
    "Male Snail": TPItemData("Bug", IC.progression, 112, 1, 0xD0),
    "Female Snail": TPItemData("Bug", IC.progression, 113, 1, 0xD1),
    "Male Dragonfly": TPItemData("Bug", IC.progression, 114, 1, 0xD2),
    "Female Dragonfly": TPItemData("Bug", IC.progression, 115, 1, 0xD3),
    "Male Ant": TPItemData("Bug", IC.progression, 116, 1, 0xD4),
    "Female Ant": TPItemData("Bug", IC.progression, 117, 1, 0xD5),
    "Male Dayfly": TPItemData("Bug", IC.progression, 118, 1, 0xD6),
    "Female Dayfly": TPItemData("Bug", IC.progression, 119, 1, 0xD7),
    "Progressive Mirror Shard": TPItemData("Item", IC.progression, 120, 4, 0xA5),
    "Progressive Fused Shadow": TPItemData("Item", IC.progression, 121, 3, 0xD8),
    "Progressive Hidden Skill": TPItemData("Item", VERY_USEFUL, 122, 7, 0xE1),
    "Progressive Sky Book": TPItemData("Item", IC.progression, 123, 7, 0xE9),
    # "Sky Character 1": TPItemData("Item", IC.useful, 132, 1, 0xDB),
    # "Sky Character 2": TPItemData("Item", IC.useful, 133, 1, 0xDC),
    # "Sky Character 3": TPItemData("Item", IC.useful, 134, 1, 0xDD),
    # "Sky Character 4": TPItemData("Item", IC.useful, 135, 1, 0xDE),
    # "Sky Character 5": TPItemData("Item", IC.useful, 136, 1, 0xDF),
    "Poe Soul": TPItemData("Poe", IC.progression_skip_balancing, 124, 60, 0xE0),
    # "Poe 1 (Fire)": TPItemData("Item", IC.useful, 125, 1, 0xEF),
    # "Poe 2 (Fire)": TPItemData("Item", IC.useful, 126, 1, 0xF0),
    # "Poe 3 (Fire)": TPItemData("Item", IC.useful, 127, 1, 0xF1),
    # "Poe 4 (Fire)": TPItemData("Item", IC.useful, 128, 1, 0xF2),
    "Ordon Pumpkin": TPItemData("Small Key", IC.progression, 129, 1, 0xF4),
    "Ordon Goat Cheese": TPItemData("Small Key", IC.progression, 130, 1, 0xF5),
    "Ice Trap": TPItemData("Trap", IC.trap, 131, 1, 0x13),
    "Victory": TPItemData("Event", IC.progression, None, 1, None),
    "Giant Bomb Bag": TPItemData("Item", IC.useful, 133, 1, 0x4F),
}

LOOKUP_ID_TO_NAME: dict[int, str] = {
    TPItem.get_apid(data.code): item
    for item, data in ITEM_TABLE.items()
    if data.code is not None
}

item_name_groups = {
    "Bottles": {
        "Empty Bottle (Fishing Hole)",
        "Milk (half) (Sera Bottle)",
        "Lantern Oil (Coro Bottle)",
        "Great Fairy Tears (Jovani)",
    },
    # "Quest Items": {
    #     "Renado's Letter",
    #     "Invoice",
    #     "Wooden Statue",
    #     "Ilias Charm",
    # },
    "Rupees": {
        "Green Rupee",
        "Blue Rupee",
        "Yellow Rupee",
        "Red Rupee",
        "Purple Rupee",
        "Orange Rupee",
        "Silver Rupee",
    },
    "Bombs": {
        "Bombs (5)",
        "Bombs (10)",
        "Bombs (20)",
        "Bombs (30)",
        "Water Bombs (3)",
        "Water Bombs (5)",
        "Water Bombs (10)",
        "Water Bombs (15)",
        "Bomblings (3)",
        "Bomblings (5)",
        "Bomblings (10)",
    },
    "Arrows": {
        "Arrows (10)",
        "Arrows (20)",
        "Arrows (30)",
    },
    "Shields": {
        "Ordon Shield",
        "Hylian Shield",
    },
    "Tunics": {
        "Zora Armor",
        "Magic Armor",
    },
    "Small Keys": {
        "Forest Temple Small Key",
        "Goron Mines Small Key",
        "Lakebed Temple Small Key",
        "Arbiters Grounds Small Key",
        "Snowpeak Ruins Small Key",
        "Temple of Time Small Key",
        "City in The Sky Small Key",
        "Palace of Twilight Small Key",
        "Hyrule Castle Small Key",
        "Ordon Pumpkin",
        "Ordon Goat Cheese",
    },
    "Big Keys": {
        "Forest Temple Big Key",
        "Goron Mines Key Shard",
        "Lakebed Temple Big Key",
        "Arbiters Grounds Big Key",
        "Bedroom Key",
        "Temple of Time Big Key",
        "City in The Sky Big Key",
        "Palace of Twilight Big Key",
        "Hyrule Castle Big Key",
    },
    "Maps and Compasses": {
        "Forest Temple Map",
        "Goron Mines Map",
        "Lakebed Temple Map",
        "Arbiters Grounds Map",
        "Snowpeak Ruins Map",
        "Temple of Time Map",
        "City in The Sky Map",
        "Palace of Twilight Map",
        "Hyrule Castle Map",
        "Forest Temple Compass",
        "Goron Mines Compass",
        "Lakebed Temple Compass",
        "Arbiters Grounds Compass",
        "Snowpeak Ruins Compass",
        "Temple of Time Compass",
        "City in The Sky Compass",
        "Palace of Twilight Compass",
        "Hyrule Castle Compass",
    },
    "Bugs": {
        "Male Beetle",
        "Female Beetle",
        "Male Butterfly",
        "Female Butterfly",
        "Male Stag Beetle",
        "Female Stag Beetle",
        "Male Grasshopper",
        "Female Grasshopper",
        "Male Phasmid",
        "Female Phasmid",
        "Male Pill Bug",
        "Female Pill Bug",
        "Male Mantis",
        "Female Mantis",
        "Male Ladybug",
        "Female Ladybug",
        "Male Snail",
        "Female Snail",
        "Male Dragonfly",
        "Female Dragonfly",
        "Male Ant",
        "Female Ant",
        "Male Dayfly",
        "Female Dayfly",
    },
    "Heart": {
        "Piece of Heart",
        "Heart Container",
    },
    # "NPC Items": {},
    # "Shop Items": {},
    # "Overworld Items": {},
}
# generic groups, (Name, substring)
_simple_groups = {
    ("Swords", "Progressive Master Sword"),
    ("Wallet", "Progressive Wallet"),
    ("Bow", "Progressive Hero's Bow"),
    ("Dominion Rod", "Progressive Dominion Rod"),
    ("Clawshots", "Progressive Clawshot"),
    ("Fishing Rod", "Progressive Fishing Rod"),
    ("Mirror Shard", "Progressive Mirror Shard"),
    ("Fused Shadows", "Progressive Fused Shadow"),
    ("Hidden Skill", "Progressive Hidden Skill"),
    ("Sky Book", "Progressive Sky Book"),
}
for basename, substring in _simple_groups:
    if basename not in item_name_groups:
        item_name_groups[basename] = set()
    for itemList in ITEM_TABLE:
        if substring in itemList:
            item_name_groups[basename].add(itemList)

del _simple_groups

ItemWheelItems = [
    "Progressive Clawshot",
    "Progressive Dominion Rod",
    "Ball and Chain",
    "Spinner",
    "Progressive Hero's Bow",
    "Iron Boots",
    "Gale Boomerang",
    "Lantern",
    "Slingshot",
    "Progressive Fishing Rod",
    "Hawkeye",
    "Bomb Bag",
    "Bomb Bag",
    "Bomb Bag",
    "Empty Bottle (Fishing Hole)",
    "Milk (half) (Sera Bottle)",
    "Lantern Oil (Coro Bottle)",
    "Great Fairy Tears (Jovani)",
    "Auru's Memo",
    "Renado's Letter",  # Covers letter, invoice, statue, charm. It doesn't matter which item you
    # have in the chain, as long as you have the slot available.
    "Horse Call",
]

BossItems = [
    "Diababa Defeated",
    "Fyrus Defeated",
    "Morpheel Defeated",
    "Stallord Defeated",
    "Blizzeta Defeated",
    "Armogohma Defeated",
    "Argorok Defeated",
    "Zant Defeated",
    "Ganondorf Defeated",
]

PortalItems = [
    "Ordon Portal",
    "South Faron Portal",
    "North Faron Portal",
    "Kakariko Gorge Portal",
    "Kakariko Village Portal",
    "Death Mountain Portal",
    "Castle Town Portal",
    "Zoras Domain Portal",
    "Lake Hylia Portal",
    "Gerudo Desert Portal",
    "Mirror Chamber Portal",
    "Snowpeak Portal",
    "Sacred Grove Portal",
    "Bridge of Eldin Portal",
    "Upper Zoras River Portal",
]

GoldenBugs = [
    "Male Beetle",
    "Female Beetle",
    "Male Butterfly",
    "Female Butterfly",
    "Male Stag Beetle",
    "Female Stag Beetle",
    "Male Grasshopper",
    "Female Grasshopper",
    "Male Phasmid",
    "Female Phasmid",
    "Male Pill Bug",
    "Female Pill Bug",
    "Male Mantis",
    "Female Mantis",
    "Male Ladybug",
    "Female Ladybug",
    "Male Snail",
    "Female Snail",
    "Male Dragonfly",
    "Female Dragonfly",
    "Male Ant",
    "Female Ant",
    "Male Dayfly",
    "Female Dayfly",
]
