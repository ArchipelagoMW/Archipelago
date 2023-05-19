import typing
from Options import Toggle, DefaultOnToggle, Option, Range, Choice, DeathLink


class RandomizeWeaponLocations(DefaultOnToggle):
    """Randomizes weapons (+86 locations)"""
    display_name = "Randomize Weapon Locations"


class RandomizeShieldLocations(DefaultOnToggle):
    """Randomizes shields (+24 locations)"""
    display_name = "Randomize Shield Locations"


class RandomizeArmorLocations(DefaultOnToggle):
    """Randomizes armor pieces (+93 locations)"""
    display_name = "Randomize Armor Locations"


class RandomizeRingLocations(DefaultOnToggle):
    """Randomizes rings (+48 locations)"""
    display_name = "Randomize Ring Locations"


class RandomizeSpellLocations(DefaultOnToggle):
    """Randomizes spells (+19 locations)"""
    display_name = "Randomize Spell Locations"


class RandomizeKeyLocations(DefaultOnToggle):
    """Randomizes items which unlock doors or bypass barriers"""
    display_name = "Randomize NPC Locations"


class RandomizeNPCLocations(Toggle):
    """Randomizes friendly NPC drops (meaning you will probably have to kill them) (+14 locations)"""
    display_name = "Randomize NPC Locations"


class RandomizeMiscLocations(Toggle):
    """Randomizes miscellaneous items (ashes, tomes, scrolls, etc.) to the pool. (+27 locations)"""
    display_name = "Randomize Miscellaneous Locations"


class RandomizeHealthLocations(Toggle):
    """Randomizes health upgrade items. (+20 locations)"""
    display_name = "Randomize Health Upgrade Locations"


class RandomizeProgressiveLocationsOption(Toggle):
    """Randomizes upgrade materials and consumables such as the titanite shards, firebombs, resin, etc...

    Instead of specific locations, these are progressive, so Titanite Shard #1 is the first titanite shard
    you pick up, regardless of whether it's from an enemy drop late in the game or an item on the ground in the
    first 5 minutes."""
    display_name = "Randomize Progressive Locations"


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


class EnableDLCOption(Toggle):
    """To use this option, you must own both the ASHES OF ARIANDEL and the RINGED CITY DLC"""
    display_name = "Add the DLC Items and Locations to the pool (+92 locations)"


dark_souls_options: typing.Dict[str, type(Option)] = {
    "enable_weapon_locations": RandomizeWeaponLocations,
    "enable_shield_locations": RandomizeShieldLocations,
    "enable_armor_locations": RandomizeArmorLocations,
    "enable_ring_locations": RandomizeRingLocations,
    "enable_spell_locations": RandomizeSpellLocations,
    "enable_key_locations": RandomizeKeyLocations,
    "enable_npc_locations": RandomizeNPCLocations,
    "enable_misc_locations": RandomizeMiscLocations,
    "enable_health_upgrade_locations": RandomizeHealthLocations,
    "enable_progressive_locations": RandomizeProgressiveLocationsOption,
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
    "enable_dlc": EnableDLCOption,
}
