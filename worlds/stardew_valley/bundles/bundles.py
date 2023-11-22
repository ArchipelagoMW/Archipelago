from random import Random
from typing import List, Dict, Union

from worlds.stardew_valley.logic.logic import StardewLogic
from worlds.stardew_valley.data.bundle_data import *
from worlds.stardew_valley.options import BundleRandomization, BundlePrice


def get_all_bundles(random: Random, logic: StardewLogic, randomization: BundleRandomization, price: BundlePrice) -> Dict[str, Bundle]:
    bundles = {}
    for bundle_key in vanilla_bundles:
        bundle_value = vanilla_bundles[bundle_key]
        bundle = Bundle(bundle_key, bundle_value)
        bundles[bundle.get_name_with_bundle()] = bundle

    if randomization == BundleRandomization.option_thematic:
        shuffle_bundles_thematically(random, bundles)
    elif randomization == BundleRandomization.option_shuffled:
        shuffle_bundles_completely(random, logic, bundles)

    price_difference = 0
    if price == BundlePrice.option_very_cheap:
        price_difference = -2
    elif price == BundlePrice.option_cheap:
        price_difference = -1
    elif price == BundlePrice.option_expensive:
        price_difference = 1

    for bundle_key in bundles:
        bundles[bundle_key].remove_rewards()
        bundles[bundle_key].change_number_required(price_difference)

    return bundles


def shuffle_bundles_completely(random: Random, logic: StardewLogic, bundles: Dict[str, Bundle]):
    total_required_item_number = sum(len(bundle.requirements) for bundle in bundles.values())
    quality_crops_items_set = set(quality_crops_items)
    all_bundle_items_without_quality_and_money = [item
                                                  for item in all_bundle_items_except_money
                                                  if item not in quality_crops_items_set] + \
                                                 random.sample(quality_crops_items, 10)
    choices = random.sample(all_bundle_items_without_quality_and_money, total_required_item_number - 4)

    items_sorted = sorted(choices, key=lambda x: logic.item_rules[x.item.name].get_difficulty())

    keys = sorted(bundles.keys())
    random.shuffle(keys)

    for key in keys:
        if not bundles[key].original_name.endswith("00g"):
            items_sorted = bundles[key].assign_requirements(items_sorted)


def shuffle_bundles_thematically(random: Random, bundles: Dict[str, Bundle]):
    shuffle_crafts_room_bundle_thematically(random, bundles)
    shuffle_pantry_bundle_thematically(random, bundles)
    shuffle_fish_tank_thematically(random, bundles)
    shuffle_boiler_room_thematically(random, bundles)
    shuffle_bulletin_board_thematically(random, bundles)
    shuffle_abandoned_jojamart_thematically(random, bundles)


def shuffle_crafts_room_bundle_thematically(random: Random, bundles: Dict[str, Bundle]):
    bundles["Spring Foraging Bundle"].randomize_requirements(random, spring_foraging_items)
    bundles["Summer Foraging Bundle"].randomize_requirements(random, summer_foraging_items)
    bundles["Fall Foraging Bundle"].randomize_requirements(random, fall_foraging_items)
    bundles["Winter Foraging Bundle"].randomize_requirements(random, winter_foraging_items)
    bundles["Exotic Foraging Bundle"].randomize_requirements(random, exotic_foraging_items)
    bundles["Construction Bundle"].randomize_requirements(random, construction_items)


def shuffle_pantry_bundle_thematically(random: Random, bundles: Dict[str, Bundle]):
    bundles["Spring Crops Bundle"].randomize_requirements(random, spring_crop_items)
    bundles["Summer Crops Bundle"].randomize_requirements(random, summer_crops_items)
    bundles["Fall Crops Bundle"].randomize_requirements(random, fall_crops_items)
    bundles["Quality Crops Bundle"].randomize_requirements(random, quality_crops_items)
    bundles["Animal Bundle"].randomize_requirements(random, animal_product_items)
    bundles["Artisan Bundle"].randomize_requirements(random, artisan_goods_items)


def shuffle_fish_tank_thematically(random: Random, bundles: Dict[str, Bundle]):
    bundles["River Fish Bundle"].randomize_requirements(random, river_fish_items)
    bundles["Lake Fish Bundle"].randomize_requirements(random, lake_fish_items)
    bundles["Ocean Fish Bundle"].randomize_requirements(random, ocean_fish_items)
    bundles["Night Fishing Bundle"].randomize_requirements(random, night_fish_items)
    bundles["Crab Pot Bundle"].randomize_requirements(random, crab_pot_items)
    bundles["Specialty Fish Bundle"].randomize_requirements(random, specialty_fish_items)


def shuffle_boiler_room_thematically(random: Random, bundles: Dict[str, Bundle]):
    bundles["Blacksmith's Bundle"].randomize_requirements(random, blacksmith_items)
    bundles["Geologist's Bundle"].randomize_requirements(random, geologist_items)
    bundles["Adventurer's Bundle"].randomize_requirements(random, adventurer_items)


def shuffle_bulletin_board_thematically(random: Random, bundles: Dict[str, Bundle]):
    bundles["Chef's Bundle"].randomize_requirements(random, chef_items)
    bundles["Dye Bundle"].randomize_requirements(random, dye_items)
    bundles["Field Research Bundle"].randomize_requirements(random, field_research_items)
    bundles["Fodder Bundle"].randomize_requirements(random, fodder_items)
    bundles["Enchanter's Bundle"].randomize_requirements(random, enchanter_items)


def shuffle_abandoned_jojamart_thematically(random: Random, bundles: Dict[str, Bundle]):
    bundles["The Missing Bundle"].randomize_requirements(random, missing_bundle_items)


def shuffle_vault_amongst_themselves(random: Random, bundles: Dict[str, Bundle]):
    bundles["2,500g Bundle"].randomize_requirements(random, vault_bundle_items)
    bundles["5,000g Bundle"].randomize_requirements(random, vault_bundle_items)
    bundles["10,000g Bundle"].randomize_requirements(random, vault_bundle_items)
    bundles["25,000g Bundle"].randomize_requirements(random, vault_bundle_items)
