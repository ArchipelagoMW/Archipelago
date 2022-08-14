from typing import List, Set
import csv
import os
from functools import lru_cache

from Utils import local_path

# These items are always available at start.
always_available_items: Set[str] = {
    'Dagger',
    'Apple',
}

weapon_materials = {
    'Titanium',
    'Obsidian',
    'Gold',
    'Blood',
    'Glass',
    'Onyx',
}

bad_items = [
    'Karate Gi',
    'Boots of Pain',
    'Crown of Thorns',
    'Glass Jaw',
    'Sunglasses',
    'Ring of Pain',
    'Ring of Becoming',
    'Ring of Shadows'
]

class_str_to_id = {
    'prog': 1,
    'useful': 2,
    'junk': 0,
    'trap': 4
}

@lru_cache(maxsize=2)
def build_item_table(split_weapons=True):
    item_table = {}
    csv_path = os.path.join('worlds', 'cotnd', 'CotND_Items.csv')
    with open(local_path(csv_path)) as itemcsv:
        reader = csv.DictReader(itemcsv, delimiter=',')
        for row in reader:
            item_name = row['AP Name']
            del row['AP Name']
            row['AP Item Class'] = class_str_to_id[row['AP Item Class']]
            row['ND Name'] = [row['ND Name']] # make singleton list for processing
            row['Default'] = True if row['Default'] == 'yes' else False

            if not split_weapons and row['Type'] == 'Weapon':
                # might have to merge this with an existing weapon
                name_parts = item_name.split(maxsplit=1)
                if name_parts[0] in weapon_materials:
                    weapon_type = name_parts[1]
                    if weapon_type == 'Cat': # hardcoded silly exception for cat
                        item_table["Cat o' Nine Tails"]['ND Name'].append(row['ND Name'][0])
                    else:
                        item_table[weapon_type]['ND Name'].append(row['ND Name'][0])
                else:
                    item_table[item_name] = row
            else:
                item_table[item_name] = row
    return item_table

# Gets all non-junk items in pool
def get_normal_items(chars, dlc_packs, reduce_start, split_weapons) -> List[str]:
    # Base item pool: not Char/Junk/Trap
    items = [item for item, data in build_item_table(split_weapons).items() if (data['Type'] not in {'Character', 'Junk', 'Trap'}
        and data['DLC'] in dlc_packs
        and (reduce_start or not data['Default'])
        and item not in always_available_items)]

    # Add character unlocks
    for char in chars:
        items.append(f"Unlock {char}")

    return items
