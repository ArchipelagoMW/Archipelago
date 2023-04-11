from typing import Dict, Union
from BaseClasses import MultiWorld
from Options import Toggle, Option, Choice


class ShuffleDoors(Choice):
    """If on, opening doors will require their respective "keys".
    In "simple", doors are sorted into logical groups, which are all opened by receiving an item.
    In "complex", the items are much more granular, and will usually only open a single door each."""
    display_name = "Shuffle Doors"
    option_none = 0
    option_simple = 1
    option_complex = 2


class OrangeTowerAccess(Choice):
    """When "Shuffle Doors" is on, this settings governs the manner in which the Orange Tower floors open up.
    On "individual", there is an item for each floor of the tower, and each floor's item is the only one needed to access that floor.
    On "vanilla", there is an item for each floor of the tower, but a floor only becomes accessible if you have the items for each lower floor as well.
    On "progressive", there are not individual items for each floor, and instead six progressive items, which open up the tower from the bottom floor upward.
    """
    display_name = "Orange Tower Access"
    option_individual = 0
    option_vanilla = 1
    option_progressive = 2


class ShuffleColors(Toggle):
    """If on, an item is added to the pool for every puzzle color (besides White).
    You will need to unlock the requisite colors in order to be able to solve puzzles of that color."""
    display_name = "Shuffle Colors"


class VictoryCondition(Choice):
    """Change the victory condition."""
    display_name = "Victory Condition"
    option_the_end = 0
    option_the_master = 1


lingo_options: Dict[str, type] = {
    "shuffle_doors": ShuffleDoors,
    "orange_tower_access": OrangeTowerAccess,
    "shuffle_colors": ShuffleColors,
    "victory_condition": VictoryCondition
}


def get_option_value(world: MultiWorld, player: int, name: str) -> Union[bool, int]:
    option = getattr(world, name, None)

    if option is None:
        return 0

    if issubclass(lingo_options[name], Toggle):
        return bool(option[player].value)
    return option[player].value
