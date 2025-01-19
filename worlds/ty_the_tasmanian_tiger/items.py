import typing

from BaseClasses import Item, ItemClassification
from worlds.alttp import ALTTPWorld


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: ItemClassification
    trap: bool = False
    quantity: int = 1
    event: bool = False


class Ty1Item(Item):
    game: str = "Ty the Tasmanian Tiger"

    def __init__(self, name, classification: ItemClassification, code: int = None, player: int = None):
        super(Ty1Item, self).__init__(name, classification, code, player)

ty1_item_table = {
    # IDs
    # Generic - 0
    # Attribute - 1
    # Bilby - 2
    # Level - 3
    # Progressive - 7
    # Junk - 8

    # Generic
    "Fire Thunder Egg": ItemData(0x8750000, ItemClassification.progression_skip_balancing),
    "Ice Thunder Egg": ItemData(0x8750001, ItemClassification.progression_skip_balancing),
    "Air Thunder Egg": ItemData(0x8750002, ItemClassification.progression_skip_balancing),
    "Golden Cog":  ItemData(0x8750003, ItemClassification.skip_balancing),
    "Stopwatch": ItemData(0x875004, ItemClassification.useful),

    # Attributes
    "Progressive Elemental Rang": ItemData(0x8750070, ItemClassification.progression_skip_balancing),
    "Swim": ItemData(0x8750010, ItemClassification.progression),
    "Dive": ItemData(0x8750011, ItemClassification.progression),
    "Second Rang": ItemData(0x8750012, ItemClassification.progression),
    "Extra Health": ItemData(0x8750013, ItemClassification.filler),
    "Boomerang": ItemData(0x8750014, ItemClassification.progression),
    "Flamerang": ItemData(0x8750015, ItemClassification.progression),
    "Frostyrang": ItemData(0x8750016, ItemClassification.progression),
    "Zappyrang": ItemData(0x8750017, ItemClassification.progression),
    "Aquarang": ItemData(0x8750018, ItemClassification.progression),
    "Zoomerang": ItemData(0x8750019, ItemClassification.useful),
    "Multirang": ItemData(0x875001A, ItemClassification.filler),
    "Infrarang": ItemData(0x875001B, ItemClassification.useful),
    "Megarang": ItemData(0x875001C, ItemClassification.filler),
    "Kaboomarang": ItemData(0x875001D, ItemClassification.filler),
    "Chronorang": ItemData(0x875001E, ItemClassification.trap),
    "Doomarang": ItemData(0x875001F, ItemClassification.progression),

    # Bilby
    "Bilby - Two Up": ItemData(0x8750020, ItemClassification.useful),
    "Bilby - Walk in the Park": ItemData(0x8750021, ItemClassification.useful),
    "Bilby - Ship Rex": ItemData(0x8750022, ItemClassification.useful),
    "Bilby - Bridge on the River Ty": ItemData(0x8750023, ItemClassification.useful),
    "Bilby - Snow Worries": ItemData(0x8750024, ItemClassification.useful),
    "Bilby - Outback Safari": ItemData(0x8750025, ItemClassification.useful),
    "Bilby - Lyre, Lyre Pants on Fire": ItemData(0x8750026, ItemClassification.useful),
    "Bilby - Beyond the Black Stump": ItemData(0x8750027, ItemClassification.useful),
    "Bilby - Rex Marks the Spot": ItemData(0x8750028, ItemClassification.useful),

    # Levels
    "Progressive Levels": ItemData(0x8750071, ItemClassification.progression_skip_balancing),
    "Portal - Two Up": ItemData(0x8750030, ItemClassification.progression_skip_balancing),
    "Portal - Walk in the Park": ItemData(0x8750031, ItemClassification.progression_skip_balancing),
    "Portal - Ship Rex": ItemData(0x8750032, ItemClassification.progression_skip_balancing),
    "Portal - Bull's Pen": ItemData(0x8750033, ItemClassification.progression_skip_balancing),
    "Portal - Bridge on the River Ty": ItemData(0x8750034, ItemClassification.progression_skip_balancing),
    "Portal - Snow Worries": ItemData(0x8750035, ItemClassification.progression_skip_balancing),
    "Portal - Outback Safari": ItemData(0x8750036, ItemClassification.progression_skip_balancing),
    "Portal - Crikey's Cove": ItemData(0x8750037, ItemClassification.progression_skip_balancing),
    "Portal - Lyre, Lyre Pants on Fire": ItemData(0x8750038, ItemClassification.progression_skip_balancing),
    "Portal - Beyond the Black Stump": ItemData(0x8750039, ItemClassification.progression_skip_balancing),
    "Portal - Rex Marks the Spot": ItemData(0x875003A, ItemClassification.progression_skip_balancing),
    "Portal - Fluffy's Fjord": ItemData(0x875003B, ItemClassification.progression_skip_balancing),
    "Portal - Cass' Pass": ItemData(0x875003C, ItemClassification.progression_skip_balancing),

    # Junk
    "Picture Frame":  ItemData(0x8750080, ItemClassification.filler),
    "Talisman": ItemData(0x8750081, ItemClassification.filler),
    "Extra Life": ItemData(0x8750082, ItemClassification.filler),
    "Opal Magnet": ItemData(0x8750083, ItemClassification.filler),

}
