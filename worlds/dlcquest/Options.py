from typing import Union, Dict, runtime_checkable, Protocol
from Options import Option, DeathLink, Choice, Toggle, SpecialRange
from dataclasses import dataclass


@runtime_checkable
class DLCQuestOption(Protocol):
    internal_name: str


@dataclass
class DLCQuestOptions:
    options: Dict[str, Union[bool, int]]

    def __getitem__(self, item: Union[str, DLCQuestOption]) -> Union[bool, int]:
        if isinstance(item, DLCQuestOption):
            item = item.internal_name

        return self.options.get(item, None)


class FalseDoubleJump(Choice):
    """If you can do a double jump without the pack for it (glitch)."""
    internal_name = "double_jump_glitch"
    display_name = "Double Jump glitch"
    option_none = 0
    option_simple = 1
    option_all = 2
    default = 0


class TimeIsMoney(Choice):
    """Is your time worth the money, are you ready to grind your sword by hand?"""
    internal_name = "time_is_money"
    display_name = "Time Is Money"
    option_required = 0
    option_optional = 1
    default = 0


class CoinSanity(Choice):
    """This is for the insane it can be 825 check, it is coin sanity"""
    internal_name = "coinsanity"
    display_name = "CoinSanity"
    option_none = 0
    option_coin = 1
    default = 0


class CoinSanityRange(SpecialRange):
    """This is the amount of coin in a coin bundle"""
    internal_name = "coinbundlequantity"
    display_name = "Coin Bundle Quantity"
    range_start = 1
    range_end = 100
    default = 20
    special_range_names = {
        "low": 5,
        "normal": 20,
        "high": 50,
    }


class EndingChoice(Choice):
    """Which ending is considered completion for the basic campaign"""
    internal_name = "ending_choice"
    display_name = "Ending Choice"
    option_any = 0
    option_true = 1
    default = 1


class Campaign(Choice):
    """Which campaign you want to play"""
    internal_name = "campaign"
    display_name = "Campaign"
    option_basic = 0
    option_live_freemium_or_die = 1
    option_both = 2
    default = 0


class ItemShuffle(Choice):
    """Should Inventory Items be separate from their DLCs and shuffled in the item pool"""
    internal_name = "item_shuffle"
    display_name = "Item Shuffle"
    option_disabled = 0
    option_shuffled = 1
    default = 0


DLCQuest_options: Dict[str, type(Option)] = {
    option.internal_name: option
    for option in [
        FalseDoubleJump,
        CoinSanity,
        CoinSanityRange,
        TimeIsMoney,
        EndingChoice,
        Campaign,
        ItemShuffle,
    ]
}
default_options = {option.internal_name: option.default for option in DLCQuest_options.values()}
DLCQuest_options["death_link"] = DeathLink


def fetch_options(world, player: int) -> DLCQuestOptions:
    return DLCQuestOptions({option: get_option_value(world, player, option) for option in DLCQuest_options})


def get_option_value(world, player: int, name: str) -> Union[bool, int]:
    assert name in DLCQuest_options, f"{name} is not a valid option for DLC Quest."

    value = getattr(world, name)

    if issubclass(DLCQuest_options[name], Toggle):
        return bool(value[player].value)
    return value[player].value
