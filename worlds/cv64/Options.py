from typing import Dict, Union
from BaseClasses import MultiWorld
from Options import Option, Choice, DefaultOnToggle, Range, Toggle, DeathLink


class IncreaseItemLimit(DefaultOnToggle):
    """If enabled, the use item-holding limit will be increased from 10 to 99 of each item."""
    display_name = "Increase Item Limit"


class RevealInvisibleItems(DefaultOnToggle):
    """If enabled, all invisible pickup items will be made visible."""
    display_name = "Reveal Invisible Items"


class StartLocation(Choice):
    """Sets the player's starting location."""
    display_name = "Start Location"
    option_forest = 0
    option_villa = 1
    option_cc = 2
    option_randomstage = 3
    option_randommap = 4


class EntranceRandomization(Choice):
    """Sets which map exit destinations to shuffle. Regardless of the setting or character chosen, the Villa coffin and
    Castle Center elevator bridges can possibly send you to two different places (depending on whether it is day or
    night for the former)."""
    display_name = "Entrance Randomization"
    option_none = 0
    option_stages = 1
    option_all = 2


class DraculasChamberCondition(Choice):
    """Sets the requirements for opening the door to Dracula's chamber."""
    display_name = "Dracula's Chamber Condition"
    option_none = 0
    option_crystal = 1
    option_bosses = 2
    option_specials = 3
    default = 1


class FightRenon(Choice):
    """Sets the condition on which the Renon fight will trigger.
    Vanilla = after spending 30,000 gold in his shop."""
    display_name = "Fight Renon"
    option_never = 0
    option_vanilla = 1
    option_always = 2
    default = 1


class FightVincent(Choice):
    """Sets the condition on which the vampire Vincent fight will trigger.
    Vanilla = after 16 or more in-game days pass."""
    display_name = "Fight Vincent"
    option_never = 0
    option_vanilla = 1
    option_always = 2
    default = 1


class BadEndingCondition(Choice):
    """Sets the condition on which the bad ending will trigger.
    Vanilla = if vampire Vincent was fought."""
    display_name = "Bad Ending Condition"
    option_never = 0
    option_vanilla = 1
    option_always = 2
    default = 1


class NumberOfStages(Range):
    """Sets how many stages are included besides Castle Keep."""
    range_start = 1
    range_end = 13
    default = 10


class Special2sPerWarp(Range):
    """Sets how many Special2s are needed per warp menu option unlock."""
    range_start = 0
    range_end = 9
    default = 5


class ExtraSpecial2s(Range):
    """Sets how many extra Speical2s are in the pool in addition to what's needed to select every warp destination."""
    range_start = 0
    range_end = 20
    default = 10


class Special1sRequired(Range):
    """Sets how many Special1s are needed to enter Dracula's chamber (if Dracula's Chamber Condition is set to
    Special1s)."""
    range_start = 1
    range_end = 50
    default = 10


class ExtraSpecial1s(Range):
    """Sets how many extra Speical1s are in the pool in addition to what's needed to enter Dracula's chamber."""
    range_start = 1
    range_end = 13
    default = 10


class CarrieLogic(Toggle):
    """If enabled, the two Underground Waterway checks beyond the crawlspace will be included; otherwise, they'll be
    left vanilla. Can be combined with Glitch Logic to include Carrie-only glitches."""
    display_name = "Carrie Logic"


class GlitchLogic(Toggle):
    """If enabled, sequence break glitches will be properly considered in logic (i.e. Left Tower Skip). Can be combined
    with Carrie Logic to include Carrie-only glitches."""
    display_name = "Glitch Logic"


cv64_options: Dict[str, Option] = {
    "NumberOfStages": NumberOfStages,
    "StartLocation": StartLocation,
    "EntranceRandomization": EntranceRandomization,
    "Special2sPerWarp": Special2sPerWarp,
    "ExtraSpecial2s": ExtraSpecial2s,
    "DraculasCondition": DraculasChamberCondition,
    "Special1sRequired": Special1sRequired,
    "ExtraSpecial1s": ExtraSpecial1s,
    "CarrieLogic": CarrieLogic,
    "GlitchLogic": GlitchLogic,
    "FightRenon": FightRenon,
    "FightVincent": FightVincent,
    "BadEndingCondition": BadEndingCondition,
    "IncreaseItemLimit": IncreaseItemLimit,
    "RevealInvisibleItems": RevealInvisibleItems,
    "DeathLink": DeathLink,
}


def is_option_enabled(world: MultiWorld, player: int, name: str) -> bool:
    return get_option_value(world, player, name) > 0


def get_option_value(world: MultiWorld, player: int, name: str) -> Union[int, dict]:
    option = getattr(world, name, None)
    if option == None:
        return 0

    return option[player].value
