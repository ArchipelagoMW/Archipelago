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

class Goal(Choice):
    """
    Determines the goal of your playthrough.
    """
    display_name = "Goal"
    option_final_rest = 0
    option_wonderland = 1
    option_deep_jungle = 2
    option_agrabah = 3
    option_monstro = 4
    option_atlantica = 5
    option_halloween_town = 6
    option_neverland = 7
    option_sephiroth = 8
    option_unknown = 9
    option_postcards = 10
    option_final_ansem = 11
    default = 11

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

@dataclass
class KH1Options(PerGameCommonOptions):
    goal: Goal
    atlantica: Atlantica
    strength_increase: StrengthIncrease
    defense_increase: DefenseIncrease
    hp_increase: HPIncrease
    ap_increase: APIncrease
    mp_increase: MPIncrease
    accessory_slot_increase: AccessorySlotIncrease
    item_slot_increase: ItemSlotIncrease
    exp_multiplier: EXPMultiplier
    required_reports: RequiredReports
    reports_in_pool: ReportsInPool
    randomize_keyblade_stats: RandomizeKeybladeStats
    keyblade_max_str: KeybladeMaxStrength
    keyblade_min_str: KeybladeMinStrength
    keyblade_max_mp: KeybladeMaxMP
    keyblade_min_mp: KeybladeMinMP
