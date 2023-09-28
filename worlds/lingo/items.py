from typing import Dict, NamedTuple, Optional, List
from types import MappingProxyType
from BaseClasses import Item, ItemClassification
from worlds.AutoWorld import World
from .static_logic import StaticLingoLogic


class ItemData(NamedTuple):
    """
    ItemData for an item in Lingo
    """
    code: int
    classification: ItemClassification
    mode: Optional[str]
    door_ids: List[str]
    painting_ids: List[str]

    def should_include(self, world: World) -> bool:
        if self.mode == "colors":
            return getattr(world.multiworld, "shuffle_colors")[world.player] > 0
        elif self.mode == "doors":
            return getattr(world.multiworld, "shuffle_doors")[world.player] > 0
        elif self.mode == "orange tower":
            # door shuffle is on and tower isn't progressive
            return getattr(world.multiworld, "shuffle_doors")[world.player] > 0\
                and not getattr(world.multiworld, "progressive_orange_tower")[world.player]
        elif self.mode == "complex door":
            return getattr(world.multiworld, "shuffle_doors")[world.player] == 2  # complex doors
        elif self.mode == "door group":
            return getattr(world.multiworld, "shuffle_doors")[world.player] == 1  # simple doors
        elif self.mode == "special":
            return False
        else:
            return True


class LingoItem(Item):
    """
    Item from the game Lingo
    """
    game: str = "Lingo"


class StaticLingoItems:
    """
    Defines the items that can be included in a Lingo world
    """

    ALL_ITEM_TABLE: MappingProxyType[str, ItemData]

    def __init__(self, static_logic: StaticLingoLogic):
        temp_item_table: Dict[str, ItemData] = {}

        for color in ["Black", "Red", "Blue", "Yellow", "Green", "Orange", "Gray", "Brown", "Purple"]:
            temp_item_table[color] = ItemData(static_logic.get_special_item_id(color), ItemClassification.progression,
                                              "colors", [], [])

        door_groups: Dict[str, List[str]] = {}
        for room_name, doors in static_logic.DOORS_BY_ROOM.items():
            for door_name, door in doors.items():
                if door.skip_item is True or door.event is True:
                    continue

                if door.group is None:
                    door_mode = "doors"
                else:
                    door_mode = "complex door"
                    door_groups.setdefault(door.group, []).extend(door.door_ids)

                if room_name in static_logic.PROGRESSION_BY_ROOM\
                        and door_name in static_logic.PROGRESSION_BY_ROOM[room_name]:
                    if room_name == "Orange Tower":
                        door_mode = "orange tower"
                    else:
                        door_mode = "special"

                temp_item_table[door.item_name] =\
                    ItemData(static_logic.get_door_item_id(room_name, door_name),
                             ItemClassification.filler if door.junk_item else ItemClassification.progression, door_mode,
                             door.door_ids, door.painting_ids)

        for group, group_door_ids in door_groups.items():
            temp_item_table[group] = ItemData(static_logic.get_door_group_item_id(group),
                                              ItemClassification.progression, "door group", group_door_ids, [])

        special_items: Dict[str, ItemClassification] = {
            "Nothing": ItemClassification.filler,
            "Slowness Trap": ItemClassification.trap,
            "Iceland Trap": ItemClassification.trap,
            "Atbash Trap": ItemClassification.trap,
            "Puzzle Skip": ItemClassification.useful,
        }

        for item_name, classification in special_items.items():
            temp_item_table[item_name] = ItemData(static_logic.get_special_item_id(item_name), classification,
                                                  "special", [], [])

        for item_name in static_logic.PROGRESSIVE_ITEMS:
            temp_item_table[item_name] = ItemData(static_logic.get_progressive_item_id(item_name),
                                                  ItemClassification.progression, "special", [], [])

        self.ALL_ITEM_TABLE = MappingProxyType(temp_item_table)
