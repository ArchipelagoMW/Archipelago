# Object classes from AP that represent different types of options that you can create
from Options import Option, FreeText, NumericOption, Toggle, DefaultOnToggle, Choice, TextChoice, Range, NamedRange, OptionGroup, PerGameCommonOptions
# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value
from typing import Type, Any


####################################################################
# NOTE: At the time that options are created, Manual has no concept of the multiworld or its own world.
#       Options are defined before the world is even created.
#
# Example of creating your own option:
#
#   class MakeThePlayerOP(Toggle):
#       """Should the player be overpowered? Probably not, but you can choose for this to do... something!"""
#       display_name = "Make me OP"
#
#   options["make_op"] = MakeThePlayerOP
#
#
# Then, to see if the option is set, you can call is_option_enabled or get_option_value.
#####################################################################


class Enable_Levels_1_to_19(Toggle):
    """
    Should levels 1 to 19 be location checks?
    """
class Enable_Levels_20_to_39(Toggle):
    """
    Should levels 20 to 39 be location checks?
    """
class Enable_Levels_40_to_59(Toggle):
    """
    Should levels 40 to 59 be location checks?
    """
class Enable_Levels_60_to_79(Toggle):
    """
    Should levels 60 to 79 be location checks?
    """
class Enable_Levels_80_to_99(Toggle):
    """
    Should levels 80 to 99 be location checks?
    """
class Enable_Runes(Toggle):
    """
    Should runes be location checks?
    """
class Is_this_an_Async_run(Toggle):
    """
    Should generation account for this being an async run?
    """

# This is called before any manual options are defined, in case you want to define your own with a clean slate or let Manual define over them
def before_options_defined(options: dict[str, Type[Option[Any]]]) -> dict[str, Type[Option[Any]]]:
    options["Enable_Levels_1_to_19"] = Enable_Levels_1_to_19
    options["Enable_Levels_20_to_39"] = Enable_Levels_20_to_39
    options["Enable_Levels_40_to_59"] = Enable_Levels_40_to_59
    options["Enable_Levels_60_to_79"] = Enable_Levels_60_to_79
    options["Enable_Levels_80_to_99"] = Enable_Levels_80_to_99
    options["Enable_Runes"] = Enable_Runes
    options["Is_this_an_Async_run"] = Is_this_an_Async_run
    return options

# This is called after any manual options are defined, in case you want to see what options are defined or want to modify the defined options
def after_options_defined(options: Type[PerGameCommonOptions]):
    # To access a modifiable version of options check the dict in options.type_hints
    # For example if you want to change DLC_enabled's display name you would do:
    # options.type_hints["DLC_enabled"].display_name = "New Display Name"

    #  Here's an example on how to add your aliases to the generated goal
    # options.type_hints['goal'].aliases.update({"example": 0, "second_alias": 1})
    # options.type_hints['goal'].options.update({"example": 0, "second_alias": 1})  #for an alias to be valid it must also be in options

    pass

# Use this Hook if you want to add your Option to an Option group (existing or not)
def before_option_groups_created(groups: dict[str, list[Type[Option[Any]]]]) -> dict[str, list[Type[Option[Any]]]]:
    # Uses the format groups['GroupName'] = [TotalCharactersToWinWith]
    return groups

def after_option_groups_created(groups: list[OptionGroup]) -> list[OptionGroup]:
    return groups
