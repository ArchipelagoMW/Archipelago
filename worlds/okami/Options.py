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


@dataclass
class OkamiOptions(PerGameCommonOptions):
    BuriedChestsByNight: BuriedChestsByNight


okami_option_groups: Dict[str, List[Any]] = {
    "General Options": [BuriedChestsByNight]
}

slot_data_options={
    "BuriedChestsByNight"
}