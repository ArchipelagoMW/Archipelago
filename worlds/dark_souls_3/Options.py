import typing
from Options import Toggle, Option, Range, Choice, DeathLink


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
    """Force the Basin of Vows to be located as a reward of defeating Pontiff Sulyvahn. It permits to ease the
    progression by preventing having to kill the Dancer of the Boreal Valley as the first boss"""
    display_name = "Late Basin of Vows"


class EnableProgressiveLocationsOption(Toggle):
    """Randomize upgrade materials such as the titanite shards, the estus shards and the consumables"""
    display_name = "Randomize materials, Estus shards and consumables (+196 checks/items)"


class EnableDLCOption(Toggle):
    """To use this option, you must own both the ASHES OF ARIANDEL and the RINGED CITY DLC"""
    display_name = "Add the DLC Items and Locations to the pool (+81 checks/items)"


dark_souls_options: typing.Dict[str, type(Option)] = {
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
    "no_spell_requirements": NoSpellRequirementsOption,
    "no_equip_load": NoEquipLoadOption,
    "death_link": DeathLink,
    "enable_progressive_locations": EnableProgressiveLocationsOption,
    "enable_dlc": EnableDLCOption,
}

