from enum import Enum
from typing import Dict, List, NamedTuple, Set

from BaseClasses import Item, ItemClassification
from .static_logic import DOORS_BY_ROOM, PROGRESSIVE_ITEMS, get_door_group_item_id, get_door_item_id, \
    get_progressive_item_id, get_special_item_id


class ItemType(Enum):
    NORMAL = 1
    COLOR = 2


class ItemData(NamedTuple):
    """
    ItemData for an item in Lingo
    """
    code: int
    classification: ItemClassification
    type: ItemType
    has_doors: bool
    painting_ids: List[str]


class LingoItem(Item):
    """
    Item from the game Lingo
    """
    game: str = "Lingo"


ALL_ITEM_TABLE: Dict[str, ItemData] = {}
ITEMS_BY_GROUP: Dict[str, List[str]] = {}

TRAP_ITEMS: List[str] = ["Slowness Trap", "Iceland Trap", "Atbash Trap"]


def load_item_data():
    global ALL_ITEM_TABLE, ITEMS_BY_GROUP

    for color in ["Black", "Red", "Blue", "Yellow", "Green", "Orange", "Gray", "Brown", "Purple"]:
        ALL_ITEM_TABLE[color] = ItemData(get_special_item_id(color), ItemClassification.progression,
                                         ItemType.COLOR, False, [])
        ITEMS_BY_GROUP.setdefault("Colors", []).append(color)

    door_groups: Set[str] = set()
    for room_name, doors in DOORS_BY_ROOM.items():
        for door_name, door in doors.items():
            if door.skip_item is True or door.event is True:
                continue

            if door.door_group is not None:
                door_groups.add(door.door_group)

            ALL_ITEM_TABLE[door.item_name] = \
                ItemData(get_door_item_id(room_name, door_name), ItemClassification.progression, ItemType.NORMAL,
                         door.has_doors, door.painting_ids)
            ITEMS_BY_GROUP.setdefault("Doors", []).append(door.item_name)

            if door.item_group is not None:
                ITEMS_BY_GROUP.setdefault(door.item_group, []).append(door.item_name)

    for group in door_groups:
        ALL_ITEM_TABLE[group] = ItemData(get_door_group_item_id(group),
                                         ItemClassification.progression, ItemType.NORMAL, True, [])
        ITEMS_BY_GROUP.setdefault("Doors", []).append(group)

    special_items: Dict[str, ItemClassification] = {
        ":)":                        ItemClassification.filler,
        "The Feeling of Being Lost": ItemClassification.filler,
        "Wanderlust":                ItemClassification.filler,
        "Empty White Hallways":      ItemClassification.filler,
        **{trap_name: ItemClassification.trap for trap_name in TRAP_ITEMS},
        "Puzzle Skip":               ItemClassification.useful,
    }

    for item_name, classification in special_items.items():
        ALL_ITEM_TABLE[item_name] = ItemData(get_special_item_id(item_name), classification,
                                             ItemType.NORMAL, False, [])

        if classification == ItemClassification.filler:
            ITEMS_BY_GROUP.setdefault("Junk", []).append(item_name)
        elif classification == ItemClassification.trap:
            ITEMS_BY_GROUP.setdefault("Traps", []).append(item_name)

    for item_name in PROGRESSIVE_ITEMS:
        ALL_ITEM_TABLE[item_name] = ItemData(get_progressive_item_id(item_name),
                                             ItemClassification.progression, ItemType.NORMAL, False, [])


# Initialize the item data at module scope.
load_item_data()
