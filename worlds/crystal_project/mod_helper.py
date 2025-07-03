import os.path
from operator import length_hint
from os import listdir, getcwd
from os.path import isfile, join
from typing import Optional, Callable, TYPE_CHECKING, Dict
from BaseClasses import Item, ItemClassification, CollectionState
from typing import List, NamedTuple
from .options import CrystalProjectOptions
from .items import item_table, equipment_index_offset, item_index_offset, job_index_offset
from .locations import get_locations, get_shops, npc_index_offset, treasure_index_offset, crystal_index_offset, shop_index_offset
from .unused_locations import get_unused_locations
from .constants.biomes import get_region_by_id
from .rules import CrystalProjectLogic
import json

if TYPE_CHECKING:
    from . import CrystalProjectWorld

class ModLocationData(NamedTuple):
    region: str
    name: str
    code: int
    offsetless_code: int
    coordinates: str
    biomeId: int
    rule_condition: str | None

class ModDataModel(object):
    def __init__(self, json_data):
        self.ID = None
        self.Title = None
        self.System = None
        self.Equipment = None
        self.Items = None
        self.Jobs = None
        self.Entities = None
        self.__dict__ = json.loads(json_data)

class IdsExcludedFromRandomization(NamedTuple):
    excluded_equipment_ids : List[int]
    excluded_item_ids : List[int]
    excluded_job_ids : List[int]

def get_mod_titles() -> List[str]:
    titles: List[str] = []
    file_directory = get_mod_directory()

    if not os.path.isdir(file_directory):
        return titles

    only_files = [f for f in listdir(file_directory) if
                  isfile(join(file_directory, f))]

    for file_name in only_files:
        file = (open(join(file_directory, file_name)))
        file_text = file.read()
        data = ModDataModel(file_text)
        titles.append(data.Title)
        file.close()

    return titles

def get_modded_items() -> List[Item]:
    empty_player_value = -1
    items: List[Item] = []
    file_directory = get_mod_directory()

    if not os.path.isdir(file_directory):
        return items

    only_files = [f for f in listdir(file_directory) if
                  isfile(join(file_directory, f))]

    for file_name in only_files:
        file = (open(join(file_directory, file_name)))
        file_text = file.read()
        data = ModDataModel(file_text)
        excluded_ids = get_excluded_ids(data)

        for item in data.Equipment:
            item_id = item['ID'] + equipment_index_offset
            item_in_pool = any(data.code == item_id for name, data in item_table.items())
            excluded = any(equipment_id == item['ID'] for equipment_id in excluded_ids.excluded_equipment_ids)
            name = 'Equipment - ' + item['Name'] + ' - ' + str(item_id)

            if not item_in_pool and not excluded:
                mod_item = Item(name, ItemClassification.useful, item_id, empty_player_value)

                if length_hint([item for (index, item) in enumerate(items) if item.code == mod_item.code]) == 0:
                    items.append(mod_item)

        for item in data.Items:
            item_id = item['ID'] + item_index_offset
            item_in_pool = any(data.code == item_id for name, data in item_table.items())
            excluded = any(item_id == item['ID'] for item_id in excluded_ids.excluded_item_ids)
            name = 'Item - ' + item['Name'] + ' - ' + str(item_id)

            if not item_in_pool and not excluded:
                mod_item = Item(name, ItemClassification.filler, item_id, empty_player_value)

                if length_hint([item for (index, item) in enumerate(items) if item.code == mod_item.code]) == 0:
                    items.append(mod_item)

        for item in data.Jobs:
            item_id = item['ID'] + job_index_offset
            item_in_pool = any(data.code == item_id for name, data in item_table.items())
            excluded = any(job_id == item['ID'] for job_id in excluded_ids.excluded_job_ids)
            is_unselectable = False
            if 'IsUnselectableJob' in item and 'IsUnselectableSubJob' in item:
                is_unselectable = item['IsUnselectableJob'] and item['IsUnselectableSubJob']
            name = 'Job - ' + item['Name'] + ' - ' + str(item_id)

            if not item_in_pool and not is_unselectable and not excluded:
                mod_item = Item(name, ItemClassification.progression, item_id, empty_player_value)

                if length_hint([item for (index, item) in enumerate(items) if item.code == mod_item.code]) == 0:
                    items.append(mod_item)

        file.close()

    return items

def update_item_classification(item: Item, rule_condition, world: "CrystalProjectWorld") -> None:
    for condition in rule_condition:
        if condition is not None:
            loot_type = condition['Data']['LootType']
            loot_id = condition['Data']['LootValue']
        else:
            continue

        if loot_type == 1:
            archipelago_loot_id = loot_id + item_index_offset
        elif loot_type == 2:
            archipelago_loot_id = loot_id + equipment_index_offset
        else:
            continue

        if archipelago_loot_id in world.item_id_to_name:
            item_name = world.item_id_to_name[archipelago_loot_id]
            if item.name == item_name:
                item.classification = ItemClassification.progression
        else:
            continue

    return None

def get_modded_locations() -> Dict[str, ModLocationData]:
    locations: Dict[str, ModLocationData] = {}
    location_codes: List[int] = []
    file_directory = get_mod_directory()

    if not os.path.isdir(file_directory):
        return locations

    only_files = [f for f in listdir(file_directory) if
                  isfile(join(file_directory, f))]

    for file_name in only_files:
        file = (open(join(file_directory, file_name)))
        file_text = file.read()
        data = ModDataModel(file_text)
        excluded_ids = get_excluded_ids(data)

        for location in data.Entities:
            entity_type = location['EntityType']
            #Entity type 0 is NPC
            if entity_type == 0:
                location = build_npc_location(location, excluded_ids)
                if location is not None and not location.name in locations and not location.code in location_codes:
                    locations[location.name] = location
                    location_codes.append(location.code)

            #Entity type 5 is Treasure
            if entity_type == 5:
                location = build_treasure_location(location, excluded_ids)
                if location is not None and not location.name in locations and not location.code in location_codes:
                    locations[location.name] = location
                    location_codes.append(location.code)

            # Entity type 6 is Crystal
            if entity_type == 6:
                location = build_crystal_location(location, excluded_ids)
                if location is not None and not location.name in locations and not location.code in location_codes:
                    locations[location.name] = location
                    location_codes.append(location.code)

        file.close()

    return locations

def get_modded_shopsanity_locations() -> Dict[str, ModLocationData]:
    locations: Dict[str, ModLocationData] = {}

    file_directory = get_mod_directory()

    if not os.path.isdir(file_directory):
        return locations

    only_files = [f for f in listdir(file_directory) if
                  isfile(join(file_directory, f))]

    for file_name in only_files:
        file = (open(join(file_directory, file_name)))
        file_text = file.read()
        data = ModDataModel(file_text)
        excluded_ids = get_excluded_ids(data)

        for location in data.Entities:
            entity_type = location['EntityType']
            # Entity type 0 is NPC
            if entity_type == 0:
                npc_locations = build_shop_locations(location, excluded_ids)
                locations.update(npc_locations)

        file.close()

    return locations

def get_mod_directory() -> str:
    current_directory = getcwd()
    mod_directory = join(current_directory, 'crystal_project_mods')

    return mod_directory

def build_npc_location(location, excluded_ids) -> Optional[ModLocationData]:
    options: CrystalProjectOptions
    biome_id = location['BiomeID']
    region = get_region_by_id(biome_id)
    item_id = location['ID']
    id_with_offset = item_id + npc_index_offset
    name = region + ' NPC - Modded NPC ' + str(item_id)
    coord = location['Coord']
    coordinates = str(coord['X']) + ',' + str(coord['Y']) + ',' + str(coord['Z'])
    has_add_inventory = False
    rule_condition = None

    pages = location['NpcData']['Pages']
    for page in pages:
        actions = page['Actions']

        for action in actions:
            # 3 is Condition, conditions can have sub actions so check those
            if action['ActionType'] == 3:
                condition = action['Data']['Condition']
                actions_true = action['Data']['ConditionActionsTrue']
                actions_false = action['Data']['ConditionActionsFalse']

                for action_true in actions_true:
                    # 8 is Add Inventory, this means it's a check
                    if action_true['ActionType'] == 8:
                        is_excluded = is_item_at_location_excluded(action_true['Data'], excluded_ids)
                        has_add_inventory = not is_excluded

                        # Condition Type 5 is Check Inventory
                        if has_add_inventory and condition['ConditionType'] == 5 and not condition['IsNegation']:
                            rule_condition = condition

                for action_false in actions_false:
                    # 8 is Add Inventory, this means it's a check
                    if action_false['ActionType'] == 8:
                        is_excluded = is_item_at_location_excluded(action_false['Data'], excluded_ids)
                        has_add_inventory = not is_excluded

                        # Condition Type 5 is Check Inventory
                        if has_add_inventory and condition['ConditionType'] == 5 and condition['IsNegation']:
                            rule_condition = condition

            # 8 is Add Inventory, this means it's a check
            if action['ActionType'] == 8:
                is_excluded = is_item_at_location_excluded(action['Data'], excluded_ids)
                has_add_inventory = not is_excluded

    if has_add_inventory:
        location_in_pool = any(location.code == id_with_offset for location in get_locations(-1, None))
        location_unused = any(location.code == id_with_offset for location in get_unused_locations())

        if not location_in_pool and not location_unused and not coordinates == "0,0,0":
            location = ModLocationData(region, name, id_with_offset, item_id, coordinates, biome_id, rule_condition)
            return location

    return None

def build_shop_locations(location, excluded_ids) -> Dict[str, ModLocationData]:
    locations: Dict[str, ModLocationData] = {}
    location_codes: List[int] = []
    options: CrystalProjectOptions
    biome_id = location['BiomeID']
    region = get_region_by_id(biome_id)
    item_id = location['ID']
    coord = location['Coord']
    coordinates = str(coord['X']) + ',' + str(coord['Y']) + ',' + str(coord['Z'])

    pages = location['NpcData']['Pages']
    for page in pages:
        actions = page['Actions']

        for action in actions:
            # 5 is Shop, only add if shopsanity is on
            if action['ActionType'] == 5:
                stock = action['Data']['Stock']
                id_offset = 10000

                for shop_item in stock:
                    shop_item_id = item_id + id_offset
                    id_with_offset = shop_item_id + shop_index_offset
                    shop_name = region + ' Shop - Modded Shop ' + str(shop_item_id)
                    shop_item_excluded = is_item_at_location_excluded(shop_item, excluded_ids)
                    shop_item_in_pool = any(location.code == id_with_offset for location in get_shops(-1, None))

                    if not shop_item_in_pool and not shop_item_excluded:
                        condition = shop_item['Condition']
                        if condition['ConditionType'] == 5 and not condition['IsNegation']:
                            rule_condition = condition
                        else:
                            rule_condition = None

                        location = ModLocationData(region, shop_name, id_with_offset, shop_item_id, coordinates, biome_id, rule_condition)
                        if not location.name in locations and not location.code in location_codes:
                            locations[location.name] = location
                            location_codes.append(location.code)

                    id_offset += 10000

    return locations

def build_treasure_location(location, excluded_ids):
    #Chests always add an item and never have conditions, so nice and easy
    biome_id = location['BiomeID']
    region = get_region_by_id(biome_id)
    item_id = location['ID']
    id_with_offset = item_id + treasure_index_offset
    name = region + ' Chest - Modded Chest ' + str(item_id)
    coord = location['Coord']
    coordinates = str(coord['X']) + ',' + str(coord['Y']) + ',' + str(coord['Z'])
    is_excluded = is_item_at_location_excluded(location['TreasureData'], excluded_ids)

    location_in_pool = any(location.code == id_with_offset for location in get_locations(-1, None))
    location_unused = any(location.code == id_with_offset for location in get_unused_locations())

    if not location_in_pool and not location_unused and not is_excluded:
        location = ModLocationData(region, name, id_with_offset, item_id, coordinates, biome_id, None)

        return location

    return None

def build_crystal_location(location, excluded_ids):
    # Crystals always add a job and never have conditions, so nice and easy
    biome_id = location['BiomeID']
    region = get_region_by_id(biome_id)
    item_id = location['ID']
    id_with_offset = item_id + crystal_index_offset
    name = region + ' Crystal - Modded Job ' + str(item_id)
    coord = location['Coord']
    coordinates = str(coord['X']) + ',' + str(coord['Y']) + ',' + str(coord['Z'])
    job_id = location['CrystalData']['JobID']
    is_excluded = job_id in excluded_ids.excluded_job_ids

    location_in_pool = any(location.code == id_with_offset for location in get_locations(-1, None))
    location_unused = any(location.code == id_with_offset for location in get_unused_locations())

    if not location_in_pool and not location_unused and not is_excluded:
        location = ModLocationData(region, name, id_with_offset, item_id, coordinates, biome_id, None)

        return location

    return None

def build_condition_rule(condition, world: "CrystalProjectWorld") -> Optional[Callable[[CollectionState], bool]]:
    logic = CrystalProjectLogic(world.player, world.options)
    if condition is not None:
        loot_type = condition['Data']['LootType']
        loot_id = condition['Data']['LootValue']
    else:
        return lambda state: logic.has_swimming(state) and logic.has_glide(state) and logic.has_vertical_movement(state)

    if loot_type == 1:
        archipelago_loot_id = loot_id + item_index_offset
    elif loot_type == 2:
        archipelago_loot_id = loot_id + equipment_index_offset
    else:
        return lambda state: logic.has_swimming(state) and logic.has_glide(state) and logic.has_vertical_movement(state)

    if archipelago_loot_id in world.item_id_to_name:
        item_name = world.item_id_to_name[archipelago_loot_id]
        return lambda state: logic.has_swimming(state) and logic.has_glide(state) and logic.has_vertical_movement(state) and state.has(item_name, world.player)
    else:
        return lambda state: logic.has_swimming(state) and logic.has_glide(state) and logic.has_vertical_movement(state)

def get_excluded_ids(mod: ModDataModel) -> IdsExcludedFromRandomization:
    if mod.System is not None and mod.System["Randomizer"] is not None:
        excluded_item_ids = mod.System['Randomizer']['ExcludeItemIDs']
        excluded_job_ids = mod.System['Randomizer']['ExcludeJobIDs']
        excluded_equipment_ids = mod.System['Randomizer']['ExcludeEquipmentIDs']

        if excluded_item_ids is None:
            excluded_item_ids = []
        if excluded_job_ids is None:
            excluded_job_ids = []
        if excluded_equipment_ids is None:
            excluded_equipment_ids = []

        return IdsExcludedFromRandomization(excluded_equipment_ids, excluded_item_ids, excluded_job_ids)
    else:
        return IdsExcludedFromRandomization([], [], [])

def is_item_at_location_excluded(data, excluded_ids: IdsExcludedFromRandomization) -> bool:
    loot_type = data['LootType']
    item_id = data['LootValue']

    #Loot Type 1 is item and 2 is equipment
    if loot_type == 1:
        return item_id in excluded_ids.excluded_item_ids
    elif loot_type == 2:
        return item_id in excluded_ids.excluded_equipment_ids

    return False