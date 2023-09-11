from typing import Dict, NamedTuple, Optional, List
from BaseClasses import Item, MultiWorld, ItemClassification
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

    def should_include(self, multiworld: MultiWorld, player: int) -> bool:
        if self.mode == "colors":
            return getattr(multiworld, "shuffle_colors")[player] > 0
        elif self.mode == "doors":
            return getattr(multiworld, "shuffle_doors")[player] > 0
        elif self.mode == "orange tower":
            # door shuffle is on and tower isn't progressive
            return getattr(multiworld, "shuffle_doors")[player] > 0\
                and not getattr(multiworld, "progressive_orange_tower")[player]
        elif self.mode == "complex door":
            return getattr(multiworld, "shuffle_doors")[player] == 2  # complex doors
        elif self.mode == "door group":
            return getattr(multiworld, "shuffle_doors")[player] == 1  # simple doors
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

    ALL_ITEM_TABLE: Dict[str, ItemData] = {}

    def create_item(self, code: int, name: str, classification: ItemClassification, mode: Optional[str] = None,
                    door_ids: Optional[List[str]] = None, painting_ids: Optional[List[str]] = None):
        new_item = ItemData(code, classification, mode, [] if door_ids is None else door_ids,
                            [] if painting_ids is None else painting_ids)
        self.ALL_ITEM_TABLE[name] = new_item

    def __init__(self, static_logic: StaticLingoLogic):
        for color in ["Black", "Red", "Blue", "Yellow", "Green", "Orange", "Gray", "Brown", "Purple"]:
            self.create_item(static_logic.get_special_item_id(color), color, ItemClassification.progression, "colors")

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

                self.create_item(static_logic.get_door_item_id(room_name, door_name), door.item_name,
                                 ItemClassification.filler if door.junk_item else ItemClassification.progression,
                                 door_mode, door.door_ids, door.painting_ids)

        for group, group_door_ids in door_groups.items():
            self.create_item(static_logic.get_door_group_item_id(group), group, ItemClassification.progression,
                             "door group", group_door_ids, [])

        special_items: Dict[str, ItemClassification] = {
            "Nothing": ItemClassification.filler,
            "Slowness Trap": ItemClassification.trap,
            "Iceland Trap": ItemClassification.trap,
            "Atbash Trap": ItemClassification.trap,
            "Puzzle Skip": ItemClassification.useful,
        }

        for item_name, classification in special_items.items():
            self.create_item(static_logic.get_special_item_id(item_name), item_name, classification, "special")

        for item_name in StaticLingoLogic.PROGRESSIVE_ITEMS:
            self.create_item(static_logic.get_progressive_item_id(item_name), item_name, ItemClassification.progression,
                             "special")
