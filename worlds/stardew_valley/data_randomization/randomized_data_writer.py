from typing import TextIO

from ..content import StardewContent
from ..data.fish_data import FishItem
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

    prepared_data = prepare_randomized_data(content, options)

    spoiler_handle.write(f"\n\nRandomized Data ({player_name}):\n")
    for category in prepared_data:
        spoiler_handle.write(f"\t{category}:\n")
        for item_name in prepared_data[category]:
            spoiler_handle.write(f"\t\t{item_name}:\n")
            for value_name in prepared_data[category][item_name]:
                spoiler_handle.write(f"\t\t\t{value_name}: {prepared_data[category][item_name][value_name]}\n")


def prepare_randomized_data(content: StardewContent, options: StardewValleyOptions):
    data_to_randomize = options.data_randomization.value

    prepared_data = dict()
    prepare_fish_data(content, data_to_randomize, prepared_data)

    return prepared_data


def prepare_fish_data(content: StardewContent, data_to_randomize: set[str], prepared_data):
    prepared_data["Fish"] = dict()
    prepare_fish_difficulty_data(content, data_to_randomize, prepared_data)
    prepare_fish_season_data(content, data_to_randomize, prepared_data)
    prepare_fish_location_data(content, data_to_randomize, prepared_data)
    prepare_fish_weather_data(content, data_to_randomize, prepared_data)


def prepare_fish_difficulty_data(content: StardewContent, data_to_randomize: set[str], prepared_data: dict):
    prepare_fish_data_aspect(content, data_to_randomize, prepared_data,
                             DataRandomizationOptionName.fish_difficulty,
                             lambda fish: fish.difficulty > 0,
                             lambda fish: fish.difficulty,
                             "difficulty")


def prepare_fish_season_data(content: StardewContent, data_to_randomize: set[str], prepared_data: dict):
    prepare_fish_data_aspect(content, data_to_randomize, prepared_data,
                             DataRandomizationOptionName.fish_season,
                             lambda fish: len(fish.seasons) > 0 and fish_is_included(data_to_randomize, fish),
                             lambda fish: list(fish.seasons),
                             "season")


def prepare_fish_location_data(content: StardewContent, data_to_randomize: set[str], prepared_data: dict):
    prepare_fish_data_aspect(content, data_to_randomize, prepared_data,
                             DataRandomizationOptionName.fish_location,
                             lambda fish: len(fish.locations) > 0 and fish_is_included(data_to_randomize, fish),
                             lambda fish: list(fish.locations),
                             "location")


def prepare_fish_weather_data(content: StardewContent, data_to_randomize: set[str], prepared_data: dict):
    prepare_fish_data_aspect(content, data_to_randomize, prepared_data,
                             DataRandomizationOptionName.fish_weather,
                             lambda fish: len(fish.weather) > 0 and fish_is_included(data_to_randomize, fish),
                             lambda fish: list(fish.weather),
                             "weather")


def prepare_fish_data_aspect(content: StardewContent, data_to_randomize: set[str], prepared_data: dict,
                             randomize_toggle: str, fish_validator, fish_data_extractor, aspect_key: str):
    if randomize_toggle not in data_to_randomize:
        return
    for fish_name, fish_data in content.fishes.items():
        if not fish_validator(fish_data):
            continue
        if fish_name not in prepared_data["Fish"]:
            prepared_data["Fish"][fish_name] = dict()
        prepared_data["Fish"][fish_name][aspect_key] = fish_data_extractor(fish_data)


def fish_is_included(data_to_randomize: set[str], fish: FishItem) -> bool:
    if DataRandomizationOptionName.fish_includes_crab_pot in data_to_randomize:
        return True
    return fish.difficulty > 0
