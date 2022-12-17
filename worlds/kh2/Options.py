from email.policy import default
from Options import Choice, OptionDict, OptionSet, ItemDict, Option, DefaultOnToggle, Range, DeathLink, Toggle
import typing
from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification

class SoraEXP(Range):
    """Sora Level exp Multiplier"""
    display = "Sora Level EXP"
    range_start = 1
    range_end = 10
    default = 5
class FinalEXP(Range):
    """Final Form exp Multiplier"""
    display_name = "Final Form EXP"
    range_start = 1 
    range_end = 10
    default = 3
class MasterEXP(Range):
    """Master Form exp Multiplier"""
    display_name = "Master Form EXP"
    range_start = 1 
    range_end = 10
    default = 3
class LimitEXP(Range):
    """Limit Form exp Multiplier"""
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
    """Valor Form exp Multiplier"""
    display_name = "Valor Form EXP"
    range_start = 1
    range_end = 10
    default = 3
class SummonEXP(Range):
    display_name = "Summon level EXP"
    range_start = 1
    range_end = 10
    default = 5
class Schmovement(Toggle):
    """Start with lvl 1 of all growth"""
    display_name = "Schmovement"
    default = True

class KeybladeMin(Range):
    """Minimum Stats for the Keyblade""" 
    display_name="Keyblade Minimum Stats"
    range_start = 0
    range_end = 20
    default=3

class KeybladeMax(Range):
    """Maximum Stats for the Keyblade"""
    display_name="Keyblade Max Stats"
    range_start = 0
    range_end = 20
    default = 7

class Visitlocking(Choice):
    #What is locked being on
    #if 0 then no visit locking  if 1 then second visits if 2 then first and second visits with one item
    display_name="Visit locking"
    option_novisitlocking=0
    option_secondvisitlocking=1
    option_firstvisitlocking=2
    default=0

class SuperBosses(Toggle):
    """Terra, Sephiroth and Data Fights Toggle"""
    display_name="Super Bosses"
    default = False

class KH2StartItems(ItemDict):
    """Choose your strating Items(currently limited on what)"""
    display_name = "KH2StartingItems"
    verify_item_name = False
    default = {}

class Level_Depth(Toggle):
    """Levels capped at 50 or 99 (true 50 false 99)"""
    display_name="Level Depth"
    default=True

class Max_Logic(Toggle):
    """Forms on forms and torn pages in cor/ag"""
    display_name="Max Logic"
    default=True

KH2_Options: typing.Dict[str, type(Option)] = {
    "Sora_Level_EXP":SoraEXP,
    "Final_Form_EXP": FinalEXP,
    "Master_Form_EXP": MasterEXP,
    "Limit_Form_EXP": LimitEXP,
    "Wisdom_Form_EXP": WisdomEXP,
    "Valor_Form_EXP": ValorEXP,
    "Summon_EXP":SummonEXP,
    "Schmovement":Schmovement,
    "Keyblade_Minimum":KeybladeMin,
    "Keyblade_Maximum":KeybladeMax,
    "Visit_locking":Visitlocking,
    "Super_Bosses":SuperBosses,
    "Starting_Items":KH2StartItems,
    "Level_Depth":Level_Depth,
    "Max_Logic":Max_Logic
    }
