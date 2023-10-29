import typing
from dataclasses import dataclass

from Options import Choice, DeathLink, DefaultOnToggle, ExcludeLocations, ItemDict, Option, PerGameCommonOptions, Range, Toggle


class RandomizeWeaponLocations(DefaultOnToggle):
    """Randomizes weapons (+101 checks)"""
    display_name = "Randomize Weapon Locations"


class RandomizeShieldLocations(DefaultOnToggle):
    """Randomizes shields (+32 checks)"""
    display_name = "Randomize Shield Locations"


class RandomizeArmorLocations(DefaultOnToggle):
    """Randomizes armor pieces (+216 checks)"""
    display_name = "Randomize Armor Locations"


class RandomizeRingLocations(DefaultOnToggle):
    """Randomizes rings (+64 checks, +101 with NG+ locations)"""
    display_name = "Randomize Ring Locations"


class RandomizeSpellLocations(DefaultOnToggle):
    """Randomizes spells (+35 checks)"""
    display_name = "Randomize Spell Locations"


class RandomizeUpgradeLocations(DefaultOnToggle):
    """Randomizes titanite and gems (+220 checks)

    By default, these locations will never include progression items, so they
    aren't mandatory checks. You can override this by customizing the
    "exclude_locations" field in your YAML config. (For example,
    "exclude_locations: []" will allow progression items in every unmissable
    location.)
    """
    display_name = "Randomize Upgrade Locations"


class RandomizeKeyLocations(DefaultOnToggle):
    """Randomizes items which unlock doors or bypass barriers.

    If these aren't randomized, the route through the game will remain unchanged.
    """
    display_name = "Randomize Key Locations"


class RandomizeBossSoulLocations(DefaultOnToggle):
    """Randomizes boss souls (+22 Locations)"""
    display_name = "Randomize Boss Soul Locations"


class RandomizeNPCLocations(DefaultOnToggle):
    """Randomizes friendly NPC drops and rewards (+34 checks)

    Although all NPC drops will be randomized, progression items will only
    appear in drops that aren't possible to lock yourself out of. Progression
    items may be available by killing NPCs, but you can always do their quest
    instead if you want.

    """
    display_name = "Randomize NPC Locations"


class RandomizeUniqueLocations(DefaultOnToggle):
    """Randomizes unique items (ashes, tomes, scrolls, etc.) (+36 checks)"""
    display_name = "Randomize Miscellaneous Locations"


class RandomizeMiscLocations(DefaultOnToggle):
    """Randomizes miscellaneous items (arrows, firebombs, soul items, etc.) (+388 locations)

    By default, these locations will never include progression items, so they
    aren't mandatory checks. You can override this by customizing the
    "exclude_locations" field in your YAML config. (For example,
    "exclude_locations: []" will allow progression items in every unmissable
    location.)
    """
    display_name = "Randomize Miscellaneous Locations"


class RandomizeHealthLocations(DefaultOnToggle):
    """Randomizes health upgrade items. (+21 checks)"""
    display_name = "Randomize Health Upgrade Locations"


class RandomizeStartingLoadout(DefaultOnToggle):
    """Randomizes the equipment characters begin with."""
    display_name = "Randomize Starting Loadout"


class RequireOneHandedStartingWeapons(Toggle):
    """Require starting equipment to be usable one-handed."""
    display_name = "Require One-Handed Starting Weapons"


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
    """Lock the equipment slots so you cannot change your armor or your left/right weapons. Works great with the Auto-equip option."""
    display_name = "Lock Equipment Slots"


class NoWeaponRequirementsOption(Toggle):
    """Disable the weapon requirements by removing any movement or damage penalties, permitting you to use any weapon early."""
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
    """Enable this option to upgrade a percentage of the pool of weapons to a
    random value between the minimum and maximum levels defined.

    All: All weapons are eligible, both basic and epic
    Basic: Only weapons that can be upgraded to +10
    Epic: Only weapons that can be upgraded to +5
    """
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
    """This option makes it so the Basin of Vows is still randomized, but guarantees you that you wont have to venture into Lothric Castle to find your Small Lothric Banner to get out of High Wall of Lothric. So you may find Basin of Vows early, but you wont have to fight Dancer to find your Small Lothric Banner."""
    display_name = "Late Basin of Vows"


class LateDLCOption(Toggle):
    """This option makes it so you are guaranteed to find your Small Doll without having to venture off into the DLC, effectively putting anything in the DLC in logic after finding both Contraption Key and Small Doll, and being able to get into Irithyll of the Boreal Valley."""
    display_name = "Late DLC"


class EnableDLCOption(Toggle):
    """To use this option, you must own both the ASHES OF ARIANDEL and the RINGED CITY DLC"""
    display_name = "Enable DLC"


class EnableNGPOption(Toggle):
    """Whether to include items and locations exclusive to NG+ cycles"""
    display_name = "Enable NG+"


class DS3ExcludeLocations(ExcludeLocations):
    """Prevent these locations from having an important item"""
    default = {"Hidden", "Small Crystal Lizards", "Miscellaneous"}


@dataclass
class DarkSouls3Options(PerGameCommonOptions):
    enable_weapon_locations: RandomizeWeaponLocations
    enable_shield_locations: RandomizeShieldLocations
    enable_armor_locations: RandomizeArmorLocations
    enable_ring_locations: RandomizeRingLocations
    enable_spell_locations: RandomizeSpellLocations
    enable_upgrade_locations: RandomizeUpgradeLocations
    enable_key_locations: RandomizeKeyLocations
    enable_boss_locations: RandomizeBossSoulLocations
    enable_npc_locations: RandomizeNPCLocations
    enable_unique_locations: RandomizeUniqueLocations
    enable_misc_locations: RandomizeMiscLocations
    enable_health_upgrade_locations: RandomizeHealthLocations
    random_starting_loadout: RandomizeStartingLoadout
    require_one_handed_starting_weapons: RequireOneHandedStartingWeapons
    pool_type: PoolTypeOption
    guaranteed_items: GuaranteedItemsOption
    auto_equip: AutoEquipOption
    lock_equip: LockEquipOption
    no_weapon_requirements: NoWeaponRequirementsOption
    randomize_infusion: RandomizeInfusionOption
    randomize_infusion_percentage: RandomizeInfusionPercentageOption
    randomize_weapon_level: RandomizeWeaponLevelOption
    randomize_weapon_level_percentage: RandomizeWeaponLevelPercentageOption
    min_levels_in_5: MinLevelsIn5WeaponPoolOption
    max_levels_in_5: MaxLevelsIn5WeaponPoolOption
    min_levels_in_10: MinLevelsIn10WeaponPoolOption
    max_levels_in_10: MaxLevelsIn10WeaponPoolOption
    late_basin_of_vows: LateBasinOfVowsOption
    late_dlc: LateDLCOption
    no_spell_requirements: NoSpellRequirementsOption
    no_equip_load: NoEquipLoadOption
    death_link: DeathLink
    enable_dlc: EnableDLCOption
    enable_ngp: EnableNGPOption
    exclude_locations: DS3ExcludeLocations
