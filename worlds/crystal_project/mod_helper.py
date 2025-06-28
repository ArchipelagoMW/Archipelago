import os.path
from os import listdir, getcwd
from os.path import isfile, join
from typing import Optional, Callable, TYPE_CHECKING
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
    rule: Optional[Callable[[CollectionState], bool]] = None

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

    for file in only_files:
        file_text = open(join(file_directory, file)).read()
        data = ModDataModel(file_text)
        titles.append(data.Title)

    return titles

def get_modded_items(player: int) -> List[Item]:
    items: List[Item] = []
    file_directory = get_mod_directory()

    if not os.path.isdir(file_directory):
        return items

    only_files = [f for f in listdir(file_directory) if
                  isfile(join(file_directory, f))]

    for file in only_files:
        file_text = open(join(file_directory, file)).read()
        data = ModDataModel(file_text)
        excluded_ids = get_excluded_ids(data)

        for item in data.Equipment:
            item_id = item['ID'] + equipment_index_offset
            item_in_pool = any(data.code == item_id for name, data in item_table.items())
            excluded = any(equipment_id == item['ID'] for equipment_id in excluded_ids.excluded_equipment_ids)
            name = 'Equipment - ' + item['Name']

            if not item_in_pool and not excluded:
                mod_item = Item(name, ItemClassification.useful, item_id, player)
                items.append(mod_item)

        for item in data.Items:
            item_id = item['ID'] + item_index_offset
            item_in_pool = any(data.code == item_id for name, data in item_table.items())
            excluded = any(item_id == item['ID'] for item_id in excluded_ids.excluded_item_ids)
            name = 'Item - ' + item['Name']

            if not item_in_pool and not excluded:
                mod_item = Item(name, ItemClassification.progression, item_id, player)
                items.append(mod_item)

        for item in data.Jobs:
            item_id = item['ID'] + job_index_offset
            item_in_pool = any(data.code == item_id for name, data in item_table.items())
            excluded = any(job_id == item['ID'] for job_id in excluded_ids.excluded_job_ids)
            is_unselectable = item['IsUnselectableJob'] and item['IsUnselectableSubJob']
            name = 'Job - ' + item['Name']

            if not item_in_pool and not is_unselectable and not excluded:
                mod_item = Item(name, ItemClassification.progression, item_id, player)
                items.append(mod_item)

    return items

def get_modded_locations(player: int, world: "CrystalProjectWorld", options: CrystalProjectOptions) -> List[ModLocationData]:
    locations: List[ModLocationData] = []
    file_directory = get_mod_directory()

    if not os.path.isdir(file_directory):
        return locations

    only_files = [f for f in listdir(file_directory) if
                  isfile(join(file_directory, f))]

    for file in only_files:
        file_text = open(join(file_directory, file)).read()
        data = ModDataModel(file_text)
        excluded_ids = get_excluded_ids(data)

        for location in data.Entities:
            entity_type = location['EntityType']
            #Entity type 0 is NPC
            if entity_type == 0:
                location = build_npc_location(location, excluded_ids, player, world, options)
                if location is not None:
                    locations.append(location)

            #Entity type 5 is Treasure
            if entity_type == 5:
                location = build_treasure_location(location, excluded_ids, player, options)
                if location is not None:
                    locations.append(location)

            # Entity type 6 is Crystal
            if entity_type == 6:
                location = build_crystal_location(location, excluded_ids, player, options)
                if location is not None:
                    locations.append(location)

    return locations

def get_modded_shopsanity_locations(player: int, world: "CrystalProjectWorld", options: CrystalProjectOptions) -> List[ModLocationData]:
    locations: List[ModLocationData] = []

    file_directory = get_mod_directory()

    if not os.path.isdir(file_directory):
        return locations

    only_files = [f for f in listdir(file_directory) if
                  isfile(join(file_directory, f))]

    for file in only_files:
        file_text = open(join(file_directory, file)).read()
        data = ModDataModel(file_text)
        excluded_ids = get_excluded_ids(data)

        for location in data.Entities:
            entity_type = location['EntityType']
            # Entity type 0 is NPC
            if entity_type == 0:
                npc_locations = build_shop_locations(location, excluded_ids, player, world, options)
                locations.extend(npc_locations)

    return locations

def get_mod_directory() -> str:
    current_directory = getcwd()
    mod_directory = join(current_directory, 'crystal_project_mods')

    return mod_directory

def build_npc_location(location, excluded_ids, player: int, world: "CrystalProjectWorld", options: CrystalProjectOptions) -> Optional[ModLocationData]:
    biome_id = location['BiomeID']
    region = get_region_by_id(biome_id)
    item_id = location['ID']
    id_with_offset = item_id + npc_index_offset
    name = region + ' NPC - Modded NPC ' + str(item_id)
    coord = location['Coord']
    coordinates = str(coord['X']) + ',' + str(coord['Y']) + ',' + str(coord['Z'])
    has_add_inventory = False
    condition_rule = None

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
                            condition_rule = build_condition_rule(condition, world, player, options)

                for action_false in actions_false:
                    # 8 is Add Inventory, this means it's a check
                    if action_false['ActionType'] == 8:
                        is_excluded = is_item_at_location_excluded(action_false['Data'], excluded_ids)
                        has_add_inventory = not is_excluded

                        # Condition Type 5 is Check Inventory
                        if has_add_inventory and condition['ConditionType'] == 5 and condition['IsNegation']:
                            condition_rule = build_condition_rule(condition, world, player, options)

            # 8 is Add Inventory, this means it's a check
            if action['ActionType'] == 8:
                is_excluded = is_item_at_location_excluded(action['Data'], excluded_ids)
                has_add_inventory = not is_excluded

    if has_add_inventory:
        location_in_pool = any(location.code == id_with_offset for location in get_locations(player, options))
        location_unused = any(location.code == id_with_offset for location in get_unused_locations())

        if not location_in_pool and not location_unused:
            if not options is None:
                logic = CrystalProjectLogic(player, options)

                if condition_rule is None:
                    # We don't know what's required to actually reach these checks, so assume worst case, it's probably less than this
                    condition_rule = lambda state: logic.has_swimming(state) and logic.has_glide(state) and logic.has_vertical_movement(state)

            location = ModLocationData(region, name, id_with_offset, item_id, coordinates, biome_id, condition_rule)
            return location

    return None

def build_shop_locations(location, excluded_ids, player: int, world: "CrystalProjectWorld", options: CrystalProjectOptions) -> List[ModLocationData]:
    logic = CrystalProjectLogic(player, options)
    locations: List[ModLocationData] = []
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
                    shop_item_in_pool = any(location.code == id_with_offset for location in get_shops(player, options))

                    if not shop_item_in_pool and not shop_item_excluded:
                        condition = shop_item['Condition']
                        if condition['ConditionType'] == 5 and not condition['IsNegation']:
                            condition_rule = build_condition_rule(condition, world, player, options)
                        else:
                            condition_rule = lambda state: logic.has_swimming(state) and logic.has_glide(state) and logic.has_vertical_movement(state)

                        location = ModLocationData(region, shop_name, id_with_offset, shop_item_id, coordinates, biome_id, condition_rule)
                        locations.append(location)

                    id_offset += 10000

    return locations

def build_treasure_location(location, excluded_ids, player, options):
    #Chests always add an item and never have conditions, so nice and easy
    biome_id = location['BiomeID']
    region = get_region_by_id(biome_id)
    item_id = location['ID']
    id_with_offset = item_id + treasure_index_offset
    name = region + ' Chest - Modded Chest ' + str(item_id)
    coord = location['Coord']
    coordinates = str(coord['X']) + ',' + str(coord['Y']) + ',' + str(coord['Z'])
    is_excluded = is_item_at_location_excluded(location['TreasureData'], excluded_ids)

    location_in_pool = any(location.code == id_with_offset for location in get_locations(player, options))
    location_unused = any(location.code == id_with_offset for location in get_unused_locations())

    if not location_in_pool and not location_unused and not is_excluded:
        logic = CrystalProjectLogic(player, options)
        condition_rule = lambda state: logic.has_swimming(state) and logic.has_glide(state) and logic.has_vertical_movement(state)
        location = ModLocationData(region, name, id_with_offset, item_id, coordinates, biome_id, condition_rule)

        return location

    return None

def build_crystal_location(location, excluded_ids, player, options):
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

    location_in_pool = any(location.code == id_with_offset for location in get_locations(player, options))
    location_unused = any(location.code == id_with_offset for location in get_unused_locations())

    if not location_in_pool and not location_unused and not is_excluded:
        logic = CrystalProjectLogic(player, options)
        condition_rule = lambda state: logic.has_swimming(state) and logic.has_glide(state) and logic.has_vertical_movement(state)
        location = ModLocationData(region, name, id_with_offset, item_id, coordinates, biome_id, condition_rule)

        return location

    return None

def build_condition_rule(condition, world: "CrystalProjectWorld", player: int, options: CrystalProjectOptions) -> Optional[Callable[[CollectionState], bool]]:
    logic = CrystalProjectLogic(player, options)
    loot_type = condition['Data']['LootType']
    loot_id = condition['Data']['LootValue']
    archipelago_loot_id = None

    if loot_type == 1:
        archipelago_loot_id = loot_id + item_index_offset
    elif loot_type == 2:
        archipelago_loot_id = loot_id + equipment_index_offset
    else:
        return lambda state: logic.has_swimming(state) and logic.has_glide(state) and logic.has_vertical_movement(state)

    if archipelago_loot_id in world.item_id_to_name:
        item_name = world.item_id_to_name[archipelago_loot_id]
        return lambda state: logic.has_swimming(state) and logic.has_glide(state) and logic.has_vertical_movement(state) and state.has(item_name, player)
    else:
        return lambda state: logic.has_swimming(state) and logic.has_glide(state) and logic.has_vertical_movement(state)

def get_excluded_ids(mod: ModDataModel) -> IdsExcludedFromRandomization:
    excluded_item_ids = mod.System['Randomizer']['ExcludeItemIDs']
    excluded_job_ids = mod.System['Randomizer']['ExcludeJobIDs']
    excluded_equipment_ids = mod.System['Randomizer']['ExcludeEquipmentIDs']

    return IdsExcludedFromRandomization(excluded_equipment_ids, excluded_item_ids, excluded_job_ids)

def is_item_at_location_excluded(data, excluded_ids: IdsExcludedFromRandomization) -> bool:
    loot_type = data['LootType']
    item_id = data['LootValue']

    #Loot Type 1 is item and 2 is equipment
    if loot_type == 1:
        return item_id in excluded_ids.excluded_item_ids
    elif loot_type == 2:
        return item_id in excluded_ids.excluded_equipment_ids

    return False