from dataclasses import dataclass

from Options import Choice, Range, Option, Toggle, DeathLink, DefaultOnToggle, OptionSet, PerGameCommonOptions

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
    Number of Accessory Slot Increases to Add to the Level Up Rewards
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
    Determines the goal of your run.
    """
    display_name = "Goal"
    option_final_rest = 0
    option_deep_jungle = 1
    option_agrabah = 2
    option_monstro = 3
    option_atlantica = 4
    option_halloween_town = 5
    option_neverland = 6
    option_sephiroth = 7
    option_unknown = 8
    default = 0

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
