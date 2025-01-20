import typing

from BaseClasses import Item, ItemClassification, MultiWorld
from worlds.ty_the_tasmanian_tiger import Ty1Options


class Ty1Item(Item):
    game: str = "Ty the Tasmanian Tiger"

    def __init__(self, name, classification: ItemClassification, code: int = None, player: int = None):
        super(Ty1Item, self).__init__(name, classification, code, player)


def create_items(world: MultiWorld, options: Ty1Options, player: int):
    #GENERATE ITEMS



ty1_item_table = {
    # IDs
    # Generic - 0
    # Attribute - 1
    # Bilby - 2
    # Level - 3
    # Progressive - 7
    # Junk - 8

    # Generic
    "Fire Thunder Egg": (0x8750000, ItemClassification.progression_skip_balancing),
    "Ice Thunder Egg": (0x8750001, ItemClassification.progression_skip_balancing),
    "Air Thunder Egg": (0x8750002, ItemClassification.progression_skip_balancing),
    "Golden Cog":  (0x8750003, ItemClassification.skip_balancing),
    "Stopwatch": (0x875004, ItemClassification.useful),

    # Attributes
    "Progressive Elemental Rang": (0x8750070, ItemClassification.progression_skip_balancing),
    "Swim": (0x8750010, ItemClassification.progression),
    "Dive": (0x8750011, ItemClassification.progression),
    "Second Rang": (0x8750012, ItemClassification.progression),
    "Extra Health": (0x8750013, ItemClassification.filler),
    "Boomerang": (0x8750014, ItemClassification.progression),
    "Flamerang": (0x8750015, ItemClassification.progression),
    "Frostyrang": (0x8750016, ItemClassification.progression),
    "Zappyrang": (0x8750017, ItemClassification.progression),
    "Aquarang": (0x8750018, ItemClassification.progression),
    "Zoomerang": (0x8750019, ItemClassification.useful),
    "Multirang": (0x875001A, ItemClassification.filler),
    "Infrarang": (0x875001B, ItemClassification.useful),
    "Megarang": (0x875001C, ItemClassification.filler),
    "Kaboomarang": (0x875001D, ItemClassification.filler),
    "Chronorang": (0x875001E, ItemClassification.trap),
    "Doomarang": (0x875001F, ItemClassification.progression),

    # Bilby
    "Bilby - Two Up": (0x8750020, ItemClassification.useful),
    "Bilby - Walk in the Park": (0x8750021, ItemClassification.useful),
    "Bilby - Ship Rex": (0x8750022, ItemClassification.useful),
    "Bilby - Bridge on the River Ty": (0x8750023, ItemClassification.useful),
    "Bilby - Snow Worries": (0x8750024, ItemClassification.useful),
    "Bilby - Outback Safari": (0x8750025, ItemClassification.useful),
    "Bilby - Lyre, Lyre Pants on Fire": (0x8750026, ItemClassification.useful),
    "Bilby - Beyond the Black Stump": (0x8750027, ItemClassification.useful),
    "Bilby - Rex Marks the Spot": (0x8750028, ItemClassification.useful),

    # Levels
    "Progressive Levels": (0x8750071, ItemClassification.progression_skip_balancing),
    "Portal - Two Up": (0x8750030, ItemClassification.progression_skip_balancing),
    "Portal - Walk in the Park": (0x8750031, ItemClassification.progression_skip_balancing),
    "Portal - Ship Rex": (0x8750032, ItemClassification.progression_skip_balancing),
    "Portal - Bull's Pen": (0x8750033, ItemClassification.progression_skip_balancing),
    "Portal - Bridge on the River Ty": (0x8750034, ItemClassification.progression_skip_balancing),
    "Portal - Snow Worries": (0x8750035, ItemClassification.progression_skip_balancing),
    "Portal - Outback Safari": (0x8750036, ItemClassification.progression_skip_balancing),
    "Portal - Crikey's Cove": (0x8750037, ItemClassification.progression_skip_balancing),
    "Portal - Lyre, Lyre Pants on Fire": (0x8750038, ItemClassification.progression_skip_balancing),
    "Portal - Beyond the Black Stump": (0x8750039, ItemClassification.progression_skip_balancing),
    "Portal - Rex Marks the Spot": (0x875003A, ItemClassification.progression_skip_balancing),
    "Portal - Fluffy's Fjord": (0x875003B, ItemClassification.progression_skip_balancing),
    "Portal - Cass' Pass": (0x875003C, ItemClassification.progression_skip_balancing),

    # Junk
    "Picture Frame":  (0x8750080, ItemClassification.filler),
    "Talisman": (0x8750081, ItemClassification.filler),
    "Extra Life": (0x8750082, ItemClassification.filler),
    "Opal Magnet": (0x8750083, ItemClassification.filler),

}
