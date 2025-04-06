from dataclasses import dataclass
import json
from typing import Any, Dict

from Options import Choice, DeathLink, DefaultOnToggle, ExcludeLocations, NamedRange, OptionDict, \
    OptionGroup, PerGameCommonOptions, Range, Removed, Toggle

## Game Options


class EarlySmallLothricBanner(Choice):
    """Force Small Lothric Banner into an early sphere in your world or across all worlds."""
    display_name = "Early Small Lothric Banner"
    option_off = 0
    option_early_global = 1
    option_early_local = 2
    default = option_off


class LateBasinOfVowsOption(Choice):
    """Guarantee that you don't need to enter Lothric Castle until later in the run.

    - **Off:** You may have to enter Lothric Castle and the areas beyond it immediately after High
      Wall of Lothric.
    - **After Small Lothric Banner:** You may have to enter Lothric Castle after Catacombs of
      Carthus.
    - **After Small Doll:** You won't have to enter Lothric Castle until after Irithyll of the
      Boreal Valley.
    """
    display_name = "Late Basin of Vows"
    option_off = 0
    alias_false = 0
    option_after_small_lothric_banner = 1
    alias_true = 1
    option_after_small_doll = 2


class LateDLCOption(Choice):
    """Guarantee that you don't need to enter the DLC until later in the run.

    - **Off:** You may have to enter the DLC after Catacombs of Carthus.
    - **After Small Doll:** You may have to enter the DLC after Irithyll of the Boreal Valley.
    - **After Basin:** You won't have to enter the DLC until after Lothric Castle.
    """
    display_name = "Late DLC"
    option_off = 0
    alias_false = 0
    option_after_small_doll = 1
    alias_true = 1
    option_after_basin = 2


class EnableDLCOption(Toggle):
    """Include DLC locations, items, and enemies in the randomized pools.

    To use this option, you must own both the "Ashes of Ariandel" and the "Ringed City" DLCs.
    """
    display_name = "Enable DLC"


class EnableNGPOption(Toggle):
    """Include items and locations exclusive to NG+ cycles."""
    display_name = "Enable NG+"


## Equipment

class RandomizeStartingLoadout(DefaultOnToggle):
    """Randomizes the equipment characters begin with."""
    display_name = "Randomize Starting Loadout"


class RequireOneHandedStartingWeapons(DefaultOnToggle):
    """Require starting equipment to be usable one-handed."""
    display_name = "Require One-Handed Starting Weapons"


class AutoEquipOption(Toggle):
    """Automatically equips any received armor or left/right weapons."""
    display_name = "Auto-Equip"


class LockEquipOption(Toggle):
    """Lock the equipment slots so you cannot change your armor or your left/right weapons.

    Works great with the Auto-equip option.
    """
    display_name = "Lock Equipment Slots"


class NoEquipLoadOption(Toggle):
    """Disable the equip load constraint from the game."""
    display_name = "No Equip Load"


class NoWeaponRequirementsOption(Toggle):
    """Disable the weapon requirements by removing any movement or damage penalties, permitting you
    to use any weapon early.
    """
    display_name = "No Weapon Requirements"


class NoSpellRequirementsOption(Toggle):
    """Disable the spell requirements permitting you to use any spell."""
    display_name = "No Spell Requirements"


## Weapons

class RandomizeInfusionOption(Toggle):
    """Enable this option to infuse a percentage of the pool of weapons and shields."""
    display_name = "Randomize Infusion"


class RandomizeInfusionPercentageOption(NamedRange):
    """The percentage of weapons/shields in the pool to be infused if Randomize Infusion is toggled.
    """
    display_name = "Percentage of Infused Weapons"
    range_start = 0
    range_end = 100
    default = 33
    # 3/155 weapons are infused in the base game, or about 2%
    special_range_names = {"similar to base game": 2}


class RandomizeWeaponLevelOption(Choice):
    """Enable this option to upgrade a percentage of the pool of weapons to a random value between
    the minimum and maximum levels defined.

    - **All:** All weapons are eligible, both basic and epic
    - **Basic:** Only weapons that can be upgraded to +10
    - **Epic:** Only weapons that can be upgraded to +5
    """
    display_name = "Randomize Weapon Level"
    option_none = 0
    option_all = 1
    option_basic = 2
    option_epic = 3


class RandomizeWeaponLevelPercentageOption(Range):
    """The percentage of weapons in the pool to be upgraded if randomize weapons level is toggled."""
    display_name = "Percentage of Randomized Weapons"
    range_start = 0
    range_end = 100
    default = 33


class MinLevelsIn5WeaponPoolOption(Range):
    """The minimum upgraded value of a weapon in the pool of weapons that can only reach +5."""
    display_name = "Minimum Level of +5 Weapons"
    range_start = 0
    range_end = 5
    default = 1


class MaxLevelsIn5WeaponPoolOption(Range):
    """The maximum upgraded value of a weapon in the pool of weapons that can only reach +5."""
    display_name = "Maximum Level of +5 Weapons"
    range_start = 0
    range_end = 5
    default = 5


class MinLevelsIn10WeaponPoolOption(Range):
    """The minimum upgraded value of a weapon in the pool of weapons that can reach +10."""
    display_name = "Minimum Level of +10 Weapons"
    range_start = 0
    range_end = 10
    default = 1


class MaxLevelsIn10WeaponPoolOption(Range):
    """The maximum upgraded value of a weapon in the pool of weapons that can reach +10."""
    display_name = "Maximum Level of +10 Weapons"
    range_start = 0
    range_end = 10
    default = 10


## Item Smoothing

class SmoothSoulItemsOption(DefaultOnToggle):
    """Distribute soul items in a similar order as the base game.

    By default, soul items will be distributed totally randomly. If this is set, less valuable soul
    items will generally appear in earlier spheres and more valuable ones will generally appear
    later.
    """
    display_name = "Smooth Soul Items"


class SmoothUpgradeItemsOption(DefaultOnToggle):
    """Distribute upgrade items in a similar order as the base game.

    By default, upgrade items will be distributed totally randomly. If this is set, lower-level
    upgrade items will generally appear in earlier spheres and higher-level ones will generally
    appear later.
    """
    display_name = "Smooth Upgrade Items"


class SmoothUpgradedWeaponsOption(DefaultOnToggle):
    """Distribute upgraded weapons in a similar order as the base game.

    By default, upgraded weapons will be distributed totally randomly. If this is set, lower-level
    weapons will generally appear in earlier spheres and higher-level ones will generally appear
    later.
    """
    display_name = "Smooth Upgraded Weapons"


### Enemies

class RandomizeEnemiesOption(DefaultOnToggle):
    """Randomize enemy and boss placements."""
    display_name = "Randomize Enemies"


class SimpleEarlyBossesOption(DefaultOnToggle):
    """Avoid replacing Iudex Gundyr and Vordt with late bosses.

    This excludes all bosses after Dancer of the Boreal Valley from these two boss fights. Disable
    it for a chance at a much harder early game.

    This is ignored unless enemies are randomized.
    """
    display_name = "Simple Early Bosses"


class ScaleEnemiesOption(DefaultOnToggle):
    """Scale randomized enemy stats to match the areas in which they appear.

    Disabling this will tend to make the early game much more difficult and the late game much
    easier.

    This is ignored unless enemies are randomized.
    """
    display_name = "Scale Enemies"


class RandomizeMimicsWithEnemiesOption(Toggle):
    """Mix Mimics into the main enemy pool.

    If this is enabled, Mimics will be replaced by normal enemies who drop the Mimic rewards on
    death, and Mimics will be placed randomly in place of normal enemies. It's recommended to enable
    Impatient Mimics as well if you enable this.

    This is ignored unless enemies are randomized.
    """
    display_name = "Randomize Mimics With Enemies"


class RandomizeSmallCrystalLizardsWithEnemiesOption(Toggle):
    """Mix small Crystal Lizards into the main enemy pool.

    If this is enabled, Crystal Lizards will be replaced by normal enemies who drop the Crystal
    Lizard rewards on death, and Crystal Lizards will be placed randomly in place of normal enemies.

    This is ignored unless enemies are randomized.
    """
    display_name = "Randomize Small Crystal Lizards With Enemies"


class ReduceHarmlessEnemiesOption(Toggle):
    """Reduce the frequency that "harmless" enemies appear.

    Enable this to add a bit of extra challenge. This severely limits the number of enemies that are
    slow to aggro, slow to attack, and do very little damage that appear in the enemy pool.

    This is ignored unless enemies are randomized.
    """
    display_name = "Reduce Harmless Enemies"


class AllChestsAreMimicsOption(Toggle):
    """Replace all chests with mimics that drop the same items.

    If "Randomize Mimics With Enemies" is set, these chests will instead be replaced with random
    enemies that drop the same items.

    This is ignored unless enemies are randomized.
    """
    display_name = "All Chests Are Mimics"


class ImpatientMimicsOption(Toggle):
    """Mimics attack as soon as you get close instead of waiting for you to open them.

    This is ignored unless enemies are randomized.
    """
    display_name = "Impatient Mimics"


class RandomEnemyPresetOption(OptionDict):
    """The YAML preset for the static enemy randomizer.

    See the static randomizer documentation in `randomizer\\presets\\README.txt` for details.
    Include this as nested YAML. For example:

    .. code-block:: YAML

      random_enemy_preset:
        RemoveSource: Ancient Wyvern; Darkeater Midir
        DontRandomize: Iudex Gundyr
    """
    display_name = "Random Enemy Preset"
    supports_weighting = False
    default = {}

    valid_keys = ["Description", "RecommendFullRandomization", "RecommendNoEnemyProgression",
                  "OopsAll", "Boss", "Miniboss", "Basic", "BuffBasicEnemiesAsBosses",
                  "DontRandomize", "RemoveSource", "Enemies"]

    @classmethod
    def get_option_name(cls, value: Dict[str, Any]) -> str:
        return json.dumps(value)


## Item & Location

class DS3ExcludeLocations(ExcludeLocations):
    """Prevent these locations from having an important item."""
    default = frozenset({"Hidden", "Small Crystal Lizards", "Upgrade", "Small Souls", "Miscellaneous"})


class ExcludedLocationBehaviorOption(Choice):
    """How to choose items for excluded locations in DS3.

    - **Allow Useful:** Excluded locations can't have progression items, but they can have useful
      items.
    - **Forbid Useful:** Neither progression items nor useful items can be placed in excluded
      locations.
    - **Do Not Randomize:** Excluded locations always contain the same item as in vanilla Dark Souls
      III.

    A "progression item" is anything that's required to unlock another location in some game. A
    "useful item" is something each game defines individually, usually items that are quite
    desirable but not strictly necessary.
    """
    display_name = "Excluded Locations Behavior"
    option_allow_useful = 1
    option_forbid_useful = 2
    option_do_not_randomize = 3
    default = 2


class MissableLocationBehaviorOption(Choice):
    """Which items can be placed in locations that can be permanently missed.

    - **Allow Useful:** Missable locations can't have progression items, but they can have useful
      items.
    - **Forbid Useful:** Neither progression items nor useful items can be placed in missable
      locations.
    - **Do Not Randomize:** Missable locations always contain the same item as in vanilla Dark Souls
      III.

    A "progression item" is anything that's required to unlock another location in some game. A
    "useful item" is something each game defines individually, usually items that are quite
    desirable but not strictly necessary.
    """
    display_name = "Missable Locations Behavior"
    option_allow_useful = 1
    option_forbid_useful = 2
    option_do_not_randomize = 3
    default = 2


@dataclass
class DarkSouls3Options(PerGameCommonOptions):
    # Game Options
    early_banner: EarlySmallLothricBanner
    late_basin_of_vows: LateBasinOfVowsOption
    late_dlc: LateDLCOption
    death_link: DeathLink
    enable_dlc: EnableDLCOption
    enable_ngp: EnableNGPOption

    # Equipment
    random_starting_loadout: RandomizeStartingLoadout
    require_one_handed_starting_weapons: RequireOneHandedStartingWeapons
    auto_equip: AutoEquipOption
    lock_equip: LockEquipOption
    no_equip_load: NoEquipLoadOption
    no_weapon_requirements: NoWeaponRequirementsOption
    no_spell_requirements: NoSpellRequirementsOption

    # Weapons
    randomize_infusion: RandomizeInfusionOption
    randomize_infusion_percentage: RandomizeInfusionPercentageOption
    randomize_weapon_level: RandomizeWeaponLevelOption
    randomize_weapon_level_percentage: RandomizeWeaponLevelPercentageOption
    min_levels_in_5: MinLevelsIn5WeaponPoolOption
    max_levels_in_5: MaxLevelsIn5WeaponPoolOption
    min_levels_in_10: MinLevelsIn10WeaponPoolOption
    max_levels_in_10: MaxLevelsIn10WeaponPoolOption

    # Item Smoothing
    smooth_soul_items: SmoothSoulItemsOption
    smooth_upgrade_items: SmoothUpgradeItemsOption
    smooth_upgraded_weapons: SmoothUpgradedWeaponsOption

    # Enemies
    randomize_enemies: RandomizeEnemiesOption
    simple_early_bosses: SimpleEarlyBossesOption
    scale_enemies: ScaleEnemiesOption
    randomize_mimics_with_enemies: RandomizeMimicsWithEnemiesOption
    randomize_small_crystal_lizards_with_enemies: RandomizeSmallCrystalLizardsWithEnemiesOption
    reduce_harmless_enemies: ReduceHarmlessEnemiesOption
    all_chests_are_mimics: AllChestsAreMimicsOption
    impatient_mimics: ImpatientMimicsOption
    random_enemy_preset: RandomEnemyPresetOption

    # Item & Location
    exclude_locations: DS3ExcludeLocations
    excluded_location_behavior: ExcludedLocationBehaviorOption
    missable_location_behavior: MissableLocationBehaviorOption

    # Removed
    pool_type: Removed
    enable_weapon_locations: Removed
    enable_shield_locations: Removed
    enable_armor_locations: Removed
    enable_ring_locations: Removed
    enable_spell_locations: Removed
    enable_key_locations: Removed
    enable_boss_locations: Removed
    enable_npc_locations: Removed
    enable_misc_locations: Removed
    enable_health_upgrade_locations: Removed
    enable_progressive_locations: Removed
    guaranteed_items: Removed
    excluded_locations: Removed
    missable_locations: Removed


option_groups = [
    OptionGroup("Equipment", [
        RandomizeStartingLoadout,
        RequireOneHandedStartingWeapons,
        AutoEquipOption,
        LockEquipOption,
        NoEquipLoadOption,
        NoWeaponRequirementsOption,
        NoSpellRequirementsOption,
    ]),
    OptionGroup("Weapons", [
        RandomizeInfusionOption,
        RandomizeInfusionPercentageOption,
        RandomizeWeaponLevelOption,
        RandomizeWeaponLevelPercentageOption,
        MinLevelsIn5WeaponPoolOption,
        MaxLevelsIn5WeaponPoolOption,
        MinLevelsIn10WeaponPoolOption,
        MaxLevelsIn10WeaponPoolOption,
    ]),
    OptionGroup("Item Smoothing", [
        SmoothSoulItemsOption,
        SmoothUpgradeItemsOption,
        SmoothUpgradedWeaponsOption,
    ]),
    OptionGroup("Enemies", [
        RandomizeEnemiesOption,
        SimpleEarlyBossesOption,
        ScaleEnemiesOption,
        RandomizeMimicsWithEnemiesOption,
        RandomizeSmallCrystalLizardsWithEnemiesOption,
        ReduceHarmlessEnemiesOption,
        AllChestsAreMimicsOption,
        ImpatientMimicsOption,
        RandomEnemyPresetOption,
    ]),
    OptionGroup("Item & Location Options", [
        DS3ExcludeLocations,
        ExcludedLocationBehaviorOption,
        MissableLocationBehaviorOption,
    ])
]
