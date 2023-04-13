from typing import Dict, NamedTuple, Optional, List
from BaseClasses import Item, MultiWorld
from .Options import get_option_value
from .static_logic import StaticLingoLogic


class ItemData(NamedTuple):
    """
    ItemData for an item in Lingo
    """
    code: Optional[int]
    progression: bool
    mode: Optional[str]
    event: bool
    door_ids: List[str]
    painting_ids: List[str]

    def should_include(self, world: MultiWorld, player: int) -> bool:
        if self.mode == "colors":
            return get_option_value(world, player, "shuffle_colors") > 0
        elif self.mode == "doors" or self.mode == "orange tower":
            if get_option_value(world, player, "shuffle_doors") > 0:
                if self.mode == "orange tower" and get_option_value(world, player, "orange_tower_access") == 2:
                    return False
                return True
            else:
                return False
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

    base_id: int = 0

    ALL_ITEM_TABLE: Dict[str, ItemData] = {}

    def create_item(self, name: str, event: bool, progression: bool, mode: Optional[str] = None,
                    door_ids: Optional[List[str]] = None, painting_ids: Optional[List[str]] = None):
        new_id = None if event is True else self.base_id + len(self.ALL_ITEM_TABLE)
        new_item = ItemData(new_id, progression, mode, event, [] if door_ids is None else door_ids,
                            [] if painting_ids is None else painting_ids)
        self.ALL_ITEM_TABLE[name] = new_item

    def __init__(self, base_id: int):
        self.base_id = base_id

        for color in ["Black", "Red", "Blue", "Yellow", "Green", "Orange", "Gray", "Brown", "Purple"]:
            self.create_item(color, False, True, "colors")

        for room_name, doors in StaticLingoLogic.DOORS_BY_ROOM.items():
            for door_name, door in doors.items():
                if door.skip_item is False:
                    self.create_item(door.item_name, False, True,
                                     "orange tower" if room_name == "Orange Tower" else "doors", door.door_ids,
                                     door.painting_ids)

        self.create_item("Progressive Orange Tower", False, True, "special")
        self.create_item("Nothing", False, False)
