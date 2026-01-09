from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

from BaseClasses import Item, ItemClassification as IC

from enum import Enum, auto

from .helpers import PSORamData

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
    ram_data: PSORamData


# Each Item instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Item class and override the "game" field.
class PSOItem(Item):
    game = "PSO"


# We comment out the boss unlocks for now to keep the checks low while we figure stuff out
ITEM_TABLE: dict[str, PSOItemData] = {
#    ItemName.UNLOCK_FOREST_1:     PSOItemData(PSOItemType.AREA,     IC.progression,                   1, PSORamData()),
#    ItemName.UNLOCK_FOREST_2:     PSOItemData(PSOItemType.AREA,     IC.progression,                   2, PSORamData()),
#    ItemName.UNLOCK_DRAGON:       PSOItemData(PSOItemType.AREA,     IC.progression,                   3, PSORamData()),
    ItemName.UNLOCK_CAVES_1:      PSOItemData(PSOItemType.AREA,     IC.progression,                   4, PSORamData(0x805127FB, 7)),
#    ItemName.UNLOCK_CAVES_2:      PSOItemData(PSOItemType.AREA,     IC.progression,                   5, PSORamData()),
#    ItemName.UNLOCK_CAVES_3:      PSOItemData(PSOItemType.AREA,     IC.progression,                   6, PSORamData()),
#    ItemName.UNLOCK_DE_ROL_LE:    PSOItemData(PSOItemType.AREA,     IC.progression,                   7, PSORamData()),
    ItemName.UNLOCK_MINES_1:      PSOItemData(PSOItemType.AREA,     IC.progression,                   8, PSORamData(0x805127FC, 6)),
#    ItemName.UNLOCK_MINES_2:      PSOItemData(PSOItemType.AREA,     IC.progression,                   9, PSORamData()),
#    ItemName.UNLOCK_VOL_OPT:      PSOItemData(PSOItemType.AREA,     IC.progression,                  10, PSORamData()),
#    ItemName.UNLOCK_RUINS_1:      PSOItemData(PSOItemType.AREA,     IC.progression,                  11, PSORamData(0x805127FE, 7)),
#    ItemName.UNLOCK_RUINS_2:      PSOItemData(PSOItemType.AREA,     IC.progression,                  12, PSORamData()),
#    ItemName.UNLOCK_RUINS_3:      PSOItemData(PSOItemType.AREA,     IC.progression,                  13, PSORamData()),
#    ItemName.UNLOCK_DARK_FALZ:    PSOItemData(PSOItemType.AREA,     IC.progression,                  14, PSORamData()),

    ItemName.FOREST_PILLAR:       PSOItemData(PSOItemType.SWITCH,   IC.progression,                  15, PSORamData(0x805127FD, 3)),
    ItemName.CAVES_PILLAR:        PSOItemData(PSOItemType.SWITCH,   IC.progression,                  16, PSORamData(0x805127FD, 2)),
    ItemName.MINES_PILLAR:        PSOItemData(PSOItemType.SWITCH,   IC.progression,                  17, PSORamData(0x805127FD, 1)),

    "Lavis Blade":                PSOItemData(PSOItemType.WEAPON,   IC.filler | IC.useful,           18, PSORamData()),

    ItemName.VICTORY:             PSOItemData(PSOItemType.EVENT,    IC.progression,                None, PSORamData()),
}


def make_item_name_to_id_dict(item_table: dict[str, PSOItemData]) -> dict[str, int | None]:
    name = item_table.keys()
    *_, code = zip(*item_table.values())
    return dict(zip(name, code))

# Every item must have a unique integer ID associated with it.
# We will have a lookup from item name to ID here that, in world.py, we will import and bind to the world class.
# Even if an item doesn't exist on specific options, it must be present in this lookup.
ITEM_NAME_TO_ID: dict[str, int | None] = make_item_name_to_id_dict(ITEM_TABLE)


# TODO: This doesn't fix the issue of Victory being None
def make_id_to_item_name_dict(item_table: dict[str, PSOItemData]) -> dict[int, str]:
    name = item_table.keys()
    *_, code = zip(*item_table.values())

    # We don't add the last element of the array, since it's the Victory table
    return dict(zip(code[:-1], name[:-1]))

# We have a reverse lookup table for getting item name from ID as well
# It's possible we don't need this, but it may be a performance trade-off given the number of items this game has
ITEM_ID_TO_NAME: dict[int, str] = make_id_to_item_name_dict(ITEM_TABLE)


# Ontop of our regular itempool, our world must be able to create arbitrary amounts of filler as requested by core.
# To do this, it must define a function called world.get_filler_item_name(), which we will define in world.py later.
# For now, let's make a function that returns the name of a random filler item here in items.py.
def get_random_filler_item_name(world: PSOWorld) -> str:
    # IMPORTANT: Whenever you need to use a random generator, you must use world.random.
    # This ensures that generating with the same generator seed twice yields the same output.
    # DO NOT use a bare random object from Python's built-in random module.
    if world.random.randint(0, 99) < world.options.trap_chance:
        # TODO: Actually put traps in here
        return "Lavis Blade"
    return "Lavis Blade"


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
    # We filter the item table for items with the 'progression' classification and return their name strings
    # since create_item takes in the unique name strings
    progression_item_names = filter(lambda _name: ITEM_TABLE[_name].classification == IC.progression, ITEM_TABLE.keys())

    itempool: list[Item] = []

    # For now, we only care about adding progression items since we don't have many locations
    # This way we don't end up having too many items and not enough places to put them
    for name in progression_item_names:
        # Keep the Victory item out of the drop pool, otherwise things might get wonky
        if name == ItemName.VICTORY:
            # Instead, we place it specifically on the goal, of which there is only one option right now
            world.get_location("Defeat Dark Falz").place_locked_item(world.create_item(name))
            continue
        itempool.append(world.create_item(name))

    number_of_items = len(itempool)

    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool

    starting_inventory: list[PSOItem] = []

    if world.options.start_with_lavis_blade:
        starting_inventory.append(world.create_item("Lavis Blade"))

    if starting_inventory:
        for item in starting_inventory:
            world.push_precollected(item)