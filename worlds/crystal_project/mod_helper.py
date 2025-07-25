import logging
import os.path
from os import listdir, getcwd
from os.path import isfile, join
from typing import Optional, Callable, TYPE_CHECKING
from BaseClasses import Item, ItemClassification, CollectionState
from typing import List, NamedTuple
from .options import CrystalProjectOptions
from .items import item_table, equipment_index_offset, item_index_offset, job_index_offset
from .locations import get_locations, get_shops, get_bosses, npc_index_offset, treasure_index_offset, crystal_index_offset, boss_index_offset, shop_index_offset
from .unused_locations import get_unused_locations
from .constants.biomes import get_display_region_by_id
from .rules import CrystalProjectLogic
import json

if TYPE_CHECKING:
    from . import CrystalProjectWorld

MAX_SUPPORTED_EDITOR_VERSION: int = 30

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
    region: str
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
                  isfile(join(file_directory, f))]

    equipment_ids_in_use: List[int] = [591, 592, 593, 594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610]
    item_ids_in_use: List[int] = [229, 230, 231, 232]
    job_ids_in_use: List[int] = []
    entity_ids_in_use: List[int] = [5000, 5001, 5002, 5003]
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
            if entity_type == 0:
                location = build_npc_location(location, mod.shifted_entity_ids, mod.excluded_ids)
                if location is not None:
                    locations.append(location)

            #Entity type 5 is Treasure
            if entity_type == 5:
                location = build_treasure_location(location, mod.shifted_entity_ids, mod.excluded_ids)
                if location is not None:
                    locations.append(location)

            # Entity type 6 is Crystal
            if entity_type == 6:
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
            if entity_type == 0:
                npc_locations = build_shop_locations(location, mod.shifted_entity_ids, mod.excluded_ids)
                locations.extend(npc_locations)

    return locations

def get_modded_bosses(mod_info: List[ModInfoModel]) -> List[ModLocationData]:
    locations: List[ModLocationData] = []

    for mod in mod_info:
        for location in mod.data_model.Entities:
            entity_type = location['EntityType']

            #Entity type 0 is NPC
            if entity_type == 0:
                location = build_boss_npc(location, mod.boss_troop_ids, mod.shifted_entity_ids)
                if location is not None:
                    locations.append(location)

            #Entity type 2 is Spark
            if entity_type == 2:
                location = build_spark_location(location, mod.shifted_entity_ids)
                if location is not None:
                    locations.append(location)

    return locations

def get_removed_locations(mod_info: List[ModInfoModel]) -> List[ModLocationData]:
    removed_locations: List[ModLocationData] = []
    vanilla_locations = get_locations(-1, None)
    vanilla_bosses = get_bosses(-1, None)
    vanilla_shops = get_shops(-1, None)

    for mod in mod_info:
        for location in mod.data_model.Entities:
            location_id = location['ID']
            biome_id = location['BiomeID']
            region = get_display_region_by_id(biome_id)
            has_no_npc_info = location['NpcData'] is None or not location['NpcData']['Pages']

            if has_no_npc_info and location['SignData'] is None and location['SparkData'] is None and location['DoorData'] is None and location['HomePointData'] is None and location['TreasureData'] is None and location['CrystalData'] is None and location['MarkerData'] is None:
                treasure_id = location_id + treasure_index_offset
                npc_id = location_id + npc_index_offset
                crystal_id = location_id + crystal_index_offset
                boss_id = location_id + boss_index_offset
                shop_id = location_id + shop_index_offset

                for vanilla_location in vanilla_locations:
                    if vanilla_location.code == treasure_id:
                        removed_locations.append(ModLocationData(region, vanilla_location.name, vanilla_location.code, location_id, '0,0,0', biome_id, None))
                    if vanilla_location.code == npc_id:
                        removed_locations.append(ModLocationData(region, vanilla_location.name, vanilla_location.code, location_id, '0,0,0', biome_id, None))
                    if vanilla_location.code == crystal_id:
                        removed_locations.append(ModLocationData(region, vanilla_location.name, vanilla_location.code, location_id, '0,0,0', biome_id, None))

                for boss in vanilla_bosses:
                    if boss.code == boss_id:
                        removed_locations.append(ModLocationData(region, boss.name, boss.code, location_id, '0,0,0', biome_id, None))

                for shop in vanilla_shops:
                    if shop.code == shop_id:
                        removed_locations.append(ModLocationData(region, shop.name, shop.code, location_id, '0,0,0', biome_id, None))

    return removed_locations

def get_mod_directory() -> str:
    current_directory = getcwd()
    mod_directory = join(current_directory, 'crystal_project_mods')

    return mod_directory

def build_npc_location(location, shifted_entity_ids: List[ModIncrementedIdData], excluded_ids: IdsExcludedFromRandomization) -> Optional[ModLocationData]:
    options: CrystalProjectOptions
    biome_id = location['BiomeID']
    region = get_display_region_by_id(biome_id)
    item_id = location['ID']

    new_id = item_id
    for incremented_id in shifted_entity_ids:
        if incremented_id.original_id == item_id:
            new_id = incremented_id.new_id

    id_with_offset = new_id + npc_index_offset
    name = region + ' NPC - Modded NPC ' + str(new_id)
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
        location_in_pool = any(location.code == id_with_offset for location in get_locations(-1, None))
        location_unused = any(location.code == id_with_offset for location in get_unused_locations())

        if not location_in_pool and not location_unused and not coordinates == "0,0,0":
            location = ModLocationData(region, name, id_with_offset, new_id, coordinates, biome_id, rule_condition)
            return location

    return None

def build_shop_locations(location, shifted_entity_ids: List[ModIncrementedIdData], excluded_ids: IdsExcludedFromRandomization) -> List[ModLocationData]:
    locations: List[ModLocationData] = []
    location_codes: List[int] = []
    options: CrystalProjectOptions
    biome_id = location['BiomeID']
    region = get_display_region_by_id(biome_id)
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
                        if not location.code in location_codes:
                            locations.append(location)
                            location_codes.append(location.code)

                    id_offset += 10000

    return locations

def build_treasure_location(location, shifted_entity_ids: List[ModIncrementedIdData], excluded_ids: IdsExcludedFromRandomization) -> Optional[ModLocationData]:
    #Chests always add an item and never have conditions, so nice and easy
    biome_id = location['BiomeID']
    region = get_display_region_by_id(biome_id)
    item_id = location['ID']

    new_id = item_id
    for incremented_id in shifted_entity_ids:
        if incremented_id.original_id == item_id:
            new_id = incremented_id.new_id

    id_with_offset = new_id + treasure_index_offset
    name = region + ' Chest - Modded Chest ' + str(new_id)
    coord = location['Coord']
    coordinates = str(coord['X']) + ',' + str(coord['Y']) + ',' + str(coord['Z'])
    is_excluded = is_item_at_location_excluded(location['TreasureData'], excluded_ids)

    location_in_pool = any(location.code == id_with_offset for location in get_locations(-1, None))
    location_unused = any(location.code == id_with_offset for location in get_unused_locations())

    if not location_in_pool and not location_unused and not is_excluded:
        location = ModLocationData(region, name, id_with_offset, new_id, coordinates, biome_id, None)
        return location

    return None

def build_crystal_location(location, shifted_entity_ids: List[ModIncrementedIdData], excluded_ids: IdsExcludedFromRandomization) -> Optional[ModLocationData]:
    # Crystals always add a job and never have conditions, so nice and easy
    biome_id = location['BiomeID']
    region = get_display_region_by_id(biome_id)
    item_id = location['ID']

    new_id = item_id
    for incremented_id in shifted_entity_ids:
        if incremented_id.original_id == item_id:
            new_id = incremented_id.new_id

    id_with_offset = new_id + crystal_index_offset
    name = region + ' Crystal - Modded Job ' + str(new_id)
    coord = location['Coord']
    coordinates = str(coord['X']) + ',' + str(coord['Y']) + ',' + str(coord['Z'])
    job_id = location['CrystalData']['JobID']
    is_excluded = job_id in excluded_ids.excluded_job_ids

    location_in_pool = any(location.code == id_with_offset for location in get_locations(-1, None))
    location_unused = any(location.code == id_with_offset for location in get_unused_locations())

    if not location_in_pool and not location_unused and not is_excluded:
        location = ModLocationData(region, name, id_with_offset, new_id, coordinates, biome_id, None)

        return location

    return None

def build_boss_npc(location, boss_troop_ids: List[int], shifted_entity_ids: List[ModIncrementedIdData]) -> Optional[ModLocationData]:
    options: CrystalProjectOptions
    biome_id = location['BiomeID']
    region = get_display_region_by_id(biome_id)
    item_id = location['ID']
    troop_id = None

    new_id = item_id
    for incremented_id in shifted_entity_ids:
        if incremented_id.original_id == item_id:
            new_id = incremented_id.new_id

    id_with_offset = new_id + boss_index_offset
    name = region + ' Boss - Modded Boss ' + str(new_id)
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
        location_in_pool = any(location.code == id_with_offset for location in get_bosses(-1, None))

        if is_boss and not location_in_pool:
            location = ModLocationData(region, name, id_with_offset, new_id, coordinates, biome_id, rule_condition)
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
    region = get_display_region_by_id(biome_id)
    item_id = location['ID']

    new_id = item_id
    for incremented_id in shifted_entity_ids:
        if incremented_id.original_id == item_id:
            new_id = incremented_id.new_id

    id_with_offset = new_id + boss_index_offset
    name = region + ' Boss - Modded Boss ' + str(new_id)
    coord = location['Coord']
    coordinates = str(coord['X']) + ',' + str(coord['Y']) + ',' + str(coord['Z'])

    location_in_pool = any(location.code == id_with_offset for location in get_bosses(-1, None))

    if not location_in_pool:
        location = ModLocationData(region, name, id_with_offset, new_id, coordinates, biome_id, None)
        return location

    return None

def build_condition_rule(condition, world: "CrystalProjectWorld") -> Optional[Callable[[CollectionState], bool]]:
    logic = CrystalProjectLogic(world.player, world.options)
    job_id = None
    loot_type = None
    loot_id = None

    if condition is not None:
        if 'Number' in condition['Data']:
            job_id = condition['Data']['Number']

        if 'LootType' in condition['Data']:
            loot_type = condition['Data']['LootType']
            loot_id = condition['Data']['LootValue']
    else:
        return lambda state: logic.has_swimming(state) and logic.has_glide(state) and logic.has_vertical_movement(state)

    if loot_type is None and job_id is not None:
        archipelago_loot_id = job_id + job_index_offset
    elif loot_type == 1:
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