from dataclasses import dataclass

from Options import NamedRange, Choice, Range, Option, Toggle, DeathLink, DefaultOnToggle, OptionSet, PerGameCommonOptions

class StrengthIncrease(Range):
    """
    Number of Strength Increases to Add to the Level Up Rewards
    """
    range_start = 0
    range_end = 100
    default = 24

class DefenseIncrease(Range):
    """
    Number of Defense Increases to Add to the Level Up Rewards
    """
    range_start = 0
    range_end = 100
    default = 24

class HPIncrease(Range):
    """
    Number of HP Increases to Add to the Level Up Rewards
    """
    range_start = 0
    range_end = 100
    default = 23

class APIncrease(Range):
    """
    Number of AP Increases to Add to the Level Up Rewards
    """
    range_start = 0
    range_end = 100
    default = 18

class MPIncrease(Range):
    """
    Number of MP Increases to Add to the Level Up Rewards
    """
    range_start = 0
    range_end = 20
    default = 7

class AccessorySlotIncrease(Range):
    """
    Number of Accessory Slot Increases to Add to the Level Up Rewards
    """
    range_start = 0
    range_end = 6
    default = 1

class ItemSlotIncrease(Range):
    """
    Number of Item Slot Increases to Add to the Level Up Rewards
    """
    range_start = 0
    range_end = 5
    default = 3

class Atlantica(Toggle):
    """
    Toggle whether Atlantica locations/items should be included.
    """
    display_name = "Atlantica"

class HundredAcreWood(Toggle):
    """
    Toggle whether to include checks in the 100 Acre Wood
    """
    display_name = "100 Acre Wood"

class SuperBosses(Toggle):
    """
    Toggle whether to include checks behind Super Bosses.  This is ignored if Super Boss Hunt is your goal.
    """
    display_name = "Super Bosses"

class Goal(Choice):
    """
    Determines the goal of your playthrough.
    Depending on your setting for Require Final Ansem, this will either yield Victory or required Ansem Reports to enter End of the World.
    Note: If requiring Final Ansem, with more than 1 Ansem Report in the pool (or more than 5 if you are using the Super Boss Hunt goal), the goal(s) will not be required, but will remain a way to get a report.
    
    Sephiroth: Defeat Sephiroth.
    Unknown: Defeat Unknown.
    Postcards: Turn in all 10 postcards in Traverse Town
    Final Ansem: Enter End of the World and defeat Ansem as normal
    Puppies: Rescue and return all 99 puppies in Traverse Town.
    Super Boss Hunt: Ansem Reports are set to appear as rewards for defeating Phantom, Kurt Zisa, Sephiroth, Ice Titan, and Unknown.  Forces require Final Ansem on.
    """
    display_name = "Goal"
    option_sephiroth = 0
    option_unknown = 1
    option_postcards = 2
    option_final_ansem = 3
    option_puppies = 4
    option_super_boss_hunt = 5
    default = 3

class RequireFinalAnsem(Toggle):
    """
    Determines whether the Victory item is behind your goal or if your goal will provide an Ansem's Report to enter End of the World and defeat Ansem.
    """
    display_name = "Require Final Ansem"

class Puppies(Choice):
    """
    Determines how dalmation puppies are shuffled into the pool.
    Full: All puppies are in one location
    Triplets: Puppies are found in triplets just as they are in the base game
    Individual: One puppy can be found per location
    """
    display_name = "Puppies"
    option_full = 0
    option_triplets = 1
    option_individual = 2
    default = 0

class EXPMultiplier(NamedRange):
    """
    Determines the multiplier to apply to EXP gained
    """
    display_name = "EXP Multiplier"
    default = 16
    range_start = default / 4
    range_end = 160
    special_range_names = {
        "0.25x": default / 4,
        "0.5x": default / 2,
        "1x": default,
        "2x": default * 2,
        "3x": default * 3,
        "4x": default * 4,
        "8x": default * 8,
        "10x": default * 10,
    }

class RequiredReports(Range):
    """
    Determines the number of Ansem's Reports needed to open End of the World
    """
    diplay_name = "Reports to Open End of the World"
    default = 4
    range_start = 1
    range_end = 13

class ReportsInPool(Range):
    """
    Determines the number of Ansem's Reports in the item pool.
    """
    diplay_name = "Reports in Pool"
    default = 4
    range_start = 1
    range_end = 13

class RandomizeKeybladeStats(DefaultOnToggle):
    """
    Determines whether Keyblade stats should be randomized
    """
    display_name = "Randomize Keyblade Stats"

class KeybladeMinStrength(Range):
    """
    Determines the lowest STR bonus a keyblade can have
    """
    display_name = "Keyblade Minimum STR Bonus"
    default = 3
    range_start = 1
    range_end = 19

class KeybladeMaxStrength(Range):
    """
    Determines the maximum STR bonus a keyblade can have
    """
    display_name = "Keyblade Maximum STR Bonus"
    default = 14
    range_start = 2
    range_end = 20

class KeybladeMinMP(Range):
    """
    Determines the minimum MP bonus a keyblade can have
    """
    display_name = "Keyblade Maximum MP Bonus"
    default = 0
    range_start = 0
    range_end = 4

class KeybladeMaxMP(Range):
    """
    Determines the minimum MP bonus a keyblade can have
    """
    display_name = "Keyblade Maximum MP Bonus"
    default = 3
    range_start = 1
    range_end = 5

class LevelChecks(Range):
    """
    Determines the maximum level for which checks can be obtained.
    """
    display_name = "Level Checks"
    default = 100
    range_start = 0
    range_end = 100

class ForceStatsOnLevels(NamedRange):
    """
    If this value is less than the value for Level Checks, this determines the minimum level from which only stat ups are obtained at level up locations
    For example, if you only want to find AP items from levels 1-50, set this value to 51.
    """
    display_name = "Force Stats on Level Starting From"
    default = 1
    range_start = 1
    range_end = 101
    special_range_names = {
        "none": 101,
        "ap-checks-to-level-50": 51,
        "all": 1
    }

class BadStartingWeapons(Toggle):
    """
    Forces Kingdom Key, Dream Sword, Dream Shield, and Dream Staff to have bad stats
    """
    display_name = "Bad Starting Weapons"

@dataclass
class KH1Options(PerGameCommonOptions):
    goal: Goal
    require_final_ansem: RequireFinalAnsem
    required_reports: RequiredReports
    reports_in_pool: ReportsInPool
    super_bosses: SuperBosses
    atlantica: Atlantica
    hundred_acre_wood: HundredAcreWood
    puppies: Puppies
    exp_multiplier: EXPMultiplier
    randomize_keyblade_stats: RandomizeKeybladeStats
    bad_starting_weapons: BadStartingWeapons
    keyblade_max_str: KeybladeMaxStrength
    keyblade_min_str: KeybladeMinStrength
    keyblade_max_mp: KeybladeMaxMP
    keyblade_min_mp: KeybladeMinMP
    level_checks: LevelChecks
    force_stats_on_levels: ForceStatsOnLevels
    strength_increase: StrengthIncrease
    defense_increase: DefenseIncrease
    hp_increase: HPIncrease
    ap_increase: APIncrease
    mp_increase: MPIncrease
    accessory_slot_increase: AccessorySlotIncrease
    item_slot_increase: ItemSlotIncrease
    
