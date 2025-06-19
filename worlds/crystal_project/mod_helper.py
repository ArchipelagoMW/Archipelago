from os import listdir, getcwd
from os.path import isfile, join
from BaseClasses import Item, ItemClassification
from typing import List
from .items import item_table, equipment_index_offset, item_index_offset, job_index_offset
import json

class ModDataModel(object):
    def __init__(self, json_data):
        self.Equipment = None
        self.Items = None
        self.Jobs = None
        self.__dict__ = json.loads(json_data)

def get_modded_items(player: int) -> List[Item]:
    items: List[Item] = []
    file_directory = get_mod_directory()
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

def get_mod_directory() -> str:
    current_directory = getcwd()
    mod_directory = join(current_directory, 'crystal_project_mods')

    return mod_directory