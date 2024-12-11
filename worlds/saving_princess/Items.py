from typing import Optional, Dict, Tuple

from BaseClasses import Item, ItemClassification as ItemClass

from .Constants import *


class SavingPrincessItem(Item):
    game: str = GAME_NAME


class ItemData:
    item_class: ItemClass
    code: Optional[int]
    count: int  # Number of copies for the item that will be made of class item_class
    count_extra: int  # Number of extra copies for the item that will be made as useful

    def __init__(self, item_class: ItemClass, code: Optional[int] = None, count: int = 1, count_extra: int = 0):
        self.item_class = item_class

        self.code = code
        if code is not None:
            self.code += BASE_ID

        # if this is filler, a trap or an event, ignore the count
        if self.item_class == ItemClass.filler or self.item_class == ItemClass.trap or code is None:
            self.count = 0
            self.count_extra = 0
        else:
            self.count = count
            self.count_extra = count_extra

    def create_item(self, player: int):
        return SavingPrincessItem(item_data_names[self], self.item_class, self.code, player)


item_dict_weapons: Dict[str, ItemData] = {
    ITEM_WEAPON_CHARGE: ItemData(ItemClass.progression, 0),
    ITEM_WEAPON_FIRE: ItemData(ItemClass.progression, 1),
    ITEM_WEAPON_ICE: ItemData(ItemClass.progression, 2),
    ITEM_WEAPON_VOLT: ItemData(ItemClass.progression, 3),
}

item_dict_upgrades: Dict[str, ItemData] = {
    ITEM_MAX_HEALTH: ItemData(ItemClass.progression, 4, 2, 4),
    ITEM_MAX_AMMO: ItemData(ItemClass.progression, 5, 2, 4),
    ITEM_RELOAD_SPEED: ItemData(ItemClass.progression, 6, 4, 2),
    ITEM_SPECIAL_AMMO: ItemData(ItemClass.useful, 7),
}

item_dict_base: Dict[str, ItemData] = {
    **item_dict_weapons,
    **item_dict_upgrades,
    ITEM_JACKET: ItemData(ItemClass.useful, 8),
}

item_dict_keys: Dict[str, ItemData] = {
    EP_ITEM_GUARD_GONE: ItemData(ItemClass.progression, 9),
    EP_ITEM_CLIFF_GONE: ItemData(ItemClass.progression, 10),
    EP_ITEM_ACE_GONE: ItemData(ItemClass.progression, 11),
    EP_ITEM_SNAKE_GONE: ItemData(ItemClass.progression, 12),
}

item_dict_expanded: Dict[str, ItemData] = {
    **item_dict_base,
    **item_dict_keys,
    EP_ITEM_POWER_ON: ItemData(ItemClass.progression, 13),
}

item_dict_filler: Dict[str, ItemData] = {
    FILLER_ITEM_HEAL: ItemData(ItemClass.filler, 14),
    FILLER_ITEM_QUICK_FIRE: ItemData(ItemClass.filler, 15),
    FILLER_ITEM_ACTIVE_CAMO: ItemData(ItemClass.filler, 16),
}

item_dict_traps: Dict[str, ItemData] = {
    TRAP_ITEM_ICE: ItemData(ItemClass.trap, 17),
    TRAP_ITEM_SHAKES: ItemData(ItemClass.trap, 18),
    TRAP_ITEM_NINJA: ItemData(ItemClass.trap, 19),
}

item_dict_events: Dict[str, ItemData] = {
    EVENT_ITEM_GUARD_GONE: ItemData(ItemClass.progression),
    EVENT_ITEM_CLIFF_GONE: ItemData(ItemClass.progression),
    EVENT_ITEM_ACE_GONE: ItemData(ItemClass.progression),
    EVENT_ITEM_SNAKE_GONE: ItemData(ItemClass.progression),
    EVENT_ITEM_POWER_ON: ItemData(ItemClass.progression),
    EVENT_ITEM_VICTORY: ItemData(ItemClass.progression),
}

item_dict: Dict[str, ItemData] = {
    **item_dict_expanded,
    **item_dict_filler,
    **item_dict_traps,
    **item_dict_events,
}

item_data_names: Dict[ItemData, str] = {value: key for key, value in item_dict.items()}
