import typing
from . import Items, ItemNames
from .MissionTables import campaign_mission_table, SC2Campaign, SC2Mission, SC2Race

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
    "Missions", "WoL Missions",
    Items.TerranItemType.Progressive.display_name,
    Items.TerranItemType.Nova_Gear.display_name,
    Items.TerranItemType.Mercenary.display_name,
    Items.ZergItemType.Ability.display_name,
    Items.ZergItemType.Morph.display_name,
    Items.ZergItemType.Strain.display_name,
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
    # Items get assigned to their flaggroup's display type
    item_name_groups.setdefault(data.type.display_name, []).append(item)
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
class ItemGroupNames:
    TERRAN_ITEMS = "Terran Items"
    """All Terran items"""
    TERRAN_UNITS = "Terran Units"
    TERRAN_GENERIC_UPGRADES = "Terran Generic Upgrades"
    """+attack/armour upgrades"""
    BARRACKS_UNITS = "Barracks Units"
    FACTORY_UNITS = "Factory Units"
    STARPORT_UNITS = "Starport Units"
    WOL_UNITS = "WoL Units"
    WOL_MERCS = "WoL Mercenaries"
    WOL_BUILDINGS = "WoL Buildings"
    WOL_UPGRADES = "WoL Upgrades"
    WOL_ITEMS = "WoL Items"
    """All items from vanilla WoL. Note some items are progressive where level 2 is not vanilla."""
    NCO_UNITS = "NCO Units"
    NCO_BUILDINGS = "NCO Buildings"
    NCO_UNIT_TECHNOLOGY = "NCO Unit Technology"
    NCO_BASELINE_UPGRADES = "NCO Baseline Upgrades"
    NCO_UPGRADES = "NCO Upgrades"
    NOVA_EQUIPMENT = "Nova Equipment"
    NCO_MAX_PROGRESSIVE_ITEMS = "NCO +Items"
    """NCO item groups that should be set to maximum progressive amounts"""
    NCO_MIN_PROGRESSIVE_ITEMS = "NCO -Items"
    """NCO item groups that should be set to minimum progressive amounts (1)"""
    TERRAN_BUILDINGS = "Terran Buildings"
    TERRAN_MERCENARIES = "Terran Mercenaries"
    TERRAN_STIMPACKS = "Terran Stimpacks"
    TERRAN_PROGRESSIVE_UPGRADES = "Terran Progressive Upgrades"
    TERRAN_ORIGINAL_PROGRESSIVE_UPGRADES = "Terran Original Progressive Upgrades"
    """Progressive items where level 1 appeared in WoL"""

    ZERG_ITEMS = "Zerg Items"
    ZERG_UNITS = "Zerg Units"
    ZERG_GENERIC_UPGRADES = "Zerg Generic Upgrades"
    """+attack/armour upgrades"""
    HOTS_UNITS = "HotS Units"
    HOTS_STRAINS = "HotS Strains"
    """Vanilla HotS strains (the upgrades you play a mini-mission for)"""
    HOTS_MUTATIONS = "HotS Mutations"
    """Vanilla HotS Mutations (basic toggleable unit upgrades)"""
    HOTS_GLOBAL_UPGRADES = "HotS Global Upgrades"
    HOTS_MORPHS = "HotS Morphs"
    KERRIGAN_ABILITIES = "Kerrigan Abilities"
    KERRIGAN_PASSIVES = "Kerrigan Passives"
    HOTS_ITEMS = "HotS Items"
    """All items from vanilla HotS"""
    ZERG_MORPHS = "Zerg Morphs"
    ZERG_MERCS = "Zerg Mercenaries"
    ZERG_BUILDINGS = "Zerg Buildings"

    PROTOSS_ITEMS = "Protoss Items"
    PROTOSS_UNITS = "Protoss Units"
    PROTOSS_GENERIC_UPGRADES = "Protoss Generic Upgrades"
    """+attack/armour upgrades"""
    GATEWAY_UNITS = "Gateway Units"
    ROBO_UNITS = "Robo Units"
    STARGATE_UNITS = "Stargate Units"
    PROPHECY_UNITS = "Prophecy Units"
    PROPHECY_BUILDINGS = "Prophecy Buildings"
    LOTV_UNITS = "LotV Units"
    LOTV_ITEMS = "LotV Items"
    LOTV_GLOBAL_UPGRADES = "LotV Global Upgrades"
    SOA_ITEMS = "SOA"
    PROTOSS_GLOBAL_UPGRADES = "Protoss Global Upgrades"
    PROTOSS_BUILDINGS = "Protoss Buildings"
    AIUR_UNITS = "Aiur"
    NERAZIM_UNITS = "Nerazim"
    TAL_DARIM_UNITS = "Tal'Darim"
    PURIFIER_UNITS = "Purifier"

    VANILLA_ITEMS = "Vanilla Items"


# Terran
item_name_groups[ItemGroupNames.TERRAN_ITEMS] = terran_items = [
    item_name for item_name, item_data in Items.item_table.items()
    if item_data.race == SC2Race.TERRAN
]
item_name_groups[ItemGroupNames.TERRAN_UNITS] = terran_units = [
    item_name for item_name, item_data in Items.item_table.items()
    if item_data.type in (Items.TerranItemType.Unit, Items.TerranItemType.Mercenary)
]
item_name_groups[ItemGroupNames.TERRAN_GENERIC_UPGRADES] = terran_generic_upgrades = [
    item_name for item_name, item_data in Items.item_table.items()
    if item_data.type == Items.TerranItemType.Upgrade
]
item_name_groups[ItemGroupNames.BARRACKS_UNITS] = barracks_units = [
    ItemNames.MARINE, ItemNames.MEDIC, ItemNames.FIREBAT, ItemNames.MARAUDER,
    ItemNames.REAPER, ItemNames.GHOST, ItemNames.SPECTRE, ItemNames.HERC,
]
item_name_groups[ItemGroupNames.FACTORY_UNITS] = factory_units = [
    ItemNames.HELLION, ItemNames.VULTURE, ItemNames.GOLIATH, ItemNames.DIAMONDBACK,
    ItemNames.SIEGE_TANK, ItemNames.THOR, ItemNames.PREDATOR, ItemNames.WIDOW_MINE,
    ItemNames.CYCLONE, ItemNames.WARHOUND,
]
item_name_groups[ItemGroupNames.STARPORT_UNITS] = starport_units = [
    ItemNames.MEDIVAC, ItemNames.WRAITH, ItemNames.VIKING, ItemNames.BANSHEE,
    ItemNames.BATTLECRUISER, ItemNames.HERCULES, ItemNames.SCIENCE_VESSEL, ItemNames.RAVEN,
    ItemNames.LIBERATOR, ItemNames.VALKYRIE,
]
item_name_groups[ItemGroupNames.TERRAN_BUILDINGS] = terran_buildings = [
    item_name for item_name, item_data in Items.item_table.items()
    if item_data.type == Items.TerranItemType.Building
]
item_name_groups[ItemGroupNames.TERRAN_MERCENARIES] = terran_mercenaries = [
    item_name for item_name, item_data in Items.item_table.items()
    if item_data.type == Items.TerranItemType.Mercenary
]
item_name_groups[ItemGroupNames.NCO_UNITS] = nco_units = [
    ItemNames.MARINE, ItemNames.MARAUDER, ItemNames.REAPER,
    ItemNames.HELLION, ItemNames.GOLIATH, ItemNames.SIEGE_TANK,
    ItemNames.RAVEN, ItemNames.LIBERATOR, ItemNames.BANSHEE, ItemNames.BATTLECRUISER,
    ItemNames.HERC,  # From that one bonus objective in mission 5
]
item_name_groups[ItemGroupNames.NCO_BUILDINGS] = nco_buildings = [
    ItemNames.BUNKER, ItemNames.MISSILE_TURRET, ItemNames.PLANETARY_FORTRESS,
]
item_name_groups[ItemGroupNames.NOVA_EQUIPMENT] = nova_equipment = [
    *[item_name for item_name, item_data in Items.item_table.items()
        if item_data.type == Items.TerranItemType.Nova_Gear],
    ItemNames.NOVA_PROGRESSIVE_STEALTH_SUIT_MODULE,
]
item_name_groups[ItemGroupNames.WOL_UNITS] = wol_units = [
    ItemNames.MARINE, ItemNames.MEDIC, ItemNames.FIREBAT, ItemNames.MARAUDER, ItemNames.REAPER,
    ItemNames.HELLION, ItemNames.VULTURE, ItemNames.GOLIATH,  ItemNames.DIAMONDBACK, ItemNames.SIEGE_TANK,
    ItemNames.MEDIVAC, ItemNames.WRAITH, ItemNames.VIKING, ItemNames.BANSHEE, ItemNames.BATTLECRUISER,
    ItemNames.GHOST, ItemNames.SPECTRE, ItemNames.THOR,
    ItemNames.PREDATOR, ItemNames.HERCULES,
    ItemNames.SCIENCE_VESSEL, ItemNames.RAVEN,
]
item_name_groups[ItemGroupNames.WOL_MERCS] = wol_mercs = [
    ItemNames.WAR_PIGS, ItemNames.DEVIL_DOGS, ItemNames.HAMMER_SECURITIES,
    ItemNames.SPARTAN_COMPANY, ItemNames.SIEGE_BREAKERS,
    ItemNames.HELS_ANGELS, ItemNames.DUSK_WINGS, ItemNames.JACKSONS_REVENGE,
]
item_name_groups[ItemGroupNames.WOL_BUILDINGS] = wol_buildings = [
    ItemNames.BUNKER, ItemNames.SENSOR_TOWER, ItemNames.PROGRESSIVE_ORBITAL_COMMAND,
    ItemNames.PERDITION_TURRET, ItemNames.PLANETARY_FORTRESS,
    ItemNames.HIVE_MIND_EMULATOR, ItemNames.PSI_DISRUPTER,
]

# Terran Upgrades
item_name_groups[ItemGroupNames.WOL_UPGRADES] = wol_upgrades = [
    # Armory Base
    ItemNames.BUNKER_PROJECTILE_ACCELERATOR, ItemNames.BUNKER_NEOSTEEL_BUNKER,
    ItemNames.MISSILE_TURRET_TITANIUM_HOUSING, ItemNames.MISSILE_TURRET_HELLSTORM_BATTERIES,
    ItemNames.SCV_ADVANCED_CONSTRUCTION, ItemNames.SCV_DUAL_FUSION_WELDERS,
    ItemNames.PROGRESSIVE_FIRE_SUPPRESSION_SYSTEM, ItemNames.PROGRESSIVE_ORBITAL_COMMAND,
    # Armory Infantry
    ItemNames.MARINE_PROGRESSIVE_STIMPACK, ItemNames.MARINE_COMBAT_SHIELD,
    ItemNames.MEDIC_ADVANCED_MEDIC_FACILITIES, ItemNames.MEDIC_STABILIZER_MEDPACKS,
    ItemNames.FIREBAT_INCINERATOR_GAUNTLETS, ItemNames.FIREBAT_JUGGERNAUT_PLATING,
    ItemNames.MARAUDER_CONCUSSIVE_SHELLS, ItemNames.MARAUDER_KINETIC_FOAM,
    ItemNames.REAPER_U238_ROUNDS, ItemNames.REAPER_G4_CLUSTERBOMB,
    # Armory Vehicles
    ItemNames.HELLION_TWIN_LINKED_FLAMETHROWER, ItemNames.HELLION_THERMITE_FILAMENTS,
    ItemNames.SPIDER_MINE_CERBERUS_MINE, ItemNames.VULTURE_PROGRESSIVE_REPLENISHABLE_MAGAZINE,
    ItemNames.GOLIATH_MULTI_LOCK_WEAPONS_SYSTEM, ItemNames.GOLIATH_ARES_CLASS_TARGETING_SYSTEM,
    ItemNames.DIAMONDBACK_PROGRESSIVE_TRI_LITHIUM_POWER_CELL, ItemNames.DIAMONDBACK_SHAPED_HULL,
    ItemNames.SIEGE_TANK_MAELSTROM_ROUNDS, ItemNames.SIEGE_TANK_SHAPED_BLAST,
    # Armory Starships
    ItemNames.MEDIVAC_RAPID_DEPLOYMENT_TUBE, ItemNames.MEDIVAC_ADVANCED_HEALING_AI,
    ItemNames.WRAITH_PROGRESSIVE_TOMAHAWK_POWER_CELLS, ItemNames.WRAITH_DISPLACEMENT_FIELD,
    ItemNames.VIKING_RIPWAVE_MISSILES, ItemNames.VIKING_PHOBOS_CLASS_WEAPONS_SYSTEM,
    ItemNames.BANSHEE_PROGRESSIVE_CROSS_SPECTRUM_DAMPENERS, ItemNames.BANSHEE_SHOCKWAVE_MISSILE_BATTERY,
    ItemNames.BATTLECRUISER_PROGRESSIVE_MISSILE_PODS, ItemNames.BATTLECRUISER_PROGRESSIVE_DEFENSIVE_MATRIX,
    # Armory Dominion
    ItemNames.GHOST_OCULAR_IMPLANTS, ItemNames.GHOST_CRIUS_SUIT,
    ItemNames.SPECTRE_PSIONIC_LASH, ItemNames.SPECTRE_NYX_CLASS_CLOAKING_MODULE,
    ItemNames.THOR_330MM_BARRAGE_CANNON, ItemNames.THOR_PROGRESSIVE_IMMORTALITY_PROTOCOL,
    # Lab Zerg
    ItemNames.BUNKER_FORTIFIED_BUNKER, ItemNames.BUNKER_SHRIKE_TURRET,
    ItemNames.PROGRESSIVE_REGENERATIVE_BIO_STEEL, ItemNames.CELLULAR_REACTOR,
    # Other 3 levels are units/buildings (Perdition, PF, Hercules, Predator, HME, Psi Disrupter)
    # Lab Protoss
    ItemNames.VANADIUM_PLATING, ItemNames.ULTRA_CAPACITORS,
    ItemNames.AUTOMATED_REFINERY, ItemNames.MICRO_FILTERING,
    ItemNames.ORBITAL_DEPOTS, ItemNames.COMMAND_CENTER_REACTOR,
    ItemNames.ORBITAL_STRIKE, ItemNames.TECH_REACTOR,
    # Other level is units (Raven, Science Vessel)
]
item_name_groups[ItemGroupNames.TERRAN_STIMPACKS] = terran_stimpacks = [
    ItemNames.MARINE_PROGRESSIVE_STIMPACK,
    ItemNames.MARAUDER_PROGRESSIVE_STIMPACK,
    ItemNames.REAPER_PROGRESSIVE_STIMPACK,
    ItemNames.FIREBAT_PROGRESSIVE_STIMPACK,
    ItemNames.HELLION_PROGRESSIVE_STIMPACK,
]
item_name_groups[ItemGroupNames.TERRAN_ORIGINAL_PROGRESSIVE_UPGRADES] = terran_original_progressive_upgrades = [
    ItemNames.PROGRESSIVE_FIRE_SUPPRESSION_SYSTEM,
    ItemNames.PROGRESSIVE_ORBITAL_COMMAND,
    ItemNames.MARINE_PROGRESSIVE_STIMPACK,
    ItemNames.VULTURE_PROGRESSIVE_REPLENISHABLE_MAGAZINE,
    ItemNames.DIAMONDBACK_PROGRESSIVE_TRI_LITHIUM_POWER_CELL,
    ItemNames.WRAITH_PROGRESSIVE_TOMAHAWK_POWER_CELLS,
    ItemNames.BANSHEE_PROGRESSIVE_CROSS_SPECTRUM_DAMPENERS,
    ItemNames.BATTLECRUISER_PROGRESSIVE_MISSILE_PODS,
    ItemNames.BATTLECRUISER_PROGRESSIVE_DEFENSIVE_MATRIX,
    ItemNames.THOR_PROGRESSIVE_IMMORTALITY_PROTOCOL,
    ItemNames.PROGRESSIVE_REGENERATIVE_BIO_STEEL,
]
item_name_groups[ItemGroupNames.NCO_BASELINE_UPGRADES] = nco_baseline_upgrades = [
    ItemNames.BUNKER_NEOSTEEL_BUNKER,  # Baseline from mission 2
    ItemNames.BUNKER_FORTIFIED_BUNKER,  # Baseline from mission 2
    ItemNames.MARINE_COMBAT_SHIELD,   # Baseline from mission 2
    ItemNames.MARAUDER_KINETIC_FOAM,  # Baseline outside WOL
    ItemNames.MARAUDER_CONCUSSIVE_SHELLS,  # Baseline from mission 2
    ItemNames.HELLION_HELLBAT_ASPECT,  # Baseline from mission 3
    ItemNames.GOLIATH_INTERNAL_TECH_MODULE,  # Baseline from mission 4
    ItemNames.GOLIATH_SHAPED_HULL,
    # ItemNames.GOLIATH_RESOURCE_EFFICIENCY,  # Supply savings baseline in NCO, mineral savings is non-NCO
    ItemNames.SIEGE_TANK_SHAPED_HULL,  # Baseline NCO gives +10; this upgrade gives +25
    ItemNames.SIEGE_TANK_SHAPED_BLAST,  # Baseline from mission 3
    ItemNames.LIBERATOR_RAID_ARTILLERY,  # Baseline in mission 5
    ItemNames.RAVEN_BIO_MECHANICAL_REPAIR_DRONE,  # Baseline in mission 5
    ItemNames.BATTLECRUISER_TACTICAL_JUMP,
    ItemNames.BATTLECRUISER_COVERT_OPS_ENGINES,
    ItemNames.PROGRESSIVE_ORBITAL_COMMAND,  # Can be upgraded from mission 2
    ItemNames.PROGRESSIVE_FIRE_SUPPRESSION_SYSTEM,  # Baseline from mission 2
    ItemNames.ORBITAL_DEPOTS,  # Baseline from mission 2
] + nco_buildings
item_name_groups[ItemGroupNames.NCO_UNIT_TECHNOLOGY] = nco_unit_technology = [
    ItemNames.MARINE_LASER_TARGETING_SYSTEM,
    ItemNames.MARINE_PROGRESSIVE_STIMPACK,
    ItemNames.MARINE_MAGRAIL_MUNITIONS,
    ItemNames.MARINE_OPTIMIZED_LOGISTICS,
    ItemNames.MARAUDER_LASER_TARGETING_SYSTEM,
    ItemNames.MARAUDER_INTERNAL_TECH_MODULE,
    ItemNames.MARAUDER_PROGRESSIVE_STIMPACK,
    ItemNames.MARAUDER_MAGRAIL_MUNITIONS,
    ItemNames.REAPER_SPIDER_MINES,
    ItemNames.REAPER_LASER_TARGETING_SYSTEM,
    ItemNames.REAPER_PROGRESSIVE_STIMPACK,
    ItemNames.REAPER_ADVANCED_CLOAKING_FIELD,
    # Reaper special ordnance gives anti-building attack, which is baseline in AP
    ItemNames.HELLION_JUMP_JETS,
    ItemNames.HELLION_PROGRESSIVE_STIMPACK,
    ItemNames.HELLION_SMART_SERVOS,
    ItemNames.HELLION_OPTIMIZED_LOGISTICS,
    ItemNames.HELLION_THERMITE_FILAMENTS,  # Called Infernal Pre-Igniter in NCO
    ItemNames.GOLIATH_ARES_CLASS_TARGETING_SYSTEM,  # Called Laser Targeting System in NCO
    ItemNames.GOLIATH_JUMP_JETS,
    ItemNames.GOLIATH_OPTIMIZED_LOGISTICS,
    ItemNames.GOLIATH_MULTI_LOCK_WEAPONS_SYSTEM,
    ItemNames.SIEGE_TANK_SPIDER_MINES, ItemNames.SIEGE_TANK_JUMP_JETS,
    ItemNames.SIEGE_TANK_INTERNAL_TECH_MODULE, ItemNames.SIEGE_TANK_SMART_SERVOS,
    # Tanks can't get Laser targeting system in NCO
    ItemNames.BANSHEE_INTERNAL_TECH_MODULE,
    ItemNames.BANSHEE_PROGRESSIVE_CROSS_SPECTRUM_DAMPENERS,
    ItemNames.BANSHEE_SHOCKWAVE_MISSILE_BATTERY,  # Banshee Special Ordnance
    # Banshees can't get laser targeting systems in NCO
    ItemNames.LIBERATOR_CLOAK,
    ItemNames.LIBERATOR_SMART_SERVOS,
    ItemNames.LIBERATOR_OPTIMIZED_LOGISTICS,
    # Liberators can't get laser targeting system in NCO
    ItemNames.RAVEN_SPIDER_MINES, 
    ItemNames.RAVEN_INTERNAL_TECH_MODULE, 
    ItemNames.RAVEN_RAILGUN_TURRET,        # Raven Magrail Munitions
    ItemNames.RAVEN_HUNTER_SEEKER_WEAPON,  # Raven Special Ordnance
    ItemNames.BATTLECRUISER_INTERNAL_TECH_MODULE,
    ItemNames.BATTLECRUISER_CLOAK,
    ItemNames.BATTLECRUISER_ATX_LASER_BATTERY,  # Battlecruiser Special Ordnance
    ItemNames.PROGRESSIVE_REGENERATIVE_BIO_STEEL,
]
item_name_groups[ItemGroupNames.NCO_UPGRADES] = nco_upgrades = nco_baseline_upgrades + nco_unit_technology
item_name_groups[ItemGroupNames.NCO_MAX_PROGRESSIVE_ITEMS] = nco_unit_technology + nova_equipment + terran_generic_upgrades
item_name_groups[ItemGroupNames.NCO_MIN_PROGRESSIVE_ITEMS] = nco_units + nco_baseline_upgrades
item_name_groups[ItemGroupNames.TERRAN_PROGRESSIVE_UPGRADES] = terran_progressive_items = [
    item_name for item_name, item_data in Items.item_table.items()
    if item_data.type in (Items.TerranItemType.Progressive, Items.TerranItemType.Progressive_2)
]
item_name_groups[ItemGroupNames.WOL_ITEMS] = vanilla_wol_items = (
    wol_units
    + wol_buildings
    + wol_mercs
    + wol_upgrades
    + terran_generic_upgrades
)

# Zerg
item_name_groups[ItemGroupNames.ZERG_ITEMS] = zerg_items = [
    item_name for item_name, item_data in Items.item_table.items()
    if item_data.race == SC2Race.ZERG
]
item_name_groups[ItemGroupNames.ZERG_BUILDINGS] = zerg_buildings = [ItemNames.SPINE_CRAWLER, ItemNames.SPORE_CRAWLER]
item_name_groups[ItemGroupNames.ZERG_UNITS] = zerg_units = [
    item_name for item_name, item_data in Items.item_table.items()
    if item_data.type in (Items.ZergItemType.Unit, Items.ZergItemType.Mercenary, Items.ZergItemType.Morph)
        and item_name not in zerg_buildings
]
item_name_groups[ItemGroupNames.ZERG_GENERIC_UPGRADES] = zerg_generic_upgrades = [
    item_name for item_name, item_data in Items.item_table.items()
    if item_data.type == Items.ZergItemType.Upgrade
]
item_name_groups[ItemGroupNames.HOTS_UNITS] = hots_units = [
    ItemNames.ZERGLING, ItemNames.SWARM_QUEEN, ItemNames.ROACH, ItemNames.HYDRALISK,
    ItemNames.ABERRATION, ItemNames.SWARM_HOST, ItemNames.MUTALISK,
    ItemNames.INFESTOR, ItemNames.ULTRALISK,
    ItemNames.ZERGLING_BANELING_ASPECT,
    ItemNames.HYDRALISK_LURKER_ASPECT,
    ItemNames.HYDRALISK_IMPALER_ASPECT,
    ItemNames.MUTALISK_CORRUPTOR_VIPER_ASPECT,
    ItemNames.MUTALISK_CORRUPTOR_BROOD_LORD_ASPECT,
]
item_name_groups[ItemGroupNames.HOTS_MORPHS] = hots_morphs = [
    ItemNames.ZERGLING_BANELING_ASPECT,
    ItemNames.HYDRALISK_IMPALER_ASPECT,
    ItemNames.HYDRALISK_LURKER_ASPECT,
    ItemNames.MUTALISK_CORRUPTOR_VIPER_ASPECT,
    ItemNames.MUTALISK_CORRUPTOR_BROOD_LORD_ASPECT,
]
item_name_groups[ItemGroupNames.ZERG_MORPHS] = zerg_morphs = [
    item_name for item_name, item_data in Items.item_table.items() if item_data.type == Items.ZergItemType.Morph
]
item_name_groups[ItemGroupNames.ZERG_MERCS] = zerg_mercs = [
    item_name for item_name, item_data in Items.item_table.items() if item_data.type == Items.ZergItemType.Mercenary
]
item_name_groups[ItemGroupNames.KERRIGAN_ABILITIES] = kerrigan_abilities = [
    item_name for item_name, item_data in Items.item_table.items() if item_data.type == Items.ZergItemType.Ability
]
item_name_groups[ItemGroupNames.KERRIGAN_PASSIVES] = kerrigan_passives = [
    ItemNames.KERRIGAN_HEROIC_FORTITUDE, ItemNames.KERRIGAN_CHAIN_REACTION,
    ItemNames.KERRIGAN_INFEST_BROODLINGS, ItemNames.KERRIGAN_FURY, ItemNames.KERRIGAN_ABILITY_EFFICIENCY,
]

# Zerg Upgrades
item_name_groups[ItemGroupNames.HOTS_STRAINS] = hots_strains = [
    item_name for item_name, item_data in Items.item_table.items() if item_data.type == Items.ZergItemType.Strain
]
item_name_groups[ItemGroupNames.HOTS_MUTATIONS] = hots_mutations = [
    ItemNames.ZERGLING_HARDENED_CARAPACE, ItemNames.ZERGLING_ADRENAL_OVERLOAD, ItemNames.ZERGLING_METABOLIC_BOOST,
    ItemNames.BANELING_CORROSIVE_ACID, ItemNames.BANELING_RUPTURE, ItemNames.BANELING_REGENERATIVE_ACID,
    ItemNames.ROACH_HYDRIODIC_BILE, ItemNames.ROACH_ADAPTIVE_PLATING, ItemNames.ROACH_TUNNELING_CLAWS,
    ItemNames.HYDRALISK_FRENZY, ItemNames.HYDRALISK_ANCILLARY_CARAPACE, ItemNames.HYDRALISK_GROOVED_SPINES,
    ItemNames.SWARM_HOST_BURROW, ItemNames.SWARM_HOST_RAPID_INCUBATION, ItemNames.SWARM_HOST_PRESSURIZED_GLANDS,
    ItemNames.MUTALISK_VICIOUS_GLAIVE, ItemNames.MUTALISK_RAPID_REGENERATION, ItemNames.MUTALISK_SUNDERING_GLAIVE,
    ItemNames.ULTRALISK_BURROW_CHARGE, ItemNames.ULTRALISK_TISSUE_ASSIMILATION, ItemNames.ULTRALISK_MONARCH_BLADES,
]
item_name_groups[ItemGroupNames.HOTS_GLOBAL_UPGRADES] = hots_global_upgrades = [
    ItemNames.KERRIGAN_ZERGLING_RECONSTITUTION,
    ItemNames.KERRIGAN_IMPROVED_OVERLORDS,
    ItemNames.KERRIGAN_AUTOMATED_EXTRACTORS,
    ItemNames.KERRIGAN_TWIN_DRONES,
    ItemNames.KERRIGAN_MALIGNANT_CREEP,
    ItemNames.KERRIGAN_VESPENE_EFFICIENCY,
]
item_name_groups[ItemGroupNames.HOTS_ITEMS] = vanilla_hots_items = (
    hots_units
    + zerg_buildings
    + kerrigan_abilities
    + hots_mutations
    + hots_strains
    + hots_global_upgrades
    + zerg_generic_upgrades
)


# Protoss
item_name_groups[ItemGroupNames.PROTOSS_ITEMS] = protoss_items = [
    item_name for item_name, item_data in Items.item_table.items()
    if item_data.race == SC2Race.PROTOSS
]
item_name_groups[ItemGroupNames.PROTOSS_UNITS] = protoss_units = [
    item_name for item_name, item_data in Items.item_table.items()
    if item_data.type in (Items.ProtossItemType.Unit, Items.ProtossItemType.Unit_2)
]
item_name_groups[ItemGroupNames.PROTOSS_GENERIC_UPGRADES] = protoss_generic_upgrades = [
    item_name for item_name, item_data in Items.item_table.items()
    if item_data.type == Items.ProtossItemType.Upgrade
]
item_name_groups[ItemGroupNames.LOTV_UNITS] = lotv_units = [
    ItemNames.ZEALOT, ItemNames.CENTURION, ItemNames.SENTINEL,
    ItemNames.STALKER, ItemNames.DRAGOON, ItemNames.ADEPT,
    ItemNames.SENTRY, ItemNames.HAVOC, ItemNames.ENERGIZER,
    ItemNames.HIGH_TEMPLAR, ItemNames.DARK_ARCHON, ItemNames.ASCENDANT,
    ItemNames.DARK_TEMPLAR, ItemNames.AVENGER, ItemNames.BLOOD_HUNTER,
    ItemNames.IMMORTAL, ItemNames.ANNIHILATOR, ItemNames.VANGUARD,
    ItemNames.COLOSSUS, ItemNames.WRATHWALKER, ItemNames.REAVER,
    ItemNames.PHOENIX, ItemNames.MIRAGE, ItemNames.CORSAIR,
    ItemNames.VOID_RAY, ItemNames.DESTROYER, ItemNames.ARBITER,
    ItemNames.CARRIER, ItemNames.TEMPEST, ItemNames.MOTHERSHIP,
]
item_name_groups[ItemGroupNames.PROPHECY_UNITS] = prophecy_units = [
    ItemNames.ZEALOT, ItemNames.STALKER, ItemNames.HIGH_TEMPLAR, ItemNames.DARK_TEMPLAR,
    ItemNames.OBSERVER, ItemNames.IMMORTAL, ItemNames.COLOSSUS,
    ItemNames.PHOENIX, ItemNames.VOID_RAY, ItemNames.CARRIER,
]
item_name_groups[ItemGroupNames.PROPHECY_BUILDINGS] = prophecy_buildings = [
    ItemNames.PHOTON_CANNON,
]
item_name_groups[ItemGroupNames.GATEWAY_UNITS] = gateway_units = [
    ItemNames.ZEALOT, ItemNames.CENTURION, ItemNames.SENTINEL, ItemNames.SUPPLICANT,
    ItemNames.STALKER, ItemNames.INSTIGATOR, ItemNames.SLAYER,
    ItemNames.SENTRY, ItemNames.HAVOC, ItemNames.ENERGIZER,
    ItemNames.DRAGOON, ItemNames.ADEPT, ItemNames.DARK_ARCHON,
    ItemNames.HIGH_TEMPLAR, ItemNames.SIGNIFIER, ItemNames.ASCENDANT,
    ItemNames.DARK_TEMPLAR, ItemNames.AVENGER, ItemNames.BLOOD_HUNTER,
]
item_name_groups[ItemGroupNames.ROBO_UNITS] = robo_units = [
    ItemNames.WARP_PRISM, ItemNames.OBSERVER,
    ItemNames.IMMORTAL, ItemNames.ANNIHILATOR, ItemNames.VANGUARD,
    ItemNames.COLOSSUS, ItemNames.WRATHWALKER,
    ItemNames.REAVER, ItemNames.DISRUPTOR,
]
item_name_groups[ItemGroupNames.STARGATE_UNITS] = stargate_units = [
    ItemNames.PHOENIX, ItemNames.MIRAGE, ItemNames.CORSAIR,
    ItemNames.VOID_RAY, ItemNames.DESTROYER,
    ItemNames.SCOUT, ItemNames.TEMPEST,
    ItemNames.CARRIER, ItemNames.MOTHERSHIP,
    ItemNames.ARBITER, ItemNames.ORACLE,
]
item_name_groups[ItemGroupNames.PROTOSS_BUILDINGS] = protoss_buildings = [
    item_name for item_name, item_data in Items.item_table.items()
    if item_data.type == Items.ProtossItemType.Building
]
item_name_groups[ItemGroupNames.AIUR_UNITS] = [
    ItemNames.ZEALOT, ItemNames.DRAGOON, ItemNames.SENTRY, ItemNames.AVENGER, ItemNames.HIGH_TEMPLAR,
    ItemNames.IMMORTAL, ItemNames.REAVER,
    ItemNames.PHOENIX, ItemNames.SCOUT, ItemNames.ARBITER, ItemNames.CARRIER,
]
item_name_groups[ItemGroupNames.NERAZIM_UNITS] = [
    ItemNames.CENTURION, ItemNames.STALKER, ItemNames.DARK_TEMPLAR, ItemNames.SIGNIFIER, ItemNames.DARK_ARCHON,
    ItemNames.ANNIHILATOR,
    ItemNames.CORSAIR, ItemNames.ORACLE, ItemNames.VOID_RAY,
]
item_name_groups[ItemGroupNames.TAL_DARIM_UNITS] = [
    ItemNames.SUPPLICANT, ItemNames.SLAYER, ItemNames.HAVOC, ItemNames.BLOOD_HUNTER, ItemNames.ASCENDANT,
    ItemNames.VANGUARD, ItemNames.WRATHWALKER,
    ItemNames.DESTROYER, ItemNames.MOTHERSHIP,
]
item_name_groups[ItemGroupNames.PURIFIER_UNITS] = [
    ItemNames.SENTINEL, ItemNames.ADEPT, ItemNames.INSTIGATOR, ItemNames.ENERGIZER,
    ItemNames.COLOSSUS, ItemNames.DISRUPTOR,
    ItemNames.MIRAGE, ItemNames.TEMPEST,
]
item_name_groups[ItemGroupNames.SOA_ITEMS] = soa_items = [
    *[item_name for item_name, item_data in Items.item_table.items() if item_data.type == Items.ProtossItemType.Spear_Of_Adun],
    ItemNames.SOA_PROGRESSIVE_PROXY_PYLON,
]
lotv_soa_items = [item_name for item_name in soa_items if item_name != ItemNames.SOA_PYLON_OVERCHARGE]
item_name_groups[ItemGroupNames.PROTOSS_GLOBAL_UPGRADES] = [
    item_name for item_name, item_data in Items.item_table.items() if item_data.type == Items.ProtossItemType.Solarite_Core
]
item_name_groups[ItemGroupNames.LOTV_GLOBAL_UPGRADES] = lotv_global_upgrades = [
    ItemNames.NEXUS_OVERCHARGE,
    ItemNames.ORBITAL_ASSIMILATORS,
    ItemNames.WARP_HARMONIZATION,
    ItemNames.MATRIX_OVERLOAD,
    ItemNames.GUARDIAN_SHELL,
    ItemNames.RECONSTRUCTION_BEAM,
]
item_name_groups[ItemGroupNames.LOTV_ITEMS] = vanilla_lotv_items = (
    lotv_units
    + protoss_buildings
    + lotv_soa_items
    + lotv_global_upgrades
    + protoss_generic_upgrades
)

item_name_groups[ItemGroupNames.VANILLA_ITEMS] = vanilla_items = (
    vanilla_wol_items + vanilla_hots_items + vanilla_lotv_items
)
