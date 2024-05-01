from typing import Dict, Union
from BaseClasses import MultiWorld
from Options import Option, Toggle, Choice, Range, FreeText


class OpenedNO4NO3(Toggle):
    """
        If true, the back door of Underground Caverns will be open
    """
    display_name = "Opened NO4 Backdoor"


class OpenedDAIARE(Toggle):
    """
        If true, the back door of Colosseum will be open
    """
    display_name = "Opened ARE Backdoor"


class OpenedDAINO2(Toggle):
    """
        If true, the back door of Olrox's Quarters will be open
    """
    display_name = "Opened NO2 Backdoor"


class Difficult(Choice):
    """
    Determines the difficult
    """
    display_name = "Difficult"
    option_easy = 0
    option_normal = 1
    option_hard = 2
    option_insane = 3
    default = 1


class BossesNeed(Range):
    """Bosses required to beat Dracula."""
    display_name = "Required Bosses Tokens"
    range_start = 0
    range_end = 20
    default = 0


class RngSongs(Toggle):
    """
        Randomize the zone songs
    """
    display_name = "Randomize Songs"


class RngShop(Toggle):
    """
        Randomize shop items
    """
    display_name = "Randomize shop items"


class NoProgShop(Toggle):
    """
        Shop items can't be progression items
    """
    display_name = "Forbid progression items on shop"


class LibCardShop(Toggle):
    """
        Shop items will have a library card in stock
    """
    display_name = "Library card will be available on librarian"


class RngPrices(Choice):
    """
    Randomize shop prices
    """
    display_name = "Shop prices"
    option_disable = 0
    option_cheap = 1
    option_normal = 2
    option_expensive = 3
    default = 0


class ExpNeed(Range):
    """Exploration tokens required to beat Dracula."""
    display_name = "Required Exploration Tokens"
    range_start = 0
    range_end = 20
    default = 0


class RngCandles(Choice):
    """
    Randomize candle drops
    """
    display_name = "Randomize candle drop"
    option_off = 0
    option_on = 1
    option_crazy = 2
    default = 0


class NoProgCandle(Toggle):
    """
        Candle drop can't be progression items
    """
    display_name = "Forbid progression items on candles"


class RngDrops(Choice):
    """
    Randomize enemies drops
    """
    display_name = "Randomize enemy drop"
    option_off = 0
    option_on = 1
    option_crazy = 2
    default = 0


class NoProgDrop(Toggle):
    """
        Enemy drop can't be progression items
    """
    display_name = "Forbid progression items on enemies"


class Enemysanity(Toggle):
    """
        Enemies become a location check
    """
    display_name = "Enemies become a location check"


class Dropsanity(Toggle):
    """
        Enemies second item drop become a location check
    """
    display_name = "Enemies drops are locations checks"


class Boostqty(Range):
    """Boosts quantity in the pool."""
    display_name = "Boost quantity"
    range_start = 0
    range_end = 50
    default = 0


class BoostWeight(FreeText):
    """Weights for randomize boosts"""
    display_name = "Boosts weights"
    default = "10;6;1;6;1;6;1;6;1;7;7;7"


class Trapqty(Range):
    """Traps quantity in the pool."""
    display_name = "Trap quantity"
    range_start = 0
    range_end = 50
    default = 0


class TrapWeight(FreeText):
    """Weights for randomize traps"""
    display_name = "Traps weights"
    default = "1;2;1;2;1;2;7;3;7;3;6;2;6;2"


class ExtraPool(FreeText):
    """Extra item added to the pool"""
    display_name = "Extra items"
    default = {}


sotn_option_definitions: Dict[str, type(Option)] = {
    "opened_no4": OpenedNO4NO3,
    "opened_are": OpenedDAIARE,
    "opened_no2": OpenedDAINO2,
    "difficult": Difficult,
    "bosses_need": BossesNeed,
    "rng_songs": RngSongs,
    "rng_shop": RngShop,
    "noprog_shop": NoProgShop,
    "lib_shop": LibCardShop,
    "rng_prices": RngPrices,
    "exp_need": ExpNeed,
    "rng_candles": RngCandles,
    "noprog_candles": NoProgCandle,
    "rng_drops": RngDrops,
    "noprog_drops": NoProgDrop,
    "enemysanity": Enemysanity,
    "dropsanity": Dropsanity,
    "boostqty": Boostqty,
    "boostweight": BoostWeight,
    "trapqty": Trapqty,
    "trapweight": TrapWeight,
    "extra_pool": ExtraPool
}


def get_option_value(multiworld: MultiWorld, player: int, name: str) -> Union[int, dict]:
    option = getattr(multiworld, name, None)
    if option is None:
        return 0

    return option[player].value
