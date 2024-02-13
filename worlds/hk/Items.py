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
    "BossEssence": lookup_type_to_names["DreamWarrior"] | lookup_type_to_names["DreamBoss"],
    "BossGeo": lookup_type_to_names["Boss_Geo"],
    "CDash": {x + "Crystal_Heart" for x in directionals},
    "Charms": lookup_type_to_names["Charm"],
    "CharmNotches": lookup_type_to_names["Notch"],
    "Claw": {x + "Mantis_Claw" for x in directionals},
    "Cloak": {x + "Mothwing_Cloak" for x in directionals} | {"Shade_Cloak", "Split_Shade_Cloak"},
    "Dive": {"Desolate_Dive", "Descending_Dark"},
    "LifebloodCocoons": lookup_type_to_names["Cocoon"],
    "Dreamers": {"Herrah", "Monomon", "Lurien"},
    "Fireball": {"Vengeful_Spirit", "Shade_Soul"},
    "GeoChests": lookup_type_to_names["Geo"],
    "GeoRocks": lookup_type_to_names["Rock"],
    "GrimmkinFlames": lookup_type_to_names["Flame"],
    "Grubs": lookup_type_to_names["Grub"],
    "JournalEntries": lookup_type_to_names["Journal"],
    "JunkPitChests": lookup_type_to_names["JunkPitChest"],
    "Keys": lookup_type_to_names["Key"],
    "LoreTablets": lookup_type_to_names["Lore"] | lookup_type_to_names["PalaceLore"],
    "Maps": lookup_type_to_names["Map"],
    "MaskShards": lookup_type_to_names["Mask"],
    "Mimics": lookup_type_to_names["Mimic"],
    "Nail": lookup_type_to_names["CursedNail"],
    "PalaceJournal": {"Journal_Entry-Seal_of_Binding"},
    "PalaceLore": lookup_type_to_names["PalaceLore"],
    "PalaceTotem": {"Soul_Totem-Palace", "Soul_Totem-Path_of_Pain"},
    "RancidEggs": lookup_type_to_names["Egg"],
    "Relics": lookup_type_to_names["Relic"],
    "Scream": {"Howling_Wraiths", "Abyss_Shriek"},
    "Skills": lookup_type_to_names["Skill"],
    "SoulTotems": lookup_type_to_names["Soul"],
    "Stags": lookup_type_to_names["Stag"],
    "VesselFragments": lookup_type_to_names["Vessel"],
    "WhisperingRoots": lookup_type_to_names["Root"],
    "WhiteFragments": {"Queen_Fragment", "King_Fragment", "Void_Heart"},
})
item_name_groups['Horizontal'] = item_name_groups['Cloak'] | item_name_groups['CDash']
item_name_groups['Vertical'] = item_name_groups['Claw'] | {'Monarch_Wings'}
