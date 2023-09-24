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
    "Skills": {skill for skill in lookup_type_to_names["Skill"]},
    "Grubs": {grub for grub in lookup_type_to_names["Grub"]},
    "Mimics": {mimic for mimic in lookup_type_to_names["Mimic"]},
    "Charms": {charm for charm in lookup_type_to_names["Charm"]},
    "Relics": {relic for relic in lookup_type_to_names["Relic"]},
    "Maps": {map for map in lookup_type_to_names["Map"]},
    "Stags": {stag for stag in lookup_type_to_names["Stag"]},
    "Cocoons": {cocoon for cocoon in lookup_type_to_names["Cocoon"]},
    "Keys": {key for key in lookup_type_to_names["Key"]},
    "PalaceLore": {palace for palace in lookup_type_to_names["PalaceLore"]},
    "GeoRocks": {rock for rock in lookup_type_to_names["Rock"]},
    "GeoChests": {chest for chest in lookup_type_to_names["Geo"]},
    "JunkPitChests": {junk for junk in lookup_type_to_names["JunkPitChest"]},
    "LoreTablets": {tablet for tablet in lookup_type_to_names["Lore"]},
    "BossEssence": {essence for essence in lookup_type_to_names["DreamWarrior"]},
    "SoulTotems": {soul for soul in lookup_type_to_names["Soul"]},
    "MaskShards": {mask for mask in lookup_type_to_names["Mask"]},
    "VesselFragments": {vessel for vessel in lookup_type_to_names["Vessel"]},
    "CharmNotch": {notch for notch in lookup_type_to_names["Notch"]},
    "RancidEggs": {egg for egg in lookup_type_to_names["Egg"]},
    "WhisperingRoots": {root for root in lookup_type_to_names["Root"]},
    "GrimmkinFlames": {flame for flame in lookup_type_to_names["Flame"]},
    "JournalEntries": {journal for journal in lookup_type_to_names["Journal"]},
    "Nail": {nail for nail in lookup_type_to_names["CursedNail"]},
    "BossGeo": {boss_geo for boss_geo in lookup_type_to_names["Boss_Geo"]},
    "Dreamers": {"Herrah", "Monomon", "Lurien"},
    "Cloak": {x + "Mothwing_Cloak" for x in directionals} | {"Shade_Cloak", "Split_Shade_Cloak"},
    "Claw": {x + "Mantis_Claw" for x in directionals},
    "CDash": {x + "Crystal_Heart" for x in directionals},
    "Fragments": {"Queen_Fragment", "King_Fragment", "Void_Heart"},
})
item_name_groups["BossEssence"].update({essence for essence in lookup_type_to_names["DreamBoss"]})
item_name_groups.update({

})
item_name_groups['Horizontal'] = item_name_groups['Cloak'] | item_name_groups['CDash']
item_name_groups['Vertical'] = item_name_groups['Claw'] | {'Monarch_Wings'}
