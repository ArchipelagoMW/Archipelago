from random import Random

from .data_randomizer_behaviors import randomizers_per_behavior
from ..content import StardewContent
from ..content.override import override
from ..data.fish_data import FishItem
from ..options import StardewValleyOptions
from ..options.options import DataRandomizationBehavior
from ..strings.ap_names.ap_option_names import DataRandomizationOptionName


def randomize_data(content: StardewContent, options: StardewValleyOptions, random: Random) -> StardewContent:
    behavior = options.data_randomization_behavior
    if behavior == DataRandomizationBehavior.option_off:
        return content

    data_to_randomize = options.data_randomization.value
    if len(data_to_randomize) <= 0:
        return content

    randomize_fish_difficulty(content, data_to_randomize, behavior, random)
    randomize_fish_season(content, data_to_randomize, behavior, random)
    randomize_fish_location(content, data_to_randomize, behavior, random)
    randomize_fish_weather(content, data_to_randomize, behavior, random)

    return content


def fish_is_included(data_to_randomize: set[str], fish_data: FishItem) -> bool:
    if DataRandomizationOptionName.fish_includes_crab_pot in data_to_randomize:
        return True
    return fish_data.difficulty > 0


def randomize_fish_difficulty(content: StardewContent, data_to_randomize: set[str], behavior: DataRandomizationBehavior, random: Random):
    if DataRandomizationOptionName.fish_difficulty not in data_to_randomize:
        return

    difficulties_by_fish = {fish_name: fish_data.difficulty for fish_name, fish_data in content.fishes.items() if fish_data.difficulty > 0}
    randomized_difficulties_per_fish = randomizers_per_behavior[behavior](difficulties_by_fish, random)

    for fish_name, fish_difficulty in randomized_difficulties_per_fish.items():
        original_fish = content.fishes[fish_name]
        content.fishes[fish_name] = override(original_fish, difficulty=fish_difficulty)


def randomize_fish_season(content: StardewContent, data_to_randomize: set[str], behavior: DataRandomizationBehavior, random: Random):
    if DataRandomizationOptionName.fish_season not in data_to_randomize:
        return

    seasons_by_fish = {fish_name: fish_data.seasons for fish_name, fish_data in content.fishes.items()
                       if len(fish_data.seasons) >= 1 and fish_is_included(data_to_randomize, fish_data)}
    randomized_seasons_per_fish = randomizers_per_behavior[behavior](seasons_by_fish, random)

    season_groups = sorted({val for val in seasons_by_fish.values()})
    possible_seasons = sorted({entry for sublist in randomized_seasons_per_fish for entry in sublist})

    for fish_name, fish_season in randomized_seasons_per_fish.items():
        original_fish = content.fishes[fish_name]

        # Crab pot fish are a massive pain to find. Let's be nice.
        minimum_seasons_for_crab_pot_fish = 2
        while original_fish.difficulty <= 0 and len(fish_season) < minimum_seasons_for_crab_pot_fish:
            added_season = random.choice(possible_seasons)
            fish_season = tuple({*fish_season, added_season})

        content.fishes[fish_name] = override(original_fish, seasons=fish_season)


def randomize_fish_location(content: StardewContent, data_to_randomize: set[str], behavior: DataRandomizationBehavior, random: Random):
    if DataRandomizationOptionName.fish_location not in data_to_randomize:
        return

    locations_by_fish = {fish_name: fish_data.locations for fish_name, fish_data in content.fishes.items()
                         if len(fish_data.locations) >= 1 and fish_is_included(data_to_randomize, fish_data)}
    randomized_locations_per_fish = randomizers_per_behavior[behavior](locations_by_fish, random)

    location_groups = sorted({val for val in locations_by_fish.values()})
    possible_locations = sorted({entry for sublist in location_groups for entry in sublist})

    for fish_name, fish_location in randomized_locations_per_fish.items():
        original_fish = content.fishes[fish_name]

        # Crab pot fish are a massive pain to find. Let's be nice.
        minimum_locations_for_crab_pot_fish = 4
        while original_fish.difficulty <= 0 and len(fish_location) < minimum_locations_for_crab_pot_fish:
            added_location = random.choice(possible_locations)
            fish_location = tuple({*fish_location, added_location})

        content.fishes[fish_name] = override(original_fish, locations=fish_location)


def randomize_fish_weather(content: StardewContent, data_to_randomize: set[str], behavior: DataRandomizationBehavior, random: Random):
    if DataRandomizationOptionName.fish_weather not in data_to_randomize:
        return

    locations_by_fish = {fish_name: fish_data.weather for fish_name, fish_data in content.fishes.items()
                         if len(fish_data.weather) >= 1 and fish_is_included(data_to_randomize, fish_data)}
    randomized_weather_per_fish = randomizers_per_behavior[behavior](locations_by_fish, random)

    for fish_name, fish_weather in randomized_weather_per_fish.items():
        original_fish = content.fishes[fish_name]
        content.fishes[fish_name] = override(original_fish, weather=fish_weather)

