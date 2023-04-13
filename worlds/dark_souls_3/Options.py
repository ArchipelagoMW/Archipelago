import typing
from Options import Toggle, Option, Range, Choice, DeathLink

class RandomizeWeaponLocations(Toggle):
    """Adds Weapon Locations to the pool. (+94 checks/items)"""
    display_name ="Randomize Weapon Locations"


class RandomizeShieldLocations(Toggle):
    """Adds Shield Locations to the pool. (+23 checks/items)"""
    display_name ="Randomize Shield Locations"


class RandomizeArmorLocations(Toggle):
    """Adds Armor Locations to the pool. (+89 checks/items)"""
    display_name ="Randomize Armor Locations"


class RandomizeRingLocations(Toggle):
    """Adds Ring Locations to the pool. (+46 checks/items)"""
    display_name ="Randomize Ring Locations"


class RandomizeSpellLocations(Toggle):
    """Adds Spell Locations to the pool. (+19 checks/items)"""
    display_name ="Randomize Spell Locations"


class RandomizeMiscLocations(Toggle):
    """Adds Miscellaneous Locations (Ashes, Tomes, Scrolls, etc.) to the pool. (+28 checks/items)"""
    display_name ="Randomize Miscellaneous Locations"


class RandomizeHealthLocations(Toggle):
    """Adds Health Upgrade Locations to the pool. (+20 checks/items)"""
    display_name ="Randomize Health Upgrade Locations"


class RandomizeNPCLocations(Toggle):
    """Adds Friendly NPC Locations to the pool. (Irina, Cornyx, Karla, Orbeck) (+13 checks/items)"""
    display_name ="Randomize NPC Locations"


class AutoEquipOption(Toggle):
    """Automatically equips any received armor or left/right weapons."""
    display_name = "Auto-equip"


class LockEquipOption(Toggle):
    """Lock the equipment slots so you cannot change your armor or your left/right weapons. Works great with the
    Auto-equip option."""
    display_name = "Lock Equipement Slots"


class NoWeaponRequirementsOption(Toggle):
    """Disable the weapon requirements by removing any movement or damage penalties.
    Permitting you to use any weapon early"""
    display_name = "No Weapon Requirements"


class NoSpellRequirementsOption(Toggle):
    """Disable the spell requirements permitting you to use any spell"""
    display_name = "No Spell Requirements"


class NoEquipLoadOption(Toggle):
    """Disable the equip load constraint from the game"""
    display_name = "No Equip load"


class RandomizeWeaponsLevelOption(Choice):
    """Enable this option to upgrade a percentage of the pool of weapons to a random value between the minimum and 
    maximum levels defined. 
    all: All weapons are eligible, both basic and epic
    basic: Only weapons that can be upgraded to +10
    epic: Only weapons that can be upgraded to +5"""
    display_name = "Randomize weapons level"
    option_none = 0
    option_all = 1
    option_basic = 2
    option_epic = 3


class RandomizeWeaponsLevelPercentageOption(Range):
    """The percentage of weapons in the pool to be upgraded if randomize weapons level is toggled"""
    display_name = "Percentage of randomized weapons"
    range_start = 1
    range_end = 100
    default = 33


class MinLevelsIn5WeaponPoolOption(Range):
    """The minimum upgraded value of a weapon in the pool of weapons that can only reach +5"""
    display_name = "Minimum level of +5 weapons"
    range_start = 1
    range_end = 5
    default = 1


class MaxLevelsIn5WeaponPoolOption(Range):
    """The maximum upgraded value of a weapon in the pool of weapons that can only reach +5"""
    display_name = "Maximum level of +5 weapons"
    range_start = 1
    range_end = 5
    default = 5


class MinLevelsIn10WeaponPoolOption(Range):
    """The minimum upgraded value of a weapon in the pool of weapons that can reach +10"""
    display_name = "Minimum level of +10 weapons"
    range_start = 1
    range_end = 10
    default = 1


class MaxLevelsIn10WeaponPoolOption(Range):
    """The maximum upgraded value of a weapon in the pool of weapons that can reach +10"""
    display_name = "Maximum level of +10 weapons"
    range_start = 1
    range_end = 10
    default = 10


class LateBasinOfVowsOption(Toggle):
    """This option makes it so the Basin of Vows is still randomized, but guarantees you that you wont have to venture into
    Lothric Castle to find your Small Lothric Banner to get out of High Wall of Lothric. So you may find Basin of Vows early, 
    but you wont have to fight Dancer to find your Small Lothric Banner."""
    display_name = "Late Basin of Vows"


class LateDLCOption(Toggle):
    """This option makes it so you are guaranteed to find your Small Doll without having to venture off into the DLC, 
    effectively putting anything in the DLC in logic after finding both Contraption Key and Small Doll, 
    and being able to get into Irithyll of the Boreal Valley"""
    display_name = "Late DLC"


class EnableProgressiveLocationsOption(Toggle):
    """Randomize upgrade materials such as the titanite shards, the estus shards and the consumables"""
    display_name = "Randomize materials, weapon upgrade shards, and consumables (+176 checks/items)"


class EnableDLCOption(Toggle):
    """To use this option, you must own both the ASHES OF ARIANDEL and the RINGED CITY DLC"""
    display_name = "Add the DLC Items and Locations to the pool (+81 checks/items)"


dark_souls_options: typing.Dict[str, type(Option)] = {
    "enable_weapon_locations": RandomizeWeaponLocations,
    "enable_shield_locations": RandomizeShieldLocations,
    "enable_armor_locations": RandomizeArmorLocations,
    "enable_ring_locations": RandomizeRingLocations,
    "enable_spell_locations": RandomizeSpellLocations,
    "enable_misc_locations": RandomizeMiscLocations,
    "enable_health_upgrade_locations": RandomizeHealthLocations,
    "enable_npc_locations": RandomizeNPCLocations,
    "auto_equip": AutoEquipOption,
    "lock_equip": LockEquipOption,
    "no_weapon_requirements": NoWeaponRequirementsOption,
    "randomize_weapons_level": RandomizeWeaponsLevelOption,
    "randomize_weapons_percentage": RandomizeWeaponsLevelPercentageOption,
    "min_levels_in_5": MinLevelsIn5WeaponPoolOption,
    "max_levels_in_5": MaxLevelsIn5WeaponPoolOption,
    "min_levels_in_10": MinLevelsIn10WeaponPoolOption,
    "max_levels_in_10": MaxLevelsIn10WeaponPoolOption,
    "late_basin_of_vows": LateBasinOfVowsOption,
    "late_dlc": LateDLCOption,
    "no_spell_requirements": NoSpellRequirementsOption,
    "no_equip_load": NoEquipLoadOption,
    "death_link": DeathLink,
    "enable_progressive_locations": EnableProgressiveLocationsOption,
    "enable_dlc": EnableDLCOption,
}

