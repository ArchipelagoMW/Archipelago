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

directionals = ('', 'Left_', 'Right_')
item_name_groups = ({
    "Skills": lookup_type_to_names["Skill"],
    "Grubs": lookup_type_to_names["Grub"],
    "Mimics": lookup_type_to_names["Mimic"],
    "Charms": lookup_type_to_names["Charm"],
    "Relics": lookup_type_to_names["Relic"],
    "Maps": lookup_type_to_names["Map"],
    "Stags": lookup_type_to_names["Stag"],
    "Cocoons": lookup_type_to_names["Cocoon"],
    "Keys": lookup_type_to_names["Key"],
    "PalaceLore": lookup_type_to_names["PalaceLore"],
    "GeoRocks": lookup_type_to_names["Rock"],
    "GeoChests": lookup_type_to_names["Geo"],
    "JunkPitChests": lookup_type_to_names["JunkPitChest"],
    "LoreTablets": lookup_type_to_names["Lore"],
    "BossEssence": lookup_type_to_names["DreamWarrior"],
    "SoulTotems": lookup_type_to_names["Soul"],
    "MaskShards": lookup_type_to_names["Mask"],
    "VesselFragments": lookup_type_to_names["Vessel"],
    "CharmNotch": lookup_type_to_names["Notch"],
    "RancidEggs": lookup_type_to_names["Egg"],
    "WhisperingRoots": lookup_type_to_names["Root"],
    "GrimmkinFlames": lookup_type_to_names["Flame"],
    "JournalEntries": lookup_type_to_names["Journal"],
    "Nail": lookup_type_to_names["CursedNail"],
    "BossGeo": lookup_type_to_names["Boss_Geo"],
    "Dreamers": {"Herrah", "Monomon", "Lurien"},
    "Cloak": {x + "Mothwing_Cloak" for x in directionals} | {"Shade_Cloak", "Split_Shade_Cloak"},
    "Claw": {x + "Mantis_Claw" for x in directionals},
    "CDash": {x + "Crystal_Heart" for x in directionals},
    "Fragments": {"Queen_Fragment", "King_Fragment", "Void_Heart"},
})
item_name_groups["BossEssence"].update(lookup_type_to_names["DreamBoss"])
item_name_groups.update({

})
item_name_groups['Horizontal'] = item_name_groups['Cloak'] | item_name_groups['CDash']
item_name_groups['Vertical'] = item_name_groups['Claw'] | {'Monarch_Wings'}
