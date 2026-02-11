from typing import Dict, Callable, Any, List

from BaseClasses import Item, ItemClassification as IClass, MultiWorld
from . import data
from .options import SonicRushOptions


def always_progression(options: SonicRushOptions, multiworld: MultiWorld) -> IClass:
    return IClass.progression


def always_progression_skip_balancing(options: SonicRushOptions, multiworld: MultiWorld) -> IClass:
    return IClass.progression_skip_balancing


def always_useful(options: SonicRushOptions, multiworld: MultiWorld) -> IClass:
    return IClass.useful


def always_filler(options: SonicRushOptions, multiworld: MultiWorld) -> IClass:
    return IClass.filler


def always_trap(options: SonicRushOptions, multiworld: MultiWorld) -> IClass:
    return IClass.trap


def fill_error_prevention(options: SonicRushOptions, multiworld: MultiWorld) -> IClass:
    return IClass.useful if len(multiworld.worlds) <= 2 else IClass.progression


zone_unlocks: Dict[str, Callable[[SonicRushOptions, MultiWorld], IClass]] = {
    zone: always_progression
    for zone in data.zone_names
}

progressive_level_selects: Dict[str, Callable[[SonicRushOptions, MultiWorld], IClass]] = {
    "Progressive Level Select (Sonic)": always_progression_skip_balancing,
    "Progressive Level Select (Blaze)": always_progression_skip_balancing,
}

emeralds: Dict[str, Callable[[SonicRushOptions, MultiWorld], IClass]] = {
    f"{color} {dim} Emerald": always_progression_skip_balancing
    for color in data.emerald_colors
    for dim in ["Chaos", "Sol"]
}

sidekicks: Dict[str, Callable[[SonicRushOptions, MultiWorld], IClass]] = {
    "Tails": always_filler,
    "Cream": always_filler,
    "Kidnapping Tails": always_trap,
    "Kidnapping Cream": always_trap,
}

fillers: Dict[str, Callable[[SonicRushOptions, MultiWorld], IClass]] = {
    "Extra Life (Sonic)": always_filler,
    "Extra Life (Blaze)": always_filler,
}

traps: Dict[str, Callable[[SonicRushOptions, MultiWorld], IClass]] = {
    "Halving Extra Lives (Sonic)": always_trap,
    "Halving Extra Lives (Blaze)": always_trap,
}

item_table: Dict[str, Callable[[SonicRushOptions, MultiWorld], IClass]] = {
    **zone_unlocks,
    **progressive_level_selects,
    **emeralds,
    **sidekicks,
    **fillers,
    **traps,
}

item_list: List[str] = [
    *zone_unlocks,
    *progressive_level_selects,
    *emeralds,
    *sidekicks,
    *fillers,
    *traps,
]


def filler(random: float) -> str:
    """Returns a random filler item."""
    pool = [
        *fillers
    ]
    return random_choice_nested(random, pool)


def trap(random: float) -> str:
    """Returns a random trap item."""
    pool = [
        *traps
    ]
    return random_choice_nested(random, pool)


def random_choice_nested(random: float, nested: List[Any]) -> Any:
    """Helper function for getting a random element from a nested list."""
    current: Any = nested
    while isinstance(current, List):
        index_float = random*len(current)
        current = current[int(index_float)]
        random = index_float-int(index_float)
    return current


item_descriptions = {}


class SonicRushItem(Item):
    game = "Sonic Rush"
