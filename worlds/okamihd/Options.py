from typing import List, TYPE_CHECKING, Dict, Any
from schema import Schema, Optional
from dataclasses import dataclass
from worlds.AutoWorld import PerGameCommonOptions
from Options import Range, Toggle, DeathLink, Choice, OptionDict, DefaultOnToggle, OptionGroup

if TYPE_CHECKING:
    from . import OkamiWorld


def create_option_groups() -> List[OptionGroup]:
    option_group_list: List[OptionGroup] = []
    for name, options in okami_option_groups.items():
        option_group_list.append(OptionGroup(name=name, options=options))

    return option_group_list


class BuriedChestsByNight(Toggle):
    """Buried chests logically require Crescent, as they're way more visible at night"""
    display_name = "Buried chests by night"
    default = 1

class ProgressiveWeapons(Toggle):
    """With this option you'll find progressive weapons for each type instead of every weapon being in the item pool."""
    display_name="Progressive Weapons"
    default = 0

class KarmicTransformers(Choice):
    """Karmic Transformers are Cosmetic items that changes Amaterasu's appearance:

    Excluded: Won't appear
    Precollected: You'll start with them already collected
    In item pool: They will be placed in item pool. You'll start with the Karmic Returner"""
    display_name = "Karmic Transformers Placement"
    option_excluded = 0
    option_precollected = 1
    option_in_item_pool = 2
    default = 1

class OpenGameStart(Toggle):
    """Remove some early events for a more open game start:
        - Restoring the river of the Heavens
        - Cutting the peach containing the villagers in Kamiki
        - Restoring Kamiki Village with Sunrise
        - Fixing Kushi's Water Mill
        - Wkaking Up Susano
        - Saving the Merchant in Kamiki
        - Opening the boulder to Shinshu field
        - Mr. Orange fight after restoring Kamiki Villagers"""
    display_name = "Remove some events for a more open start"
    default = 1

#
#class PraiseSanity(Choice):
#    """Randomize Praise Rewards"""
#    display_name = "Randomise Praise Rewards"
#    default = 0
#    options = {
#        "None" :0,
#        "Exclude Animals":1,
#        "Full":2 # 607 Locations, Total of 7724 praise, but you need less to max everything(6020)
#    }
#
#
@dataclass
class OkamiOptions(PerGameCommonOptions):
    BuriedChestsByNight: BuriedChestsByNight
    KarmicTransformers: KarmicTransformers
    OpenGameStart: OpenGameStart
    ProgressiveWeapons:ProgressiveWeapons
#    PraiseSanity:PraiseSanity


okami_option_groups: Dict[str, List[Any]] = {
    "General Options": [
        BuriedChestsByNight,
        KarmicTransformers,
        OpenGameStart,
        ProgressiveWeapons
        #PraiseSanity
        ],

}

slot_data_options = {
    "BuriedChestsByNight",
    "KarmicTransformers",
    "OpenGameStart",
    "ProgressiveWeapons"
#    "PraiseSanity"
}
