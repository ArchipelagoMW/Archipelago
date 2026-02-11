from typing import Dict, NamedTuple, Optional

from BaseClasses import Item, ItemClassification
from .Names import ItemName

gato_roboto_base_id: int = 10000

class GatoRobotoItem(Item):
    game = "Gato Roboto"
    
class GatoRobotoItemData(NamedTuple):
    code: Optional[int] = None
    type: ItemClassification = ItemClassification.filler
    
modules_item_data_table: Dict[str, GatoRobotoItemData] = {
    ItemName.module_bigshot: GatoRobotoItemData(gato_roboto_base_id + 212, ItemClassification.useful),
    ItemName.module_coolant: GatoRobotoItemData(gato_roboto_base_id + 211, ItemClassification.useful),
    ItemName.module_decoder: GatoRobotoItemData(gato_roboto_base_id + 209, ItemClassification.progression),
    ItemName.module_hopper: GatoRobotoItemData(gato_roboto_base_id + 214, ItemClassification.progression),
    ItemName.module_missile: GatoRobotoItemData(gato_roboto_base_id + 210, ItemClassification.progression),
    ItemName.module_phase: GatoRobotoItemData(gato_roboto_base_id + 216, ItemClassification.progression),
    ItemName.module_repeater: GatoRobotoItemData(gato_roboto_base_id + 213, ItemClassification.useful),
    ItemName.module_spinjump: GatoRobotoItemData(gato_roboto_base_id + 215, ItemClassification.progression)
}

healthkits_item_data_table: Dict[str, GatoRobotoItemData] = {
    ItemName.healthkit_landing_site_west: GatoRobotoItemData(gato_roboto_base_id + 16),
    ItemName.healthkit_landing_site_east: GatoRobotoItemData(gato_roboto_base_id + 17),
    ItemName.healthkit_nexus_west: GatoRobotoItemData(gato_roboto_base_id + 18,),
    ItemName.healthkit_nexus_east: GatoRobotoItemData(gato_roboto_base_id + 19),
    ItemName.healthkit_aqueducts_west: GatoRobotoItemData(gato_roboto_base_id + 20),
    ItemName.healthkit_aqueducts_east: GatoRobotoItemData(gato_roboto_base_id + 21),
    ItemName.healthkit_heater_core_west: GatoRobotoItemData(gato_roboto_base_id + 22),
    ItemName.healthkit_heater_core_east: GatoRobotoItemData(gato_roboto_base_id + 23),
    ItemName.healthkit_ventilation: GatoRobotoItemData(gato_roboto_base_id + 24),
    ItemName.healthkit_incubator: GatoRobotoItemData(gato_roboto_base_id + 25)
}

cartridges_item_data_table: Dict[str, GatoRobotoItemData] = {
    ItemName.cartridge_bark: GatoRobotoItemData(gato_roboto_base_id + 2, ItemClassification.progression),
    ItemName.cartridge_nicotine: GatoRobotoItemData(gato_roboto_base_id + 3, ItemClassification.progression),
    ItemName.cartridge_starboard: GatoRobotoItemData(gato_roboto_base_id + 4, ItemClassification.progression),
    ItemName.cartridge_coffee_stain: GatoRobotoItemData(gato_roboto_base_id + 5, ItemClassification.progression),
    ItemName.cartridge_virtual_cat: GatoRobotoItemData(gato_roboto_base_id + 6, ItemClassification.progression),
    ItemName.cartridge_port: GatoRobotoItemData(gato_roboto_base_id + 7, ItemClassification.progression),
    ItemName.cartridge_meowtrix: GatoRobotoItemData(gato_roboto_base_id + 8, ItemClassification.progression),
    ItemName.cartridge_goop: GatoRobotoItemData(gato_roboto_base_id + 9, ItemClassification.progression),
    ItemName.cartridge_urine: GatoRobotoItemData(gato_roboto_base_id + 10, ItemClassification.progression),
    ItemName.cartridge_tamagato: GatoRobotoItemData(gato_roboto_base_id + 11, ItemClassification.progression),
    ItemName.cartridge_gris: GatoRobotoItemData(gato_roboto_base_id + 12, ItemClassification.progression),
    ItemName.cartridge_chewed_gum: GatoRobotoItemData(gato_roboto_base_id + 13, ItemClassification.progression),
    ItemName.cartridge_swamp_matcha: GatoRobotoItemData(gato_roboto_base_id + 14, ItemClassification.progression),
    ItemName.cartridge_grape: GatoRobotoItemData(gato_roboto_base_id + 15, ItemClassification.progression)
}

heater_events_item_data_table: Dict[str, GatoRobotoItemData] = {
    ItemName.progressive_heater_core_1: GatoRobotoItemData(gato_roboto_base_id + 254, ItemClassification.progression),
    ItemName.progressive_heater_core_2: GatoRobotoItemData(gato_roboto_base_id + 255, ItemClassification.progression),
    ItemName.progressive_heater_core_3: GatoRobotoItemData(gato_roboto_base_id + 256, ItemClassification.progression),
}

aqueduct_events_item_data_table: Dict[str, GatoRobotoItemData] = {
    ItemName.progressive_aqueducts_1: GatoRobotoItemData(gato_roboto_base_id + 237, ItemClassification.progression),
    ItemName.progressive_aqueducts_2: GatoRobotoItemData(gato_roboto_base_id + 238, ItemClassification.progression),
    ItemName.progressive_aqueducts_3: GatoRobotoItemData(gato_roboto_base_id + 239, ItemClassification.progression),
}

vent_events_item_data_table: Dict[str, GatoRobotoItemData] = {
    ItemName.progressive_ventilation_1: GatoRobotoItemData(gato_roboto_base_id + 262, ItemClassification.progression),
    ItemName.progressive_ventilation_2: GatoRobotoItemData(gato_roboto_base_id + 263, ItemClassification.progression),
    ItemName.progressive_ventilation_3: GatoRobotoItemData(gato_roboto_base_id + 264, ItemClassification.progression),
}

victory_item_data_table: Dict[str, GatoRobotoItemData] = {
    ItemName.victory: GatoRobotoItemData(gato_roboto_base_id + 999, ItemClassification.progression_skip_balancing)
}

item_data_table: Dict[str, GatoRobotoItemData] = {
    **modules_item_data_table, 
    **cartridges_item_data_table,
    **healthkits_item_data_table,
    **heater_events_item_data_table,
    **aqueduct_events_item_data_table,
    **vent_events_item_data_table,
    **victory_item_data_table
}

item_table = {name: data.code for name, data in item_data_table.items()}