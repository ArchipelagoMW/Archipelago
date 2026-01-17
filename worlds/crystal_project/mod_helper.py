import logging
import os.path
from os import listdir, getcwd
from os.path import isfile, join
from typing import Optional, Callable, TYPE_CHECKING
from BaseClasses import Item, ItemClassification, CollectionState
from typing import List, NamedTuple
from .options import CrystalProjectOptions
from .items import item_table, equipment_index_offset, item_index_offset, job_index_offset
from .locations import LocationData, get_treasure_and_npc_locations, get_shop_locations, get_boss_locations, npc_index_offset, treasure_index_offset, crystal_index_offset, \
    boss_index_offset, shop_index_offset, get_crystal_locations
from .home_point_locations import get_home_points
from .unused_locations import get_unused_locations
from .constants.biomes import get_display_region_by_id
from .constants.display_regions import *
from .constants.keys import *
from .constants.key_items import *
from .rules import CrystalProjectLogic
import json

if TYPE_CHECKING:
    from . import CrystalProjectWorld, home_point_location_index_offset

MAX_SUPPORTED_EDITOR_VERSION: int = 32

NPC_ENTITY_TYPE: int = 0 #Could be a boss or an npc check or a store or not a check at all
SPARK_ENTITY_TYPE: int = 2 #Could be a boss or not a boss
HOME_POINT_ENTITY_TYPE: int = 4
TREASURE_ENTITY_TYPE: int = 5
CRYSTAL_ENTITY_TYPE: int = 6

class ModDataModel(object):
    def __init__(self, json_data):
        self.ID = None
        self.Title = None
        self.EditorVersion = None
        self.System = None
        self.Equipment = None
        self.Items = None
        self.Jobs = None
        self.Entities = None
        self.Sparks = None
        self.Troops = None
        self.Monsters = None
        self.__dict__ = json.loads(json_data)

class ModLocationData(NamedTuple):
    display_region: str
    name: str
    code: int
    offsetless_code: int
    coordinates: str
    biomeId: int
    rule_condition: str | None

class ModIncrementedIdData(NamedTuple):
    original_id: int
    new_id: int
    mod_guid: str

class IdsExcludedFromRandomization(NamedTuple):
    excluded_equipment_ids : List[int]
    excluded_item_ids : List[int]
    excluded_job_ids : List[int]

class ModInfoModel(NamedTuple):
    mod_id: str
    mod_name: str
    load_order: int
    data_model: ModDataModel
    shifted_equipment_ids: List[ModIncrementedIdData]
    shifted_item_ids: List[ModIncrementedIdData]
    shifted_job_ids: List[ModIncrementedIdData]
    shifted_entity_ids: List[ModIncrementedIdData]
    shifted_spark_ids: List[ModIncrementedIdData]
    boss_troop_ids: List[int]
    excluded_ids: IdsExcludedFromRandomization

def get_mod_info() -> List[ModInfoModel]:
    data: List[ModInfoModel] = []
    file_directory = get_mod_directory()

    if not os.path.isdir(file_directory):
        return data

    only_files = [f for f in listdir(file_directory) if
                  f.endswith(".json") and isfile(join(file_directory, f))]

    equipment_ids_in_use: List[int] = [591, 592, 593, 594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610]
    item_ids_in_use: List[int] = [229, 230, 231, 232]
    job_ids_in_use: List[int] = []
    entity_ids_in_use: List[int] = [5000, 5001, 5002, 5003, 5004, 5005, 5006, 5007, 5008, 5009, 5010, 5011, 5012, 5013, 5014]
    spark_ids_in_use: List[int] = []
    order_loaded = 1

    for file_name in only_files:
        file = (open(join(file_directory, file_name)))
        file_text = file.read()
        file_data = ModDataModel(file_text)

        if file_data.EditorVersion <= MAX_SUPPORTED_EDITOR_VERSION:
            excluded_ids = get_excluded_ids(file_data)

            shifted_equipment_ids: List[ModIncrementedIdData] = []
            for item in file_data.Equipment:
                item_id = item['ID']

                #Biggest vanilla ID is 590, we only want non-vanilla items
                if item_id > 590:
                    next_id = get_next_mod_id(item_id, equipment_ids_in_use)
                    shifted_equipment_ids.append(ModIncrementedIdData(item_id, next_id, file_data.ID))
                    equipment_ids_in_use.append(next_id)

            shifted_item_ids: List[ModIncrementedIdData] = []
            for item in file_data.Items:
                item_id = item['ID']

                #Biggest vanilla ID is 228
                if item_id > 228:
                    next_id = get_next_mod_id(item_id, item_ids_in_use)
                    shifted_item_ids.append(ModIncrementedIdData(item_id, next_id, file_data.ID))
                    item_ids_in_use.append(next_id)

            shifted_job_ids: List[ModIncrementedIdData] = []
            for item in file_data.Jobs:
                item_id = item['ID']

                #Biggest vanilla ID is 23
                if item_id > 23:
                    next_id = get_next_mod_id(item_id, job_ids_in_use)
                    shifted_job_ids.append(ModIncrementedIdData(item_id, next_id, file_data.ID))
                    job_ids_in_use.append(next_id)

            shifted_entity_ids: List[ModIncrementedIdData] = []
            for item in file_data.Entities:
                item_id = item['ID']

                #Biggest vanilla ID is 4999
                if item_id > 4999:
                    next_id = get_next_mod_id(item_id, entity_ids_in_use)
                    shifted_entity_ids.append(ModIncrementedIdData(item_id, next_id, file_data.ID))
                    entity_ids_in_use.append(next_id)

            shifted_spark_ids: List[ModIncrementedIdData] = []
            for item in file_data.Sparks:
                item_id = item['ID']

                #Biggest vanilla ID is 224
                if item_id > 224:
                    next_id = get_next_mod_id(item_id, spark_ids_in_use)
                    shifted_spark_ids.append(ModIncrementedIdData(item_id, next_id, file_data.ID))
                    spark_ids_in_use.append(next_id)

            boss_monster_ids: List[int] = []
            boss_troop_ids: List[int] = []

            for monster in file_data.Monsters:
                if monster['IsBoss']:
                    boss_monster_ids.append(monster['ID'])

            for troop in file_data.Troops:
                for monster in troop['Members']:
                    if monster['MonsterID'] in boss_monster_ids:
                        boss_troop_ids.append(troop['ID'])

            data.append(ModInfoModel(file_data.ID, file_data.Title, order_loaded, file_data, shifted_equipment_ids, shifted_item_ids, shifted_job_ids, shifted_entity_ids, shifted_spark_ids, boss_troop_ids, excluded_ids))
            order_loaded = order_loaded + 1
        else:
            message = f"Mod {file_data.Title} was skipped because the editor version was {file_data.EditorVersion}. Archipelago currently only supports mods with editor version {MAX_SUPPORTED_EDITOR_VERSION} or lower."
            logging.getLogger().info(message)

        file.close()

    return data

def get_modded_items(mod_info: List[ModInfoModel]) -> List[Item]:
    empty_player_value = -1
    items: List[Item] = []

    for mod in mod_info:
        for item in mod.data_model.Equipment:
            item_id = item['ID']
            excluded = any(item_id == excluded_id for excluded_id in mod.excluded_ids.excluded_equipment_ids)

            if excluded:
                continue

            new_id = item_id
            for incremented_id in mod.shifted_equipment_ids:
                if incremented_id.original_id == item_id:
                    new_id = incremented_id.new_id

            offset_id = new_id + equipment_index_offset
            item_in_pool = any(offset_id == data.code for name, data in item_table.items())
            name = 'Equipment - ' + item['Name'] + ' - ' + str(offset_id)

            if not item_in_pool:
                mod_item = Item(name, ItemClassification.useful, offset_id, empty_player_value)
                items.append(mod_item)

        for item in mod.data_model.Items:
            item_id = item['ID']
            excluded = any(item_id == excluded_id for excluded_id in mod.excluded_ids.excluded_item_ids)

            if excluded:
                continue

            new_id = item_id
            for incremented_id in mod.shifted_item_ids:
                if incremented_id.original_id == item_id:
                    new_id = incremented_id.new_id

            offset_id = new_id + item_index_offset
            item_in_pool = any(offset_id == data.code for name, data in item_table.items())
            name = 'Item - ' + item['Name'] + ' - ' + str(offset_id)

            if not item_in_pool:
                mod_item = Item(name, ItemClassification.filler, offset_id, empty_player_value)
                items.append(mod_item)

        for item in mod.data_model.Jobs:
            item_id = item['ID']
            excluded = any(item_id == excluded_id for excluded_id in mod.excluded_ids.excluded_job_ids)

            if excluded:
                continue

            new_id = item_id
            for incremented_id in mod.shifted_job_ids:
                if incremented_id.original_id == item_id:
                    new_id = incremented_id.new_id

            offset_id = new_id + job_index_offset
            item_in_pool = any(offset_id == data.code for name, data in item_table.items())

            is_unselectable = False
            if 'IsUnselectableJob' in item and 'IsUnselectableSubJob' in item:
                is_unselectable = item['IsUnselectableJob'] and item['IsUnselectableSubJob']
            name = 'Job - ' + item['Name'] + ' - ' + str(offset_id)

            if not item_in_pool and not is_unselectable:
                mod_item = Item(name, ItemClassification.progression, offset_id, empty_player_value)
                items.append(mod_item)

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

def get_modded_locations(mod_info: List[ModInfoModel]) -> List[ModLocationData]:
    locations: List[ModLocationData] = []

    for mod in mod_info:
        for location in mod.data_model.Entities:
            entity_type = location['EntityType']
            #Entity type 0 is NPC
            if entity_type == NPC_ENTITY_TYPE:
                location = build_npc_location(location, mod.shifted_entity_ids, mod.excluded_ids)
                if location is not None:
                    locations.append(location)

            #Entity type 5 is Treasure
            if entity_type == TREASURE_ENTITY_TYPE:
                location = build_treasure_location(location, mod.shifted_entity_ids, mod.excluded_ids)
                if location is not None:
                    locations.append(location)

            # Entity type 6 is Crystal
            if entity_type == CRYSTAL_ENTITY_TYPE:
                location = build_crystal_location(location, mod.shifted_entity_ids, mod.excluded_ids)
                if location is not None:
                    locations.append(location)

    return locations

def get_modded_shopsanity_locations(mod_info: List[ModInfoModel]) -> List[ModLocationData]:
    locations: List[ModLocationData] = []

    for mod in mod_info:
        for location in mod.data_model.Entities:
            entity_type = location['EntityType']
            # Entity type 0 is NPC
            if entity_type == NPC_ENTITY_TYPE:
                code_list = [location.code for location in locations]
                npc_locations = build_shop_locations(location, mod.shifted_entity_ids, mod.excluded_ids, code_list)
                locations.extend(npc_locations)

    return locations

def get_modded_bosses(mod_info: List[ModInfoModel]) -> List[ModLocationData]:
    locations: List[ModLocationData] = []

    for mod in mod_info:
        for location in mod.data_model.Entities:
            entity_type = location['EntityType']

            #Entity type 0 is NPC
            if entity_type == NPC_ENTITY_TYPE:
                location = build_boss_npc(location, mod.boss_troop_ids, mod.shifted_entity_ids)
                if location is not None:
                    locations.append(location)

            #Entity type 2 is Spark
            if entity_type == SPARK_ENTITY_TYPE:
                location = build_spark_location(location, mod.shifted_entity_ids)
                if location is not None:
                    locations.append(location)

    return locations

def get_modded_home_points(mod_info: List[ModInfoModel]) -> List[ModLocationData]:
    locations: List[ModLocationData] = []

    for mod in mod_info:
        for location in mod.data_model.Entities:
            entity_type = location['EntityType']

            # Entity type 0 is NPC
            if entity_type == HOME_POINT_ENTITY_TYPE:
                location = build_home_point_location(location, mod.shifted_entity_ids)
                if location is not None:
                    locations.append(location)

    return locations

def get_removed_locations(mod_info: List[ModInfoModel]) -> List[LocationData]:
    removed_locations: List[LocationData] = []
    vanilla_treasures_and_npcs = get_treasure_and_npc_locations(-1, None)
    vanilla_crystals = get_crystal_locations(-1, None)
    vanilla_bosses = get_boss_locations(-1, None)
    vanilla_shops = get_shop_locations(-1, None)

    for mod in mod_info:
        for location in mod.data_model.Entities:
            location_id = location['ID']
            has_no_npc_info = location['NpcData'] is None or not location['NpcData']['Pages']
            entity_type = location['EntityType']

            treasure_id = location_id + treasure_index_offset
            npc_id = location_id + npc_index_offset
            crystal_id = location_id + crystal_index_offset
            boss_id = location_id + boss_index_offset
            shop_id = location_id + shop_index_offset

            removed_this_location: bool = False
            should_be_removed_because_no_npc_info: bool = False

            if has_no_npc_info and location['SignData'] is None and location['SparkData'] is None and location['DoorData'] is None and location['HomePointData'] is None and location['TreasureData'] is None and location['CrystalData'] is None and location['MarkerData'] is None:
                should_be_removed_because_no_npc_info = True

            for treasure_or_npc in vanilla_treasures_and_npcs:
                if (treasure_or_npc.code == treasure_id and (should_be_removed_because_no_npc_info
                    # If the item's entity type is definitely not a treasure or npc, then remove the vanilla location, because it's type was changed by the mod
                    or entity_type != TREASURE_ENTITY_TYPE)):
                    removed_locations.append(LocationData(treasure_or_npc.ap_region, treasure_or_npc.name, location_id))
                    removed_this_location = True
                    break

                if (treasure_or_npc.code == npc_id and (should_be_removed_because_no_npc_info
                    # If the item's entity type is definitely not a treasure or npc, then remove the vanilla location, because it's type was changed by the mod
                    or entity_type != NPC_ENTITY_TYPE)):
                    removed_locations.append(LocationData(treasure_or_npc.ap_region, treasure_or_npc.name, location_id))
                    removed_this_location = True
                    break

            if not removed_this_location:
                for crystal in vanilla_crystals:
                    if (crystal.code == crystal_id and (should_be_removed_because_no_npc_info
                        # If the item's entity type is definitely not a crystal, then remove the vanilla location, because it's type was changed by the mod
                        or entity_type != CRYSTAL_ENTITY_TYPE)):
                        removed_locations.append(LocationData(crystal.ap_region, crystal.name, location_id))
                        removed_this_location = True
                        break

            if not removed_this_location:
                for boss in vanilla_bosses:
                    if (boss.code == boss_id and (should_be_removed_because_no_npc_info
                        # If the item's entity type is definitely not an npc or spark, then remove the vanilla location, because it's type was changed by the mod
                        or (entity_type != NPC_ENTITY_TYPE and entity_type != SPARK_ENTITY_TYPE))):
                        removed_locations.append(LocationData(boss.ap_region, boss.name, location_id))
                        removed_this_location = True
                        break

            if not removed_this_location:
                for shop in vanilla_shops:
                    if (shop.code == shop_id and (should_be_removed_because_no_npc_info
                        # If the item's entity type is definitely not an npc, then remove the vanilla location, because it's type was changed by the mod
                        or entity_type != NPC_ENTITY_TYPE)):
                        removed_locations.append(LocationData(shop.ap_region, shop.name, location_id))
                        removed_this_location = True
                        break

    return removed_locations

def get_removed_home_points(mod_info: List[ModInfoModel]) -> List[LocationData]:
    removed_locations: List[LocationData] = []
    vanilla_home_points = get_home_points()

    for mod in mod_info:
        for location in mod.data_model.Entities:
            location_id = location['ID']
            has_no_npc_info = location['NpcData'] is None or not location['NpcData']['Pages']
            entity_type = location['EntityType']
            should_be_removed_because_no_npc_info: bool = False

            if has_no_npc_info and location['SignData'] is None and location['SparkData'] is None and location[
                'DoorData'] is None and location['HomePointData'] is None and location['TreasureData'] is None and \
                    location['CrystalData'] is None and location['MarkerData'] is None:
                should_be_removed_because_no_npc_info = True

            for home_point in vanilla_home_points:
                if (home_point.code == location_id and (should_be_removed_because_no_npc_info
                                                             # If the item's entity type is definitely not a home point, then remove the vanilla location, because it's type was changed by the mod
                                                             or entity_type != HOME_POINT_ENTITY_TYPE)):
                    removed_locations.append(LocationData(home_point.ap_region, home_point.name, location_id))
                    break

    return removed_locations

def get_mod_directory() -> str:
    current_directory = getcwd()
    mod_directory = join(current_directory, 'crystal_project_mods')

    return mod_directory

def build_npc_location(location, shifted_entity_ids: List[ModIncrementedIdData], excluded_ids: IdsExcludedFromRandomization) -> Optional[ModLocationData]:
    options: CrystalProjectOptions
    biome_id = location['BiomeID']
    display_region = get_display_region_by_id(biome_id)
    item_id = location['ID']

    new_id = item_id
    for incremented_id in shifted_entity_ids:
        if incremented_id.original_id == item_id:
            new_id = incremented_id.new_id

    id_with_offset = new_id + npc_index_offset
    name = display_region + ' NPC - Modded NPC ' + str(new_id)
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
                    # 8 is Add Inventory 74 is Add Job, this means it's a check
                    if action_true['ActionType'] == 8 or action_true['ActionType'] == 74:
                        if action_true['ActionType'] == 8:
                            is_excluded = is_item_at_location_excluded(action_true['Data'], excluded_ids)
                        else:
                            is_excluded = is_job_at_location_excluded(action_true['Data'], excluded_ids)

                        has_add_inventory = not is_excluded

                        # Condition Type 5 is Check Inventory
                        if has_add_inventory and condition['ConditionType'] == 5 and not condition['IsNegation']:
                            rule_condition = condition

                        # Condition Type 11 is Job present and 21 is Job Mastered
                        if has_add_inventory and (condition['ConditionType'] == 11 or condition['ConditionType'] == 21):
                            rule_condition = condition

                for action_false in actions_false:
                    # 8 is Add Inventory 74 is Add Job, this means it's a check
                    if action_false['ActionType'] == 8 or action_false['ActionType'] == 74:
                        if action_false['ActionType'] == 8:
                            is_excluded = is_item_at_location_excluded(action_false['Data'], excluded_ids)
                        else:
                            is_excluded = is_job_at_location_excluded(action_false['Data'], excluded_ids)

                        has_add_inventory = not is_excluded

                        # Condition Type 5 is Check Inventory
                        if has_add_inventory and condition['ConditionType'] == 5 and condition['IsNegation']:
                            rule_condition = condition

                        # Condition Type 11 is Job present and 21 is Job Mastered
                        if has_add_inventory and (condition['ConditionType'] == 11 or condition['ConditionType'] == 21):
                            rule_condition = condition

            # 8 is Add Inventory 74 is Add Job, this means it's a check
            if action['ActionType'] == 8 or action['ActionType'] == 74:
                if action['ActionType'] == 8:
                    is_excluded = is_item_at_location_excluded(action['Data'], excluded_ids)
                else:
                    is_excluded = is_job_at_location_excluded(action['Data'], excluded_ids)

                has_add_inventory = not is_excluded

    if has_add_inventory:
        location_in_pool = any(location.code == id_with_offset for location in get_treasure_and_npc_locations(-1, None))
        location_unused = any(location.code == id_with_offset for location in get_unused_locations())

        if not location_in_pool and not location_unused and not coordinates == "0,0,0":
            location = ModLocationData(display_region, name, id_with_offset, new_id, coordinates, biome_id, rule_condition)
            return location

    return None

def build_shop_locations(location, shifted_entity_ids: List[ModIncrementedIdData], excluded_ids: IdsExcludedFromRandomization, other_mod_codes) -> List[ModLocationData]:
    locations: List[ModLocationData] = []
    location_codes: List[int] = []
    options: CrystalProjectOptions
    biome_id = location['BiomeID']
    display_region = get_display_region_by_id(biome_id)
    item_id = location['ID']
    coord = location['Coord']
    coordinates = str(coord['X']) + ',' + str(coord['Y']) + ',' + str(coord['Z'])

    new_id = item_id
    for incremented_id in shifted_entity_ids:
        if incremented_id.original_id == item_id:
            new_id = incremented_id.new_id

    pages = location['NpcData']['Pages']
    for page in pages:
        actions = page['Actions']

        for action in actions:
            # 5 is Shop, only add if shopsanity is on
            if action['ActionType'] == 5:
                stock = action['Data']['Stock']
                id_offset = 10000

                for shop_item in stock:
                    shop_item_id = new_id + id_offset
                    id_with_offset = shop_item_id + shop_index_offset
                    shop_name = display_region + ' Shop - Modded Shop ' + str(shop_item_id)
                    shop_item_excluded = is_item_at_location_excluded(shop_item, excluded_ids)
                    shop_item_in_pool = any(location.code == id_with_offset for location in get_shop_locations(-1, None))

                    if not shop_item_in_pool and not shop_item_excluded:
                        condition = shop_item['Condition']
                        if condition['ConditionType'] == 5 and not condition['IsNegation']:
                            rule_condition = condition
                        else:
                            rule_condition = None

                        location = ModLocationData(display_region, shop_name, id_with_offset, shop_item_id, coordinates, biome_id, rule_condition)
                        if not location.code in location_codes and not location.code in other_mod_codes:
                            locations.append(location)
                            location_codes.append(location.code)

                    id_offset += 10000

    return locations

def build_treasure_location(location, shifted_entity_ids: List[ModIncrementedIdData], excluded_ids: IdsExcludedFromRandomization) -> Optional[ModLocationData]:
    #Chests always add an item and never have conditions, so nice and easy
    biome_id = location['BiomeID']
    display_region = get_display_region_by_id(biome_id)
    item_id = location['ID']

    new_id = item_id
    for incremented_id in shifted_entity_ids:
        if incremented_id.original_id == item_id:
            new_id = incremented_id.new_id

    id_with_offset = new_id + treasure_index_offset
    name = display_region + ' Chest - Modded Chest ' + str(new_id)
    coord = location['Coord']
    coordinates = str(coord['X']) + ',' + str(coord['Y']) + ',' + str(coord['Z'])
    is_excluded = is_item_at_location_excluded(location['TreasureData'], excluded_ids)

    location_in_pool = any(location.code == id_with_offset for location in get_treasure_and_npc_locations(-1, None))
    location_unused = any(location.code == id_with_offset for location in get_unused_locations())

    if not location_in_pool and not location_unused and not is_excluded:
        location = ModLocationData(display_region, name, id_with_offset, new_id, coordinates, biome_id, None)
        return location

    return None

def build_crystal_location(location, shifted_entity_ids: List[ModIncrementedIdData], excluded_ids: IdsExcludedFromRandomization) -> Optional[ModLocationData]:
    # Crystals always add a job and never have conditions, so nice and easy
    biome_id = location['BiomeID']
    display_region = get_display_region_by_id(biome_id)
    item_id = location['ID']

    new_id = item_id
    for incremented_id in shifted_entity_ids:
        if incremented_id.original_id == item_id:
            new_id = incremented_id.new_id

    id_with_offset = new_id + crystal_index_offset
    name = display_region + ' Crystal - Modded Job ' + str(new_id)
    coord = location['Coord']
    coordinates = str(coord['X']) + ',' + str(coord['Y']) + ',' + str(coord['Z'])
    job_id = location['CrystalData']['JobID']
    is_excluded = job_id in excluded_ids.excluded_job_ids

    location_in_pool = any(location.code == id_with_offset for location in get_crystal_locations(-1, None))
    location_unused = any(location.code == id_with_offset for location in get_unused_locations())

    if not location_in_pool and not location_unused and not is_excluded:
        location = ModLocationData(display_region, name, id_with_offset, new_id, coordinates, biome_id, None)

        return location

    return None

def build_boss_npc(location, boss_troop_ids: List[int], shifted_entity_ids: List[ModIncrementedIdData]) -> Optional[ModLocationData]:
    options: CrystalProjectOptions
    biome_id = location['BiomeID']
    display_region = get_display_region_by_id(biome_id)
    item_id = location['ID']
    troop_id = None

    new_id = item_id
    for incremented_id in shifted_entity_ids:
        if incremented_id.original_id == item_id:
            new_id = incremented_id.new_id

    id_with_offset = new_id + boss_index_offset
    name = display_region + ' Boss - Modded Boss ' + str(new_id)
    coord = location['Coord']
    coordinates = str(coord['X']) + ',' + str(coord['Y']) + ',' + str(coord['Z'])
    has_battle = False
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
                    # 27 is Battle
                    if action_true['ActionType'] == 27:
                        troop_id = action_true['Data']['TroopID']
                        has_battle = True

                        # Condition Type 5 is Check Inventory
                        if has_battle and condition['ConditionType'] == 5 and not condition['IsNegation']:
                            rule_condition = condition

                        # Condition Type 11 is Job present and 21 is Job Mastered
                        if has_battle and (condition['ConditionType'] == 11 or condition['ConditionType'] == 21):
                            rule_condition = condition

                for action_false in actions_false:
                    # 8 is Add Inventory 74 is Add Job, this means it's a check
                    if action_false['ActionType'] == 27:
                        troop_id = action_false['Data']['TroopID']
                        has_battle = True

                        # Condition Type 5 is Check Inventory
                        if has_battle and condition['ConditionType'] == 5 and condition['IsNegation']:
                            rule_condition = condition

                        # Condition Type 11 is Job present and 21 is Job Mastered
                        if has_battle and (condition['ConditionType'] == 11 or condition['ConditionType'] == 21):
                            rule_condition = condition

            # 27 is battle
            if action['ActionType'] == 27:
                troop_id = action['Data']['TroopID']
                has_battle = True

    if has_battle:
        is_boss = troop_id in boss_troop_ids
        location_in_pool = any(location.code == id_with_offset for location in get_boss_locations(-1, None))

        if is_boss and not location_in_pool:
            location = ModLocationData(display_region, name, id_with_offset, new_id, coordinates, biome_id, rule_condition)
            return location

    return None

def build_spark_location(location, shifted_entity_ids: List[ModIncrementedIdData]) -> Optional[ModLocationData]:
    if not location['SparkData']:
        return None

    is_unique = location['SparkData']['IsUnique']

    if not is_unique:
        #not a boss
        return None

    options: CrystalProjectOptions
    biome_id = location['BiomeID']
    display_region = get_display_region_by_id(biome_id)
    item_id = location['ID']

    new_id = item_id
    for incremented_id in shifted_entity_ids:
        if incremented_id.original_id == item_id:
            new_id = incremented_id.new_id

    id_with_offset = new_id + boss_index_offset
    name = display_region + ' Boss - Modded Boss ' + str(new_id)
    coord = location['Coord']
    coordinates = str(coord['X']) + ',' + str(coord['Y']) + ',' + str(coord['Z'])

    location_in_pool = any(location.code == id_with_offset for location in get_boss_locations(-1, None))

    if not location_in_pool:
        location = ModLocationData(display_region, name, id_with_offset, new_id, coordinates, biome_id, None)
        return location

    return None

def build_home_point_location(location, shifted_entity_ids: List[ModIncrementedIdData]) -> Optional[ModLocationData]:
    biome_id = location['BiomeID']
    display_region = get_display_region_by_id(biome_id)
    item_id = location['ID']
    name = location['HomePointData']['Name']

    new_id = item_id
    for incremented_id in shifted_entity_ids:
        if incremented_id.original_id == item_id:
            new_id = incremented_id.new_id

    name = 'Home Point - Modded Home Point ' + name + ' ' + str(new_id)
    coord = location['Coord']
    coordinates = str(coord['X']) + ',' + str(coord['Y']) + ',' + str(coord['Z'])

    location_in_pool = any(location.code == item_id for location in get_home_points())

    if not location_in_pool:
        location = ModLocationData(display_region, name, new_id, new_id, coordinates, biome_id, None)
        return location

    return None

def build_condition_rule(region, condition, world: "CrystalProjectWorld") -> Optional[Callable[[CollectionState], bool]]:
    logic = CrystalProjectLogic(world.player, world.options)
    job_id = None
    loot_type = None
    loot_id = None

    region_rule = build_region_specific_rules(region, world.player, logic)

    if condition is not None:
        if 'Number' in condition['Data']:
            job_id = condition['Data']['Number']

        if 'LootType' in condition['Data']:
            loot_type = condition['Data']['LootType']
            loot_id = condition['Data']['LootValue']
    else:
        return lambda state: logic.has_swimming(state) and logic.has_glide(state) and logic.has_vertical_movement(state) and region_rule

    if loot_type is None and job_id is not None:
        archipelago_loot_id = job_id + job_index_offset
    elif loot_type == 1:
        archipelago_loot_id = loot_id + item_index_offset
    elif loot_type == 2:
        archipelago_loot_id = loot_id + equipment_index_offset
    else:
        return lambda state: logic.has_swimming(state) and logic.has_glide(state) and logic.has_vertical_movement(state) and region_rule

    if archipelago_loot_id in world.item_id_to_name:
        item_name = world.item_id_to_name[archipelago_loot_id]
        return lambda state: logic.has_swimming(state) and logic.has_glide(state) and logic.has_vertical_movement(state) and state.has(item_name, world.player) and region_rule
    else:
        return lambda state: logic.has_swimming(state) and logic.has_glide(state) and logic.has_vertical_movement(state) and region_rule

def build_region_specific_rules(region, player:int, logic: CrystalProjectLogic) -> Optional[Callable[[CollectionState], bool]]:
    if region == CAPITAL_SEQUOIA_DISPLAY_NAME:
        return lambda state: logic.has_key(state, LUXURY_KEY) and state.has(PROGRESSIVE_LUXURY_PASS, player) and logic.has_key(state, GARDENERS_KEY)
    elif region == SARA_SARA_BAZAAR_DISPLAY_NAME:
        return lambda state: logic.has_key(state, ROOM_ONE_KEY)
    elif region == CAPITAL_JAIL_DISPLAY_NAME:
        return lambda state: logic.has_key(state, SOUTH_WING_KEY) and logic.has_key(state, WEST_WING_KEY) and logic.has_key(state, EAST_WING_KEY) and logic.has_key(state, DARK_WING_KEY) and logic.has_key(state, CELL_KEY, 6)
    elif region == BEAURIOR_ROCK_DISPLAY_NAME:
        return lambda state: logic.has_key(state, SMALL_KEY, 4) and logic.has_key(state, BEAURIOR_BOSS_KEY)
    elif region == SLIP_GLIDE_RIDE_DISPLAY_NAME:
        return lambda state: logic.has_key(state, RED_DOOR_KEY, 3)
    elif region == SEQUOIA_ATHENAEUM_DISPLAY_NAME:
        return lambda state: logic.has_key(state, ICE_PUZZLE_KEY, 6)
    elif region == CASTLE_RAMPARTS_DISPLAY_NAME:
        return lambda state: logic.has_key(state, RAMPART_KEY)
    else:
        return lambda state: True

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

def get_next_mod_id(base_mod_id: int, ids_in_use: List[int]) -> int:
    while base_mod_id in ids_in_use:
        base_mod_id += 1

    return base_mod_id

def is_item_at_location_excluded(data, excluded_ids: IdsExcludedFromRandomization) -> bool:
    loot_type = data['LootType']
    item_id = data['LootValue']

    #Loot Type 1 is item and 2 is equipment
    if loot_type == 1:
        return item_id in excluded_ids.excluded_item_ids
    elif loot_type == 2:
        return item_id in excluded_ids.excluded_equipment_ids

    return False

def is_job_at_location_excluded(data, excluded_ids: IdsExcludedFromRandomization) -> bool:
    job_id = data['Value']
    return job_id in excluded_ids.excluded_job_ids