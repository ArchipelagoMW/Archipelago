"""This module represents item definitions for Trails in the Sky the 3rd"""

from collections import Counter
import itertools
from typing import Dict, List, NamedTuple, Optional, Set

from .names.item_name import ItemName
from .names.location_name import LocationName
from .names.check_type_name import CheckTypeName
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
    ItemName.all_sepith_min_id: TitsThe3rdItemData(360000, ItemClassification.filler),
    ItemName.all_sepith_max_id: TitsThe3rdItemData(369999, ItemClassification.filler),
    ItemName.character_min_id: TitsThe3rdItemData(70000, ItemClassification.filler),
    ItemName.character_max_id: TitsThe3rdItemData(71000, ItemClassification.filler),
    ItemName.area_min_id: TitsThe3rdItemData(200000, ItemClassification.filler),
    ItemName.area_max_id: TitsThe3rdItemData(299999, ItemClassification.filler),
    ItemName.recipe_min_id: TitsThe3rdItemData(80000, ItemClassification.filler),
    ItemName.recipe_max_id: TitsThe3rdItemData(81000, ItemClassification.filler),
    ItemName.craft_min_id: TitsThe3rdItemData(400000, ItemClassification.filler),
    ItemName.craft_max_id: TitsThe3rdItemData(400999, ItemClassification.filler),
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
    ItemName.amar_spiritus: TitsThe3rdItemData(410, ItemClassification.filler),
    ItemName.miso_fish: TitsThe3rdItemData(436, ItemClassification.filler),
    ItemName.castel_castella: TitsThe3rdItemData(402, ItemClassification.filler),
    ItemName.fresh_water: TitsThe3rdItemData(411, ItemClassification.filler),
    ItemName.fishy_finale: TitsThe3rdItemData(437, ItemClassification.filler),
    ItemName.tear_balm: TitsThe3rdItemData(501, ItemClassification.filler),
    ItemName.teara_balm: TitsThe3rdItemData(502, ItemClassification.filler),
    ItemName.tearal_balm: TitsThe3rdItemData(514, ItemClassification.filler),
    ItemName.reviving_balm: TitsThe3rdItemData(508, ItemClassification.filler),
    ItemName.celestial_balm: TitsThe3rdItemData(509, ItemClassification.filler),
    ItemName.ep_charge: TitsThe3rdItemData(510, ItemClassification.filler),
    ItemName.smelling_salts: TitsThe3rdItemData(512, ItemClassification.filler),
    ItemName.insulating_tape: TitsThe3rdItemData(506, ItemClassification.filler),
    ItemName.softening_balm: TitsThe3rdItemData(505, ItemClassification.filler),
    ItemName.s_tablet: TitsThe3rdItemData(518, ItemClassification.filler),
    ItemName.purging_balm: TitsThe3rdItemData(504, ItemClassification.filler),
    ItemName.zeram_powder: TitsThe3rdItemData(517, ItemClassification.filler),
    ItemName.curia_balm: TitsThe3rdItemData(499, ItemClassification.filler),
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
    ItemName.white_bracelet_plus: TitsThe3rdItemData(361, ItemClassification.useful),
    ItemName.proxy_puppet: TitsThe3rdItemData(325, ItemClassification.useful),
    ItemName.long_barrel_2: TitsThe3rdItemData(332, ItemClassification.useful),
    ItemName.crimson_eye: TitsThe3rdItemData(394, ItemClassification.useful),
    ItemName.pearl_earring: TitsThe3rdItemData(362, ItemClassification.useful),
    ItemName.pearl_earring_plus: TitsThe3rdItemData(363, ItemClassification.useful),
    ItemName.silver_earring: TitsThe3rdItemData(350, ItemClassification.useful),
    ItemName.tiger_heart: TitsThe3rdItemData(392, ItemClassification.useful),
    ItemName.skull_pendant: TitsThe3rdItemData(368, ItemClassification.useful),
    # Weapons
    ItemName.akashic_heart: TitsThe3rdItemData(1184, ItemClassification.useful),
    ItemName.stun_gb: TitsThe3rdItemData(1274, ItemClassification.useful),
    ItemName.kumo_no_tachi: TitsThe3rdItemData(1230, ItemClassification.useful),
    ItemName.stinger_m: TitsThe3rdItemData(1139, ItemClassification.useful),
    ItemName.sting_edges: TitsThe3rdItemData(1049, ItemClassification.useful),
    ItemName.aion_bow: TitsThe3rdItemData(1365, ItemClassification.useful),
    ItemName.silvahn: TitsThe3rdItemData(1455, ItemClassification.useful),
    # Armor
    ItemName.bestia_coat: TitsThe3rdItemData(1553, ItemClassification.useful),
    ItemName.gaia_greaves: TitsThe3rdItemData(105, ItemClassification.useful),
}

quartz_table: Dict[str, TitsThe3rdItemData] = {
    ItemName.hp_1: TitsThe3rdItemData(600, ItemClassification.useful),
    ItemName.hp_2: TitsThe3rdItemData(601, ItemClassification.useful),
    ItemName.hp_3: TitsThe3rdItemData(602, ItemClassification.useful),
    ItemName.ep_1: TitsThe3rdItemData(603, ItemClassification.useful),
    ItemName.ep_2: TitsThe3rdItemData(604, ItemClassification.useful),
    ItemName.attack_1: TitsThe3rdItemData(606, ItemClassification.useful),
    ItemName.attack_2: TitsThe3rdItemData(607, ItemClassification.useful),
    ItemName.attack_3: TitsThe3rdItemData(608, ItemClassification.useful),
    ItemName.defend_1: TitsThe3rdItemData(609, ItemClassification.useful),
    ItemName.defend_2: TitsThe3rdItemData(610, ItemClassification.useful),
    ItemName.mind_1: TitsThe3rdItemData(612, ItemClassification.useful),
    ItemName.mind_2: TitsThe3rdItemData(613, ItemClassification.useful),
    ItemName.shield_1: TitsThe3rdItemData(615, ItemClassification.useful),
    ItemName.shield_2: TitsThe3rdItemData(616, ItemClassification.useful),
    ItemName.hit_1: TitsThe3rdItemData(618, ItemClassification.useful),
    ItemName.hit_2: TitsThe3rdItemData(619, ItemClassification.useful),
    ItemName.evade_1: TitsThe3rdItemData(621, ItemClassification.useful),
    ItemName.evade_2: TitsThe3rdItemData(622, ItemClassification.useful),
    ItemName.move_1: TitsThe3rdItemData(624, ItemClassification.useful),
    ItemName.action_1: TitsThe3rdItemData(627, ItemClassification.useful),
    ItemName.action_2: TitsThe3rdItemData(628, ItemClassification.useful),
    ItemName.range_1: TitsThe3rdItemData(630, ItemClassification.useful),
    ItemName.poison: TitsThe3rdItemData(637, ItemClassification.useful),
    ItemName.information: TitsThe3rdItemData(657, ItemClassification.useful),
    ItemName.cast_1: TitsThe3rdItemData(710, ItemClassification.useful),
    ItemName.cast_2: TitsThe3rdItemData(711, ItemClassification.useful),
    ItemName.ep_cut_1: TitsThe3rdItemData(712, ItemClassification.useful),
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
    ItemName.all_sepith_100_50: TitsThe3rdItemData(370000, ItemClassification.filler),
    ItemName.all_sepith_100: TitsThe3rdItemData(meta_data_table[ItemName.all_sepith_min_id].code + 100, ItemClassification.filler),
    ItemName.all_sepith_200: TitsThe3rdItemData(meta_data_table[ItemName.all_sepith_min_id].code + 200, ItemClassification.filler),
    ItemName.all_sepith_500: TitsThe3rdItemData(meta_data_table[ItemName.all_sepith_min_id].code + 500, ItemClassification.filler),
    ItemName.all_sepith_1000: TitsThe3rdItemData(meta_data_table[ItemName.all_sepith_min_id].code + 1000, ItemClassification.filler),
}

character_table: Dict[str, TitsThe3rdItemData] = {
    ItemName.kevin: TitsThe3rdItemData(meta_data_table[ItemName.character_min_id].code + 8, ItemClassification.progression),
    ItemName.ries: TitsThe3rdItemData(meta_data_table[ItemName.character_min_id].code + 14, ItemClassification.progression),
    ItemName.tita: TitsThe3rdItemData(meta_data_table[ItemName.character_min_id].code + 6, ItemClassification.progression),
    ItemName.julia: TitsThe3rdItemData(meta_data_table[ItemName.character_min_id].code + 13, ItemClassification.progression),
    ItemName.mueller: TitsThe3rdItemData(meta_data_table[ItemName.character_min_id].code + 12, ItemClassification.progression),
    ItemName.josette: TitsThe3rdItemData(meta_data_table[ItemName.character_min_id].code + 10, ItemClassification.progression),
    ItemName.joshua: TitsThe3rdItemData(meta_data_table[ItemName.character_min_id].code + 1, ItemClassification.progression),
}

area_unlock_table: Dict[str, TitsThe3rdItemData] = {  # Item ID is 200000 + flag number
    ItemName.jade_corridor_unlock_1: TitsThe3rdItemData(meta_data_table[ItemName.area_min_id].code + 256, ItemClassification.progression),
    ItemName.jade_corridor_unlock_2: TitsThe3rdItemData(meta_data_table[ItemName.area_min_id].code + 257, ItemClassification.progression),
    ItemName.jade_corridor_arseille_unlock: TitsThe3rdItemData(meta_data_table[ItemName.area_min_id].code + 258, ItemClassification.progression),
    ItemName.day_grancel_south_unlock: TitsThe3rdItemData(meta_data_table[ItemName.area_min_id].code + 259, ItemClassification.progression),
    ItemName.day_grancel_north_unlock: TitsThe3rdItemData(meta_data_table[ItemName.area_min_id].code + 260, ItemClassification.progression),
    ItemName.day_grancel_east_unlock: TitsThe3rdItemData(meta_data_table[ItemName.area_min_id].code + 261, ItemClassification.progression),
    ItemName.day_grancel_west_unlock: TitsThe3rdItemData(meta_data_table[ItemName.area_min_id].code + 262, ItemClassification.progression),
    ItemName.day_grancel_port_unlock: TitsThe3rdItemData(meta_data_table[ItemName.area_min_id].code + 270, ItemClassification.progression),
    ItemName.bobcat_unlock: TitsThe3rdItemData(meta_data_table[ItemName.area_min_id].code + 267, ItemClassification.progression),
    ItemName.night_grancel_south_unlock: TitsThe3rdItemData(meta_data_table[ItemName.area_min_id].code + 263, ItemClassification.progression),
    ItemName.night_grancel_north_unlock: TitsThe3rdItemData(meta_data_table[ItemName.area_min_id].code + 264, ItemClassification.progression),
    ItemName.night_grancel_east_unlock: TitsThe3rdItemData(meta_data_table[ItemName.area_min_id].code + 265, ItemClassification.progression),
    ItemName.night_grancel_west_unlock: TitsThe3rdItemData(meta_data_table[ItemName.area_min_id].code + 266, ItemClassification.progression),
    ItemName.night_grancel_port_unlock: TitsThe3rdItemData(meta_data_table[ItemName.area_min_id].code + 271, ItemClassification.progression),
    ItemName.grancel_arena_unlock: TitsThe3rdItemData(meta_data_table[ItemName.area_min_id].code + 269, ItemClassification.progression),
    ItemName.grancel_castle_unlock: TitsThe3rdItemData(meta_data_table[ItemName.area_min_id].code + 268, ItemClassification.progression),
    ItemName.grancel_castle_basement_unlock: TitsThe3rdItemData(meta_data_table[ItemName.area_min_id].code + 273, ItemClassification.progression),
}

craft_unlock_table: Dict[str, TitsThe3rdItemData] = { # Item ID is 400000 + character ID
    ItemName.estelle_progressive_craft: TitsThe3rdItemData(meta_data_table[ItemName.craft_min_id].code, ItemClassification.useful),
    ItemName.joshua_progressive_craft: TitsThe3rdItemData(meta_data_table[ItemName.craft_min_id].code + 1, ItemClassification.useful),
    ItemName.scherazard_progressive_craft: TitsThe3rdItemData(meta_data_table[ItemName.craft_min_id].code + 2, ItemClassification.useful),
    ItemName.olivier_progressive_craft: TitsThe3rdItemData(meta_data_table[ItemName.craft_min_id].code + 3, ItemClassification.useful),
    ItemName.kloe_progressive_craft: TitsThe3rdItemData(meta_data_table[ItemName.craft_min_id].code + 4, ItemClassification.useful),
    ItemName.agate_progressive_craft: TitsThe3rdItemData(meta_data_table[ItemName.craft_min_id].code + 5, ItemClassification.useful),
    ItemName.tita_progressive_craft: TitsThe3rdItemData(meta_data_table[ItemName.craft_min_id].code + 6, ItemClassification.useful),
    ItemName.zin_progressive_craft: TitsThe3rdItemData(meta_data_table[ItemName.craft_min_id].code + 7, ItemClassification.useful),
    ItemName.kevin_progressive_craft: TitsThe3rdItemData(meta_data_table[ItemName.craft_min_id].code + 8, ItemClassification.useful),
    ItemName.anelace_progressive_craft: TitsThe3rdItemData(meta_data_table[ItemName.craft_min_id].code + 9, ItemClassification.useful),
    ItemName.josette_progressive_craft: TitsThe3rdItemData(meta_data_table[ItemName.craft_min_id].code + 10, ItemClassification.useful),
    ItemName.richard_progressive_craft: TitsThe3rdItemData(meta_data_table[ItemName.craft_min_id].code + 11, ItemClassification.useful),
    ItemName.mueller_progressive_craft: TitsThe3rdItemData(meta_data_table[ItemName.craft_min_id].code + 12, ItemClassification.useful),
    ItemName.julia_progressive_craft: TitsThe3rdItemData(meta_data_table[ItemName.craft_min_id].code + 13, ItemClassification.useful),
    ItemName.ries_progressive_craft: TitsThe3rdItemData(meta_data_table[ItemName.craft_min_id].code + 14, ItemClassification.useful),
    ItemName.renne_progressive_craft: TitsThe3rdItemData(meta_data_table[ItemName.craft_min_id].code + 15, ItemClassification.useful),
}

key_item_table: Dict[str, TitsThe3rdItemData] = {
    ItemName.bennu_defeat: TitsThe3rdItemData(500000, ItemClassification.progression),
    ItemName.kloe_rescue: TitsThe3rdItemData(500001, ItemClassification.progression),
    ItemName.entrance_exam_results: TitsThe3rdItemData(831, ItemClassification.progression),
}


item_data_table: Dict[str, TitsThe3rdItemData] = {
    **consumable_table,
    **recipe_table,
    **equipment_table,
    **quartz_table,
    **currency_table,
    **key_item_table,
    **character_table,
    **area_unlock_table,
    **meta_data_table,
    **craft_unlock_table,
}

item_groups: Dict[str, Set[str]] = {
    "Consumables": set(consumable_table.keys()),
    "Recipes": set(recipe_table.keys()),
    "Equipment": set(equipment_table.keys()),
    "Quartz": set(quartz_table.keys()),
    "Currency": set(currency_table.keys()),
    "Characters": set(character_table.keys()),
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
default_craft_pool: Counter[str] = Counter()
# fills the pool counters according to info in location_table
# obviously ignores commented lines, just uncomment them to add them to the pools
for location in location_table:
    if location_table[location].vanilla_item != "":
        item = {location_table[location].vanilla_item: 1}
        match location_table[location].check_type:
            case CheckTypeName.chest:
                default_chest_pool.update(item)
            case CheckTypeName.character_quartz:
                default_character_quartz_pool.update(item)
            case CheckTypeName.area_unlock:
                default_item_pool.update(item)
            case CheckTypeName.craft:
                default_craft_pool.update(item)

default_character_to_location = {
    ItemName.tita: LocationName.sealing_stone_tita,
    ItemName.julia: LocationName.sealing_stone_julia,
    ItemName.mueller: LocationName.sealing_stone_mueller,
    ItemName.josette: LocationName.sealing_stone_josette,
    ItemName.joshua: LocationName.sealing_stone_joshua,
}

area_flag_to_name = {area_flag.code - meta_data_table[ItemName.area_min_id].code: area_name.replace("Area Expansion: ", "") for area_name, area_flag in area_unlock_table.items()}
character_id_to_name = {
    character_id.code - meta_data_table[ItemName.character_min_id].code: character_name.replace("Area Expansion: ", "") for character_name, character_id in character_table.items()
}
