import typing

from BaseClasses import Item, ItemClassification
from .Names import ItemName
from worlds.alttp import ALTTPWorld


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool
    trap: bool = False
    quantity: int = 1
    event: bool = False


class Ty1Item(Item):
    game: str = "Ty the Tasmanian Tiger"

    def __init__(self, name, classification: ItemClassification, code: int = None, player: int = None):
        super(Ty1Item, self).__init__(name, classification, code, player)


filler: a regular item or trash item

useful: item that is especially useful. Cannot be placed on excluded or unreachable locations. When combined with
    another flag like "progression", it means "an especially useful progression item".

trap: negative impact on the player

skip_balancing: denotes that an item should not be moved to an earlier sphere for the purpose of balancing
    (to be combined with progression; see below)

progression_skip_balancing: the combination of progression and skip_balancing, i.e., a progression item that will
    not be moved around by progression balancing; used, e.g., for currency or tokens, to not flood early spheres


ty1_item_table = {
    # IDs
    # Generic - 0
    # Attribute - 1-2
    # Bilby - 3
    # Level - 4
    # Progressive - 7
    # Junk - 8

    # Generic
    "Fire Thunder Egg": ItemData(0x875001, ItemClassification.progression_skip_balancing),
    "Ice Thunder Egg": ItemData(0x875002, ItemClassification.progression_skip_balancing),
    "Air Thunder Egg": ItemData(0x875003, ItemClassification.progression_skip_balancing),
    "Golden Cog":  ItemData(0x875004, ItemClassification.skip_balancing),
    "Stopwatch": ItemData(0x87505, ItemClassification.useful)

    # Attributes
    "Progressive Elemental Rang": ItemData(0x875070, ItemClassification.progression_skip_balancing)
    "Swim": ItemData(0x875010, ItemClassification.progression),
    "Dive": ItemData(0x875011, ItemClassification.progression),
    "2nd Rang": ItemData(0x875012, ItemClassification.progression),
    "Extra Health": ItemData(0x875013, ItemClassification.filler),
    "Boomerang": ItemData(0x875014, ItemClassification.progression),
    "Flamerang": ItemData(0x875015, ItemClassification.progression),
    "Frostyrang": ItemData(0x875016, ItemClassification.progression),
    "Zappyrang": ItemData(0x875017, ItemClassification.progression),
    "Aquarang": ItemData(0x875018, ItemClassification.progression),
    "Zoomerang": ItemData(0x875019, ItemClassification.useful),
    "Multirang": ItemData(0x875020, ItemClassification.filler),
    "Infrarang": ItemData(0x875021, ItemClassification.useful),
    "Megarang": ItemData(0x875022, ItemClassification.filler),
    "Kaboomarang": ItemData(0x875023, ItemClassification.filler),
    "Chronorang": ItemData(0x875024, ItemClassification.trap),
    "Doomarang": ItemData(0x875025, ItemClassification.progression),

    # Bilby
    "Bilby - Two Up": ItemData(0x875030, ItemClassification.useful)
    "Bilby - Walk in the Park": ItemData(0x875031, ItemClassification.useful)
    "Bilby - Ship Rex": ItemData(0x875032, ItemClassification.useful)
    "Bilby - Bridge on the River Ty": ItemData(0x875033, ItemClassification.useful)
    "Bilby - Snow Worries": ItemData(0x875034, ItemClassification.useful)
    "Bilby - Outback Safari": ItemData(0x875035, ItemClassification.useful)
    "Bilby - Lyre, Lyre Pants on Fire": ItemData(0x875036, ItemClassification.useful)
    "Bilby - Beyond the Black Stump": ItemData(0x875037, ItemClassification.useful)
    "Bilby - Rex Marks the Spot": ItemData(0x875038, ItemClassification.useful)

    # Levels
    "Progressive Levels": ItemData(0x875071, ItemClassification.progression_skip_balancing)
    "Portal - Two Up": ItemData(0x875040, ItemClassification.progression_skip_balancing)
    "Portal - Walk in the Park": ItemData(0x875041, ItemClassification.progression_skip_balancing)
    "Portal - Ship Rex": ItemData(0x875042, ItemClassification.progression_skip_balancing)
    "Portal - Bull's Pen": ItemData(0x875043, ItemClassification.progression_skip_balancing)
    "Portal - Bridge on the River Ty": ItemData(0x875044, ItemClassification.progression_skip_balancing)
    "Portal - Snow Worries": ItemData(0x875045, ItemClassification.progression_skip_balancing)
    "Portal - Outback Safari": ItemData(0x875046, ItemClassification.progression_skip_balancing)
    "Portal - Crikey's Cove": ItemData(0x875047, ItemClassification.progression_skip_balancing)
    "Portal - Lyre, Lyre Pants on Fire": ItemData(0x875048, ItemClassification.progression_skip_balancing)
    "Portal - Beyond the Black Stump": ItemData(0x875049, ItemClassification.progression_skip_balancing)
    "Portal - Rex Marks the Spot": ItemData(0x875050, ItemClassification.progression_skip_balancing)
    "Portal - Fluffy's Fjord": ItemData(0x875051, ItemClassification.progression_skip_balancing)
    "Portal - Cass' Pass": ItemData(0x875052, ItemClassification.progression_skip_balancing)

    # Junk
    "Picture Frame"  ItemData(0x875080, False),
    "Talisman" ItemData(0x875082, False),
}
