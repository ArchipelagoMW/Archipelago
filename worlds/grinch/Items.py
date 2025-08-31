from typing import NamedTuple, Optional

from .RamHandler import GrinchRamData
from BaseClasses import Item
from BaseClasses import ItemClassification as IC #IC can be any name, saves having to type the whole word in code

class GrinchItemData(NamedTuple):
    item_group: str #arbituary that can be whatever it can be, basically the field/property for item groups
    id: Optional[int]
    classification: IC
    update_ram_addr: list[GrinchRamData]
    second_item_group: Optional[str] = None

class GrinchItem(Item):
    game: str = "The Grinch"

    #Tells server what item id it is
    @staticmethod
    def get_apid(id: int):
        #If you give me an input id, I will return the Grinch equivalent server/ap id
        base_id: int = 42069
        return base_id + id if id is not None else None

    def __init__(self, name: str, player: int, data: GrinchItemData):
        super(GrinchItem, self).__init__(name,data.classification, GrinchItem.get_apid(data.id), player)

        self.type = data.item_group
        self.item_id = data.id

#allows hinting of items via category
def get_item_names_per_category() -> dict[str, set[str]]:
    categories: dict[str, set[str]] = {}

    for name, data in ALL_ITEMS_TABLE.items():
        categories.setdefault(data.item_group, set()).add(name)

    return categories

#Gadgets
#All gadgets require at least 4 different blueprints to be unlocked in the computer in Mount Crumpit.
GADGETS_TABLE: dict[str, GrinchItemData] = {
    "Binoculars": GrinchItemData("Gadgets", 100, IC.useful,
        [GrinchRamData(0x0102B6, value=0x40), GrinchRamData(0x0102B7, value=0x41),
        GrinchRamData(0x0102B8, value=0x44), GrinchRamData(0x0102B9, value=0x45),
        # GrinchRamData(0x0100BC, binary_bit_pos=0)
         ]),
    "Rotten Egg Launcher": GrinchItemData("Gadgets", 101, IC.progression,
        [GrinchRamData(0x0102BA, value=0x40), GrinchRamData(0x0102BB, value=0x41),
        GrinchRamData(0x0102BC, value=0x44), GrinchRamData(0x0102BD, value=0x45),
        # GrinchRamData(0x0100BC, binary_bit_pos=1)
         ]),
    "Rocket Spring": GrinchItemData("Gadgets", 102, IC.progression,
        [GrinchRamData(0x0102BE, value=0x40), GrinchRamData(0x0102BF, value=0x41),
        GrinchRamData(0x0102C0, value=0x42), GrinchRamData(0x0102C1, value=0x44),
        GrinchRamData(0x0102C2, value=0x45), GrinchRamData(0x0102C3, value=0x46),
        GrinchRamData(0x0102C4, value=0x48), GrinchRamData(0x0102C5, value=0x49),
        GrinchRamData(0x0102C6, value=0x4A),
         # GrinchRamData(0x0100BC, binary_bit_pos=2)
         ]),
    "Slime Shooter": GrinchItemData("Gadgets", 103, IC.progression,
        [GrinchRamData(0x0102C7, value=0x40), GrinchRamData(0x0102C8, value=0x41),
        GrinchRamData(0x0102C9, value=0x42), GrinchRamData(0x0102CA, value=0x44),
        GrinchRamData(0x0102CB, value=0x45), GrinchRamData(0x0102CC, value=0x46),
        GrinchRamData(0x0102CD, value=0x48), GrinchRamData(0x0102CE, value=0x49),
        GrinchRamData(0x0102CF, value=0x4A),
         # GrinchRamData(0x0100BC, binary_bit_pos=3)
         ]),
    "Octopus Climbing Device": GrinchItemData("Gadgets", 104, IC.progression,
        [GrinchRamData(0x0102D0, value=0x40), GrinchRamData(0x0102D1, value=0x41),
        GrinchRamData(0x0102D2, value=0x42), GrinchRamData(0x0102D3, value=0x44),
        GrinchRamData(0x0102D4, value=0x45), GrinchRamData(0x0102D5, value=0x46),
        GrinchRamData(0x0102D6, value=0x48), GrinchRamData(0x0102D7, value=0x49),
        GrinchRamData(0x0102D8, value=0x4A),
         # GrinchRamData(0x0100BC, binary_bit_pos=4)
         ]),
    "Marine Mobile": GrinchItemData("Gadgets", 105, IC.progression,
        [GrinchRamData(0x0102D9, value=0x40), GrinchRamData(0x0102DA, value=0x41),
        GrinchRamData(0x0102DB, value=0x42), GrinchRamData(0x0102DC, value=0x43),
        GrinchRamData(0x0102DD, value=0x44), GrinchRamData(0x0102DE, value=0x45),
        GrinchRamData(0x0102DF, value=0x46), GrinchRamData(0x0102E0, value=0x47),
        GrinchRamData(0x0102E1, value=0x48), GrinchRamData(0x0102E2, value=0x49),
        GrinchRamData(0x0102E3, value=0x4A), GrinchRamData(0x0102E4, value=0x4B),
        GrinchRamData(0x0102E5, value=0x4C), GrinchRamData(0x0102E6, value=0x4D),
        GrinchRamData(0x0102E7, value=0x4E), GrinchRamData(0x0102E8, value=0x4F),
        # GrinchRamData(0x0100BC, binary_bit_pos=5)
         ]),
    "Grinch Copter": GrinchItemData("Gadgets", 106, IC.progression,
        [GrinchRamData(0x0102E9, value=0x40), GrinchRamData(0x0102EA, value=0x41),
        GrinchRamData(0x0102EB, value=0x42), GrinchRamData(0x0102EC, value=0x43),
        GrinchRamData(0x0102ED, value=0x44), GrinchRamData(0x0102EE, value=0x45),
        GrinchRamData(0x0102EF, value=0x46), GrinchRamData(0x0102F0, value=0x47),
        GrinchRamData(0x0102F1, value=0x48), GrinchRamData(0x0102F2, value=0x49),
        GrinchRamData(0x0102F3, value=0x4A), GrinchRamData(0x0102F4, value=0x4B),
        GrinchRamData(0x0102F5, value=0x4C), GrinchRamData(0x0102F6, value=0x4D),
        GrinchRamData(0x0102F7, value=0x4E), GrinchRamData(0x0102F8, value=0x4F),
        # GrinchRamData(0x0100BC, binary_bit_pos=6)
    ])
}

#Mission Specific Items
MISSION_ITEMS_TABLE: dict[str, GrinchItemData] = {
    "Who Cloak": GrinchItemData("Mission Specific Items", 200, IC.progression,
        [GrinchRamData(0x0101F9, binary_bit_pos=0)], second_item_group="Useful Items"),
    "Painting Bucket": GrinchItemData("Mission Specific Items", 201, IC.progression_deprioritized,
        [GrinchRamData(0x0101F9, binary_bit_pos=1)], second_item_group="Useful Items"),
    "Scissors": GrinchItemData("Mission Specific Items", 202, IC.progression_deprioritized,
        [GrinchRamData(0x0101F9, binary_bit_pos=6), GrinchRamData(0x0100C2, binary_bit_pos=1)],
        second_item_group="Useful Items"),
    "Glue Bucket": GrinchItemData("Mission Specific Items", 203, IC.progression_deprioritized,
        [GrinchRamData(0x0101F9, binary_bit_pos=4)], second_item_group="Useful Items"),
    "Cable Car Access Card": GrinchItemData("Mission Specific Items", 204, IC.progression,
        [GrinchRamData(0x0101F9, binary_bit_pos=5)], second_item_group="Useful Items"),
    "Drill": GrinchItemData("Mission Specific Items", 205, IC.progression_deprioritized,
        [GrinchRamData(0x0101FA, binary_bit_pos=2)], second_item_group="Useful Items"),
    "Rope": GrinchItemData("Mission Specific Items", 206, IC.progression_deprioritized,
        [GrinchRamData(0x0101FA, binary_bit_pos=1)], second_item_group="Useful Items"),
    "Hook": GrinchItemData("Mission Specific Items", 207, IC.progression_deprioritized,
        [GrinchRamData(0x0101FA, binary_bit_pos=0)], second_item_group="Useful Items"),
    "Sculpting Tools": GrinchItemData("Mission Specific Items", 208, IC.progression_deprioritized,
        [GrinchRamData(0x0101F9, binary_bit_pos=2)], second_item_group="Useful Items"),
    "Hammer": GrinchItemData("Mission Specific Items", 209, IC.progression_deprioritized,
        [GrinchRamData(0x0101F9, binary_bit_pos=3)], second_item_group="Useful Items"),
    "Scout Clothes": GrinchItemData("Mission Specific Items", 210, IC.progression,
        [GrinchRamData(0x0101F9, binary_bit_pos=7)], second_item_group="Useful Items")
}

#Sleigh Parts
# SLEIGH_PARTS_TABLE: dict[str, GrinchItemData] = {
#     "Exhaust Pipes": GrinchItemData("Sleigh Parts", 300, IC.progression_skip_balancing,
#         [GrinchRamData(0x0101FB, binary_bit_pos=2)]),
#     "GPS": GrinchItemData("Sleigh Parts", 301, IC.useful,
#         [GrinchRamData(0x0101FB, binary_bit_pos=5)]),
#     "Tires": GrinchItemData("Sleigh Parts", 302, IC.progression_skip_balancing,
#         [GrinchRamData(0x0101FB, binary_bit_pos=4)]),
#     "Skis": GrinchItemData("Sleigh Parts", 303, IC.progression_skip_balancing,
#         [GrinchRamData(0x0101FB, binary_bit_pos=3)]),
#     "Twin-End Tuba": GrinchItemData("Sleigh Parts", 304, IC.progression_skip_balancing,
#         [GrinchRamData(0x0101FB, binary_bit_pos=6)])
# }

#Access Keys
KEYS_TABLE: dict[str, GrinchItemData] = {
    # "Whoville Vacuum Access": GrinchItemData("Vacuum Access", 400, IC.progression,
    #     [GrinchRamData()]),
    "Who Forest Vacuum Access": GrinchItemData("Vacuum Access", 401, IC.progression,
        [GrinchRamData(0x0100AA, binary_bit_pos=2)]),
    "Who Dump Vacuum Access": GrinchItemData("Vacuum Access", 402, IC.progression,
        [GrinchRamData(0x0100AA, binary_bit_pos=3)]),
    "Who Lake Vacuum Access": GrinchItemData("Vacuum Access", 403, IC.progression,
        [GrinchRamData(0x0100AA, binary_bit_pos=4)]),
    # "Progressive Vacuum Access": GrinchItemData("Vacuum Access", 404, IC.progression,
    #     [GrinchRamData()]),
    # "Spin N' Win Door Unlock": GrinchItemData("Supadow Door Unlocks", 405, IC.progression,
    #     [GrinchRamData()]),
    # "Dankamania Door Unlock": GrinchItemData("Supadow Door Unlocks", 406, IC.progression,
    #     [GrinchRamData()]),
    # "The Copter Race Contest Door Unlock": GrinchItemData("Supadow Door Unlocks", 407, IC.progression,
    #     [GrinchRamData()]),
    # "Progressive Supadow Door Unlock": GrinchItemData("Supadow Door Unlocks", 408, IC.progression,
    #     [GrinchRamData()]),
    # "Bike Race Access": GrinchItemData("Supadow Door Unlocks", 409, IC.progression,
    #     [GrinchRamData()])
    "Sleigh Room Key": GrinchItemData("Sleigh Room", 410, IC.progression,
        [GrinchRamData(0x010200, binary_bit_pos=6), GrinchRamData(0x0100AA, binary_bit_pos=5)])
}

#Misc Items
MISC_ITEMS_TABLE: dict[str, GrinchItemData] = {
    # This item may not function properly if you receive it during a loading screen or in Mount Crumpit
    # "Fully Healed Grinch": GrinchItemData("Health Items", 500, IC.filler,
    #     [GrinchRamData(0x0E8FDC, value=120)]),
    "5 Rotten Eggs": GrinchItemData("Rotten Egg Bundles", 502, IC.filler,
        [GrinchRamData(0x010058, value=5, update_existing_value=True, max_count=200, bit_size=2)]),
    "10 Rotten Eggs": GrinchItemData("Rotten Egg Bundles", 503, IC.filler,
        [GrinchRamData(0x010058, value=10, update_existing_value=True, max_count=200, bit_size=2)]),
    "20 Rotten Eggs": GrinchItemData("Rotten Egg Bundles", 504, IC.filler,
        [GrinchRamData(0x010058, value=20, update_existing_value=True, max_count=200, bit_size=2)])
}

USEFUL_IC_TABLE: dict[str, GrinchItemData] = {
    "Heart of Stone": GrinchItemData("Health Items", 501, IC.useful,
        [GrinchRamData(0x0100ED, value=1, update_existing_value=True, max_count=4)])
}

#Traps
TRAPS_TABLE: dict[str, GrinchItemData] = {
# alias to Ice Trap for traplink
    # "Freeze Trap": GrinchItemData("Traps", 600, IC.trap, [GrinchRamData()]),
    # "Bee Trap": GrinchItemData("Traps", 601, IC.trap, [GrinchRamData()]),
    # "Electrocution Trap": GrinchItemData("Traps", 602, IC.trap, [GrinchRamData()]),
# alias to Slowness Trap for traplink
    # "Tip Toe Trap": GrinchItemData("Traps", 603, IC.trap, [GrinchRamData()]),
# This item may not function properly if you receive it during a loading screen or in Mount Crumpit
#     "Damage Trap": GrinchItemData("Traps", 604, IC.trap, [GrinchRamData(0x0E8FDC, value=-20, update_existing_value=True)]),
    "Depletion Trap": GrinchItemData("Traps", 605, IC.trap, [GrinchRamData(0x010058, value=0, bit_size=2)]),
    "Dump it to Crumpit": GrinchItemData("Traps", 606, IC.trap, #Alias to Home Trap for traplink
        [GrinchRamData(0x010000, value=0x05), GrinchRamData(0x08FB94, value=1)]),
#alias to Spring Trap for traplink
    # "Rocket Spring Trap": GrinchItemData("Traps", 607, IC.trap, [GrinchRamData()]),
#alias to Home Trap for traplink
    "Who sent me back?": GrinchItemData("Traps", 608, IC.trap, [GrinchRamData(0x08FB94, value=1)]),
    # "Cutscene Trap": GrinchItemData("Traps", 609, IC.trap, [GrinchRamData()]),
    # "No Vac Trap": GrinchItemData("Traps", 610, IC.trap, [GrinchRamData(0x0102DA, value=0]),
    # "Invisible Trap": GrinchItemData("Traps", 611, IC.trap, [GrinchRamData(0x0102DA, value=0, bit_size=4)])
    # "Child Trap": GrinchItemData("Traps", 612, IC.trap,[GrinchRamData()])
}

#Movesets
# MOVES_TABLE: dict[str, GrinchItemData] = {
#     "Bad Breath": GrinchItemData("Movesets", 700, IC.progression, [GrinchRamData(0x0100BB, binary_bit_pos=1)]),
#     "Pancake": GrinchItemData("Movesets", 701, IC.progression, [GrinchRamData(0x0100BB, binary_bit_pos=2)]),
#     "Push & Pull": GrinchItemData("Movesets", 702, IC.progression, [GrinchRamData(0x0100BB, binary_bit_pos=3)]),
#     "Max": GrinchItemData("Movesets", 703, IC.progression, [GrinchRamData(0x0100BB, binary_bit_pos=4)]),
#     "Tip Toe": GrinchItemData("Movesets", 704, IC.progression, [GrinchRamData(0x0100BB, binary_bit_pos=5)])
# }
#Double star combines all dictionaries from each individual list together
ALL_ITEMS_TABLE: dict[str, GrinchItemData] = {
    **GADGETS_TABLE,
    **MISSION_ITEMS_TABLE,
    **KEYS_TABLE,
    **MISC_ITEMS_TABLE,
    **TRAPS_TABLE,
    **USEFUL_IC_TABLE,
    # **SLEIGH_PARTS_TABLE,
    # **MOVES_TABLE,
}

# Psuedocoding traplink table
# BEE_TRAP_EQUIV = ["Army Trap", "Buyon Trap", "Ghost", "Gooey Bag", "OmoTrap", "Police Trap"]
# ICE_TRAP_EQUIV = ["Chaos Control Trap", "Freeze Trap", "Frozen Trap", "Honey Trap", "Paralyze Trap", "Stun Trap", "Bubble Trap"]
# DAMAGE_TRAP_EQUIV = ["Banana Trap", "Bomb", "Bonk Trap", "Fire Trap", "Laughter Trap", "Nut Trap", "Push Trap", "Squash Trap", "Thwimp Trap", "TNT Barrel Trap", "Meteor Trap"]
# SPRING_TRAP_EQUIV = ["Eject Ability", "Hiccup Trap", "Jump Trap", "Jumping Jacks Trap", "Whoops! Trap"]
# HOME_TRAP_EQUIV = ["Blue Balls Curse", "Instant Death Trap"]
# SLOWNESS_TRAP_EQUIV = ["Iron Boots Trap", "Slow Trap", "Sticky Floor Trap"]
# CUTSCENE_TRAP_EQUIV = ["Phone Trap"]
# ELEC_TRAP_EQUIV = []

def grinch_items_to_id() -> dict[str, int]:
    item_mappings: dict[str, int] = {}
    for ItemName, ItemData in ALL_ITEMS_TABLE.items():
        item_mappings.update({ItemName: GrinchItem.get_apid(ItemData.id)})
    return item_mappings