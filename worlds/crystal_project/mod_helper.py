import os.path
from os import listdir, getcwd
from os.path import isfile, join
from BaseClasses import Item, ItemClassification
from typing import List
from .options import CrystalProjectOptions
from .items import item_table, equipment_index_offset, item_index_offset, job_index_offset
from .locations import LocationData, get_locations, npc_index_offset
from .constants.biomes import get_region_by_id
from .rules import CrystalProjectLogic
import json

class ModDataModel(object):
    def __init__(self, json_data):
        self.Equipment = None
        self.Items = None
        self.Jobs = None
        self.Entities = None
        self.__dict__ = json.loads(json_data)

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

        for item in data.Equipment:
            item_id = item['ID'] + equipment_index_offset
            item_in_pool = any(data.code == item_id for name, data in item_table.items())
            name = 'Equipment - ' + item['Name']

            if not item_in_pool:
                mod_item = Item(name, ItemClassification.useful, item_id, player)
                items.append(mod_item)

        for item in data.Items:
            item_id = item['ID'] + item_index_offset
            item_in_pool = any(data.code == item_id for name, data in item_table.items())
            name = 'Item - ' + item['Name']

            if not item_in_pool:
                mod_item = Item(name, ItemClassification.progression, item_id, player)
                items.append(mod_item)

        for item in data.Jobs:
            item_id = item['ID'] + job_index_offset
            item_in_pool = any(data.code == item_id for name, data in item_table.items())
            is_unselectable = item['IsUnselectableJob'] and item['IsUnselectableSubJob']
            name = 'Job - ' + item['Name']

            if not item_in_pool and not is_unselectable:
                mod_item = Item(name, ItemClassification.progression, item_id, player)
                items.append(mod_item)

    return items

def get_modded_locations(player: int, options: CrystalProjectOptions) -> List[LocationData]:
    locations: List[LocationData] = []
    file_directory = get_mod_directory()

    if not os.path.isdir(file_directory):
        return locations

    only_files = [f for f in listdir(file_directory) if
                  isfile(join(file_directory, f))]

    for file in only_files:
        file_text = open(join(file_directory, file)).read()
        data = ModDataModel(file_text)

        for location in data.Entities:
            #Entity type 0 is NPC
            if location['EntityType'] == 0:
                region = get_region_by_id(location['BiomeID'])
                name = region + ' NPC - Modded NPC'
                item_id = location['ID'] + npc_index_offset
                has_add_inventory = False

                pages = location['NpcData']['Pages']
                for page in pages:
                    actions = page['Actions']

                    for action in actions:
                        #3 is Condition, conditions can have sub actions so check those
                        if action['ActionType'] == 3:
                            condition = action['Data']['Condition']
                            actions_true = action['Data']['ConditionActionsTrue']
                            actions_false = action['Data']['ConditionActionsFalse']

                            for action_true in actions_true:
                                if action_true['ActionType'] == 8:
                                    has_add_inventory = True

                            for action_false in actions_false:
                                if action_false['ActionType'] == 8:
                                    has_add_inventory = True

                        #8 is Add Inventory, this means it's a check
                        if action['ActionType'] == 8:
                            has_add_inventory = True

                if has_add_inventory:
                    item_in_pool = any(location.code == item_id for location in get_locations(player, options))

                    if not item_in_pool:
                        rule = None
                        if not options is None:
                            #We don't know what's required to actually reach these checks, so assume worst case, it's probably less than this
                            logic = CrystalProjectLogic(player, options)
                            rule = lambda state: logic.has_swimming(state) and logic.has_glide(state) and logic.has_vertical_movement(state)

                        location = LocationData(region, name, item_id, rule)
                        locations.append(location)

    return locations

def get_mod_directory() -> str:
    current_directory = getcwd()
    mod_directory = join(current_directory, 'crystal_project_mods')

    return mod_directory