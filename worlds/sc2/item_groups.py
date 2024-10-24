import typing
from . import item_names, items
from .mission_tables import campaign_mission_table, SC2Campaign, SC2Mission, SC2Race

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
    items.TerranItemType.Progressive.display_name,
    items.TerranItemType.Nova_Gear.display_name,
    items.TerranItemType.Mercenary.display_name,
    items.ZergItemType.Ability.display_name,
    items.ZergItemType.Morph.display_name,
    items.ZergItemType.Strain.display_name,
}

# Some item names only differ in bracketed parts
# These items are ambiguous for short-hand name groups
bracketless_duplicates: typing.Set[str]
# This is a list of names in ItemNames with bracketed parts removed, for internal use
_shortened_names = [(name[:name.find(' (')] if '(' in name else name)
      for name in [item_names.__dict__[name] for name in item_names.__dir__() if not name.startswith('_')]]
# Remove the first instance of every short-name from the full item list
bracketless_duplicates = set(_shortened_names)
for name in bracketless_duplicates:
    _shortened_names.remove(name)
# The remaining short-names are the duplicates
bracketless_duplicates = set(_shortened_names)
del _shortened_names

# All items get sorted into their data type
for item, data in items.get_full_item_list().items():
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
    MENGSK_UNITS = "Mengsk Units"
    TERRAN_VETERANCY_UNITS= "Terran Veterancy Units"

    ZERG_ITEMS = "Zerg Items"
    ZERG_UNITS = "Zerg Units"
    ZERG_GENERIC_UPGRADES = "Zerg Generic Upgrades"
    """+attack/armour upgrades"""
    HOTS_UNITS = "HotS Units"
    HOTS_BUILDINGS = "HotS Buildings"
    HOTS_STRAINS = "HotS Strains"
    """Vanilla HotS strains (the upgrades you play a mini-mission for)"""
    HOTS_MUTATIONS = "HotS Mutations"
    """Vanilla HotS Mutations (basic toggleable unit upgrades)"""
    HOTS_GLOBAL_UPGRADES = "HotS Global Upgrades"
    HOTS_MORPHS = "HotS Morphs"
    KERRIGAN_ABILITIES = "Kerrigan Abilities"
    KERRIGAN_HOTS_ABILITIES = "Kerrigan HotS Abilities"
    KERRIGAN_PASSIVES = "Kerrigan Passives"
    KERRIGAN_TIER_1 = "Kerrigan Tier 1"
    KERRIGAN_TIER_2 = "Kerrigan Tier 2"
    KERRIGAN_TIER_3 = "Kerrigan Tier 3"
    KERRIGAN_TIER_4 = "Kerrigan Tier 4"
    KERRIGAN_TIER_5 = "Kerrigan Tier 5"
    KERRIGAN_TIER_6 = "Kerrigan Tier 6"
    KERRIGAN_TIER_7 = "Kerrigan Tier 7"
    HOTS_ITEMS = "HotS Items"
    """All items from vanilla HotS"""
    OVERLORD_UPGRADES = "Overlord Upgrades"
    ZERG_MORPHS = "Zerg Morphs"
    ZERG_MERCS = "Zerg Mercenaries"
    ZERG_BUILDINGS = "Zerg Buildings"
    INF_TERRAN_ITEMS = "Infested Terran Items"
    """All items from Stukov co-op subfaction"""
    INF_TERRAN_UNITS = "Infested Terran Units"
    INF_TERRAN_UPGRADES = "Infested Terran Upgrades"

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
    WAR_COUNCIL = "Protoss War Council Upgrades"
    AIUR_UNITS = "Aiur"
    NERAZIM_UNITS = "Nerazim"
    TAL_DARIM_UNITS = "Tal'Darim"
    PURIFIER_UNITS = "Purifier"

    VANILLA_ITEMS = "Vanilla Items"
    OVERPOWERED_ITEMS = "Overpowered Items"

    @classmethod
    def get_all_group_names(cls) -> typing.Set[str]:
        return {
            name for identifier, name in cls.__dict__.items()
            if not identifier.startswith('_')
            and not identifier.startswith('get_')
        }


# Terran
item_name_groups[ItemGroupNames.TERRAN_ITEMS] = terran_items = [
    item_name for item_name, item_data in items.item_table.items()
    if item_data.race == SC2Race.TERRAN
]
item_name_groups[ItemGroupNames.TERRAN_UNITS] = terran_units = [
    item_name for item_name, item_data in items.item_table.items()
    if item_data.type in (items.TerranItemType.Unit, items.TerranItemType.Unit_2, items.TerranItemType.Mercenary)
]
item_name_groups[ItemGroupNames.TERRAN_GENERIC_UPGRADES] = terran_generic_upgrades = [
    item_name for item_name, item_data in items.item_table.items()
    if item_data.type == items.TerranItemType.Upgrade
]
item_name_groups[ItemGroupNames.BARRACKS_UNITS] = barracks_units = [
    item_names.MARINE, item_names.MEDIC, item_names.FIREBAT, item_names.MARAUDER,
    item_names.REAPER, item_names.GHOST, item_names.SPECTRE, item_names.HERC, item_names.AEGIS_GUARD,
    item_names.EMPERORS_SHADOW, item_names.DOMINION_TROOPER, item_names.SON_OF_KORHAL,
    item_names.FIELD_RESPONSE_THETA,
]
item_name_groups[ItemGroupNames.FACTORY_UNITS] = factory_units = [
    item_names.HELLION, item_names.VULTURE, item_names.GOLIATH, item_names.DIAMONDBACK,
    item_names.SIEGE_TANK, item_names.THOR, item_names.PREDATOR, item_names.WIDOW_MINE,
    item_names.CYCLONE, item_names.WARHOUND, item_names.SHOCK_DIVISION, item_names.BLACKHAMMER,
    item_names.BULWARK_COMPANY,
]
item_name_groups[ItemGroupNames.STARPORT_UNITS] = starport_units = [
    item_names.MEDIVAC, item_names.WRAITH, item_names.VIKING, item_names.BANSHEE,
    item_names.BATTLECRUISER, item_names.HERCULES, item_names.SCIENCE_VESSEL, item_names.RAVEN,
    item_names.LIBERATOR, item_names.VALKYRIE, item_names.PRIDE_OF_AUGUSTRGRAD, item_names.SKY_FURY,
    item_names.EMPERORS_GUARDIAN, item_names.NIGHT_HAWK, item_names.NIGHT_WOLF,
]
item_name_groups[ItemGroupNames.TERRAN_BUILDINGS] = terran_buildings = [
    item_name for item_name, item_data in items.item_table.items()
    if item_data.type == items.TerranItemType.Building
]
item_name_groups[ItemGroupNames.TERRAN_MERCENARIES] = terran_mercenaries = [
    item_name for item_name, item_data in items.item_table.items()
    if item_data.type == items.TerranItemType.Mercenary
]
item_name_groups[ItemGroupNames.NCO_UNITS] = nco_units = [
    item_names.MARINE, item_names.MARAUDER, item_names.REAPER,
    item_names.HELLION, item_names.GOLIATH, item_names.SIEGE_TANK,
    item_names.RAVEN, item_names.LIBERATOR, item_names.BANSHEE, item_names.BATTLECRUISER,
    item_names.HERC,  # From that one bonus objective in mission 5
]
item_name_groups[ItemGroupNames.NCO_BUILDINGS] = nco_buildings = [
    item_names.BUNKER, item_names.MISSILE_TURRET, item_names.PLANETARY_FORTRESS,
]
item_name_groups[ItemGroupNames.NOVA_EQUIPMENT] = nova_equipment = [
    *[item_name for item_name, item_data in items.item_table.items()
        if item_data.type == items.TerranItemType.Nova_Gear],
    item_names.NOVA_PROGRESSIVE_STEALTH_SUIT_MODULE,
]
item_name_groups[ItemGroupNames.WOL_UNITS] = wol_units = [
    item_names.MARINE, item_names.MEDIC, item_names.FIREBAT, item_names.MARAUDER, item_names.REAPER,
    item_names.HELLION, item_names.VULTURE, item_names.GOLIATH,  item_names.DIAMONDBACK, item_names.SIEGE_TANK,
    item_names.MEDIVAC, item_names.WRAITH, item_names.VIKING, item_names.BANSHEE, item_names.BATTLECRUISER,
    item_names.GHOST, item_names.SPECTRE, item_names.THOR,
    item_names.PREDATOR, item_names.HERCULES,
    item_names.SCIENCE_VESSEL, item_names.RAVEN,
]
item_name_groups[ItemGroupNames.WOL_MERCS] = wol_mercs = [
    item_names.WAR_PIGS, item_names.DEVIL_DOGS, item_names.HAMMER_SECURITIES,
    item_names.SPARTAN_COMPANY, item_names.SIEGE_BREAKERS,
    item_names.HELS_ANGELS, item_names.DUSK_WINGS, item_names.JACKSONS_REVENGE,
]
item_name_groups[ItemGroupNames.WOL_BUILDINGS] = wol_buildings = [
    item_names.BUNKER, item_names.SENSOR_TOWER, item_names.COMMAND_CENTER_MULE, item_names.COMMAND_CENTER_SCANNER_SWEEP,
    item_names.PERDITION_TURRET, item_names.PLANETARY_FORTRESS,
    item_names.HIVE_MIND_EMULATOR, item_names.PSI_DISRUPTER,
]
item_name_groups[ItemGroupNames.MENGSK_UNITS] = [
    item_names.AEGIS_GUARD, item_names.EMPERORS_SHADOW,
    item_names.SHOCK_DIVISION, item_names.BLACKHAMMER,
    item_names.PRIDE_OF_AUGUSTRGRAD, item_names.SKY_FURY,
    item_names.DOMINION_TROOPER,
]
item_name_groups[ItemGroupNames.TERRAN_VETERANCY_UNITS] = [
    item_names.AEGIS_GUARD, item_names.EMPERORS_SHADOW, item_names.SHOCK_DIVISION, item_names.BLACKHAMMER,
    item_names.PRIDE_OF_AUGUSTRGRAD, item_names.SKY_FURY, item_names.SON_OF_KORHAL, item_names.FIELD_RESPONSE_THETA,
    item_names.BULWARK_COMPANY, item_names.NIGHT_HAWK, item_names.EMPERORS_GUARDIAN, item_names.NIGHT_WOLF,
]

# Terran Upgrades
item_name_groups[ItemGroupNames.WOL_UPGRADES] = wol_upgrades = [
    # Armory Base
    item_names.BUNKER_PROJECTILE_ACCELERATOR, item_names.BUNKER_NEOSTEEL_BUNKER,
    item_names.MISSILE_TURRET_TITANIUM_HOUSING, item_names.MISSILE_TURRET_HELLSTORM_BATTERIES,
    item_names.SCV_ADVANCED_CONSTRUCTION, item_names.SCV_DUAL_FUSION_WELDERS,
    item_names.PROGRESSIVE_FIRE_SUPPRESSION_SYSTEM, item_names.COMMAND_CENTER_MULE, item_names.COMMAND_CENTER_SCANNER_SWEEP,
    # Armory Infantry
    item_names.MARINE_PROGRESSIVE_STIMPACK, item_names.MARINE_COMBAT_SHIELD,
    item_names.MEDIC_ADVANCED_MEDIC_FACILITIES, item_names.MEDIC_STABILIZER_MEDPACKS,
    item_names.FIREBAT_INCINERATOR_GAUNTLETS, item_names.FIREBAT_JUGGERNAUT_PLATING,
    item_names.MARAUDER_CONCUSSIVE_SHELLS, item_names.MARAUDER_KINETIC_FOAM,
    item_names.REAPER_U238_ROUNDS, item_names.REAPER_G4_CLUSTERBOMB,
    # Armory Vehicles
    item_names.HELLION_TWIN_LINKED_FLAMETHROWER, item_names.HELLION_THERMITE_FILAMENTS,
    item_names.SPIDER_MINE_CERBERUS_MINE, item_names.VULTURE_PROGRESSIVE_REPLENISHABLE_MAGAZINE,
    item_names.GOLIATH_MULTI_LOCK_WEAPONS_SYSTEM, item_names.GOLIATH_ARES_CLASS_TARGETING_SYSTEM,
    item_names.DIAMONDBACK_PROGRESSIVE_TRI_LITHIUM_POWER_CELL, item_names.DIAMONDBACK_SHAPED_HULL,
    item_names.SIEGE_TANK_MAELSTROM_ROUNDS, item_names.SIEGE_TANK_SHAPED_BLAST,
    # Armory Starships
    item_names.MEDIVAC_RAPID_DEPLOYMENT_TUBE, item_names.MEDIVAC_ADVANCED_HEALING_AI,
    item_names.WRAITH_PROGRESSIVE_TOMAHAWK_POWER_CELLS, item_names.WRAITH_DISPLACEMENT_FIELD,
    item_names.VIKING_RIPWAVE_MISSILES, item_names.VIKING_PHOBOS_CLASS_WEAPONS_SYSTEM,
    item_names.BANSHEE_PROGRESSIVE_CROSS_SPECTRUM_DAMPENERS, item_names.BANSHEE_SHOCKWAVE_MISSILE_BATTERY,
    item_names.BATTLECRUISER_PROGRESSIVE_MISSILE_PODS, item_names.BATTLECRUISER_PROGRESSIVE_DEFENSIVE_MATRIX,
    # Armory Dominion
    item_names.GHOST_OCULAR_IMPLANTS, item_names.GHOST_CRIUS_SUIT,
    item_names.SPECTRE_PSIONIC_LASH, item_names.SPECTRE_NYX_CLASS_CLOAKING_MODULE,
    item_names.THOR_330MM_BARRAGE_CANNON, item_names.THOR_PROGRESSIVE_IMMORTALITY_PROTOCOL,
    # Lab Zerg
    item_names.BUNKER_FORTIFIED_BUNKER, item_names.BUNKER_SHRIKE_TURRET,
    item_names.PROGRESSIVE_REGENERATIVE_BIO_STEEL, item_names.CELLULAR_REACTOR,
    # Other 3 levels are units/buildings (Perdition, PF, Hercules, Predator, HME, Psi Disrupter)
    # Lab Protoss
    item_names.VANADIUM_PLATING, item_names.ULTRA_CAPACITORS,
    item_names.AUTOMATED_REFINERY, item_names.MICRO_FILTERING,
    item_names.ORBITAL_DEPOTS, item_names.COMMAND_CENTER_COMMAND_CENTER_REACTOR,
    item_names.ORBITAL_STRIKE, item_names.TECH_REACTOR,
    # Other level is units (Raven, Science Vessel)
]
item_name_groups[ItemGroupNames.TERRAN_STIMPACKS] = terran_stimpacks = [
    item_names.MARINE_PROGRESSIVE_STIMPACK,
    item_names.MARAUDER_PROGRESSIVE_STIMPACK,
    item_names.REAPER_PROGRESSIVE_STIMPACK,
    item_names.FIREBAT_PROGRESSIVE_STIMPACK,
    item_names.HELLION_PROGRESSIVE_STIMPACK,
]
item_name_groups[ItemGroupNames.TERRAN_ORIGINAL_PROGRESSIVE_UPGRADES] = terran_original_progressive_upgrades = [
    item_names.PROGRESSIVE_FIRE_SUPPRESSION_SYSTEM,
    item_names.MARINE_PROGRESSIVE_STIMPACK,
    item_names.VULTURE_PROGRESSIVE_REPLENISHABLE_MAGAZINE,
    item_names.DIAMONDBACK_PROGRESSIVE_TRI_LITHIUM_POWER_CELL,
    item_names.WRAITH_PROGRESSIVE_TOMAHAWK_POWER_CELLS,
    item_names.BANSHEE_PROGRESSIVE_CROSS_SPECTRUM_DAMPENERS,
    item_names.BATTLECRUISER_PROGRESSIVE_MISSILE_PODS,
    item_names.BATTLECRUISER_PROGRESSIVE_DEFENSIVE_MATRIX,
    item_names.THOR_PROGRESSIVE_IMMORTALITY_PROTOCOL,
    item_names.PROGRESSIVE_REGENERATIVE_BIO_STEEL,
]
item_name_groups[ItemGroupNames.NCO_BASELINE_UPGRADES] = nco_baseline_upgrades = [
    item_names.BUNKER_NEOSTEEL_BUNKER,  # Baseline from mission 2
    item_names.BUNKER_FORTIFIED_BUNKER,  # Baseline from mission 2
    item_names.MARINE_COMBAT_SHIELD,   # Baseline from mission 2
    item_names.MARAUDER_KINETIC_FOAM,  # Baseline outside WOL
    item_names.MARAUDER_CONCUSSIVE_SHELLS,  # Baseline from mission 2
    item_names.REAPER_KINETIC_FOAM, # Baseline from mission 2
    item_names.HELLION_HELLBAT_ASPECT,  # Baseline from mission 3
    item_names.GOLIATH_INTERNAL_TECH_MODULE,  # Baseline from mission 4
    item_names.GOLIATH_SHAPED_HULL,
    # ItemNames.GOLIATH_RESOURCE_EFFICIENCY,  # Supply savings baseline in NCO, mineral savings is non-NCO
    item_names.SIEGE_TANK_SHAPED_HULL,  # Baseline NCO gives +10; this upgrade gives +25
    item_names.SIEGE_TANK_SHAPED_BLAST,  # Baseline from mission 3
    item_names.LIBERATOR_RAID_ARTILLERY,  # Baseline in mission 5
    item_names.RAVEN_BIO_MECHANICAL_REPAIR_DRONE,  # Baseline in mission 5
    item_names.BATTLECRUISER_TACTICAL_JUMP,
    item_names.BATTLECRUISER_COVERT_OPS_ENGINES,
    item_names.PROGRESSIVE_FIRE_SUPPRESSION_SYSTEM,  # Baseline from mission 2
    item_names.ORBITAL_DEPOTS,  # Baseline from mission 2
    item_names.COMMAND_CENTER_SCANNER_SWEEP,  # In NCO you must actually morph Command Center into Orbital Command
    item_names.COMMAND_CENTER_EXTRA_SUPPLIES,  # But in AP this works WoL-style
] + nco_buildings
item_name_groups[ItemGroupNames.NCO_UNIT_TECHNOLOGY] = nco_unit_technology = [
    item_names.MARINE_LASER_TARGETING_SYSTEM,
    item_names.MARINE_PROGRESSIVE_STIMPACK,
    item_names.MARINE_MAGRAIL_MUNITIONS,
    item_names.MARINE_OPTIMIZED_LOGISTICS,
    item_names.MARAUDER_LASER_TARGETING_SYSTEM,
    item_names.MARAUDER_INTERNAL_TECH_MODULE,
    item_names.MARAUDER_PROGRESSIVE_STIMPACK,
    item_names.MARAUDER_MAGRAIL_MUNITIONS,
    item_names.REAPER_SPIDER_MINES,
    item_names.REAPER_LASER_TARGETING_SYSTEM,
    item_names.REAPER_PROGRESSIVE_STIMPACK,
    item_names.REAPER_ADVANCED_CLOAKING_FIELD,
    # Reaper special ordnance gives anti-building attack, which is baseline in AP
    item_names.HELLION_JUMP_JETS,
    item_names.HELLION_PROGRESSIVE_STIMPACK,
    item_names.HELLION_SMART_SERVOS,
    item_names.HELLION_OPTIMIZED_LOGISTICS,
    item_names.HELLION_THERMITE_FILAMENTS,  # Called Infernal Pre-Igniter in NCO
    item_names.GOLIATH_ARES_CLASS_TARGETING_SYSTEM,  # Called Laser Targeting System in NCO
    item_names.GOLIATH_JUMP_JETS,
    item_names.GOLIATH_OPTIMIZED_LOGISTICS,
    item_names.GOLIATH_MULTI_LOCK_WEAPONS_SYSTEM,
    item_names.SIEGE_TANK_SPIDER_MINES,
    item_names.SIEGE_TANK_JUMP_JETS,
    item_names.SIEGE_TANK_INTERNAL_TECH_MODULE,
    item_names.SIEGE_TANK_SMART_SERVOS,
    # Tanks can't get Laser targeting system in NCO
    item_names.BANSHEE_INTERNAL_TECH_MODULE,
    item_names.BANSHEE_PROGRESSIVE_CROSS_SPECTRUM_DAMPENERS,
    item_names.BANSHEE_SHOCKWAVE_MISSILE_BATTERY,  # Banshee Special Ordnance
    # Banshees can't get laser targeting systems in NCO
    item_names.LIBERATOR_CLOAK,
    item_names.LIBERATOR_SMART_SERVOS,
    item_names.LIBERATOR_OPTIMIZED_LOGISTICS,
    # Liberators can't get laser targeting system in NCO
    item_names.RAVEN_SPIDER_MINES, 
    item_names.RAVEN_INTERNAL_TECH_MODULE, 
    item_names.RAVEN_RAILGUN_TURRET,        # Raven Magrail Munitions
    item_names.RAVEN_HUNTER_SEEKER_WEAPON,  # Raven Special Ordnance
    item_names.BATTLECRUISER_INTERNAL_TECH_MODULE,
    item_names.BATTLECRUISER_CLOAK,
    item_names.BATTLECRUISER_ATX_LASER_BATTERY,  # Battlecruiser Special Ordnance
    item_names.PROGRESSIVE_REGENERATIVE_BIO_STEEL,
]
item_name_groups[ItemGroupNames.NCO_UPGRADES] = nco_upgrades = nco_baseline_upgrades + nco_unit_technology
item_name_groups[ItemGroupNames.NCO_MAX_PROGRESSIVE_ITEMS] = nco_unit_technology + nova_equipment + terran_generic_upgrades
item_name_groups[ItemGroupNames.NCO_MIN_PROGRESSIVE_ITEMS] = nco_units + nco_baseline_upgrades
item_name_groups[ItemGroupNames.TERRAN_PROGRESSIVE_UPGRADES] = terran_progressive_items = [
    item_name for item_name, item_data in items.item_table.items()
    if item_data.type in (items.TerranItemType.Progressive, items.TerranItemType.Progressive_2)
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
    item_name for item_name, item_data in items.item_table.items()
    if item_data.race == SC2Race.ZERG
]
item_name_groups[ItemGroupNames.ZERG_BUILDINGS] = zerg_buildings = [
    item_names.SPINE_CRAWLER,
    item_names.SPORE_CRAWLER,
    item_names.INFESTED_BUNKER,
    item_names.NYDUS_WORM,
    item_names.OMEGA_WORM]
item_name_groups[ItemGroupNames.ZERG_UNITS] = zerg_units = [
    item_name for item_name, item_data in items.item_table.items()
    if item_data.type in (items.ZergItemType.Unit, items.ZergItemType.Mercenary, items.ZergItemType.Morph)
        and item_name not in zerg_buildings
]
# For W/A upgrades
zerg_ground_units = [
    item_names.ZERGLING, item_names.SWARM_QUEEN, item_names.ROACH, item_names.HYDRALISK, item_names.ABERRATION,
    item_names.SWARM_HOST, item_names.INFESTOR, item_names.ULTRALISK, item_names.ZERGLING_BANELING_ASPECT,
    item_names.HYDRALISK_LURKER_ASPECT, item_names.HYDRALISK_IMPALER_ASPECT, item_names.ULTRALISK_TYRANNOZOR_ASPECT,
    item_names.ROACH_RAVAGER_ASPECT, item_names.DEFILER, item_names.ROACH_PRIMAL_IGNITER_ASPECT,
    item_names.INFESTED_MARINE, item_names.INFESTED_BUNKER, item_names.INFESTED_DIAMONDBACK,
    item_names.INFESTED_SIEGE_TANK,
]
zerg_melee_wa = [
    item_names.ZERGLING, item_names.ABERRATION, item_names.ULTRALISK, item_names.ZERGLING_BANELING_ASPECT,
    item_names.ULTRALISK_TYRANNOZOR_ASPECT, item_names.INFESTED_BUNKER,
]
zerg_ranged_wa = [
    item_names.SWARM_QUEEN, item_names.ROACH, item_names.HYDRALISK, item_names.SWARM_HOST,
    item_names.HYDRALISK_LURKER_ASPECT, item_names.HYDRALISK_IMPALER_ASPECT, item_names.ULTRALISK_TYRANNOZOR_ASPECT,
    item_names.ROACH_RAVAGER_ASPECT, item_names.ROACH_PRIMAL_IGNITER_ASPECT, item_names.INFESTED_MARINE,
    item_names.INFESTED_BUNKER, item_names.INFESTED_DIAMONDBACK, item_names.INFESTED_SIEGE_TANK,
]
zerg_air_units = [
    item_names.MUTALISK, item_names.MUTALISK_CORRUPTOR_VIPER_ASPECT, item_names.MUTALISK_CORRUPTOR_BROOD_LORD_ASPECT,
    item_names.CORRUPTOR, item_names.BROOD_QUEEN, item_names.SCOURGE, item_names.MUTALISK_CORRUPTOR_GUARDIAN_ASPECT,
    item_names.MUTALISK_CORRUPTOR_DEVOURER_ASPECT, item_names.INFESTED_BANSHEE, item_names.INFESTED_LIBERATOR,
]
item_name_groups[ItemGroupNames.ZERG_GENERIC_UPGRADES] = zerg_generic_upgrades = [
    item_name for item_name, item_data in items.item_table.items()
    if item_data.type == items.ZergItemType.Upgrade
]
item_name_groups[ItemGroupNames.HOTS_UNITS] = hots_units = [
    item_names.ZERGLING, item_names.SWARM_QUEEN, item_names.ROACH, item_names.HYDRALISK,
    item_names.ABERRATION, item_names.SWARM_HOST, item_names.MUTALISK,
    item_names.INFESTOR, item_names.ULTRALISK,
    item_names.ZERGLING_BANELING_ASPECT,
    item_names.HYDRALISK_LURKER_ASPECT,
    item_names.HYDRALISK_IMPALER_ASPECT,
    item_names.MUTALISK_CORRUPTOR_VIPER_ASPECT,
    item_names.MUTALISK_CORRUPTOR_BROOD_LORD_ASPECT,
]
item_name_groups[ItemGroupNames.HOTS_BUILDINGS] = hots_buildings = [
    item_names.SPINE_CRAWLER,
    item_names.SPORE_CRAWLER,
]
item_name_groups[ItemGroupNames.HOTS_MORPHS] = hots_morphs = [
    item_names.ZERGLING_BANELING_ASPECT,
    item_names.HYDRALISK_IMPALER_ASPECT,
    item_names.HYDRALISK_LURKER_ASPECT,
    item_names.MUTALISK_CORRUPTOR_VIPER_ASPECT,
    item_names.MUTALISK_CORRUPTOR_BROOD_LORD_ASPECT,
]
item_name_groups[ItemGroupNames.ZERG_MORPHS] = zerg_morphs = [
    item_name for item_name, item_data in items.item_table.items() if item_data.type == items.ZergItemType.Morph
]
item_name_groups[ItemGroupNames.ZERG_MERCS] = zerg_mercs = [
    item_name for item_name, item_data in items.item_table.items() if item_data.type == items.ZergItemType.Mercenary
]
item_name_groups[ItemGroupNames.KERRIGAN_ABILITIES] = kerrigan_abilities = [
    item_name for item_name, item_data in items.item_table.items() if item_data.type == items.ZergItemType.Ability
]
item_name_groups[ItemGroupNames.KERRIGAN_PASSIVES] = kerrigan_passives = [
    item_names.KERRIGAN_HEROIC_FORTITUDE, item_names.KERRIGAN_CHAIN_REACTION,
    item_names.KERRIGAN_INFEST_BROODLINGS, item_names.KERRIGAN_FURY, item_names.KERRIGAN_ABILITY_EFFICIENCY,
]
item_name_groups[ItemGroupNames.KERRIGAN_TIER_1] = kerrigan_tier_1 = [
    item_names.KERRIGAN_CRUSHING_GRIP, item_names.KERRIGAN_HEROIC_FORTITUDE, item_names.KERRIGAN_LEAPING_STRIKE
]
item_name_groups[ItemGroupNames.KERRIGAN_TIER_2] = kerrigan_tier_2= [
    item_names.KERRIGAN_CRUSHING_GRIP, item_names.KERRIGAN_CHAIN_REACTION, item_names.KERRIGAN_PSIONIC_SHIFT
]
item_name_groups[ItemGroupNames.KERRIGAN_TIER_3] = kerrigan_tier_3 = [
    item_names.TWIN_DRONES, item_names.AUTOMATED_EXTRACTORS, item_names.ZERGLING_RECONSTITUTION
]
item_name_groups[ItemGroupNames.KERRIGAN_TIER_4] = kerrigan_tier_4 = [
    item_names.KERRIGAN_MEND, item_names.KERRIGAN_SPAWN_BANELINGS, item_names.KERRIGAN_WILD_MUTATION
]
item_name_groups[ItemGroupNames.KERRIGAN_TIER_5] = kerrigan_tier_5 = [
    item_names.MALIGNANT_CREEP, item_names.VESPENE_EFFICIENCY, item_names.OVERLORD_IMPROVED_OVERLORDS
]
item_name_groups[ItemGroupNames.KERRIGAN_TIER_6] = kerrigan_tier_6 = [
    item_names.KERRIGAN_INFEST_BROODLINGS, item_names.KERRIGAN_FURY, item_names.KERRIGAN_ABILITY_EFFICIENCY
]
item_name_groups[ItemGroupNames.KERRIGAN_TIER_7] = kerrigan_tier_7 = [
    item_names.KERRIGAN_APOCALYPSE, item_names.KERRIGAN_SPAWN_LEVIATHAN, item_names.KERRIGAN_DROP_PODS
]
item_name_groups[ItemGroupNames.KERRIGAN_HOTS_ABILITIES] = kerrigan_hots_abilities = [
    ability for tiers in [
        kerrigan_tier_1, kerrigan_tier_2, kerrigan_tier_4, kerrigan_tier_6, kerrigan_tier_7
    ] for ability in tiers
]

item_name_groups[ItemGroupNames.OVERLORD_UPGRADES] = [
    item_names.OVERLORD_ANTENNAE,
    item_names.OVERLORD_VENTRAL_SACS,
    item_names.OVERLORD_GENERATE_CREEP,
    item_names.OVERLORD_PNEUMATIZED_CARAPACE,
    item_names.OVERLORD_IMPROVED_OVERLORDS,
    item_names.OVERLORD_OVERSEER_ASPECT,
]

# Zerg Upgrades
item_name_groups[ItemGroupNames.HOTS_STRAINS] = hots_strains = [
    item_name for item_name, item_data in items.item_table.items() if item_data.type == items.ZergItemType.Strain
]
item_name_groups[ItemGroupNames.HOTS_MUTATIONS] = hots_mutations = [
    item_names.ZERGLING_HARDENED_CARAPACE, item_names.ZERGLING_ADRENAL_OVERLOAD, item_names.ZERGLING_METABOLIC_BOOST,
    item_names.BANELING_CORROSIVE_ACID, item_names.BANELING_RUPTURE, item_names.BANELING_REGENERATIVE_ACID,
    item_names.ROACH_HYDRIODIC_BILE, item_names.ROACH_ADAPTIVE_PLATING, item_names.ROACH_TUNNELING_CLAWS,
    item_names.HYDRALISK_FRENZY, item_names.HYDRALISK_ANCILLARY_CARAPACE, item_names.HYDRALISK_GROOVED_SPINES,
    item_names.SWARM_HOST_BURROW, item_names.SWARM_HOST_RAPID_INCUBATION, item_names.SWARM_HOST_PRESSURIZED_GLANDS,
    item_names.MUTALISK_VICIOUS_GLAIVE, item_names.MUTALISK_RAPID_REGENERATION, item_names.MUTALISK_SUNDERING_GLAIVE,
    item_names.ULTRALISK_BURROW_CHARGE, item_names.ULTRALISK_TISSUE_ASSIMILATION, item_names.ULTRALISK_MONARCH_BLADES,
]
item_name_groups[ItemGroupNames.HOTS_GLOBAL_UPGRADES] = hots_global_upgrades = [
    item_names.ZERGLING_RECONSTITUTION,
    item_names.OVERLORD_IMPROVED_OVERLORDS,
    item_names.AUTOMATED_EXTRACTORS,
    item_names.TWIN_DRONES,
    item_names.MALIGNANT_CREEP,
    item_names.VESPENE_EFFICIENCY,
]
item_name_groups[ItemGroupNames.HOTS_ITEMS] = vanilla_hots_items = (
    hots_units
    + hots_buildings
    + kerrigan_hots_abilities
    + hots_mutations
    + hots_strains
    + hots_global_upgrades
    + zerg_generic_upgrades
)

# Zerg - Infested Terran (Stukov Co-op)
item_name_groups[ItemGroupNames.INF_TERRAN_UNITS] = infterr_units = [
    item_names.INFESTED_MARINE,
    item_names.INFESTED_BUNKER]
item_name_groups[ItemGroupNames.INF_TERRAN_UPGRADES] = infterr_upgrades = [
    item_names.INFESTED_SCV_BUILD_CHARGES,
    item_names.INFESTED_MARINE_PLAGUED_MUNITIONS,
    item_names.INFESTED_MARINE_RETINAL_AUGMENTATION,
    item_names.INFESTED_BUNKER_CALCIFIED_ARMOR,
    item_names.INFESTED_BUNKER_REGENERATIVE_PLATING,
    item_names.INFESTED_BUNKER_ENGORGED_BUNKERS
]
item_name_groups[ItemGroupNames.INF_TERRAN_ITEMS] = (
    infterr_units
    + infterr_upgrades
)

# Protoss
item_name_groups[ItemGroupNames.PROTOSS_ITEMS] = protoss_items = [
    item_name for item_name, item_data in items.item_table.items()
    if item_data.race == SC2Race.PROTOSS
]
item_name_groups[ItemGroupNames.PROTOSS_UNITS] = protoss_units = [
    item_name for item_name, item_data in items.item_table.items()
    if item_data.type in (items.ProtossItemType.Unit, items.ProtossItemType.Unit_2)
]
protoss_ground_wa = [
    item_names.ZEALOT, item_names.CENTURION, item_names.SENTINEL, item_names.SUPPLICANT,
    item_names.SENTRY, item_names.ENERGIZER,
    item_names.STALKER, item_names.INSTIGATOR, item_names.SLAYER, item_names.DRAGOON, item_names.ADEPT,
    item_names.HIGH_TEMPLAR, item_names.SIGNIFIER, item_names.ASCENDANT,
    item_names.DARK_TEMPLAR, item_names.BLOOD_HUNTER, item_names.AVENGER,
    item_names.DARK_ARCHON,
    item_names.IMMORTAL, item_names.ANNIHILATOR, item_names.VANGUARD, item_names.STALWART,
    item_names.COLOSSUS, item_names.WRATHWALKER,
    item_names.REAVER,
]
protoss_air_wa = [
    item_names.WARP_PRISM_PHASE_BLASTER,
    item_names.PHOENIX, item_names.MIRAGE, item_names.CORSAIR, item_names.SKIRMISHER,
    item_names.VOID_RAY, item_names.DESTROYER, item_names.WARP_RAY, item_names.DAWNBRINGER,
    item_names.CARRIER, item_names.SKYLORD, item_names.TRIREME,
    item_names.SCOUT, item_names.TEMPEST, item_names.MOTHERSHIP,
    item_names.ARBITER, item_names.ORACLE,
]
item_name_groups[ItemGroupNames.PROTOSS_GENERIC_UPGRADES] = protoss_generic_upgrades = [
    item_name for item_name, item_data in items.item_table.items()
    if item_data.type == items.ProtossItemType.Upgrade
]
item_name_groups[ItemGroupNames.LOTV_UNITS] = lotv_units = [
    item_names.ZEALOT, item_names.CENTURION, item_names.SENTINEL,
    item_names.STALKER, item_names.DRAGOON, item_names.ADEPT,
    item_names.SENTRY, item_names.HAVOC, item_names.ENERGIZER,
    item_names.HIGH_TEMPLAR, item_names.DARK_ARCHON, item_names.ASCENDANT,
    item_names.DARK_TEMPLAR, item_names.AVENGER, item_names.BLOOD_HUNTER,
    item_names.IMMORTAL, item_names.ANNIHILATOR, item_names.VANGUARD,
    item_names.COLOSSUS, item_names.WRATHWALKER, item_names.REAVER,
    item_names.PHOENIX, item_names.MIRAGE, item_names.CORSAIR,
    item_names.VOID_RAY, item_names.DESTROYER, item_names.ARBITER,
    item_names.CARRIER, item_names.TEMPEST, item_names.MOTHERSHIP,
]
item_name_groups[ItemGroupNames.PROPHECY_UNITS] = prophecy_units = [
    item_names.ZEALOT, item_names.STALKER, item_names.HIGH_TEMPLAR, item_names.DARK_TEMPLAR,
    item_names.OBSERVER, item_names.COLOSSUS,
    item_names.PHOENIX, item_names.WARP_RAY, item_names.CARRIER,
]
item_name_groups[ItemGroupNames.PROPHECY_BUILDINGS] = prophecy_buildings = [
    item_names.PHOTON_CANNON,
]
item_name_groups[ItemGroupNames.GATEWAY_UNITS] = gateway_units = [
    item_names.ZEALOT, item_names.CENTURION, item_names.SENTINEL, item_names.SUPPLICANT,
    item_names.STALKER, item_names.INSTIGATOR, item_names.SLAYER,
    item_names.SENTRY, item_names.HAVOC, item_names.ENERGIZER,
    item_names.DRAGOON, item_names.ADEPT, item_names.DARK_ARCHON,
    item_names.HIGH_TEMPLAR, item_names.SIGNIFIER, item_names.ASCENDANT,
    item_names.DARK_TEMPLAR, item_names.AVENGER, item_names.BLOOD_HUNTER,
]
item_name_groups[ItemGroupNames.ROBO_UNITS] = robo_units = [
    item_names.WARP_PRISM, item_names.OBSERVER,
    item_names.IMMORTAL, item_names.ANNIHILATOR, item_names.VANGUARD, item_names.STALWART,
    item_names.COLOSSUS, item_names.WRATHWALKER,
    item_names.REAVER, item_names.DISRUPTOR,
]
item_name_groups[ItemGroupNames.STARGATE_UNITS] = stargate_units = [
    item_names.PHOENIX, item_names.SKIRMISHER, item_names.MIRAGE, item_names.CORSAIR,
    item_names.VOID_RAY, item_names.DESTROYER, item_names.WARP_RAY, item_names.DAWNBRINGER,
    item_names.CARRIER, item_names.SKYLORD, item_names.TRIREME,
    item_names.TEMPEST, item_names.SCOUT, item_names.MOTHERSHIP,
    item_names.ARBITER, item_names.ORACLE,
]
item_name_groups[ItemGroupNames.PROTOSS_BUILDINGS] = protoss_buildings = [
    item_name for item_name, item_data in items.item_table.items()
    if item_data.type == items.ProtossItemType.Building
]
item_name_groups[ItemGroupNames.AIUR_UNITS] = [
    item_names.ZEALOT, item_names.DRAGOON, item_names.SENTRY, item_names.AVENGER, item_names.HIGH_TEMPLAR,
    item_names.IMMORTAL, item_names.REAVER,
    item_names.PHOENIX, item_names.SCOUT, item_names.ARBITER, item_names.CARRIER,
]
item_name_groups[ItemGroupNames.NERAZIM_UNITS] = [
    item_names.CENTURION, item_names.STALKER, item_names.DARK_TEMPLAR, item_names.SIGNIFIER, item_names.DARK_ARCHON,
    item_names.ANNIHILATOR,
    item_names.CORSAIR, item_names.ORACLE, item_names.VOID_RAY,
]
item_name_groups[ItemGroupNames.TAL_DARIM_UNITS] = [
    item_names.SUPPLICANT, item_names.SLAYER, item_names.HAVOC, item_names.BLOOD_HUNTER, item_names.ASCENDANT,
    item_names.VANGUARD, item_names.WRATHWALKER,
    item_names.SKIRMISHER, item_names.DESTROYER, item_names.SKYLORD, item_names.MOTHERSHIP,
]
item_name_groups[ItemGroupNames.PURIFIER_UNITS] = [
    item_names.SENTINEL, item_names.ADEPT, item_names.INSTIGATOR, item_names.ENERGIZER,
    item_names.STALWART, item_names.COLOSSUS, item_names.DISRUPTOR,
    item_names.MIRAGE, item_names.DAWNBRINGER, item_names.TRIREME, item_names.TEMPEST,
]
item_name_groups[ItemGroupNames.SOA_ITEMS] = soa_items = [
    *[item_name for item_name, item_data in items.item_table.items() if item_data.type == items.ProtossItemType.Spear_Of_Adun],
    item_names.SOA_PROGRESSIVE_PROXY_PYLON,
]
lotv_soa_items = [item_name for item_name in soa_items if item_name != item_names.SOA_PYLON_OVERCHARGE]
item_name_groups[ItemGroupNames.PROTOSS_GLOBAL_UPGRADES] = [
    item_name for item_name, item_data in items.item_table.items() if item_data.type == items.ProtossItemType.Solarite_Core
]
item_name_groups[ItemGroupNames.LOTV_GLOBAL_UPGRADES] = lotv_global_upgrades = [
    item_names.NEXUS_OVERCHARGE,
    item_names.ORBITAL_ASSIMILATORS,
    item_names.WARP_HARMONIZATION,
    item_names.MATRIX_OVERLOAD,
    item_names.GUARDIAN_SHELL,
    item_names.RECONSTRUCTION_BEAM,
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

item_name_groups[ItemGroupNames.WAR_COUNCIL] = [
    item_name for item_name, item_data in items.item_table.items()
    if item_data.type in (items.ProtossItemType.War_Council, items.ProtossItemType.War_Council_2)
]

item_name_groups[ItemGroupNames.OVERPOWERED_ITEMS] = [
    item_names.SIEGE_TANK_GRADUATING_RANGE,
    item_names.SIEGE_TANK_RESOURCE_EFFICIENCY,
    item_names.BATTLECRUISER_ATX_LASER_BATTERY,
    item_names.PROGRESSIVE_REGENERATIVE_BIO_STEEL,
    item_names.MECHANICAL_KNOW_HOW,
    item_names.MERCENARY_MUNITIONS,

    item_names.KERRIGAN_APOCALYPSE,
    item_names.KERRIGAN_DROP_PODS,
    item_names.KERRIGAN_SPAWN_LEVIATHAN,

    item_names.REAVER_RESOURCE_EFFICIENCY,
    item_names.SOA_TIME_STOP,
    item_names.SOA_SOLAR_LANCE,
    # Note: This is more an issue of having multiple ults at the same time, rather than solar bombardment in particular.
    # Can be removed from the list if we get an SOA ult combined cooldown or energy cost on it.
    item_names.SOA_SOLAR_BOMBARDMENT,
    item_names.MOTHERSHIP,
]
