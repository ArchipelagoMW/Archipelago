from Options import Choice, Option, Range, Toggle, OptionSet
import typing

from worlds.kh2 import SupportAbility_Table, ActionAbility_Table


class SoraEXP(Range):
    """Sora Level Exp Multiplier"""
    display_name = "Sora Level EXP"
    range_start = 1
    range_end = 10
    default = 5


class FinalEXP(Range):
    """Final Form Exp Multiplier"""
    display_name = "Final Form EXP"
    range_start = 1
    range_end = 10
    default = 3


class MasterEXP(Range):
    """Master Form Exp Multiplier"""
    display_name = "Master Form EXP"
    range_start = 1
    range_end = 10
    default = 3


class LimitEXP(Range):
    """Limit Form Exp Multiplier"""
    display_name = "Limit Form EXP"
    range_start = 1
    range_end = 10
    default = 3


class WisdomEXP(Range):
    """Wisdom Form Exp Multiplier"""
    display_name = "Wisdom Form EXP"
    range_start = 1
    range_end = 10
    default = 3


class ValorEXP(Range):
    """Valor Form Exp Multiplier"""
    display_name = "Valor Form EXP"
    range_start = 1
    range_end = 10
    default = 3


class SummonEXP(Range):
    """Summon Exp Multiplier"""
    display_name = "Summon level EXP"
    range_start = 1
    range_end = 10
    default = 5


class Schmovement(Choice):
    """Level of Progressive Movement You Start With"""
    display_name = "Schmovement"
    option_level_0 = 0
    option_level_1 = 1
    option_level_2 = 2
    option_level_3 = 3
    option_level_4 = 4
    default = 1


class RandomGrowth(Range):
    """Amount of Random Growth Abilities You Start With"""
    display_name = "Random Starting Growth"
    range_start = 0
    range_end = 20
    default = 0


class KeybladeMin(Range):
    """Minimum Stats for the Keyblade"""
    display_name = "Keyblade Minimum Stats"
    range_start = 0
    range_end = 20
    default = 3


class KeybladeMax(Range):
    """Maximum Stats for the Keyblade"""
    display_name = "Keyblade Max Stats"
    range_start = 0
    range_end = 20
    default = 7


class Visitlocking(Choice):
    """Determines the level of visit locking
    No Visit Locking:No visit locks(everything is sphere 1.Not Recommended)# BK is making a lot of money
    Second Visit Locking:Start with 13 visit locking items for every first visit.
    First and Second Visit Locking:One item for First Visit Two For Second Visit"""
    display_name = "Visit locking"
    option_no_visit_locking = 0  # starts with 27 visit locking
    option_second_visit_locking = 1  # starts with 13 (no icecream/picture)
    option_first_and_second_visit_locking = 2  # starts with nothing
    default = 2


class RandomVisitLockingItem(Range):
    """Start with random amount of visit locking items."""
    display_name = "Random Visit Locking Item"
    range_start = 0
    range_end = 25
    default = 3


class SuperBosses(Toggle):
    """Terra, Sephiroth and Data Fights Toggle."""
    display_name = "Super Bosses"
    default = False


class Cups(Choice):
    """Olympus Cups Toggles
        No Cups: No Cups.
        Cups: Has every cup except Paradox.
        Cups and Hades Paradox: Has Every Cup On."""
    display_name = "Olympus Cups"
    option_no_cups = 0
    option_cups = 1
    option_cups_and_hades_paradox = 2
    default = 1


class LevelDepth(Choice):
    """Determines How many locations you want on levels
    Level 50:23 checks spread through 50 levels
    Level 99:23 checks spread through 99 levels
    Level 50 sanity:check per level for 50 levels
    Level 99 sanity:check per level for 99 levels
    Level 1: no checks on levels(checks are replaced with stats)"""
    display_name = "Level Depth"
    option_level_50 = 0
    option_level_99 = 1
    option_level_50_sanity = 2
    option_level_99_sanity = 3
    option_level_1 = 4
    default = 0


class PromiseCharm(Toggle):
    """Add Promise Charm to the Pool"""
    display_name = "Promise Charm"
    default = False


class KeybladeAbilities(Choice):
    """Action:Has Action Abilities on Keyblades
    Support:Has Support Abilities on Keyblades"""
    display_name = "Keyblade Abilities"
    option_support = 0
    option_action = 1
    option_both = 2
    default = 2


class BlacklistKeyblade(OptionSet):
    """Black List these Abilities on Keyblades"""
    display_name = "Blacklist Keyblade Abilities"
    valid_keys = set(SupportAbility_Table.keys()).union(ActionAbility_Table.keys())

class Goal(Choice):
    """Win Condition
    Three Proofs: Obtain the Three Proofs and Have a Gold Crown on Sora's Head.
    Lucky Emblem Hunt: Acquire The Amount of Lucky Emblems you have set.
    Hitlist: Kill the Superbosses on the "Hitlist" then synth ultima weapon."""
    display_name = "Goal"
    option_three_proofs = 0
    option_lucky_emblem_hunt = 1
    option_hitlist = 2
    default = 0


class FinalXemnas(Toggle):
    """Kill Final Xemnas to Beat the Game.
    This is in addition to your Goal. I.E. get three proofs+kill final Xemnas"""
    display_name = "Final Xemnas"
    default = True


class LuckyEmblemsRequired(Range):
    """Number of Lucky Emblems to collect to Open The Final Door bosses.
    If Goal is not Lucky Emblem Hunt this does nothing."""
    display_name = "Lucky Emblems Required"
    range_start = 1
    range_end = 60
    default = 25


class LuckyEmblemsAmount(Range):
    """Number of Lucky Emblems that are in the pool.
    If Goal is not Lucky Emblem Hunt this does nothing."""
    display_name = "Lucky Emblems Available"
    range_start = 1
    range_end = 60
    default = 40


class BountyRequired(Range):
    """Number of Bounties that are Required.
        If Goal is not Hitlist this does nothing."""
    display_name = "Bounties Required"
    range_start = 1
    range_end = 24
    default = 7


class BountyAmount(Range):
    """Number of Bounties that are in the pool.
        If Goal is not Hitlist this does nothing."""
    display_name = "Bounties Available"
    range_start = 1
    range_end = 24
    default = 13


KH2_Options: typing.Dict[str, type(Option)] = {
    "Sora_Level_EXP":         SoraEXP,
    "Final_Form_EXP":         FinalEXP,
    "Master_Form_EXP":        MasterEXP,
    "Limit_Form_EXP":         LimitEXP,
    "Wisdom_Form_EXP":        WisdomEXP,
    "Valor_Form_EXP":         ValorEXP,
    "Summon_EXP":             SummonEXP,
    "Schmovement":            Schmovement,
    "Keyblade_Minimum":       KeybladeMin,
    "Keyblade_Maximum":       KeybladeMax,
    "Visitlocking":           Visitlocking,
    "RandomVisitLockingItem": RandomVisitLockingItem,
    "SuperBosses":            SuperBosses,
    "LevelDepth":             LevelDepth,
    "Promise_Charm":          PromiseCharm,
    "KeybladeAbilities":      KeybladeAbilities,
    "BlacklistKeyblade":      BlacklistKeyblade,
    "RandomGrowth":           RandomGrowth,
    "Goal":                   Goal,
    "FinalXemnas":            FinalXemnas,
    "LuckyEmblemsAmount":     LuckyEmblemsAmount,
    "LuckyEmblemsRequired":   LuckyEmblemsRequired,
    "BountyAmount":           BountyAmount,
    "BountyRequired":         BountyRequired,
    "Cups":                   Cups,

}
