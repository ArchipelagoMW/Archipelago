from typing import Dict, NamedTuple, Optional
from BaseClasses import Item, MultiWorld
from .Options import get_option_value
from .static_logic import StaticLingoLogic


class ItemData(NamedTuple):
    """
    ItemData for an item in Lingo
    """
    code: Optional[int]
    progression: bool
    mode: Optional[str] = None
    event: bool = False
    orange_tower: bool = False

    def should_include(self, world: MultiWorld, player: int) -> bool:
        if self.mode == "colors":
            return get_option_value(world, player, "shuffle_colors") > 0
        elif self.mode == "doors":
            if get_option_value(world, player, "shuffle_doors") > 0:
                if self.orange_tower and get_option_value(world, player, "orange_tower_access") == 2:
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
    ALL_ITEM_TABLE: Dict[str, ItemData] = {}

    def __init__(self, base_id: int):
        item_tab = dict()

        for color in ["Black", "Red", "Blue", "Yellow", "Green", "Orange", "Gray", "Brown", "Purple"]:
            item_tab[color] = ItemData(base_id + len(item_tab), True, "colors")

        for room_name, doors in StaticLingoLogic.DOORS_BY_ROOM.items():
            for door_name, door in doors.items():
                if door.skip_item is False:
                    item_tab[door.item_name] = \
                        ItemData(base_id + len(item_tab), True, mode="doors", orange_tower=room_name == "Orange Tower")

        item_tab["Progressive Orange Tower"] = ItemData(base_id + len(item_tab), True, "special")
        item_tab["Nothing"] = ItemData(base_id + len(item_tab), False)

        for key, item in item_tab.items():
            self.ALL_ITEM_TABLE[key] = item
