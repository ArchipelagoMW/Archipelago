from typing import List, TYPE_CHECKING, Dict, Any
from schema import Schema, Optional
from dataclasses import dataclass
from worlds.AutoWorld import PerGameCommonOptions
from Options import Range, Toggle, DeathLink, Choice, OptionDict, DefaultOnToggle, OptionGroup
from ..ahit import slot_data_options

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


class StartWithDivineInstrument(Toggle):
    """Start with a Divine Instrument"""
    display_name = "Start with a Divine Instrument"
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
    StartWithDivineInstrument: StartWithDivineInstrument
#    PraiseSanity:PraiseSanity


okami_option_groups: Dict[str, List[Any]] = {
    "General Options": [
        BuriedChestsByNight,
        StartWithDivineInstrument,
        #PraiseSanity
        ],

}

slot_data_options = {
    "BuriedChestsByNight",
    "StartWithDivineInstrument"
#    "PraiseSanity"
}
