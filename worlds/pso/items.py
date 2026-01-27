from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

from BaseClasses import Item, ItemClassification as IC

from enum import Enum, auto

from .helpers import PSORamData
from .options import Goal

from .strings.item_names import Item as ItemName

if TYPE_CHECKING:
    from .world import PSOWorld

# PSO Items show up in the world as 5 different physical items, which we differentiate here
# We may want to expand this to include more specific typing, or do sub-typing for each category
# But this is fine for now
class PSOItemType(Enum):
    """
    Specifies the type of items in terms of PSO items
    We want a way to delineate between different inventory items as well as world items
    """

    WEAPON = auto()
    ITEM = auto()
    ARMOR = auto()
    RARE = auto()
    MESETA = auto()
    AREA = auto()
    SWITCH = auto()
    EVENT = auto()


class PSOItemData(NamedTuple):
    type: PSOItemType
    classification: IC
    code: int | None
    max_grind: int | None
    ram_data: PSORamData


# Each Item instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Item class and override the "game" field.
class PSOItem(Item):
    game = "Phantasy Star Online Episode I & II Plus"


# We comment out the boss unlocks for now to keep the checks low while we figure stuff out
ITEM_TABLE: dict[str, PSOItemData] = {
    ItemName.UNLOCK_FOREST_1:     PSOItemData(PSOItemType.AREA,     IC.progression,           1, None, PSORamData()),
#    ItemName.UNLOCK_FOREST_2:     PSOItemData(PSOItemType.AREA,     IC.progression,           2, None, PSORamData()),
#    ItemName.UNLOCK_DRAGON:       PSOItemData(PSOItemType.AREA,     IC.progression,           3, None, PSORamData()),
    ItemName.UNLOCK_CAVES_1:      PSOItemData(PSOItemType.AREA,     IC.progression,           4, None, PSORamData(0x805127FB, 7)),
#    ItemName.UNLOCK_CAVES_2:      PSOItemData(PSOItemType.AREA,     IC.progression,           5, None, PSORamData()),
#    ItemName.UNLOCK_CAVES_3:      PSOItemData(PSOItemType.AREA,     IC.progression,           6, None, PSORamData()),
#    ItemName.UNLOCK_DE_ROL_LE:    PSOItemData(PSOItemType.AREA,     IC.progression,           7, None, PSORamData()),
    ItemName.UNLOCK_MINES_1:      PSOItemData(PSOItemType.AREA,     IC.progression,           8, None, PSORamData(0x805127FC, 6)),
#    ItemName.UNLOCK_MINES_2:      PSOItemData(PSOItemType.AREA,     IC.progression,           9, None, PSORamData()),
#    ItemName.UNLOCK_VOL_OPT:      PSOItemData(PSOItemType.AREA,     IC.progression,          10, None, PSORamData()),
#    ItemName.UNLOCK_RUINS_1:      PSOItemData(PSOItemType.AREA,     IC.progression,          11, None, PSORamData(0x805127FE, 7)),
#    ItemName.UNLOCK_RUINS_2:      PSOItemData(PSOItemType.AREA,     IC.progression,          12, None, PSORamData()),
#    ItemName.UNLOCK_RUINS_3:      PSOItemData(PSOItemType.AREA,     IC.progression,          13, None, PSORamData()),
#    ItemName.UNLOCK_DARK_FALZ:    PSOItemData(PSOItemType.AREA,     IC.progression,          14, None, PSORamData()),

    ItemName.FOREST_PILLAR:       PSOItemData(PSOItemType.SWITCH,   IC.progression,          15, None, PSORamData(0x805127FD, 3)),
    ItemName.CAVES_PILLAR:        PSOItemData(PSOItemType.SWITCH,   IC.progression,          16, None, PSORamData(0x805127FD, 2)),
    ItemName.MINES_PILLAR:        PSOItemData(PSOItemType.SWITCH,   IC.progression,          17, None, PSORamData(0x805127FD, 1)),

    "Lavis Blade":                PSOItemData(PSOItemType.WEAPON,   IC.filler | IC.useful,   18, None, PSORamData()),

    ItemName.SABER:               PSOItemData(PSOItemType.WEAPON,   IC.filler,               20, 35, PSORamData(byte_data=b'\x01\x00')),
    ItemName.BRAND:               PSOItemData(PSOItemType.WEAPON,   IC.filler,               21, 32, PSORamData(byte_data=b'\x01\x01')),
    ItemName.BUSTER:              PSOItemData(PSOItemType.WEAPON,   IC.filler,               22, 30, PSORamData(byte_data=b'\x01\x02')),

    ItemName.SWORD:               PSOItemData(PSOItemType.WEAPON,   IC.filler,               25, 46, PSORamData(byte_data=b'\x02\x00')),
    ItemName.GIGUSH:              PSOItemData(PSOItemType.WEAPON,   IC.filler,               26, 32, PSORamData(byte_data=b'\x02\x01')),

    ItemName.DAGGER:              PSOItemData(PSOItemType.WEAPON,   IC.filler,               30, 65, PSORamData(byte_data=b'\x03\x00')),
    ItemName.KNIFE:               PSOItemData(PSOItemType.WEAPON,   IC.filler,               31, 50, PSORamData(byte_data=b'\x03\x01')),
    ItemName.BLADE:               PSOItemData(PSOItemType.WEAPON,   IC.filler,               32, 35, PSORamData(byte_data=b'\x03\x02')),

    ItemName.PARTISAN:            PSOItemData(PSOItemType.WEAPON,   IC.filler,               35, 35, PSORamData(byte_data=b'\x04\x00')),
    ItemName.HALBERT:             PSOItemData(PSOItemType.WEAPON,   IC.filler,               36, 30, PSORamData(byte_data=b'\x04\x01')),

    ItemName.SLICER:              PSOItemData(PSOItemType.WEAPON,   IC.filler,               40, 20, PSORamData(byte_data=b'\x05\x00')),

    ItemName.HANDGUN:             PSOItemData(PSOItemType.WEAPON,   IC.filler,               45, 75, PSORamData(byte_data=b'\x06\x00')),
    ItemName.AUTOGUN:             PSOItemData(PSOItemType.WEAPON,   IC.filler,               46, 50, PSORamData(byte_data=b'\x06\x01')),
    ItemName.LOCKGUN:             PSOItemData(PSOItemType.WEAPON,   IC.filler,               47, 35, PSORamData(byte_data=b'\x06\x02')),

    ItemName.RIFLE:               PSOItemData(PSOItemType.WEAPON,   IC.filler,               50, 65, PSORamData(byte_data=b'\x07\x00')),
    ItemName.SNIPER:              PSOItemData(PSOItemType.WEAPON,   IC.filler,               51, 55, PSORamData(byte_data=b'\x07\x01')),

    ItemName.MECHGUN:             PSOItemData(PSOItemType.WEAPON,   IC.filler,               55,  9, PSORamData(byte_data=b'\x08\x00')),
    ItemName.ASSAULT:             PSOItemData(PSOItemType.WEAPON,   IC.filler,               56,  9, PSORamData(byte_data=b'\x08\x01')),

    ItemName.SHOT:                PSOItemData(PSOItemType.WEAPON,   IC.filler,               60, 20, PSORamData(byte_data=b'\x09\x00')),

    ItemName.CANE:                PSOItemData(PSOItemType.WEAPON,   IC.filler,               65, 55, PSORamData(byte_data=b'\x0A\x00')),
    ItemName.STICK:               PSOItemData(PSOItemType.WEAPON,   IC.filler,               66, 40, PSORamData(byte_data=b'\x0A\x01')),

    ItemName.ROD:                 PSOItemData(PSOItemType.WEAPON,   IC.filler,               70, 75, PSORamData(byte_data=b'\x0B\x00')),
    ItemName.POLE:                PSOItemData(PSOItemType.WEAPON,   IC.filler,               71, 50, PSORamData(byte_data=b'\x0B\x01')),

    ItemName.WAND:                PSOItemData(PSOItemType.WEAPON,   IC.filler,               75, 15, PSORamData(byte_data=b'\x0C\x00')),
    ItemName.STAFF:               PSOItemData(PSOItemType.WEAPON,   IC.filler,               76, 15, PSORamData(byte_data=b'\x0C\x01')),


    ItemName.VICTORY:             PSOItemData(PSOItemType.EVENT,    IC.progression,        None, None, PSORamData()),
}


def make_item_name_to_id_dict(item_table: dict[str, PSOItemData]) -> dict[str, int | None]:
    name = item_table.keys()
    *_, code = zip(*item_table.values())
    return dict(zip(name, code))

# Every item must have a unique integer ID associated with it.
# We will have a lookup from item name to ID here that, in world.py, we will import and bind to the world class.
# Even if an item doesn't exist on specific options, it must be present in this lookup.
# ITEM_NAME_TO_ID: dict[str, int | None] =  make_item_name_to_id_dict(ITEM_TABLE)
ITEM_NAME_TO_ID: dict[str, int | None] = {key: item.code for (key, item) in ITEM_TABLE.items()}


# TODO: This doesn't fix the issue of Victory being None
def make_id_to_item_name_dict(item_table: dict[str, PSOItemData]) -> dict[int, str]:
    name = item_table.keys()
    *_, code = zip(*item_table.values())

    # We don't add the last element of the array, since it's the Victory table
    return dict(zip(list(code)[:-1], list(name)[:-1]))

# We have a reverse lookup table for getting item name from ID as well
# It's possible we don't need this, but it may be a performance trade-off given the number of items this game has
ITEM_ID_TO_NAME: dict[int, str] = {id: name for (name, id) in ITEM_NAME_TO_ID.items() if id is not None}


# Ontop of our regular itempool, our world must be able to create arbitrary amounts of filler as requested by core.
# To do this, it must define a function called world.get_filler_item_name(), which we will define in world.py later.
# For now, let's make a function that returns the name of a random filler item here in items.py.
def get_random_filler_item_name(world: PSOWorld) -> str:
    # IMPORTANT: Whenever you need to use a random generator, you must use world.random.
    # This ensures that generating with the same generator seed twice yields the same output.
    # DO NOT use a bare random object from Python's built-in random module.
    if world.random.randint(0, 99) < world.options.trap_chance:
        # TODO: Actually put traps in here
        print("And this is where we'd put a trap, if we had one.")

    # Use a random number to decide what kind of filler item to give
    # TODO: It might be possible to assign each item a "weight" and then compile a struct based on what items are available and filter on that
    value = world.random.randint(0, 99)
    if 0 <= value < 6:
        return ItemName.SABER
    elif 6 <= value < 10:
        return ItemName.BRAND
    elif 10 <= value < 12:
        return ItemName.BUSTER
    elif 12 <= value < 16:
        return ItemName.SWORD
    elif 16 <= value < 19:
        return ItemName.GIGUSH
    elif 19 <= value < 23:
        return ItemName.DAGGER
    elif 23 <= value < 26:
        return ItemName.KNIFE
    elif 26 <= value < 27:
        return ItemName.BLADE
    elif 27 <= value < 37:
        return ItemName.PARTISAN
    elif 37 <= value < 39:
        return ItemName.HALBERT
    elif 39 <= value < 47:
        return ItemName.SLICER
    elif 47 <= value < 53:
        return ItemName.HANDGUN
    elif 53 <= value < 57:
        return ItemName.AUTOGUN
    elif 57 <= value < 59:
        return ItemName.LOCKGUN
    elif 59 <= value < 63:
        return ItemName.RIFLE
    elif 63 <= value < 66:
        return ItemName.SNIPER
    elif 66 <= value < 71:
        return ItemName.MECHGUN
    elif 71 <= value < 73:
        return ItemName.ASSAULT
    elif 73 <= value < 77:
        return ItemName.SHOT
    elif 77 <= value < 83:
        return ItemName.CANE
    elif 83 <= value < 87:
        return ItemName.STICK
    elif 87 <= value < 91:
        return ItemName.ROD
    elif 91 <= value < 94:
        return ItemName.POLE
    elif 94 <= value < 98:
        return ItemName.WAND
    elif 98 <= value < 100:
        return ItemName.STAFF
    # If we somehow missed a value, just give them a saber.
    return ItemName.SABER


def create_item_with_correct_classification(world: PSOWorld, name: str) -> PSOItem:
    # We may rewrite this to be more straight forward, but until we know if we're using multiple
    # classifications, we leave it for now.
    testing = True
    classification = ITEM_TABLE[name].classification

    # It is perfectly normal and valid for an item's classification to differ based on the player's options.
    # In our case, Health Upgrades are only relevant to logic (and thus labeled as "progression") in hard mode.
    if not testing and name == "Lavis Blade":
        classification = IC.useful

    return PSOItem(name, classification, ITEM_NAME_TO_ID[name], world.player)


# With those two helper functions defined, let's now get to actually creating and submitting our itempool.
def create_all_items(world: PSOWorld) -> None:
    # We start with Forest 1 unlocked by default
    starting_inventory: list[PSOItem] = [create_item_with_correct_classification(world, ItemName.UNLOCK_FOREST_1)]

    if world.options.start_with_lavis_blade:
        starting_inventory.append(world.create_item("Lavis Blade"))

    if starting_inventory:
        for item in starting_inventory:
            world.push_precollected(item)


    # We filter the item table for items with the 'progression' classification and return their name strings
    # since create_item takes in the unique name strings
    progression_item_names = filter(lambda _name: ITEM_TABLE[_name].classification == IC.progression, ITEM_TABLE.keys())

    itempool: list[Item] = []

    # For now, we only care about adding progression items since we don't have many locations
    # This way we don't end up having too many items and not enough places to put them
    for name in progression_item_names:
        # Keep the Victory item out of the drop pool, otherwise things might get wonky
        if name == ItemName.VICTORY:
            # Instead, we place it specifically on the goal
            goal_location: str
            if world.options.goal == Goal.option_defeat_the_dragon:
                goal_location = "Defeat Dragon"
            else:
                goal_location = "Defeat Dark Falz"
            # TODO: Figure out if this is the right way to do this
            # world.get_location(goal_location).place_locked_item(world.create_item(name))
            continue
        itempool.append(world.create_item(name))

    number_of_items = len(itempool)

    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool