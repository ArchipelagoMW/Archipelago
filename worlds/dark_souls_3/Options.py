from copy import deepcopy
from dataclasses import dataclass
import json
import typing

from Options import Choice, DeathLink, DefaultOnToggle, ExcludeLocations, ItemDict, NamedRange, Option, PerGameCommonOptions, Range, Toggle, VerifyKeys


class ExcludedLocationsOption(Choice):
    """Which items can be placed in excluded locations in DS3.

    * Unnecessary: Excluded locations can't have progression items, but they can
      have useful items.
    * Unimportant: Neither progression items nor useful items can be placed in
      excluded locations.
    * Unrandomized: Excluded locations always contain the same item as in
      vanilla Dark Souls III.

    A "progression item" is anything that's required to unlock another location
    in some game. A "useful item" is something each game defines individually,
    usually items that are quite desirable but not strictly necessary.
    """
    display_name = "Excluded Locations"
    option_unnecessary = 1
    option_unimportant = 2
    option_unrandomized = 3
    default = 2


class MissableLocationsOption(Choice):
    """Which items can be placed in locations that can be permanently missed.

    * Unnecessary: Missable locations can't have progression items, but they can
      have useful items.
    * Unimportant: Neither progression items nor useful items can be placed in
      missable locations.
    * Unrandomized: Missable locations always contain the same item as in
      vanilla Dark Souls III.

    A "progression item" is anything that's required to unlock another location
    in some game. A "useful item" is something each game defines individually,
    usually items that are quite desirable but not strictly necessary.
    """
    display_name = "Missable Locations"
    option_unnecessary = 1
    option_unimportant = 2
    option_unrandomized = 3
    default = 2
    

class RandomizeWeaponLocations(DefaultOnToggle):
    """DEPRECATED (use "Excluded Locations" options instead)

    Setting this to false is now equivalent to adding "Weapons" to the "Exclude
    Locations" option. It does _not_ cause the locations not be randomized
    unless "Excluded Locations" is also set to "Unrandomized".
    """
    display_name = "Randomize Weapon Locations"


class RandomizeShieldLocations(DefaultOnToggle):
    """DEPRECATED (use "Excluded Locations" options instead)

    Setting this to false is now equivalent to adding "Shields" to the "Exclude
    Locations" option. It does _not_ cause the locations not be randomized
    unless "Excluded Locations" is also set to "Unrandomized".
    """
    display_name = "Randomize Shield Locations"


class RandomizeArmorLocations(DefaultOnToggle):
    """DEPRECATED (use "Excluded Locations" options instead)

    Setting this to false is now equivalent to adding "Armor" to the "Exclude
    Locations" option. It does _not_ cause the locations not be randomized
    unless "Excluded Locations" is also set to "Unrandomized".
    """
    display_name = "Randomize Armor Locations"


class RandomizeRingLocations(DefaultOnToggle):
    """DEPRECATED (use "Excluded Locations" options instead)

    Setting this to false is now equivalent to adding "Rings" to the "Exclude
    Locations" option. It does _not_ cause the locations not be randomized
    unless "Excluded Locations" is also set to "Unrandomized".
    """
    display_name = "Randomize Ring Locations"


class RandomizeSpellLocations(DefaultOnToggle):
    """DEPRECATED (use "Excluded Locations" options instead)

    Setting this to false is now equivalent to adding "Spells" to the "Exclude
    Locations" option. It does _not_ cause the locations not be randomized
    unless "Excluded Locations" is also set to "Unrandomized".
    """
    display_name = "Randomize Spell Locations"


class RandomizeKeyLocations(DefaultOnToggle):
    """DEPRECATED (use "Excluded Locations" options instead)

    Setting this to false is now equivalent to adding "Progression" to the
    "Exclude Locations" option. It does _not_ cause the locations not be
    randomized unless "Excluded Locations" is also set to "Unrandomized".
    """
    display_name = "Randomize Key Locations"


class RandomizeBossSoulLocations(DefaultOnToggle):
    """DEPRECATED (use "Excluded Locations" options instead)

    Setting this to false is now equivalent to adding "Boss Souls" to the
    "Exclude Locations" option. It does _not_ cause the locations not be
    randomized unless "Excluded Locations" is also set to "Unrandomized".
    """
    display_name = "Randomize Boss Soul Locations"


class RandomizeNPCLocations(DefaultOnToggle):
    """DEPRECATED (use "Excluded Locations" options instead)

    Setting this to false is now equivalent to adding "Friendly NPC Rewards" to
    the "Exclude Locations" option. It does _not_ cause the locations not be
    randomized unless "Excluded Locations" is also set to "Unrandomized".
    """
    display_name = "Randomize NPC Locations"


class RandomizeMiscLocations(DefaultOnToggle):
    """DEPRECATED (use "Excluded Locations" options instead)

    Setting this to false is now equivalent to adding "Unique" to the "Exclude
    Locations" option. It does _not_ cause the locations not be randomized
    unless "Excluded Locations" is also set to "Unrandomized".
    """
    display_name = "Randomize Miscellaneous Locations"


class RandomizeHealthLocations(DefaultOnToggle):
    """DEPRECATED (use "Excluded Locations" options instead)

    Setting this to false is now equivalent to adding "Healing" to the "Exclude
    Locations" option. It does _not_ cause the locations not be randomized
    unless "Excluded Locations" is also set to "Unrandomized".
    """
    display_name = "Randomize Health Locations"


class RandomizeProgressiveLocationsOption(DefaultOnToggle):
    """DEPRECATED (use "Excluded Locations" options instead)

    Setting this to false is now equivalent to adding "Miscellaneous" to the
    "Exclude Locations" option. It does _not_ cause the locations not be
    randomized unless "Excluded Locations" is also set to "Unrandomized".
    """
    display_name = "Randomize Progressive Locations"


class SmoothSoulItemsOption(DefaultOnToggle):
    """Whether to distribute soul items in a similar order as the base game.

    By default, soul items will be distributed totally randomly. If this is set,
    less valuable soul items will generally appear in earlier spheres and more
    valuable ones will generally appear later.
    """
    display_name = "Smooth Soul Items"


class SmoothUpgradeItemsOption(DefaultOnToggle):
    """Whether to distribute upgrade items in a similar order as the base game.

    By default, upgrade items will be distributed totally randomly. If this is
    set, lower-level upgrade items will generally appear in earlier spheres and
    higher-level ones will generally appear later.
    """
    display_name = "Smooth Upgrade Items"


class SmoothUpgradedWeaponsOption(DefaultOnToggle):
    """Whether to distribute upgraded weapons in a similar order as the base game.

    By default, upgraded weapons will be distributed totally randomly. If this
    is set, lower-level weapons will generally appear in earlier spheres and
    higher-level ones will generally appear later.
    """
    display_name = "Smooth Upgraded Weapons"


class RandomizeStartingLoadout(DefaultOnToggle):
    """Randomizes the equipment characters begin with."""
    display_name = "Randomize Starting Loadout"


class RequireOneHandedStartingWeapons(DefaultOnToggle):
    """Require starting equipment to be usable one-handed."""
    display_name = "Require One-Handed Starting Weapons"


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


class RandomizeInfusionPercentageOption(NamedRange):
    """The percentage of weapons/shields in the pool to be infused if Randomize Infusion is toggled"""
    display_name = "Percentage of Infused Weapons"
    range_start = 0
    range_end = 100
    default = 33
    # 3/155 weapons are infused in the base game, or about 2%
    special_range_names = {"similar to base game": 2}


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


class EarlySmallLothricBanner(Choice):
    """This option makes it so the user can choose to force the Small Lothric Banner into an early sphere in their world or
    into an early sphere across all worlds."""
    display_name = "Early Small Lothric Banner"
    option_off = 0
    option_early_global = 1
    option_early_local = 2
    default = option_off


class LateBasinOfVowsOption(Choice):
    """This option makes it so the Basin of Vows is still randomized, but you can choose the requirements to venture into Lothric Castle.
    "Off": You may have to enter Lothric Castle and the areas beyond it before finding your Small Lothric Banner.
    "After Small Lothric Banner": You are guaranteed to find your Small Lothric Banner before needing to enter Lothric Castle.
    "After Small Doll": You are guaranteed to find your Small Lothric Banner and your Small Doll before needing to enter Lothric Castle."""
    display_name = "Late Basin of Vows"
    option_off = 0
    alias_false = 0
    option_after_small_lothric_banner = 1
    alias_true = 1
    option_after_small_doll = 2


class LateDLCOption(Choice):
    """This option makes it so the Small Doll is still randomized, but you can choose the requirements to venture into Painted World of Ariandel.
    "Off": You may have to enter Ariandel and the areas beyond it before finding your Small Doll.
    "After Small Doll": You are guaranteed to find your Small Doll before needing to enter Ariandel.
    "After Basin": You are guaranteed to find your Small Doll and your Basin of Vows before needing to enter Ariandel."""
    display_name = "Late DLC"
    option_off = 0
    alias_false = 0
    option_after_small_doll = 1
    alias_true = 1
    option_after_basin = 2


class EnableDLCOption(Toggle):
    """To use this option, you must own both the ASHES OF ARIANDEL and the RINGED CITY DLC"""
    display_name = "Enable DLC"


class EnableNGPOption(Toggle):
    """Whether to include items and locations exclusive to NG+ cycles"""
    display_name = "Enable NG+"


class RandomizeEnemiesOption(DefaultOnToggle):
    """Whether to randomize enemy and boss placements.

    If this is enabled, the Storm Ruler sword is granted immediately upon meeting Yhorm the Giant
    instead of being randomized into the world.
    """
    display_name = "Randomize Enemies"


class RandomEnemyPresetOption(Option[typing.Dict[str, typing.Any]], VerifyKeys):
    """The YAML preset for the offline enemy randomizer.
    
    See the offline randomizer documentation in randomizer\\presets\\README.txt for details.
    """
    display_name = "Random Enemy Preset"
    supports_weighting = False
    default = {}

    valid_keys = ["Description", "RecommendFullRandomization", "RecommendNoEnemyProgression",
                 "OopsAll", "Boss", "Miniboss", "Basic", "BuffBasicEnemiesAsBosses",
                 "DontRandomize", "RemoveSource", "Enemies"]

    def __init__(self, value: typing.Dict[str, typing.Any]):
        self.value = deepcopy(value)

    def get_option_name(self, value: typing.Dict[str, typing.Any]):
        return json.dumps(value)

    @classmethod
    def from_any(cls, data: typing.Dict[str, typing.Any]) -> "RandomEnemyPresetOption":
        if type(data) == dict:
            cls.verify_keys(data)
            return cls(data)
        else:
            raise NotImplementedError(f"Must be a dictionary, got {type(data)}")


class RandomizeMimicsWithEnemiesOption(Toggle):
    """Whether to mix Mimics into the main enemy pool.

    If this is enabled, Mimics will be replaced by normal enemies who drop the Mimic rewards on
    death, and Mimics will be placed randomly in place of normal enemies. It's recommended to
    enable Impatient Mimcs as well if you enable this.

    This is ignored unless enemies are randomized.
    """
    display_name = "Randomize Mimics With Enemies"


class RandomizeSmallCrystalLizardsWithEnemiesOption(Toggle):
    """Whether to mix small Crystal Lizards into the main enemy pool.

    If this is enabled, Crystal Lizards will be replaced by normal enemies who drop the Crystal
    Lizard rewards on death, and Crystal Lizards will be placed randomly in place of normal
    enemies.

    This is ignored unless enemies are randomized.
    """
    display_name = "Randomize Small Crystal Lizards With Enemies"


class ReduceHarmlessEnemiesOption(Toggle):
    """Whether to reduce the frequency that "harmless" enemies appear.

    Enable this to add a bit of extra challenge. This severely limits the number of enemies that
    are slow to aggro, slow to attack, and do very little damage that appear in the enemy pool.

    This is ignored unless enemies are randomized.
    """
    display_name = "Reduce Harmless Enemies"


class SimpleEarlyBossesOption(DefaultOnToggle):
    """Whether to avoid replacing Iudex Gundyr and Vordt with late bosses.

    This excludes all bosses after Dancer of the Boreal Valley from these two boss fights. Disable
    it for a chance at a much harder early game.

    This is ignored unless enemies are randomized.
    """
    display_name = "Simple Early Bosses"


class ScaleEnemiesOption(DefaultOnToggle):
    """Whether to scale randomized enemy stats to match the areas in which they appear.

    Disabling this will tend to make the early game much more difficult and the late game much
    easier.

    This is ignored unless enemies are randomized.
    """
    display_name = "Scale Enemies"


class AllChestsAreMimicsOption(Toggle):
    """Whether to replace all chests with mimics that drop the same items.

    If "Randomize Mimics With Enemies" is set, these chests will instead be replaced with random
    enemies that drop the same items.

    This is ignored unless enemies are randomized.
    """
    display_name = "All Chests Are Mimics"


class ImpatientMimicsOption(Toggle):
    """Whether mimics should attack as soon as you get close.

    This is ignored unless enemies are randomized.
    """
    display_name = "Impatient Mimics"


class DS3ExcludeLocations(ExcludeLocations):
    """Prevent these locations from having an important item"""
    default = {"Hidden", "Small Crystal Lizards", "Upgrade", "Small Souls", "Miscellaneous"}


@dataclass
class DarkSouls3Options(PerGameCommonOptions):
    excluded_locations: ExcludedLocationsOption
    missable_locations: MissableLocationsOption
    enable_weapon_locations: RandomizeWeaponLocations
    enable_shield_locations: RandomizeShieldLocations
    enable_armor_locations: RandomizeArmorLocations
    enable_ring_locations: RandomizeRingLocations
    enable_spell_locations: RandomizeSpellLocations
    enable_key_locations: RandomizeKeyLocations
    enable_boss_locations: RandomizeBossSoulLocations
    enable_npc_locations: RandomizeNPCLocations
    enable_misc_locations: RandomizeMiscLocations
    enable_health_upgrade_locations: RandomizeHealthLocations
    enable_progressive_locations: RandomizeProgressiveLocationsOption
    smooth_soul_items: SmoothSoulItemsOption
    smooth_upgrade_items: SmoothUpgradeItemsOption
    smooth_upgraded_weapons: SmoothUpgradedWeaponsOption
    random_starting_loadout: RandomizeStartingLoadout
    require_one_handed_starting_weapons: RequireOneHandedStartingWeapons
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
    early_banner: EarlySmallLothricBanner
    late_basin_of_vows: LateBasinOfVowsOption
    late_dlc: LateDLCOption
    no_spell_requirements: NoSpellRequirementsOption
    no_equip_load: NoEquipLoadOption
    death_link: DeathLink
    enable_dlc: EnableDLCOption
    enable_ngp: EnableNGPOption
    randomize_enemies: RandomizeEnemiesOption
    random_enemy_preset: RandomEnemyPresetOption
    randomize_mimics_with_enemies: RandomizeMimicsWithEnemiesOption
    randomize_small_crystal_lizards_with_enemies: RandomizeSmallCrystalLizardsWithEnemiesOption
    reduce_harmless_enemies: ReduceHarmlessEnemiesOption
    simple_early_bosses: SimpleEarlyBossesOption
    scale_enemies: ScaleEnemiesOption
    all_chests_are_mimics: AllChestsAreMimicsOption
    impatient_mimics: ImpatientMimicsOption
    exclude_locations: DS3ExcludeLocations
