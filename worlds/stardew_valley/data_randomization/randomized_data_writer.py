from typing import TextIO

from ..content import StardewContent
from ..data.fish_data import crab_pot_difficulty
from ..data.game_item import ItemTag
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
    for category in sorted(prepared_data.keys()):
        spoiler_handle.write(f"\t{category}:\n")
        for item_name in sorted(prepared_data[category].keys()):
            spoiler_handle.write(f"\t\t{item_name}:\n")
            for value_name in sorted(prepared_data[category][item_name].keys()):
                spoiler_handle.write(f"\t\t\t{value_name}: {prepared_data[category][item_name][value_name]}\n")


def prepare_randomized_data(content: StardewContent, options: StardewValleyOptions):
    data_to_randomize = options.data_randomization.value

    prepared_data = dict()
    prepare_fish_data(content, data_to_randomize, prepared_data)
    prepare_crop_data(content, data_to_randomize, prepared_data)

    return prepared_data


def prepare_fish_data(content: StardewContent, data_to_randomize: set[str], prepared_data):
    prepared_data["Fish"] = dict()
    prepare_fish_catch_method_data(content, data_to_randomize, prepared_data)
    prepare_fish_difficulty_data(content, data_to_randomize, prepared_data)
    prepare_fish_season_data(content, data_to_randomize, prepared_data)
    prepare_fish_location_data(content, data_to_randomize, prepared_data)
    prepare_fish_weather_data(content, data_to_randomize, prepared_data)
    prepare_fish_sell_price_data(content, data_to_randomize, prepared_data)


def prepare_crop_data(content: StardewContent, data_to_randomize: set[str], prepared_data):
    prepared_data["Crops"] = dict()
    prepare_crop_sell_price_data(content, data_to_randomize, prepared_data)


def prepare_fish_catch_method_data(content: StardewContent, data_to_randomize: set[str], prepared_data: dict):
    prepare_fish_data_aspect(content, data_to_randomize, prepared_data,
                             DataRandomizationOptionName.fish_catch_method,
                             lambda fish: True,
                             lambda fish: "Crab Pot" if fish.difficulty == crab_pot_difficulty else "Fishing Rod",
                             "Method")


def prepare_fish_difficulty_data(content: StardewContent, data_to_randomize: set[str], prepared_data: dict):
    prepare_fish_data_aspect(content, data_to_randomize, prepared_data,
                             DataRandomizationOptionName.fish_difficulty,
                             lambda fish: fish.difficulty > 0,
                             lambda fish: fish.difficulty,
                             "Difficulty")


def prepare_fish_season_data(content: StardewContent, data_to_randomize: set[str], prepared_data: dict):
    prepare_fish_data_aspect(content, data_to_randomize, prepared_data,
                             DataRandomizationOptionName.fish_season,
                             lambda fish: len(fish.seasons) > 0 and fish.difficulty != crab_pot_difficulty,
                             lambda fish: list(fish.seasons),
                             "Season")


def prepare_fish_location_data(content: StardewContent, data_to_randomize: set[str], prepared_data: dict):
    prepare_fish_data_aspect(content, data_to_randomize, prepared_data,
                             DataRandomizationOptionName.fish_location,
                             lambda fish: len(fish.locations) > 0,
                             lambda fish: list(fish.locations),
                             "Location")


def prepare_fish_weather_data(content: StardewContent, data_to_randomize: set[str], prepared_data: dict):
    prepare_fish_data_aspect(content, data_to_randomize, prepared_data,
                             DataRandomizationOptionName.fish_weather,
                             lambda fish: len(fish.weather) > 0 and fish.difficulty != crab_pot_difficulty,
                             lambda fish: list(fish.weather),
                             "Weather")


def prepare_fish_sell_price_data(content: StardewContent, data_to_randomize: set[str], prepared_data: dict):
    prepare_fish_data_aspect(content, data_to_randomize, prepared_data,
                             DataRandomizationOptionName.fish_sell_price,
                             lambda fish: fish.sell_price > 0,
                             lambda fish: fish.sell_price,
                             "SellPrice")


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


def prepare_crop_sell_price_data(content: StardewContent, data_to_randomize: set[str], prepared_data: dict):
    prepare_crop_data_aspect(content, data_to_randomize, prepared_data,
                             DataRandomizationOptionName.crop_sell_price,
                             lambda crop: crop.sell_price > 0,
                             lambda crop: crop.sell_price,
                             "SellPrice")


def prepare_crop_data_aspect(content: StardewContent, data_to_randomize: set[str], prepared_data: dict,
                             randomize_toggle: str, crop_validator, crop_data_extractor, aspect_key: str):
    if randomize_toggle not in data_to_randomize:
        return
    crop_item_tags = [ItemTag.FRUIT, ItemTag.VEGETABLE, ItemTag.FORAGE, ItemTag.EDIBLE_MUSHROOM]
    for crop_name, crop_data in content.game_items.items():
        if not any(tag in crop_data.tags for tag in crop_item_tags):
            continue
        if not crop_validator(crop_data):
            continue
        if crop_name not in prepared_data["Crops"]:
            prepared_data["Crops"][crop_name] = dict()
        prepared_data["Crops"][crop_name][aspect_key] = crop_data_extractor(crop_data)
