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


class Goal(Choice):
    """
    Goal
    """
    display_name = "Goal"
    option_richter = 0
    option_shaft = 1
    option_rs = 2
    option_dracula = 3
    option_talisman = 4
    option_td = 5
    default = 3


class NumberOfTalismans(Range):
    """
    Amount of Talismans in game. It might be less based on available locations
    """
    display_name = "Max Number of Talismans"
    range_start = 1
    range_end = 255
    default = 100


class PercentageOfTalismans(Range):
    """
    How many talismans to beat the game
    """
    display_name = "Required Percentage of Talismans"
    range_start = 1
    range_end = 100
    default = 100


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


class XpModifier(Range):
    """Override Monster XP modifier in percentage"""
    display_name = "XP modifier"
    range_start = 0
    range_end = 300
    default = 0


class AttModifier(Range):
    """Override Monster attack modifier in percentage"""
    display_name = "Attack modifier"
    range_start = 0
    range_end = 300
    default = 0


class HpModifier(Range):
    """Override Monster HP modifier in percentage"""
    display_name = "HP modifier"
    range_start = 0
    range_end = 300
    default = 0


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


class ProgShop(Toggle):
    """
        Shop items can be progression items
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


class ProgCandle(Toggle):
    """
        Candle drop can be progression items
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


class ProgDrop(Toggle):
    """
        Enemy drop can be progression items
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


class BonusLuck(Range):
    """A hack way to have bonus luck and help with dropsanity"""
    display_name = "Hacky luck"
    range_start = 0
    range_end = 999
    default = 0


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
    default = "1;2;1;2;1;2;7;3;7;3;8;5;7;6;2;6;2;6;2"


class RandRules(Choice):
    """
    Define randomize rules
    """
    display_name = "Randomize random rules"
    option_full = 0
    option_limited = 1
    option_expanded = 2
    default = 0


class InfiniteWing(Toggle):
    """
        Makes wing smash remains until hit a wall or run out of MP
    """
    display_name = "Infinite wing smash while transform into bat"


class ExtraPool(FreeText):
    """Extra item added to the pool"""
    display_name = "Extra items"
    default = {}


sotn_option_definitions: Dict[str, type(Option)] = {
    "opened_no4": OpenedNO4NO3,
    "opened_are": OpenedDAIARE,
    "opened_no2": OpenedDAINO2,
    "goal": Goal,
    "num_talisman": NumberOfTalismans,
    "per_talisman": PercentageOfTalismans,
    "difficult": Difficult,
    "xp_mod": XpModifier,
    "att_mod": AttModifier,
    "hp_mod": HpModifier,
    "bosses_need": BossesNeed,
    "rng_songs": RngSongs,
    "rng_shop": RngShop,
    "prog_shop": ProgShop,
    "lib_shop": LibCardShop,
    "rng_prices": RngPrices,
    "exp_need": ExpNeed,
    "rng_candles": RngCandles,
    "prog_candles": ProgCandle,
    "rng_drops": RngDrops,
    "prog_drops": ProgDrop,
    "enemysanity": Enemysanity,
    "dropsanity": Dropsanity,
    "bonus_luck": BonusLuck,
    "boostqty": Boostqty,
    "boostweight": BoostWeight,
    "trapqty": Trapqty,
    "trapweight": TrapWeight,
    "rand_rules": RandRules,
    "infinite_wing": InfiniteWing,
    "extra_pool": ExtraPool
}


def get_option_value(multiworld: MultiWorld, player: int, name: str) -> Union[int, dict]:
    option = getattr(multiworld, name, None)
    if option is None:
        return 0

    return option[player].value
