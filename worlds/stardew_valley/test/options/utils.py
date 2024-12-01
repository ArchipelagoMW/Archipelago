from argparse import Namespace
from typing import Any, Iterable

from BaseClasses import PlandoOptions
from Options import VerifyKeys
from ... import StardewValleyWorld
from ...options import StardewValleyOptions


def fill_dataclass_with_default(test_options: dict[str, Any]) -> StardewValleyOptions:
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
