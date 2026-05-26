from typing import TextIO

from ..content import StardewContent
from ..data.fish_data import crab_pot_difficulty
from ..data.game_item import ItemTag
from ..data.harvest import HarvestCropSource
from ..data.shop import ShopSource
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
    for category_name in sorted(prepared_data.keys()):
        spoiler_handle.write(f"\t{category_name}:\n")
        category_value = prepared_data[category_name]
        for item_name in sorted(category_value.keys()):
            spoiler_handle.write(f"\t\t{item_name}:\n")
            item_value = category_value[item_name]
            for value_name in sorted(item_value.keys()):
                value = item_value[value_name]
                if isinstance(value, dict):
                    spoiler_handle.write(f"\t\t\t{value_name}:\n")
                    for sub_value_name in sorted(value.keys()):
                        sub_value = value[sub_value_name]
                        spoiler_handle.write(f"\t\t\t\t{sub_value_name}: {sub_value}\n")
                else:
                    spoiler_handle.write(f"\t\t\t{value_name}: {value}\n")


def prepare_randomized_data(content: StardewContent, options: StardewValleyOptions):
    data_to_randomize = options.data_randomization.value

    prepared_data = dict()
    prepare_fish_data(content, data_to_randomize, prepared_data)
    prepare_crop_data(content, data_to_randomize, prepared_data)
    prepare_festival_data(content, data_to_randomize, prepared_data)
    prepare_shops_data(content, data_to_randomize, prepared_data)

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
    prepare_crop_growth_time_data(content, data_to_randomize, prepared_data)
    prepare_crop_growth_season_data(content, data_to_randomize, prepared_data)
    prepare_crop_which_seed_data(content, data_to_randomize, prepared_data)


def prepare_festival_data(content: StardewContent, data_to_randomize: set[str], prepared_data):
    prepared_data["Festivals"] = dict()
    prepare_festival_season_data(content, data_to_randomize, prepared_data)
    prepare_festival_days_data(content, data_to_randomize, prepared_data)


def prepare_shops_data(content: StardewContent, data_to_randomize: set[str], prepared_data):
    prepared_data["Shops"] = dict()
    prepare_shops_currencies_data(content, data_to_randomize, prepared_data)
    prepare_shops_prices_data(content, data_to_randomize, prepared_data)
    prepare_shops_materials_data(content, data_to_randomize, prepared_data)


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


def prepare_crop_growth_time_data(content: StardewContent, data_to_randomize: set[str], prepared_data: dict):
    prepare_crop_data_aspect(content, data_to_randomize, prepared_data,
                             DataRandomizationOptionName.growth_time,
                             lambda crop: any(isinstance(source, HarvestCropSource) and source.growth_time >= 1 for source in crop.sources),
                             lambda crop: [source.growth_time for source in crop.sources if isinstance(source, HarvestCropSource)],
                             "GrowthTime")


def prepare_crop_growth_season_data(content: StardewContent, data_to_randomize: set[str], prepared_data: dict):
    prepare_crop_data_aspect(content, data_to_randomize, prepared_data,
                             DataRandomizationOptionName.growth_season,
                             lambda crop: any(isinstance(source, HarvestCropSource) and len(source.seasons) >= 1 for source in crop.sources),
                             lambda crop: [source.seasons for source in crop.sources if isinstance(source, HarvestCropSource)],
                             "Season")


def prepare_crop_which_seed_data(content: StardewContent, data_to_randomize: set[str], prepared_data: dict):
    prepare_crop_data_aspect(content, data_to_randomize, prepared_data,
                             DataRandomizationOptionName.crop_which_seed,
                             lambda crop: any(isinstance(source, HarvestCropSource) and source.seed in content.game_items for source in crop.sources),
                             lambda crop: [source.seed for source in crop.sources if isinstance(source, HarvestCropSource)],
                             "Seed")


def prepare_crop_data_aspect(content: StardewContent, data_to_randomize: set[str], prepared_data: dict,
                             randomize_toggle: str, crop_validator, crop_data_extractor, aspect_key: str):
    if randomize_toggle not in data_to_randomize:
        return
    crop_item_tags = [ItemTag.FRUIT, ItemTag.VEGETABLE, ItemTag.CROPSANITY, ItemTag.FORAGE, ItemTag.EDIBLE_MUSHROOM]
    for crop_name, crop_data in content.game_items.items():
        tags_valid = any(tag in crop_data.tags for tag in crop_item_tags)
        if not tags_valid:
            continue
        if not crop_validator(crop_data):
            continue
        if crop_name not in prepared_data["Crops"]:
            prepared_data["Crops"][crop_name] = dict()
        extracted_data = crop_data_extractor(crop_data)
        if isinstance(extracted_data, list) and len(extracted_data) == 1:
            extracted_data = extracted_data[0]
        prepared_data["Crops"][crop_name][aspect_key] = extracted_data


def prepare_festival_season_data(content: StardewContent, data_to_randomize: set[str], prepared_data: dict):
    prepare_festival_data_aspect(content, data_to_randomize, prepared_data,
                                 DataRandomizationOptionName.festival_season,
                                 lambda festival: festival.duration == 1,
                                 lambda festival: festival.season,
                                 "Season")


def prepare_festival_days_data(content: StardewContent, data_to_randomize: set[str], prepared_data: dict):
    prepare_festival_data_aspect(content, data_to_randomize, prepared_data,
                                 DataRandomizationOptionName.festival_season,
                                 lambda festival: festival.duration == 1,
                                 lambda festival: ",".join([str(x) for x in range(festival.day, festival.day+festival.duration)]),
                                 "Day")


def prepare_festival_data_aspect(content: StardewContent, data_to_randomize: set[str], prepared_data: dict,
                                 randomize_toggle: str, festival_validator, festival_data_extractor, aspect_key: str):
    if randomize_toggle not in data_to_randomize:
        return
    for festival_name, festival_data in content.festivals.items():
        if not festival_validator(festival_data):
            continue
        if festival_name not in prepared_data["Festivals"]:
            prepared_data["Festivals"][festival_name] = dict()
        prepared_data["Festivals"][festival_name][aspect_key] = festival_data_extractor(festival_data)


def prepare_shops_currencies_data(content: StardewContent, data_to_randomize: set[str], prepared_data: dict):
    prepare_shop_data_aspect(content, data_to_randomize, prepared_data,
                             DataRandomizationOptionName.shop_currencies,
                             lambda shop_source: shop_source.currency is not None and shop_source.price is not None and shop_source.price >= 1,
                             lambda shop_source: shop_source.currency,
                             "Currency")
    prepare_shop_data_aspect(content, data_to_randomize, prepared_data,
                             DataRandomizationOptionName.shop_currencies,
                             lambda shop_source: shop_source.currency is not None and shop_source.price is not None,
                             lambda shop_source: shop_source.price,
                             "Price")


def prepare_shops_prices_data(content: StardewContent, data_to_randomize: set[str], prepared_data: dict):
    prepare_shop_data_aspect(content, data_to_randomize, prepared_data,
                             DataRandomizationOptionName.shop_prices,
                             lambda shop_source: shop_source.price is not None,
                             lambda shop_source: shop_source.price,
                             "Price")


def prepare_shops_materials_data(content: StardewContent, data_to_randomize: set[str], prepared_data: dict):
    prepare_shop_data_aspect(content, data_to_randomize, prepared_data,
                             DataRandomizationOptionName.shop_extra_materials,
                             lambda shop_source: shop_source.items_price is not None,
                             lambda shop_source: {item_price[1]: item_price[0] for item_price in shop_source.items_price},
                             "Materials")


def prepare_shop_data_aspect(content: StardewContent, data_to_randomize: set[str], prepared_data: dict,
                             randomize_toggle: str, shop_source_validator, shop_source_data_extractor, aspect_key: str):
    if randomize_toggle not in data_to_randomize:
        return
    for item_name, item_data in content.game_items.items():
        prepare_shop_item_aspect(prepared_data, shop_source_validator, shop_source_data_extractor, aspect_key, item_name, item_data)
    for building_name, building_data in content.farm_buildings.items():
        prepare_shop_item_aspect(prepared_data, shop_source_validator, shop_source_data_extractor, aspect_key, building_name, building_data)
    for tool_upgrade_name, tool_upgrade_data in content.tool_upgrades.items():
        prepare_shop_item_aspect(prepared_data, shop_source_validator, shop_source_data_extractor, aspect_key, tool_upgrade_name, tool_upgrade_data)
    for animal_name, animal_data in content.animals.items():
        prepare_shop_item_aspect(prepared_data, shop_source_validator, shop_source_data_extractor, aspect_key, animal_name, animal_data)
    for cooking_recipe_name, cooking_recipe_data in content.cooking_recipes.items():
        prepare_shop_item_aspect(prepared_data, shop_source_validator, shop_source_data_extractor, aspect_key, cooking_recipe_name, cooking_recipe_data)
    for crafting_recipe_name, crafting_recipe_data in content.crafting_recipes.items():
        prepare_shop_item_aspect(prepared_data, shop_source_validator, shop_source_data_extractor, aspect_key, crafting_recipe_name, crafting_recipe_data)


def prepare_shop_item_aspect(prepared_data, shop_source_validator, shop_source_data_extractor, aspect_key, item_name: str, item_data):
    shop_sources = [source for source in item_data.sources if isinstance(source, ShopSource)]
    if len(shop_sources) <= 0:
        return
    for source in shop_sources:
        if not shop_source_validator(source):
            continue
        if source.shop_region not in prepared_data["Shops"]:
            prepared_data["Shops"][source.shop_region] = dict()
        if item_name not in prepared_data["Shops"][source.shop_region]:
            prepared_data["Shops"][source.shop_region][item_name] = dict()
        extracted_data = shop_source_data_extractor(source)
        if isinstance(extracted_data, list) and len(extracted_data) == 1:
            extracted_data = extracted_data[0]
        prepared_data["Shops"][source.shop_region][item_name][aspect_key] = extracted_data
