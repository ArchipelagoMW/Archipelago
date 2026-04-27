from random import Random
from typing import cast

from .data_randomizer_behaviors import randomizers_per_behavior
from ..content import StardewContent, content_packs
from ..content.override import override
from ..data import season_data
from ..data.fish_data import FishItem, crab_pot_difficulty
from ..data.harvest import HarvestCropSource
from ..data.mod_only_data.crops_prices import all_crop_sell_prices
from ..data.mod_only_data.fish_prices import all_fish_sell_prices
from ..data.mod_only_data.growth_times import all_growth_times
from ..data.shop import ShopSource
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

    randomize_fish_data(behavior, content, data_to_randomize, random)
    randomize_crops_data(behavior, content, data_to_randomize, random)
    randomize_festivals_data(behavior, content, data_to_randomize, random)
    randomize_shops_data(behavior, content, data_to_randomize, random)

    return content


def randomize_fish_data(behavior, content, data_to_randomize, random):
    randomize_fish_catch_method(content, data_to_randomize, behavior, random)
    randomize_fish_difficulty(content, data_to_randomize, behavior, random)
    randomize_fish_location(content, data_to_randomize, behavior, random)
    randomize_fish_season(content, data_to_randomize, behavior, random)
    randomize_fish_weather(content, data_to_randomize, behavior, random)
    randomize_fish_sell_prices(content, data_to_randomize, behavior, random)


def randomize_crops_data(behavior, content, data_to_randomize, random):
    randomize_crop_sell_prices(content, data_to_randomize, behavior, random)
    randomize_crop_growth_times(content, data_to_randomize, behavior, random)
    randomize_crop_growth_seasons(content, data_to_randomize, behavior, random)
    randomize_crop_which_seed(content, data_to_randomize, behavior, random)


def randomize_festivals_data(behavior, content, data_to_randomize, random):
    randomize_festival_seasons(content, data_to_randomize, behavior, random)
    randomize_festival_dates(content, data_to_randomize, behavior, random)
    sanitize_festival_dates(content, data_to_randomize, behavior, random)


def randomize_shops_data(behavior, content, data_to_randomize, random):
    randomize_shop_currencies(content, data_to_randomize, behavior, random)
    randomize_shop_prices(content, data_to_randomize, behavior, random)


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


def randomize_crop_growth_times(content: StardewContent, data_to_randomize: set[str], behavior: DataRandomizationBehavior, random: Random):
    if DataRandomizationOptionName.growth_time not in data_to_randomize:
        return

    harvest_sources_included = list(content.find_sources_of_type(HarvestCropSource))
    seeds_included = [source.seed for source in harvest_sources_included]
    growth_times_by_seed = {seed_name: growth_time for seed_name, growth_time in all_growth_times.items() if seed_name in seeds_included and growth_time > 0}
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


def randomize_crop_growth_seasons(content: StardewContent, data_to_randomize: set[str], behavior: DataRandomizationBehavior, random: Random):
    if DataRandomizationOptionName.growth_season not in data_to_randomize:
        return

    harvest_sources_included = list(content.find_sources_of_type(HarvestCropSource))

    seasons_by_seed = {harvest_source.seed: harvest_source.seasons for harvest_source in harvest_sources_included if len(harvest_source.seasons) >= 1}
    randomized_seasons_per_seed = randomizers_per_behavior[behavior](seasons_by_seed, random)

    for item_name, item in content.game_items.items():
        harvest_sources = [source for source in item.sources if isinstance(source, HarvestCropSource) and source.seed in randomized_seasons_per_seed]
        if len(harvest_sources) <= 0:
            continue
        modified_harvest_sources = [override(source, seasons=randomized_seasons_per_seed[source.seed]) for source in harvest_sources]
        new_sources = list(item.sources)
        new_sources = [source for source in new_sources if source not in harvest_sources]
        new_sources.extend(modified_harvest_sources)
        content.game_items[item_name] = override(item, sources=new_sources)


def randomize_crop_which_seed(content: StardewContent, data_to_randomize: set[str], behavior: DataRandomizationBehavior, random: Random):
    if DataRandomizationOptionName.crop_which_seed not in data_to_randomize:
        return

    harvest_sources_included = list(content.find_sources_of_type(HarvestCropSource))

    seed_by_crop = dict()
    for game_item in content.game_items.values():
        harvest_sources = [source for source in game_item.sources if source in harvest_sources_included]
        if any(harvest_sources):
            assert len(harvest_sources) == 1
            seed_by_crop[game_item.name] = harvest_sources[0].seed

    randomized_seeds_by_crops = randomizers_per_behavior[DataRandomizationBehavior.option_shuffled](seed_by_crop, random)

    for item_name, item in content.game_items.items():
        if item_name not in randomized_seeds_by_crops:
            continue
        harvest_sources = [source for source in item.sources if isinstance(source, HarvestCropSource)]
        if len(harvest_sources) <= 0:
            continue
        modified_harvest_sources = [override(source, seed=randomized_seeds_by_crops[item_name]) for source in harvest_sources]
        new_sources = list(item.sources)
        new_sources = [source for source in new_sources if source not in harvest_sources]
        new_sources.extend(modified_harvest_sources)
        content.game_items[item_name] = override(item, sources=new_sources)


def randomize_festival_seasons(content: StardewContent, data_to_randomize: set[str], behavior: DataRandomizationBehavior, random: Random):
    if DataRandomizationOptionName.festival_season not in data_to_randomize:
        return

    seasons_by_festival = {festival_name: festival_data.season for festival_name, festival_data in content.festivals.items() if festival_data.duration == 1}
    randomized_seasons_per_festival = randomizers_per_behavior[behavior](seasons_by_festival, random)

    for festival_name, festival_season in randomized_seasons_per_festival.items():
        original_festival = content.festivals[festival_name]
        content.festivals[festival_name] = override(original_festival, season=festival_season)


def randomize_festival_dates(content: StardewContent, data_to_randomize: set[str], behavior: DataRandomizationBehavior, random: Random):
    if DataRandomizationOptionName.festival_date not in data_to_randomize:
        return

    day_by_festival = {festival_name: festival_data.day for festival_name, festival_data in content.festivals.items() if festival_data.duration == 1}
    randomized_days_per_festival = randomizers_per_behavior[behavior](day_by_festival, random, 1, 28)

    for festival_name, festival_day in randomized_days_per_festival.items():
        original_festival = content.festivals[festival_name]
        content.festivals[festival_name] = override(original_festival, day=festival_day)


def sanitize_festival_dates(content: StardewContent, data_to_randomize: set[str], behavior: DataRandomizationBehavior, random: Random):
    festival_names = list([festival_name for festival_name, festival_data in content.festivals.items() if festival_data.duration == 1])
    all_valid = False
    while not all_valid:
        all_valid = True
        taken_days = set()
        random.shuffle(festival_names)
        festival_order = list([festival_name for festival_name, festival_data in content.festivals.items() if festival_data.duration != 1])
        festival_order.extend(festival_names)
        for festival_name in festival_order:
            festival_data = content.festivals[festival_name]
            for i in range(0, festival_data.duration):
                day = festival_data.day+i
                if day < 1 or day > 28:
                    all_valid = False
                    break
                day_key = f"{festival_data.season}{day}"
                if day_key in taken_days:
                    all_valid = False
                    break
                taken_days.add(day_key)
            if not all_valid:
                assert festival_data.duration == 1
                new_day = random.randint(1, 29)
                content.festivals[festival_name] = override(festival_data, day=new_day)
                break


def randomize_shop_currencies(content: StardewContent, data_to_randomize: set[str], behavior: DataRandomizationBehavior, random: Random):
    if DataRandomizationOptionName.shop_currencies not in data_to_randomize:
        return

    shop_sources_included = list([cast(ShopSource, shop_source) for shop_source in content.find_sources_of_type(ShopSource) if shop_source.price is not None and shop_source.price >= 1])
    shop_currencies_by_source = {shop_source: (shop_source.currency, shop_source.price) for shop_source in shop_sources_included}
    randomized_shop_currencies = randomizers_per_behavior[behavior](shop_currencies_by_source, random)

    for item_name, item_data in content.game_items.items():
        new_sources = get_new_currency_sources(item_data, randomized_shop_currencies)
        if new_sources is not None:
            content.game_items[item_name] = override(item_data, sources=new_sources)
    for building_name, building_data in content.farm_buildings.items():
        new_sources = get_new_currency_sources(building_data, randomized_shop_currencies)
        if new_sources is not None:
            content.farm_buildings[building_name] = override(building_data, sources=new_sources)
    for tool_upgrade_name, tool_upgrade_data in content.tool_upgrades.items():
        new_sources = get_new_currency_sources(tool_upgrade_data, randomized_shop_currencies)
        if new_sources is not None:
            content.tool_upgrades[tool_upgrade_name] = override(tool_upgrade_data, sources=new_sources)
    for animal_name, animal_data in content.animals.items():
        new_sources = get_new_currency_sources(animal_data, randomized_shop_currencies)
        if new_sources is not None:
            content.animals[animal_name] = override(animal_data, sources=new_sources)


def get_new_currency_sources(data, randomized_shop_currencies):
    shop_sources = [source for source in data.sources if isinstance(source, ShopSource) and source in randomized_shop_currencies]
    if len(shop_sources) <= 0:
        return None

    modified_shop_sources = [override(source, currency=randomized_shop_currencies[source][0], price=randomized_shop_currencies[source][1]) for source in shop_sources]
    new_sources = list(data.sources)
    new_sources = [source for source in new_sources if source not in shop_sources]
    new_sources.extend(modified_shop_sources)
    return new_sources


def randomize_shop_prices(content: StardewContent, data_to_randomize: set[str], behavior: DataRandomizationBehavior, random: Random):
    if DataRandomizationOptionName.shop_prices not in data_to_randomize:
        return

    shop_sources_included = list([cast(ShopSource, shop_source) for shop_source in content.find_sources_of_type(ShopSource) if shop_source.price is not None and shop_source.price >= 1])
    shop_sources_by_currency = dict()
    for shop_source in shop_sources_included:
        if shop_source.currency not in shop_sources_by_currency:
            shop_sources_by_currency[shop_source.currency]: list[ShopSource] = []
        shop_sources_by_currency[shop_source.currency].append(shop_source)

    for currency, shop_sources in shop_sources_by_currency.items():
        if DataRandomizationOptionName.shop_prices_across_vendors not in data_to_randomize:
            shop_sources_by_vendor = dict()
            for shop_source in shop_sources:
                if shop_source.shop_region not in shop_sources_by_vendor:
                    shop_sources_by_vendor[shop_source.shop_region] = []
                shop_sources_by_vendor[shop_source.shop_region].append(shop_source)
            for vendor, vendor_shop_sources in shop_sources_by_vendor.items():
                randomize_shop_prices_group(content, behavior, random, vendor_shop_sources)
        else:
            randomize_shop_prices_group(content, behavior, random, shop_sources)


def randomize_shop_prices_group(content: StardewContent, behavior: DataRandomizationBehavior, random: Random, shop_sources: list[ShopSource]):
    prices_by_shop_sources = {shop_source: shop_source.price for shop_source in shop_sources if shop_source.price is not None and shop_source.price >= 1}
    randomized_prices_per_shop_source = randomizers_per_behavior[behavior](prices_by_shop_sources, random)
    for item_name, item_data in content.game_items.items():
        new_sources = get_new_price_sources(item_data, randomized_prices_per_shop_source)
        if new_sources is not None:
            content.game_items[item_name] = override(item_data, sources=new_sources)
    for building_name, building_data in content.farm_buildings.items():
        new_sources = get_new_price_sources(building_data, randomized_prices_per_shop_source)
        if new_sources is not None:
            content.farm_buildings[building_name] = override(building_data, sources=new_sources)
    for tool_upgrade_name, tool_upgrade_data in content.tool_upgrades.items():
        new_sources = get_new_price_sources(tool_upgrade_data, randomized_prices_per_shop_source)
        if new_sources is not None:
            content.tool_upgrades[tool_upgrade_name] = override(tool_upgrade_data, sources=new_sources)
    for animal_name, animal_data in content.animals.items():
        new_sources = get_new_price_sources(animal_data, randomized_prices_per_shop_source)
        if new_sources is not None:
            content.animals[animal_name] = override(animal_data, sources=new_sources)


def get_new_price_sources(data, randomized_prices_per_shop_source):
    shop_sources = [source for source in data.sources if isinstance(source, ShopSource) and source in randomized_prices_per_shop_source]
    if len(shop_sources) <= 0:
        return None
    modified_shop_sources = [override(source, price=randomized_prices_per_shop_source[source]) for source in shop_sources]
    new_sources = list(data.sources)
    new_sources = [source for source in new_sources if source not in shop_sources]
    new_sources.extend(modified_shop_sources)
    return new_sources
