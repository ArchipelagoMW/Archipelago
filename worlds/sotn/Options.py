from typing import Dict, Union
from BaseClasses import MultiWorld
from Options import Option, Toggle


class OpenedNO4NO3(Toggle):
    """
        If true, the back door of Underground Caverns will be open
    """
    display_name = "OpenedNO4NO3"


class OpenedDAIARE(Toggle):
    """
        If true, the back door of Colosseum will be open
    """
    display_name = "OpenedDAIARE"


class OpenedDAINO2(Toggle):
    """
        If true, the back door of Olrox's Quarters will be open
    """
    display_name = "OpenedDAINO2"


sotn_option_definitions: Dict[str, type(Option)] = {
    "OpenedNO4NO3": OpenedNO4NO3,
    "OpenedDAIARE": OpenedDAIARE,
    "OpenedDAINO2": OpenedDAINO2,
}


def get_option_value(multiworld: MultiWorld, player: int, name: str) -> Union[int, dict]:
    option = getattr(multiworld, name, None)
    if option is None:
        return 0

    return option[player].value
