import typing

from Options import Toggle, DefaultOnToggle, Option, Range, Choice, ItemDict, DeathLink


class RandomizeWeaponLocations(DefaultOnToggle):
    """Randomizes weapons (+76 locations)"""
    display_name = "Randomize Weapon Locations"


class RandomizeShieldLocations(DefaultOnToggle):
    """Randomizes shields (+24 locations)"""
    display_name = "Randomize Shield Locations"


class RandomizeArmorLocations(DefaultOnToggle):
    """Randomizes armor pieces (+97 locations)"""
    display_name = "Randomize Armor Locations"


class RandomizeRingLocations(DefaultOnToggle):
    """Randomizes rings (+49 locations)"""
    display_name = "Randomize Ring Locations"


class RandomizeSpellLocations(DefaultOnToggle):
    """Randomizes spells (+18 locations)"""
    display_name = "Randomize Spell Locations"


class RandomizeKeyLocations(DefaultOnToggle):
    """Randomizes items which unlock doors or bypass barriers"""
    display_name = "Randomize Key Locations"


class RandomizeBossSoulLocations(DefaultOnToggle):
    """Randomizes Boss Souls (+18 Locations)"""
    display_name = "Randomize Boss Soul Locations"


class RandomizeNPCLocations(Toggle):
    """Randomizes friendly NPC drops (meaning you will probably have to kill them) (+14 locations)"""
    display_name = "Randomize NPC Locations"


class RandomizeMiscLocations(Toggle):
    """Randomizes miscellaneous items (ashes, tomes, scrolls, etc.) to the pool. (+36 locations)"""
    display_name = "Randomize Miscellaneous Locations"


class RandomizeHealthLocations(Toggle):
    """Randomizes health upgrade items. (+21 locations)"""
    display_name = "Randomize Health Upgrade Locations"


class RandomizeProgressiveLocationsOption(Toggle):
    """Randomizes upgrade materials and consumables such as the titanite shards, firebombs, resin, etc...

    Instead of specific locations, these are progressive, so Titanite Shard #1 is the first titanite shard
    you pick up, regardless of whether it's from an enemy drop late in the game or an item on the ground in the
    first 5 minutes."""
    display_name = "Randomize Progressive Locations"


class PoolTypeOption(Choice):
    """Changes which non-progression items you add to the pool

    Shuffle: Items are picked from the locations being randomized
    Various: Items are picked from a list of all items in the game, but are the same type of item they replace"""
    display_name = "Pool Type"
    option_shuffle = 0
    option_various = 1


class GuaranteedItemsOption(ItemDict):
    """Guarantees that the specified items will be in the item pool"""
    display_name = "Guaranteed Items"


class AutoEquipOption(Toggle):
    """Automatically equips any received armor or left/right weapons."""
    display_name = "Auto-Equip"


class LockEquipOption(Toggle):
    """Lock the equipment slots so you cannot change your armor or your left/right weapons. Works great with the
    Auto-equip option."""
    display_name = "Lock Equipment Slots"


class NoWeaponRequirementsOption(Toggle):
    """Disable the weapon requirements by removing any movement or damage penalties.
    Permitting you to use any weapon early"""
    display_name = "No Weapon Requirements"


class NoSpellRequirementsOption(Toggle):
    """Disable the spell requirements permitting you to use any spell"""
    display_name = "No Spell Requirements"


class NoEquipLoadOption(Toggle):
    """Disable the equip load constraint from the game"""
    display_name = "No Equip Load"


class RandomizeInfusionOption(Toggle):
    """Enable this option to infuse a percentage of the pool of weapons and shields."""
    display_name = "Randomize Infusion"


class RandomizeInfusionPercentageOption(Range):
    """The percentage of weapons/shields in the pool to be infused if Randomize Infusion is toggled"""
    display_name = "Percentage of Infused Weapons"
    range_start = 0
    range_end = 100
    default = 33


class RandomizeWeaponLevelOption(Choice):
    """Enable this option to upgrade a percentage of the pool of weapons to a random value between the minimum and 
    maximum levels defined.

    All: All weapons are eligible, both basic and epic
    Basic: Only weapons that can be upgraded to +10
    Epic: Only weapons that can be upgraded to +5"""
    display_name = "Randomize Weapon Level"
    option_none = 0
    option_all = 1
    option_basic = 2
    option_epic = 3


class RandomizeWeaponLevelPercentageOption(Range):
    """The percentage of weapons in the pool to be upgraded if randomize weapons level is toggled"""
    display_name = "Percentage of Randomized Weapons"
    range_start = 0
    range_end = 100
    default = 33


class MinLevelsIn5WeaponPoolOption(Range):
    """The minimum upgraded value of a weapon in the pool of weapons that can only reach +5"""
    display_name = "Minimum Level of +5 Weapons"
    range_start = 0
    range_end = 5
    default = 1


class MaxLevelsIn5WeaponPoolOption(Range):
    """The maximum upgraded value of a weapon in the pool of weapons that can only reach +5"""
    display_name = "Maximum Level of +5 Weapons"
    range_start = 0
    range_end = 5
    default = 5


class MinLevelsIn10WeaponPoolOption(Range):
    """The minimum upgraded value of a weapon in the pool of weapons that can reach +10"""
    display_name = "Minimum Level of +10 Weapons"
    range_start = 0
    range_end = 10
    default = 1


class MaxLevelsIn10WeaponPoolOption(Range):
    """The maximum upgraded value of a weapon in the pool of weapons that can reach +10"""
    display_name = "Maximum Level of +10 Weapons"
    range_start = 0
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
    and being able to get into Irithyll of the Boreal Valley."""
    display_name = "Late DLC"


class EnableDLCOption(Toggle):
    """To use this option, you must own both the ASHES OF ARIANDEL and the RINGED CITY DLC"""
    display_name = "Enable DLC"


dark_souls_options: typing.Dict[str, Option] = {
    "enable_weapon_locations": RandomizeWeaponLocations,
    "enable_shield_locations": RandomizeShieldLocations,
    "enable_armor_locations": RandomizeArmorLocations,
    "enable_ring_locations": RandomizeRingLocations,
    "enable_spell_locations": RandomizeSpellLocations,
    "enable_key_locations": RandomizeKeyLocations,
    "enable_boss_locations": RandomizeBossSoulLocations,
    "enable_npc_locations": RandomizeNPCLocations,
    "enable_misc_locations": RandomizeMiscLocations,
    "enable_health_upgrade_locations": RandomizeHealthLocations,
    "enable_progressive_locations": RandomizeProgressiveLocationsOption,
    "pool_type": PoolTypeOption,
    "guaranteed_items": GuaranteedItemsOption,
    "auto_equip": AutoEquipOption,
    "lock_equip": LockEquipOption,
    "no_weapon_requirements": NoWeaponRequirementsOption,
    "randomize_infusion": RandomizeInfusionOption,
    "randomize_infusion_percentage": RandomizeInfusionPercentageOption,
    "randomize_weapon_level": RandomizeWeaponLevelOption,
    "randomize_weapon_level_percentage": RandomizeWeaponLevelPercentageOption,
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
