"""This module represents item definitions for Trails in the Sky the 3rd"""
from typing import Dict, NamedTuple, Optional, Set

from .names.item_name import ItemName
from BaseClasses import Item, ItemClassification

class TitsThe3rdItem(Item):
    """Trails in the Sky the 3rd Item Definition"""
    game: str = "Trails in the Sky the 3rd"

    def __init__(self, name, classification: ItemClassification, code: Optional[int], player: int):
        super(TitsThe3rdItem, self).__init__(name, classification, code, player)

class TitsThe3rdItemData(NamedTuple):
    """Trails in the Sky the 3rd Item Data"""
    code: int
    classification: ItemClassification


def get_item_id(item_name: ItemName):
    if item_name not in item_data_table:
        raise Exception(f"{item_name} is not part of location list. Something went wrong?")
    return item_data_table[item_name].code


consumable_table: Dict[str, TitsThe3rdItemData] = {
    ItemName.extra_spicy_fries: TitsThe3rdItemData(408, ItemClassification.filler),
    ItemName.fresh_water: TitsThe3rdItemData(411, ItemClassification.filler),
    ItemName.fishy_finale: TitsThe3rdItemData(437, ItemClassification.filler),
    ItemName.tear_balm: TitsThe3rdItemData(501, ItemClassification.filler),
    ItemName.teara_balm: TitsThe3rdItemData(502, ItemClassification.filler),
    ItemName.reviving_balm: TitsThe3rdItemData(508, ItemClassification.filler),
    ItemName.ep_charge: TitsThe3rdItemData(510, ItemClassification.filler),
    ItemName.smelling_salts: TitsThe3rdItemData(512, ItemClassification.filler),
}

recipe_table: Dict[str, TitsThe3rdItemData] = {
    ItemName.easy_paella_recipe: TitsThe3rdItemData(10000, ItemClassification.filler),
}

equipment_table: Dict[str, TitsThe3rdItemData] = {
    ItemName.royal_spikes: TitsThe3rdItemData(102, ItemClassification.useful),
    ItemName.black_bangle: TitsThe3rdItemData(356, ItemClassification.useful),
    ItemName.glam_choker: TitsThe3rdItemData(358, ItemClassification.useful),
}

quartz_table: Dict[str, TitsThe3rdItemData] = {
    ItemName.hit_2: TitsThe3rdItemData(619, ItemClassification.useful),
    ItemName.information: TitsThe3rdItemData(657, ItemClassification.useful),
}

currency_table: Dict[str, TitsThe3rdItemData] = {
    ItemName.mira_300: TitsThe3rdItemData(20000, ItemClassification.filler),
    ItemName.lower_elements_sepith_50: TitsThe3rdItemData(20001, ItemClassification.filler),
    ItemName.higher_elements_sepith_50: TitsThe3rdItemData(20002, ItemClassification.filler),
}

key_item_table: Dict[str, TitsThe3rdItemData] = {ItemName.bennu_defeat: TitsThe3rdItemData(500000, ItemClassification.progression)}

item_data_table: Dict[str, TitsThe3rdItemData] = {
    **consumable_table,
    **recipe_table,
    **equipment_table,
    **quartz_table,
    **currency_table,
    **key_item_table,
}

item_groups: Dict[str, Set[str]] = {
    "Consumables": set(consumable_table.keys()),
    "Recipes": set(recipe_table.keys()),
    "Equipment": set(equipment_table.keys()),
    "Quartz": set(quartz_table.keys()),
    "Currency": set(currency_table.keys()),
}

item_table: Dict[str, int] = {name: data.code for name, data in item_data_table.items()}

default_item_pool: Dict[str, int] = {
    ItemName.extra_spicy_fries: 1,  # Default locations: 9864
    ItemName.fresh_water: 1,  # Default locations: 9880
    ItemName.fishy_finale: 1,  # Default locations: 9884
    ItemName.tear_balm: 2,  # Default locations: 9858, 9865
    ItemName.teara_balm: 2,  # Default locations: 9720, 9722
    ItemName.reviving_balm: 1,  # Default locations: 9874
    ItemName.ep_charge: 2,  # Default locations: 9721, 9723
    ItemName.smelling_salts: 1,  # Default locations: 9866
    ItemName.easy_paella_recipe: 1,  # Default locations: 9873
    ItemName.royal_spikes: 1,  # Default locations: 9869
    ItemName.black_bangle: 1,  # Default locations: 9867
    ItemName.glam_choker: 1,  # Default locations: 9868
    ItemName.hit_2: 1,  # Default locations: 9872
    ItemName.information: 1,  # Default locations: 9857
    ItemName.mira_300: 2,  # Default locations: 9859, 9875
    ItemName.lower_elements_sepith_50: 1,  # Default locations: 9881
    ItemName.higher_elements_sepith_50: 1,  # Default locations: 9885
}
