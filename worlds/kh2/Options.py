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


class Stats(Range):
    #Keyblade stats 
    display_name="Keyblade"
    range_start = 0
    range_end = 10
    default=5

class Visitlocking(Range):
    #What is locked being on
    #if 1 then no visit locking   if 2 then second visits if 3 then first and second visits with one item
    display_name="Visit locking"
    range_start=0
    range_end=3
    default=1

class SuperBosses(Toggle):
    #Terra,Datas and Sephiroath
    display_name="Super Bosses"
    default = False

class KH2StartItems(ItemDict):
    """Mapping of Factorio internal item-name to amount granted on start."""
    display_name = "KH2StartingItems"
    verify_item_name = False
    default = {"Way to the Dawn": 1, "Beast's Claw": 1}

class Level_Depth(Toggle):
    display_name="Level Depth"
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
    }
