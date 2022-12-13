from email.policy import default
from Options import Choice, OptionDict, OptionSet, ItemDict, Option, DefaultOnToggle, Range, DeathLink, Toggle
import typing
from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification

class FinalEXP(Range):
    """Range of EXP for the Final form"""
    display_name = "Final Form Level"
    range_start = 1 
    range_end = 10
    default = 3
class MasterEXP(Range):
    """Range of EXP for the forms"""
    display_name = "Master Form Level"
    range_start = 1 
    range_end = 10
    default = 3
class LimitEXP(Range):
    """Range of EXP for the forms"""
    display_name = "Limit Form Level"
    range_start = 1
    range_end = 10
    default = 3
class WisdomEXP(Range):
    """Range of EXP for the forms"""
    display_name = "Wisdom Form Level"
    range_start = 1
    range_end = 10
    default = 3
class ValorEXP(Range):
    """Range of EXP for the forms"""
    display_name = "Valor Form Level"
    range_start = 1
    range_end = 10
    default = 3

class Schmovement(Toggle):
    """Start with lvl 1 growth"""
    display_name = "Schmovement"
    default = True

class Stats(Range):
    #Keyblade stats 
    display_name="Keyblade"
    range_start = 0
    range_end = 10
    default=5

class Visitlocking(Choice):
    #What is locked being on
    #if 0 then no visit locking  if 1 then second visits if 2 then first and second visits with one item
    display_name="Visit locking"
    option_novisitlocking=0
    option_secondvisitlocking=1
    option_firstvisitlocking=2
    default=0

class SuperBosses(Toggle):
    #Terra,Datas and Sephiroath
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
    "Final_Form_Level": FinalEXP,
    "Master_Form_Level": MasterEXP,
    "Limit_Form_Level": LimitEXP,
    "Wisdom_Form_Level": WisdomEXP,
    "Valor_Form_Level": ValorEXP,
    "Schmovement":Schmovement,
    "Keyblade":Stats,
    "Visit_locking":Visitlocking,
    "Super_Bosses":SuperBosses,
    "KH2StartingItems":KH2StartItems,
    "Level_Depth":Level_Depth,
    "Max_Logic":Max_Logic
    }
