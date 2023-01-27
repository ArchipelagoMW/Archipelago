from Options import Choice, Option,  Range, Toggle, OptionSet
import typing



class SoraEXP(Range):
    """Sora Level Exp Multiplier"""
    display = "Sora Level EXP"
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
    """WIsdom Form exp Multiplier"""
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
    """Summon's Exp Multiplier"""
    display_name = "Summon level EXP"
    range_start = 1
    range_end = 10
    default = 5


class Schmovement(Choice):
    """Level of Growth You Start With"""
    display_name = "Schmovement"
    option_level_0 = 0
    option_level_1 = 1
    option_level_2 = 2
    option_level_3 = 3
    option_level_4 = 4
    default = 1

class RandomGrowth(Range):
    """Amount of Random Growth Abilites You Start With"""
    display_name="Random Starting Growth"
    range_start=0
    range_end=20
    default=0

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
    # What is locked being on
    # if 0 then no visit locking  if 1 then second visits if 2 then first and second visits with one item
    display_name = "Visit locking"
    option_no_visit_locking = 0
    option_second_visit_locking = 1
    option_first_visit_locking = 2
    default = 0


class SuperBosses(Toggle):
    """Terra, Sephiroth and Data Fights Toggle"""
    display_name = "Super Bosses"
    default = False


class LevelDepth(Choice):
    # What is locked being on
    # if 0 then no visit locking  if 1 then second visits if 2 then first and second visits with one item
    display_name = "Level Depth"
    option_level_50 = 0
    option_level_99 = 1
    option_level_99_sanity=2
    option_level_50_sanity=3
    option_level_1=4
    default = 0

class Max_Logic(Toggle):
    """Forms on forms and torn pages in cor/ag"""
    display_name = "Max Logic"
    default = True


class Promise_Charm(Toggle):
    """Add Promise Charm to the Pool"""
    display_name = "Promise Charm"
    default = False

class Keyblade_Abilities(Choice):
    """Action:Has Action Abilites on Keyblades Support:Has Support Abilites on Keyblades"""
    display_name = "Keyblade Abilities"
    option_support = 0
    option_action = 1
    option_both = 2
    default=2

class BlacklistKeyblade(OptionSet):
    """Black List these Abilities on Keyblades"""
    display_name = "BlackList Keyblade Abilities"
    verify_item_name = True

KH2_Options: typing.Dict[str, type(Option)] = {
    "Sora_Level_EXP": SoraEXP,
    "Final_Form_EXP": FinalEXP,
    "Master_Form_EXP": MasterEXP,
    "Limit_Form_EXP": LimitEXP,
    "Wisdom_Form_EXP": WisdomEXP,
    "Valor_Form_EXP": ValorEXP,
    "Summon_EXP": SummonEXP,
    "Schmovement": Schmovement,
    "Keyblade_Minimum": KeybladeMin,
    "Keyblade_Maximum": KeybladeMax,
    "Visit_locking": Visitlocking,
    "Super_Bosses": SuperBosses,
    "Level_Depth": LevelDepth,
    "Max_Logic": Max_Logic,
    "Promise_Charm": Promise_Charm,
    "Keyblade_Abilities":Keyblade_Abilities,
    "BlacklistKeyblade":BlacklistKeyblade,
    "RandomGrowth":RandomGrowth,
}
