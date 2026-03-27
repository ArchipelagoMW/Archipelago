from typing import TextIO

from ..content import StardewContent
from ..options import StardewValleyOptions
from ..options.options import DataRandomizationBehavior
from ..strings.ap_names.ap_option_names import DataRandomizationOptionName


def add_randomized_data_to_spoiler_log(spoiler_handle: TextIO, player_name: str, content: StardewContent, options: StardewValleyOptions):
    behavior = options.data_randomization_behavior
    if behavior == DataRandomizationBehavior.option_off:
        return

    data_to_randomize = options.data_randomization.value
    if len(data_to_randomize) <= 0:
        return

    data_to_print = dict()

    prepare_fish_difficulty_for_print(content, data_to_randomize, data_to_print)
    prepare_fish_season_for_print(content, data_to_randomize, data_to_print)

    spoiler_handle.write(f"\n\nRandomized Data ({player_name}):\n")
    for item_name in data_to_print:
        spoiler_handle.write(f"\t{item_name}:\n")
        for value_name in data_to_print[item_name]:
            spoiler_handle.write(f"\t\t{value_name}: {data_to_print[item_name][value_name]}\n")


def prepare_fish_difficulty_for_print(content, data_to_randomize, data_to_print):
    if DataRandomizationOptionName.fish_difficulty not in data_to_randomize:
        return
    for fish_name, fish_data in content.fishes.items():
        if fish_data.difficulty <= 0:
            continue
        if fish_name not in data_to_print:
            data_to_print[fish_name] = dict()
        data_to_print[fish_name]["difficulty"] = fish_data.difficulty


def prepare_fish_season_for_print(content, data_to_randomize, data_to_print):
    if DataRandomizationOptionName.fish_season not in data_to_randomize:
        return
    for fish_name, fish_data in content.fishes.items():
        if fish_name not in data_to_print:
            data_to_print[fish_name] = dict()
        data_to_print[fish_name]["season"] = fish_data.seasons
