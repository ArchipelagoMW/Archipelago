from dataclasses import dataclass

from Options import Choice, Range, Option, Toggle, DeathLink, DefaultOnToggle, OptionSet, PerGameCommonOptions

class Cure(DefaultOnToggle):
    """
    Toggle whether Cure cards should be included in the item pool.
    """
    display_name = "Cure"

class EarlyCure(DefaultOnToggle):
    """
    Toggle whether one of the starting checks should include Cure 4-6
    """
    display_name = "Early Cure"

class Zeroes(DefaultOnToggle):
    """
    Toggle whether 0 value cards are included in card sets
    """
    display_name = "Zeroes"

class AttackPower(Range):
    """
    Modifier for Sora's strike power.  Default is 10
    """
    display_name = "Attack Power"
    range_start = 1
    range_end = 100
    default = 10

class DaysLocations(Toggle):
    """
    Toggle whether locations not available to the player until they watch 358/2 Days are included in the locations list.
    """
    display_name = "Days Locations"

class ChecksBehindLeon(Toggle):
    """
    Toggle whether to include checks behind the Leon sleight tutorial.  If left off, the player can safely skip that room.
    """
    display_name = "Checks Behind Leon"

class ChecksBehindMinigames(Toggle):
    """
    Toggle whether to include checks behind 100 Acre Woods Minigames.
    """
    display_name = "Checks Behind Minigames"

class ChecksBehindSleightsLevels(Toggle):
    """
    Toggle whether to include checks behind Sleights received from Leveling Up.
    """
    display_name = "Checks Behind Level Up Sleights"

class EXPMultiplier(Range):
    """
    Multiplier to apply to XP received.
    """
    display_name = "EXP Multiplier"
    range_start = 1
    range_end = 10
    default = 1

@dataclass
class KHRECOMOptions(PerGameCommonOptions):
    cure: Cure
    early_cure: EarlyCure
    days_locations: DaysLocations
    checks_behind_leon: ChecksBehindLeon
    exp_multiplier: EXPMultiplier
    minigames: ChecksBehindMinigames
    levels: ChecksBehindSleightsLevels
    zeroes: Zeroes
    attack_power: AttackPower
