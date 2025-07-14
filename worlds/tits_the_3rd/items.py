"""This module represents item definitions for Trails in the Sky the 3rd"""

from collections import Counter
import itertools
from typing import Dict, List, NamedTuple, Optional, Set

from .names.item_name import ItemName
from .names.location_name import LocationName
from .tables.location_list import location_table
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

meta_data_table: Dict[str, TitsThe3rdItemData] = {
    ItemName.mira_min_id: TitsThe3rdItemData(100000, ItemClassification.filler),
    ItemName.mira_max_id: TitsThe3rdItemData(199999, ItemClassification.filler),
    ItemName.lower_elements_sepith_min_id: TitsThe3rdItemData(300000, ItemClassification.filler),
    ItemName.lower_elements_sepith_max_id: TitsThe3rdItemData(300999, ItemClassification.filler),
    ItemName.higher_elements_sepith_min_id: TitsThe3rdItemData(350000, ItemClassification.filler),
    ItemName.higher_elements_sepith_max_id: TitsThe3rdItemData(350999, ItemClassification.filler),
    ItemName.character_min_id: TitsThe3rdItemData(70000, ItemClassification.filler),
    ItemName.character_max_id: TitsThe3rdItemData(71000, ItemClassification.filler),
    ItemName.area_min_id: TitsThe3rdItemData(200000, ItemClassification.filler),
    ItemName.area_max_id: TitsThe3rdItemData(299999, ItemClassification.filler),
    ItemName.recipe_min_id: TitsThe3rdItemData(80000, ItemClassification.filler),
    ItemName.recipe_max_id: TitsThe3rdItemData(81000, ItemClassification.filler),
}

consumable_table: Dict[str, TitsThe3rdItemData] = {
    ItemName.extra_spicy_fries: TitsThe3rdItemData(408, ItemClassification.filler),
    ItemName.fried_phoenix: TitsThe3rdItemData(428, ItemClassification.filler),
    ItemName.brain_roast: TitsThe3rdItemData(412, ItemClassification.filler),
    ItemName.swingwich: TitsThe3rdItemData(409, ItemClassification.filler),
    ItemName.repellent_dish: TitsThe3rdItemData(404, ItemClassification.filler),
    ItemName.fluffy_crepe: TitsThe3rdItemData(332, ItemClassification.filler),
    ItemName.septium_drops: TitsThe3rdItemData(503, ItemClassification.filler),
    ItemName.queenly_cookie: TitsThe3rdItemData(480, ItemClassification.filler),
    ItemName.fresh_water: TitsThe3rdItemData(411, ItemClassification.filler),
    ItemName.fishy_finale: TitsThe3rdItemData(437, ItemClassification.filler),
    ItemName.tear_balm: TitsThe3rdItemData(501, ItemClassification.filler),
    ItemName.teara_balm: TitsThe3rdItemData(502, ItemClassification.filler),
    ItemName.reviving_balm: TitsThe3rdItemData(508, ItemClassification.filler),
    ItemName.celestial_balm: TitsThe3rdItemData(509, ItemClassification.filler),
    ItemName.ep_charge: TitsThe3rdItemData(510, ItemClassification.filler),
    ItemName.smelling_salts: TitsThe3rdItemData(512, ItemClassification.filler),
    ItemName.insulating_tape: TitsThe3rdItemData(506, ItemClassification.filler),
    ItemName.softening_balm: TitsThe3rdItemData(505, ItemClassification.filler),
    ItemName.s_tablet: TitsThe3rdItemData(518, ItemClassification.filler),
    ItemName.purging_balm: TitsThe3rdItemData(504, ItemClassification.filler),
    ItemName.zeram_powder: TitsThe3rdItemData(517, ItemClassification.filler),
}

recipe_table: Dict[str, TitsThe3rdItemData] = {
    ItemName.easy_paella_recipe: TitsThe3rdItemData(meta_data_table[ItemName.recipe_min_id].code + 1, ItemClassification.filler),
}

equipment_table: Dict[str, TitsThe3rdItemData] = {
    ItemName.royal_spikes: TitsThe3rdItemData(102, ItemClassification.useful),
    ItemName.black_bangle: TitsThe3rdItemData(356, ItemClassification.useful),
    ItemName.black_bangle_plus: TitsThe3rdItemData(357, ItemClassification.useful),
    ItemName.glam_choker: TitsThe3rdItemData(358, ItemClassification.useful),
    ItemName.glam_choker_plus: TitsThe3rdItemData(359, ItemClassification.useful),
    ItemName.white_bracelet: TitsThe3rdItemData(360, ItemClassification.useful),
    ItemName.proxy_puppet: TitsThe3rdItemData(325, ItemClassification.useful),
    ItemName.long_barrel_2: TitsThe3rdItemData(332, ItemClassification.useful),
    ItemName.crimson_eye: TitsThe3rdItemData(394, ItemClassification.useful),
    ItemName.pearl_earings: TitsThe3rdItemData(362, ItemClassification.useful),
    # Weapons
    ItemName.akashic_heart: TitsThe3rdItemData(1184, ItemClassification.useful),
    ItemName.stun_gb: TitsThe3rdItemData(1274, ItemClassification.useful),
    # Armor
    ItemName.bestia_coat: TitsThe3rdItemData(1553, ItemClassification.useful),
}

quartz_table: Dict[str, TitsThe3rdItemData] = {
    ItemName.hp_1: TitsThe3rdItemData(600, ItemClassification.useful),
    ItemName.hp_2: TitsThe3rdItemData(601, ItemClassification.useful),
    ItemName.attack_1: TitsThe3rdItemData(606, ItemClassification.useful),
    ItemName.attack_2: TitsThe3rdItemData(607, ItemClassification.useful),
    ItemName.shield_1: TitsThe3rdItemData(615, ItemClassification.useful),
    ItemName.shield_2: TitsThe3rdItemData(616, ItemClassification.useful),
    ItemName.hit_1: TitsThe3rdItemData(618, ItemClassification.useful),
    ItemName.hit_2: TitsThe3rdItemData(619, ItemClassification.useful),
    ItemName.move_1: TitsThe3rdItemData(624, ItemClassification.useful),
    ItemName.action_1: TitsThe3rdItemData(627, ItemClassification.useful),
    ItemName.range_1: TitsThe3rdItemData(630, ItemClassification.useful),
    ItemName.information: TitsThe3rdItemData(657, ItemClassification.useful),
    ItemName.ep_cut_2: TitsThe3rdItemData(713, ItemClassification.useful),
    ItemName.scent: TitsThe3rdItemData(720, ItemClassification.useful),
    ItemName.eagle_eye: TitsThe3rdItemData(721, ItemClassification.useful),
    ItemName.haze: TitsThe3rdItemData(722, ItemClassification.useful),
}

currency_table: Dict[str, TitsThe3rdItemData] = {
    # Mira
    ItemName.mira_300: TitsThe3rdItemData(meta_data_table[ItemName.mira_min_id].code + 300, ItemClassification.filler),
    ItemName.mira_500: TitsThe3rdItemData(meta_data_table[ItemName.mira_min_id].code + 500, ItemClassification.filler),
    ItemName.mira_1000: TitsThe3rdItemData(meta_data_table[ItemName.mira_min_id].code + 1000, ItemClassification.filler),
    ItemName.mira_5000: TitsThe3rdItemData(meta_data_table[ItemName.mira_min_id].code + 5000, ItemClassification.filler),
    ItemName.mira_10000: TitsThe3rdItemData(meta_data_table[ItemName.mira_min_id].code + 10000, ItemClassification.filler),
    # Low Sepith
    ItemName.lower_elements_sepith_50: TitsThe3rdItemData(meta_data_table[ItemName.lower_elements_sepith_min_id].code + 50, ItemClassification.filler),
    ItemName.lower_elements_sepith_100: TitsThe3rdItemData(meta_data_table[ItemName.lower_elements_sepith_min_id].code + 100, ItemClassification.filler),
    ItemName.lower_elements_sepith_250: TitsThe3rdItemData(meta_data_table[ItemName.lower_elements_sepith_min_id].code + 250, ItemClassification.filler),
    ItemName.lower_elements_sepith_500: TitsThe3rdItemData(meta_data_table[ItemName.lower_elements_sepith_min_id].code + 500, ItemClassification.filler),
    # High Sepith
    ItemName.higher_elements_sepith_50: TitsThe3rdItemData(meta_data_table[ItemName.higher_elements_sepith_min_id].code + 50, ItemClassification.filler),
    ItemName.higher_elements_sepith_100: TitsThe3rdItemData(meta_data_table[ItemName.higher_elements_sepith_min_id].code + 100, ItemClassification.filler),
    ItemName.higher_elements_sepith_250: TitsThe3rdItemData(meta_data_table[ItemName.higher_elements_sepith_min_id].code + 250, ItemClassification.filler),
    ItemName.higher_elements_sepith_500: TitsThe3rdItemData(meta_data_table[ItemName.higher_elements_sepith_min_id].code + 500, ItemClassification.filler),
}

character_table: Dict[str, TitsThe3rdItemData] = {
    ItemName.kevin: TitsThe3rdItemData(meta_data_table[ItemName.character_min_id].code + 8, ItemClassification.progression),
    ItemName.ries: TitsThe3rdItemData(meta_data_table[ItemName.character_min_id].code + 14, ItemClassification.progression),
    ItemName.tita: TitsThe3rdItemData(meta_data_table[ItemName.character_min_id].code + 6, ItemClassification.progression),
    ItemName.julia: TitsThe3rdItemData(meta_data_table[ItemName.character_min_id].code + 13, ItemClassification.progression),
}

character_spoiler_table: Dict[str, TitsThe3rdItemData] = {
    ItemName.kevin_spoiler: TitsThe3rdItemData(meta_data_table[ItemName.character_min_id].code + 8, ItemClassification.progression),
    ItemName.ries_spoiler: TitsThe3rdItemData(meta_data_table[ItemName.character_min_id].code + 14, ItemClassification.progression),
    ItemName.tita_spoiler: TitsThe3rdItemData(meta_data_table[ItemName.character_min_id].code + 6, ItemClassification.progression),
    ItemName.julia_spoiler: TitsThe3rdItemData(meta_data_table[ItemName.character_min_id].code + 13, ItemClassification.progression),
}

area_unlock_table: Dict[str, TitsThe3rdItemData] = {  # Item ID is 200000 + flag number
    ItemName.jade_corridor_unlock_1: TitsThe3rdItemData(meta_data_table[ItemName.area_min_id].code + 256, ItemClassification.progression),
    ItemName.jade_corridor_unlock_2: TitsThe3rdItemData(meta_data_table[ItemName.area_min_id].code + 257, ItemClassification.progression),
    ItemName.jade_corridor_arseille_unlock: TitsThe3rdItemData(meta_data_table[ItemName.area_min_id].code + 258, ItemClassification.progression),
}

key_item_table: Dict[str, TitsThe3rdItemData] = {ItemName.bennu_defeat: TitsThe3rdItemData(500000, ItemClassification.progression)}


item_data_table: Dict[str, TitsThe3rdItemData] = {
    **consumable_table,
    **recipe_table,
    **equipment_table,
    **quartz_table,
    **currency_table,
    **key_item_table,
    **character_table,
    **character_spoiler_table,
    **area_unlock_table,
    **meta_data_table,
}

item_groups: Dict[str, Set[str]] = {
    "Consumables": set(consumable_table.keys()),
    "Recipes": set(recipe_table.keys()),
    "Equipment": set(equipment_table.keys()),
    "Quartz": set(quartz_table.keys()),
    "Currency": set(currency_table.keys()),
    "Characters": set(character_table.keys()),
    "Characters Spoiler": set(character_spoiler_table.keys()),
    "Area Unlock": set(area_unlock_table.keys()),
}

filler_items: List[str] = list(
    itertools.chain(
        item_groups["Consumables"],
        item_groups["Currency"],
        item_groups["Equipment"],
        item_groups["Quartz"],
    )
)

item_table: Dict[str, int] = {name: data.code for name, data in item_data_table.items()}

default_item_pool: Counter[str] = Counter()
default_chest_pool: Counter[str] = Counter()
default_character_quartz_pool: Counter[str] = Counter()
# fills the pool counters according to info in location_table
for location in location_table:
    if location_table[location].vanilla_item != "":
        if location_table[location].check_type == "Chest":
            default_chest_pool[location_table[location].vanilla_item] += 1
        if location_table[location].check_type == "Character Quartz":
            default_character_quartz_pool[location_table[location].vanilla_item] += 1
        if location_table[location].check_type == "Area Unlock":
            default_item_pool[location_table[location].vanilla_item] += 1

default_character_to_location = {
    ItemName.tita: LocationName.sealing_stone_tita,
    ItemName.julia: LocationName.sealing_stone_julia,
}
