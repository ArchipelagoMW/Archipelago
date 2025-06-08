from enum import IntEnum
from typing import NamedTuple
import random
from BaseClasses import Item


class MedievilItemCategory(IntEnum):
    FILLER = 0
    PROGRESSION = 1
    FUN = 2
    LEVEL_END = 4
    SKIP = 5

class MedievilItemData(NamedTuple):
    name: str
    m_code: str
    category: MedievilItemCategory


class MedievilItem(Item):
    game: str = "Medievil"
    category: MedievilItemCategory
    default_item_name: str


    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 9900000
        return {item_data.name: (base_id + item_data.m_code if item_data.m_code is not None else None) for item_data in _all_items}


key_item_names = {
}


_all_items = [MedievilItemData(row[0], row[1], row[2]) for row in [    
    ("Gold (50)", 1000, MedievilItemCategory.FILLER),
    ("Gold (100)", 1001, MedievilItemCategory.FILLER),
    ("Gold (150)", 1002, MedievilItemCategory.FILLER),
    ("Daggers (10)", 1004, MedievilItemCategory.FILLER),
    ("Daggers (20)", 1005, MedievilItemCategory.FILLER),
    ("Broadsword Energy (20)", 1006, MedievilItemCategory.FILLER),
    ("Broadsword Energy (50)", 1007, MedievilItemCategory.FILLER),
    ("Club Energy (20)", 1008, MedievilItemCategory.FILLER),
    ("Club Energy (50)", 1009, MedievilItemCategory.FILLER),
    ("Chicken Drumsticks (10)", 1010, MedievilItemCategory.FILLER),
    ("Crossbow Ammo (20)", 1011, MedievilItemCategory.FILLER),
    ("Crossbow Ammo (50)", 1012, MedievilItemCategory.FILLER),
    ("Longbow Ammo (20)", 1013, MedievilItemCategory.FILLER),
    ("Longbow Ammo (50)", 1014, MedievilItemCategory.FILLER),
    ("Fire Longbow Ammo (20)", 1015, MedievilItemCategory.FILLER),
    ("Fire Longbow Ammo (50)", 1016, MedievilItemCategory.FILLER),
    ("Magic Longbow Ammo (20)", 1017, MedievilItemCategory.FILLER),
    ("Magic Longbow Ammo (50)", 1018, MedievilItemCategory.FILLER),
    ("Spear Ammo (20)", 1019, MedievilItemCategory.FILLER),
    ("Spear Ammo (50)", 1020, MedievilItemCategory.FILLER),
    ("Lightning Charge (30)", 1021, MedievilItemCategory.FILLER),
    ("Lightning Charge (50)", 1022, MedievilItemCategory.FILLER),
    ("Copper Shield Charge (50)", 1023, MedievilItemCategory.FILLER),
    ("Copper Shield Charge (100)", 1024, MedievilItemCategory.FILLER),
    ("Silver Shield Charge (50)", 1025, MedievilItemCategory.FILLER),
    ("Silver Shield Charge (100)", 1026, MedievilItemCategory.FILLER),
    ("Gold Shield Charge (50)", 1026, MedievilItemCategory.FILLER),
    ("Gold Shield Charge (100)", 1027, MedievilItemCategory.FILLER),
    ("Level_End", 9900, MedievilItemCategory.LEVEL_END)
]]

item_descriptions = {
}

item_dictionary = {item_data.name: item_data for item_data in _all_items}

def BuildItemPool(count, options):
    item_pool = []
    included_itemcount = 0

    if options.guaranteed_items.value:
        for item_name in options.guaranteed_items.value:
            item = item_dictionary[item_name]
            item_pool.append(item)
            included_itemcount = included_itemcount + 1
    remaining_count = count - included_itemcount
    
    for i in range(remaining_count):
        itemList = [item for item in _all_items]
        item = random.choice(itemList)
        item_pool.append(item)
    
    random.shuffle(item_pool)
    return item_pool