from random import Random

from .data_randomizer_behaviors import randomizers_per_behavior
from ..content import StardewContent
from ..data.fish_data import change_fish_difficulty, change_fish_season
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

    return content


def randomize_fish_difficulty(content: StardewContent, data_to_randomize: set[str], behavior: DataRandomizationBehavior, random: Random):
    if DataRandomizationOptionName.fish_difficulty not in data_to_randomize:
        return

    difficulties_by_fish = {fish_name: fish_data.difficulty for fish_name, fish_data in content.fishes.items() if fish_data.difficulty > 0}
    randomized_difficulties_per_fish = randomizers_per_behavior[behavior](difficulties_by_fish, random)

    for fish_name, fish_difficulty in randomized_difficulties_per_fish.items():
        original_fish = content.fishes[fish_name]
        content.fishes[fish_name] = change_fish_difficulty(original_fish, fish_difficulty)


def randomize_fish_season(content: StardewContent, data_to_randomize: set[str], behavior: DataRandomizationBehavior, random: Random):
    if DataRandomizationOptionName.fish_season not in data_to_randomize:
        return

    seasons_by_fish = {fish_name: fish_data.seasons for fish_name, fish_data in content.fishes.items() if fish_data.difficulty > 0}
    randomized_seasons_per_fish = randomizers_per_behavior[behavior](seasons_by_fish, random)

    for fish_name, fish_season in randomized_seasons_per_fish.items():
        original_fish = content.fishes[fish_name]
        content.fishes[fish_name] = change_fish_season(original_fish, fish_season)

