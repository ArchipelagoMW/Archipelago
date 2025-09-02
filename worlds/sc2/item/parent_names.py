"""
Identifiers for complex item parent structures.
Defined separately from item_parents to avoid a circular import
item_names -> item_parent_names -> item_tables -> item_parents
"""

# Terran
DOMINION_TROOPER_WEAPONS = "Dominion Trooper Weapons"
INFANTRY_UNITS = "Infantry Units"
INFANTRY_WEAPON_UNITS = "Infantry Weapon Units"
ORBITAL_COMMAND_AND_PLANETARY = "Orbital Command Abilities + Planetary Fortress"  # MULE | Scan | Supply Drop
SIEGE_TANK_AND_TRANSPORT = "Siege Tank + Transport"
SIEGE_TANK_AND_MEDIVAC = "Siege Tank + Medivac"
SPIDER_MINE_SOURCE = "Spider Mine Source"
STARSHIP_UNITS = "Starship Units"
STARSHIP_WEAPON_UNITS = "Starship Weapon Units"
VEHICLE_UNITS = "Vehicle Units"
VEHICLE_WEAPON_UNITS = "Vehicle Weapon Units"
TERRAN_MERCENARIES = "Terran Mercenaries"

# Zerg
ANY_NYDUS_WORM = "Any Nydus Worm"
BANELING_SOURCE = "Any Baneling Source"  # Baneling aspect | Kerrigan Spawn Banelings
INFESTED_UNITS = "Infested Units"
INFESTED_FACTORY_OR_STARPORT = "Infested Factory or Starport"
MORPH_SOURCE_AIR = "Air Morph Source"  # Morphling | Mutalisk | Corruptor
MORPH_SOURCE_ROACH = "Roach Morph Source"  # Morphling | Roach
MORPH_SOURCE_ZERGLING = "Zergling Morph Source"  # Morphling | Zergling
MORPH_SOURCE_HYDRALISK = "Hydralisk Morph Source"  # Morphling | Hydralisk
MORPH_SOURCE_ULTRALISK = "Ultralisk Morph Source"  # Morphling | Ultralisk
ZERG_UPROOTABLE_BUILDINGS = "Zerg Uprootable Buildings"
ZERG_MELEE_ATTACKER = "Zerg Melee Attacker"
ZERG_MISSILE_ATTACKER = "Zerg Missile Attacker"
ZERG_CARAPACE_UNIT = "Zerg Carapace Unit"
ZERG_FLYING_UNIT = "Zerg Flying Unit"
ZERG_MERCENARIES = "Zerg Mercenaries"
ZERG_OUROBOUROS_CONDITION = "Zerg Ourobouros Condition"

# Protoss
ARCHON_SOURCE = "Any Archon Source"
CARRIER_CLASS = "Carrier Class"
CARRIER_OR_TRIREME = "Carrier | Trireme"
DARK_ARCHON_SOURCE = "Dark Archon Source"
DARK_TEMPLAR_CLASS = "Dark Templar Class"
STORM_CASTER = "Storm Caster"
IMMORTAL_OR_ANNIHILATOR = "Immortal | Annihilator"
PHOENIX_CLASS = "Phoenix Class"
SENTRY_CLASS = "Sentry Class"
SENTRY_CLASS_OR_SHIELD_BATTERY = "Sentry Class | Shield Battery"
STALKER_CLASS = "Stalker Class"
SUPPLICANT_AND_ASCENDANT = "Supplicant + Ascendant"
VOID_RAY_CLASS = "Void Ray Class"
ZEALOT_OR_SENTINEL_OR_CENTURION = "Zealot | Sentinel | Centurion"
PROTOSS_STATIC_DEFENSE = "Protoss Static Defense"
PROTOSS_ATTACKING_BUILDING = "Protoss Attacking Structure"
SCOUT_CLASS = "Scout Class"
SCOUT_OR_OPPRESSOR_OR_MISTWING = "Scout | Oppressor | Mist Wing"
