from random import Random

from .data_randomizer_behaviors import randomizers_per_behavior
from ..content import StardewContent, content_packs
from ..content.override import override
from ..data import season_data
from ..data.fish_data import FishItem, crab_pot_difficulty
from ..data.harvest import HarvestCropSource
from ..data.mod_only_data.crops_prices import all_crop_sell_prices
from ..data.mod_only_data.fish_prices import all_fish_sell_prices
from ..data.mod_only_data.growth_times import all_growth_times
from ..options import StardewValleyOptions
from ..options.options import DataRandomizationBehavior
from ..strings.ap_names.ap_option_names import DataRandomizationOptionName
from ..strings.region_names import LogicRegion, Region
from ..strings.season_names import Season
from ..strings.weather_names import Weather


def randomize_data(content: StardewContent, options: StardewValleyOptions, random: Random) -> StardewContent:
    behavior = options.data_randomization_behavior
    if behavior == DataRandomizationBehavior.option_off:
        return content

    data_to_randomize = options.data_randomization.value
    if len(data_to_randomize) <= 0:
        return content

    randomize_fish_catch_method(content, data_to_randomize, behavior, random)
    randomize_fish_difficulty(content, data_to_randomize, behavior, random)
    randomize_fish_location(content, data_to_randomize, behavior, random)
    randomize_fish_season(content, data_to_randomize, behavior, random)
    randomize_fish_weather(content, data_to_randomize, behavior, random)
    randomize_fish_sell_prices(content, data_to_randomize, behavior, random)
    randomize_crop_sell_prices(content, data_to_randomize, behavior, random)
    # randomize_seed_sell_prices(content, data_to_randomize, behavior, random)
    randomize_crop_growth_times(content, data_to_randomize, behavior, random)

    return content


def fish_is_included(data_to_randomize: set[str], fish_data: FishItem) -> bool:
    if DataRandomizationOptionName.fish_catch_method in data_to_randomize:
        return True
    return fish_data.difficulty != crab_pot_difficulty


def randomize_fish_catch_method(content: StardewContent, data_to_randomize: set[str], behavior: DataRandomizationBehavior, random: Random):
    if DataRandomizationOptionName.fish_catch_method not in data_to_randomize:
        return

    catch_method_by_fish = {fish_name: fish_data.difficulty == crab_pot_difficulty for fish_name, fish_data in content.fishes.items()}
    randomized_catch_method_per_fish = randomizers_per_behavior[behavior](catch_method_by_fish, random)

    for fish_name, is_crab_pot in randomized_catch_method_per_fish.items():
        original_fish = content.fishes[fish_name]
        original_difficulty = original_fish.difficulty
        if is_crab_pot:
            fish_difficulty = crab_pot_difficulty
            if original_difficulty != fish_difficulty:
                locations = random.choice([LogicRegion.crab_pot_freshwater, LogicRegion.crab_pot_seawater])
                # base game doesn't allow going wild with crab pot fish
                content.fishes[fish_name] = override(content.fishes[fish_name],
                                                     difficulty=fish_difficulty,
                                                     locations=(locations,),
                                                     seasons=season_data.all_seasons,
                                                     weather=(Weather.sun, Weather.rain,))
            continue
        elif original_difficulty == crab_pot_difficulty:
            fish_difficulty = random.randrange(10, 111)
            if original_fish.locations[0] == LogicRegion.crab_pot_seawater:
                fish_locations = (Region.beach,)
            else:
                fish_locations = (Region.town, LogicRegion.forest_river, LogicRegion.forest_pond, Region.mountain,)
            content.fishes[fish_name] = override(content.fishes[fish_name],
                                                 difficulty=fish_difficulty,
                                                 locations=fish_locations,)
            continue
        else:
            fish_difficulty = original_difficulty
        content.fishes[fish_name] = override(original_fish, difficulty=fish_difficulty)


def randomize_fish_difficulty(content: StardewContent, data_to_randomize: set[str], behavior: DataRandomizationBehavior, random: Random):
    if DataRandomizationOptionName.fish_difficulty not in data_to_randomize:
        return

    difficulties_by_fish = {fish_name: fish_data.difficulty for fish_name, fish_data in content.fishes.items() if fish_data.difficulty != crab_pot_difficulty}
    randomized_difficulties_per_fish = randomizers_per_behavior[behavior](difficulties_by_fish, random)

    for fish_name, fish_difficulty in randomized_difficulties_per_fish.items():
        original_fish = content.fishes[fish_name]
        content.fishes[fish_name] = override(original_fish, difficulty=fish_difficulty)


def randomize_fish_location(content: StardewContent, data_to_randomize: set[str], behavior: DataRandomizationBehavior, random: Random):
    if DataRandomizationOptionName.fish_location not in data_to_randomize:
        return

    locations_by_fish = {fish_name: fish_data.locations for fish_name, fish_data in content.fishes.items()
                         if len(fish_data.locations) >= 1 and fish_data.difficulty != crab_pot_difficulty}
    randomized_locations_per_fish = randomizers_per_behavior[behavior](locations_by_fish, random)

    for fish_name, fish_location in randomized_locations_per_fish.items():
        original_fish = content.fishes[fish_name]
        content.fishes[fish_name] = override(original_fish, locations=fish_location)

    locations_by_crab_pot_fish = {fish_name: fish_data.locations for fish_name, fish_data in content.fishes.items()
                                  if len(fish_data.locations) >= 1 and fish_data.difficulty == crab_pot_difficulty}
    randomized_locations_per_crab_pot_fish = randomizers_per_behavior[behavior](locations_by_crab_pot_fish, random)

    for fish_name, fish_location in randomized_locations_per_crab_pot_fish.items():
        original_fish = content.fishes[fish_name]
        content.fishes[fish_name] = override(original_fish, locations=fish_location)


def randomize_fish_season(content: StardewContent, data_to_randomize: set[str], behavior: DataRandomizationBehavior, random: Random):
    has_magic_bait = content_packs.ginger_island_content_pack.name in content.registered_packs and content_packs.qi_board_content_pack.name in content.registered_packs

    seasons_by_fish = {fish_name: fish_data.seasons for fish_name, fish_data in content.fishes.items()
                       if len(fish_data.seasons) >= 1 and fish_data.difficulty != crab_pot_difficulty}

    # The reason we do this, is so that the night market winter exception can occur even if seasons were not randomized.
    # This is because only randomizing the locations suffices to cause the problem
    if DataRandomizationOptionName.fish_season in data_to_randomize:
        randomized_seasons_per_fish = randomizers_per_behavior[behavior](seasons_by_fish, random)
    elif has_magic_bait:
        return
    else:
        randomized_seasons_per_fish = seasons_by_fish

    for fish_name, fish_season in randomized_seasons_per_fish.items():
        original_fish = content.fishes[fish_name]
        if not has_magic_bait and LogicRegion.night_market in original_fish.locations and Season.winter not in fish_season:
            fish_season += (Season.winter,)
        content.fishes[fish_name] = override(original_fish, seasons=fish_season)


def randomize_fish_weather(content: StardewContent, data_to_randomize: set[str], behavior: DataRandomizationBehavior, random: Random):
    if DataRandomizationOptionName.fish_weather not in data_to_randomize:
        return

    locations_by_fish = {fish_name: fish_data.weather for fish_name, fish_data in content.fishes.items()
                         if len(fish_data.weather) >= 1 and fish_data.difficulty != crab_pot_difficulty}
    randomized_weather_per_fish = randomizers_per_behavior[behavior](locations_by_fish, random)

    for fish_name, fish_weather in randomized_weather_per_fish.items():
        original_fish = content.fishes[fish_name]
        content.fishes[fish_name] = override(original_fish, weather=fish_weather)


def randomize_fish_sell_prices(content: StardewContent, data_to_randomize: set[str], behavior: DataRandomizationBehavior, random: Random):
    if DataRandomizationOptionName.fish_sell_price not in data_to_randomize:
        return

    fishes_included = content.fishes.keys()
    sell_prices_by_fish = {fish_name: fish_price for fish_name, fish_price in all_fish_sell_prices.items() if fish_name in fishes_included}
    randomized_sell_prices_per_fish = randomizers_per_behavior[behavior](sell_prices_by_fish, random)

    for fish_name, fish_price in randomized_sell_prices_per_fish.items():
        original_fish = content.fishes[fish_name]
        content.fishes[fish_name] = override(original_fish, sell_price=fish_price)


def randomize_crop_sell_prices(content: StardewContent, data_to_randomize: set[str], behavior: DataRandomizationBehavior, random: Random):
    if DataRandomizationOptionName.crop_sell_price not in data_to_randomize:
        return

    crops_included = content.game_items.keys()
    sell_prices_by_crop = {crop_name: crop_price for crop_name, crop_price in all_crop_sell_prices.items() if crop_name in crops_included}
    randomized_sell_prices_per_crop = randomizers_per_behavior[behavior](sell_prices_by_crop, random)

    for crop_name, crop_price in randomized_sell_prices_per_crop.items():
        original_crop = content.game_items[crop_name]
        content.game_items[crop_name] = override(original_crop, sell_price=crop_price)


# def randomize_seed_sell_prices(content: StardewContent, data_to_randomize: set[str], behavior: DataRandomizationBehavior, random: Random):
#     if DataRandomizationOptionName.seed_prices not in data_to_randomize:
#         return
#
#     seeds_included = content.game_items.keys()
#     sell_prices_by_seed = {seed_name: seed_price for seed_name, seed_price in all_seed_prices.items() if seed_name in seeds_included}
#     randomized_sell_prices_per_seed = randomizers_per_behavior[behavior](sell_prices_by_seed, random)
#
#     for seed_name, seed_price in randomized_sell_prices_per_seed.items():
#         original_seed = content.game_items[seed_name]
#         content.game_items[seed_name] = override(original_seed, sell_price=seed_price)


def randomize_crop_growth_times(content: StardewContent, data_to_randomize: set[str], behavior: DataRandomizationBehavior, random: Random):
    if DataRandomizationOptionName.seed_growth_time not in data_to_randomize:
        return

    harvest_sources_included = content.find_sources_of_type(HarvestCropSource)
    seeds_included = [source.seed for source in harvest_sources_included]
    growth_times_by_seed = {seed_name: growth_time for seed_name, growth_time in all_growth_times.items() if seed_name in seeds_included}
    randomized_growth_times_per_seed = randomizers_per_behavior[behavior](growth_times_by_seed, random)

    for item_name, item in content.game_items.items():
        harvest_sources = [source for source in item.sources if isinstance(source, HarvestCropSource) and source.seed in randomized_growth_times_per_seed]
        if len(harvest_sources) <= 0:
            continue
        modified_harvest_sources = [override(source, growth_time=randomized_growth_times_per_seed[source.seed]) for source in harvest_sources]
        new_sources = list(item.sources)
        new_sources = [source for source in new_sources if source not in harvest_sources]
        new_sources.extend(modified_harvest_sources)
        content.game_items[item_name] = override(item, sources=new_sources)
