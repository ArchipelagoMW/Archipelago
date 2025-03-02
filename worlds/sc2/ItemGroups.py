import typing
from . import Items, ItemNames
from .MissionTables import campaign_mission_table, SC2Campaign, SC2Mission

"""
Item name groups, given to Archipelago and used in YAMLs and /received filtering.
For non-developers the following will be useful:
* Items with a bracket get groups named after the unbracketed part
  * eg. "Advanced Healing AI (Medivac)" is accessible as "Advanced Healing AI"
  * The exception to this are item names that would be ambiguous (eg. "Resource Efficiency")
* Item flaggroups get unique groups as well as combined groups for numbered flaggroups
  * eg. "Unit" contains all units, "Armory" contains "Armory 1" through "Armory 6"
  * The best place to look these up is at the bottom of Items.py
* Items that have a parent are grouped together
  * eg. "Zergling Items" contains all items that have "Zergling" as a parent
  * These groups do NOT contain the parent item
  * This currently does not include items with multiple potential parents, like some LotV unit upgrades
* All items are grouped by their race ("Terran", "Protoss", "Zerg", "Any")
* Hand-crafted item groups can be found at the bottom of this file
"""

item_name_groups: typing.Dict[str, typing.List[str]] = {}

# Groups for use in world logic
item_name_groups["Missions"] = ["Beat " + mission.mission_name for mission in SC2Mission]
item_name_groups["WoL Missions"] = ["Beat " + mission.mission_name for mission in campaign_mission_table[SC2Campaign.WOL]] + \
                                   ["Beat " + mission.mission_name for mission in campaign_mission_table[SC2Campaign.PROPHECY]]

# These item name groups should not show up in documentation
unlisted_item_name_groups = {
    "Missions", "WoL Missions"
}

# Some item names only differ in bracketed parts
# These items are ambiguous for short-hand name groups
bracketless_duplicates: typing.Set[str]
# This is a list of names in ItemNames with bracketed parts removed, for internal use
_shortened_names = [(name[:name.find(' (')] if '(' in name else name)
      for name in [ItemNames.__dict__[name] for name in ItemNames.__dir__() if not name.startswith('_')]]
# Remove the first instance of every short-name from the full item list
bracketless_duplicates = set(_shortened_names)
for name in bracketless_duplicates:
    _shortened_names.remove(name)
# The remaining short-names are the duplicates
bracketless_duplicates = set(_shortened_names)
del _shortened_names

# All items get sorted into their data type
for item, data in Items.get_full_item_list().items():
    # Items get assigned to their flaggroup's type
    item_name_groups.setdefault(data.type, []).append(item)
    # Numbered flaggroups get sorted into an unnumbered group
    # Currently supports numbers of one or two digits
    if data.type[-2:].strip().isnumeric():
        type_group = data.type[:-2].strip()
        item_name_groups.setdefault(type_group, []).append(item)
        # Flaggroups with numbers are unlisted
        unlisted_item_name_groups.add(data.type)
    # Items with a bracket get a short-hand name group for ease of use in YAMLs
    if '(' in item:
        short_name = item[:item.find(' (')]
        # Ambiguous short-names are dropped
        if short_name not in bracketless_duplicates:
            item_name_groups[short_name] = [item]
            # Short-name groups are unlisted
            unlisted_item_name_groups.add(short_name)
    # Items with a parent get assigned to their parent's group
    if data.parent_item:
        # The parent groups need a special name, otherwise they are ambiguous with the parent
        parent_group = f"{data.parent_item} Items"
        item_name_groups.setdefault(parent_group, []).append(item)
        # Parent groups are unlisted
        unlisted_item_name_groups.add(parent_group)
    # All items get assigned to their race's group
    race_group = data.race.name.capitalize()
    item_name_groups.setdefault(race_group, []).append(item)


# Hand-made groups
item_name_groups["Aiur"] = [
    ItemNames.ZEALOT, ItemNames.DRAGOON, ItemNames.SENTRY, ItemNames.AVENGER, ItemNames.HIGH_TEMPLAR,
    ItemNames.IMMORTAL, ItemNames.REAVER,
    ItemNames.PHOENIX, ItemNames.SCOUT, ItemNames.ARBITER, ItemNames.CARRIER,
]
item_name_groups["Nerazim"] = [
    ItemNames.CENTURION, ItemNames.STALKER, ItemNames.DARK_TEMPLAR, ItemNames.SIGNIFIER, ItemNames.DARK_ARCHON,
    ItemNames.ANNIHILATOR,
    ItemNames.CORSAIR, ItemNames.ORACLE, ItemNames.VOID_RAY,
]
item_name_groups["Tal'Darim"] = [
    ItemNames.SUPPLICANT, ItemNames.SLAYER, ItemNames.HAVOC, ItemNames.BLOOD_HUNTER, ItemNames.ASCENDANT,
    ItemNames.VANGUARD, ItemNames.WRATHWALKER,
    ItemNames.DESTROYER, ItemNames.MOTHERSHIP,
    ItemNames.WARP_PRISM_PHASE_BLASTER,
]
item_name_groups["Purifier"] = [
    ItemNames.SENTINEL, ItemNames.ADEPT, ItemNames.INSTIGATOR, ItemNames.ENERGIZER,
    ItemNames.COLOSSUS, ItemNames.DISRUPTOR,
    ItemNames.MIRAGE, ItemNames.TEMPEST,
]