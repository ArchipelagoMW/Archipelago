from argparse import Namespace
from typing import Any, Iterable

from BaseClasses import PlandoOptions
from Options import VerifyKeys
from ... import StardewValleyWorld
from ...options import StardewValleyOptions, StardewValleyOption


def parse_class_option_keys(test_options: dict[str | StardewValleyOption, Any] | None) -> dict:
    """ Now the option class is allowed as key. """
    if test_options is None:
        return {}
    parsed_options = {}

    for option, value in test_options.items():
        if hasattr(option, "internal_name"):
            assert option.internal_name not in test_options, "Defined two times by class and internal_name"
            parsed_options[option.internal_name] = value
        else:
            assert option in StardewValleyOptions.type_hints, \
                f"All keys of world_options must be a possible Stardew Valley option, {option} is not."
            parsed_options[option] = value

    return parsed_options


def fill_dataclass_with_default(test_options: dict[str | StardewValleyOption, Any] | None) -> StardewValleyOptions:
    test_options = parse_class_option_keys(test_options)

    filled_options = {}
    for option_name, option_class in StardewValleyOptions.type_hints.items():

        value = option_class.from_any(test_options.get(option_name, option_class.default))

        if issubclass(option_class, VerifyKeys):
            # Values should already be verified, but just in case...
            value.verify(StardewValleyWorld, "Tester", PlandoOptions.bosses)

        filled_options[option_name] = value

    return StardewValleyOptions(**filled_options)


def fill_namespace_with_default(test_options: dict[str, Any] | Iterable[dict[str, Any]]) -> Namespace:
    if isinstance(test_options, dict):
        test_options = [test_options]

    args = Namespace()
    for option_name, option_class in StardewValleyOptions.type_hints.items():
        all_players_option = {}

        for player_id, player_options in enumerate(test_options):
            # Player id starts at 1
            player_id += 1
            player_name = f"Tester{player_id}"

            value = option_class.from_any(player_options.get(option_name, option_class.default))

            if issubclass(option_class, VerifyKeys):
                # Values should already be verified, but just in case...
                value.verify(StardewValleyWorld, player_name, PlandoOptions.bosses)

            all_players_option[player_id] = value

        setattr(args, option_name, all_players_option)

    return args
