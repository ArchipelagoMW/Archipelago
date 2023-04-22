from typing import Dict, Union
from BaseClasses import MultiWorld
from Options import Toggle, Option, Choice, DefaultOnToggle, Range


class ShuffleDoors(Choice):
    """If on, opening doors will require their respective "keys".
    In "simple", doors are sorted into logical groups, which are all opened by receiving an item.
    In "complex", the items are much more granular, and will usually only open a single door each."""
    display_name = "Shuffle Doors"
    option_none = 0
    option_simple = 1
    option_complex = 2


class ProgressiveOrangeTower(DefaultOnToggle):
    """When "Shuffle Doors" is on, this setting governs the manner in which the Orange Tower floors open up.
    If off, there is an item for each floor of the tower, and each floor's item is the only one needed to access that floor.
    If on, there are six progressive items, which open up the tower from the bottom floor upward.
    """
    display_name = "Progressive Orange Tower"


class ReduceChecks(DefaultOnToggle):
    """When "Shuffle Doors" is off, there are far more location checks than there are items.
    Enabling reduce checks will remove many of the locations that are associated with opening doors.
    This option is ignored if "Shuffle Doors" is on."""
    display_name = "Reduce Checks"


class ShuffleColors(Toggle):
    """If on, an item is added to the pool for every puzzle color (besides White).
    You will need to unlock the requisite colors in order to be able to solve puzzles of that color."""
    display_name = "Shuffle Colors"


class ShufflePanels(Choice):
    """If on, the puzzles on each panel are randomized.
    On "rearrange", the puzzles are the same as the ones in the base game, but are placed in different areas."""
    display_name = "Shuffle Panels"
    option_none = 0
    option_rearrange = 1


class ShufflePaintings(Toggle):
    """If on, the destination, location, and appearance of the painting warps in the game will be randomized."""
    display_name = "Shuffle Paintings"


class VictoryCondition(Choice):
    """Change the victory condition."""
    display_name = "Victory Condition"
    option_the_end = 0
    option_the_master = 1


class TrapPercentage(Range):
    """Replaces junk items with traps, at the specified rate."""
    display_name = "Trap Percentage"
    range_start = 0
    range_end = 100
    default = 20


class DeathLink(Toggle):
    """If on: Whenever another player on death link dies, you will be returned to the starting room."""
    display_name = "Death Link"


lingo_options: Dict[str, type] = {
    "shuffle_doors": ShuffleDoors,
    "progressive_orange_tower": ProgressiveOrangeTower,
    "reduce_checks": ReduceChecks,
    "shuffle_colors": ShuffleColors,
    "shuffle_panels": ShufflePanels,
    "shuffle_paintings": ShufflePaintings,
    "victory_condition": VictoryCondition,
    "trap_percentage": TrapPercentage,
    "death_link": DeathLink
}


def get_option_value(world: MultiWorld, player: int, name: str) -> Union[bool, int]:
    option = getattr(world, name, None)

    if option is None:
        return 0

    if issubclass(lingo_options[name], Toggle):
        return bool(option[player].value)
    return option[player].value
