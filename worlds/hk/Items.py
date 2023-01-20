from typing import Dict, Set, NamedTuple
from .ExtractedData import items, logic_items, item_effects

item_table = {}


class HKItemData(NamedTuple):
    advancement: bool
    id: int
    type: str


for i, (item_name, item_type) in enumerate(items.items(), start=0x1000000):
    item_table[item_name] = HKItemData(advancement=item_name in logic_items or item_name in item_effects,
                                       id=i, type=item_type)

lookup_id_to_name: Dict[int, str] = {data.id: item_name for item_name, data in item_table.items()}
lookup_type_to_names: Dict[str, Set[str]] = {}
for item, item_data in item_table.items():
    lookup_type_to_names.setdefault(item_data.type, set()).add(item)

item_name_groups = {group: lookup_type_to_names[group] for group in ("Skill", "Charm", "Mask", "Vessel",
                                                                     "Relic", "Root", "Map", "Stag", "Cocoon",
                                                                     "Soul", "DreamWarrior", "DreamBoss")}

directionals = ('', 'Left_', 'Right_')

item_name_groups.update({
    "Dreamers": {"Herrah", "Monomon", "Lurien"},
    "Cloak": {x + 'Mothwing_Cloak' for x in directionals} | {'Shade_Cloak', 'Split_Shade_Cloak'},
    "Claw": {x + 'Mantis_Claw' for x in directionals},
    "CDash": {x + 'Crystal_Heart' for x in directionals},
    "Fragments": {"Queen_Fragment", "King_Fragment", "Void_Heart"},
})
item_name_groups['Horizontal'] = item_name_groups['Cloak'] | item_name_groups['CDash']
item_name_groups['Vertical'] = item_name_groups['Claw'] | {'Monarch_Wings'}
