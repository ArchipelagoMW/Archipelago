import typing

from Options import Choice, Range, Option, Toggle, DeathLink, DefaultOnToggle, OptionList


class Bosses(Range):
    """
    Determines the goal of the seed
    Knautilus: Scuttle the Knautilus in Krematoa and defeat Baron K. Roolenstein
    Banana Bird Hunt: Find a certain number of Banana Birds and rescue their mother
    """
    display_name = "Bosses Required"
    range_start = 0
    range_end = 11
    default = 6


class Goal(Choice):
    """
    Which Difficulty Level to use
    NORML: The Normal Difficulty
    HARDR: Many DK Barrels are removed
    TUFST: Most DK Barrels and all Midway Barrels are removed
    """
    display_name = "6-8 Condition"
    option_castles = 0
    option_bosses = 1
    option_open = 2
    default = 0

class ExtraStages(Toggle):
    """
    Whether or not the 6 Extra stages can be required.
    """
    display_name = "Include Extra Levels"

class EggCap(Range):
    """
    Determines the goal of the seed
    Knautilus: Scuttle the Knautilus in Krematoa and defeat Baron K. Roolenstein
    Banana Bird Hunt: Find a certain number of Banana Birds and rescue their mother
    """
    display_name = "Starting Egg Capacity"
    range_start = 1
    range_end = 6
    default = 6


class InventoryLogic(Toggle):
    """
    Whether or not the 6 Extra stages can be required.
    """
    display_name = "Inventory Items in Logic"




dkc3_options: typing.Dict[str, type(Option)] = {
    #"death_link": DeathLink,                                 # Disabled
    "goal": Goal,
    #"include_trade_sequence": IncludeTradeSequence,          # Disabled
    "bosses": Bosses,
    "item_logic": InventoryLogic,
    "require_extra": ExtraStages,
    "egg_limit": EggCap,
}
