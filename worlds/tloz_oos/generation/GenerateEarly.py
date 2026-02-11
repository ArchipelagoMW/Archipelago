from Options import OptionError
from ..Options import OracleOfSeasonsOldMenShuffle
from ..Util import get_old_man_values_pool
from ..World import OracleOfSeasonsWorld
from ..data import LOCATIONS_DATA, ITEMS_DATA
from ..data.Constants import DIRECTIONS, SEASONS, DIRECTION_LEFT, DIRECTION_UP, SEASON_NAMES, VALID_RUPEE_PRICE_VALUES, AVERAGE_PRICE_PER_LOCATION


def generate_early(world: OracleOfSeasonsWorld) -> None:
    if world.options.randomize_ai:
        world.options.golden_beasts_requirement.value = 0

    conflicting_rings = world.options.required_rings.value & world.options.excluded_rings.value
    if len(conflicting_rings) > 0:
        raise OptionError("Required Rings and Excluded Rings contain the same element(s)", conflicting_rings)

    world.remaining_progressive_gasha_seeds = world.options.deterministic_gasha_locations.value

    pick_essences_in_game(world)
    if len(world.essences_in_game) < world.options.treehouse_old_man_requirement:
        world.options.treehouse_old_man_requirement.value = len(world.essences_in_game)

    restrict_non_local_items(world)
    randomize_default_seasons(world)
    randomize_old_men(world)

    if world.options.randomize_lost_woods_item_sequence:
        # Pick 4 random seasons & directions (last one has to be "left")
        world.lost_woods_item_sequence = []
        for i in range(4):
            world.lost_woods_item_sequence.append([
                world.random.choice(DIRECTIONS) if i < 3 else DIRECTION_LEFT,
                world.random.choice(SEASONS)
            ])

    if world.options.randomize_lost_woods_main_sequence:
        # Pick 4 random seasons & directions (last one has to be "up")
        world.lost_woods_main_sequence = []
        for i in range(4):
            world.lost_woods_main_sequence.append([
                world.random.choice(DIRECTIONS) if i < 3 else DIRECTION_UP,
                world.random.choice(SEASONS)
            ])

    if world.options.randomize_samasa_gate_code:
        world.samasa_gate_code = []
        for i in range(world.options.samasa_gate_code_length.value):
            world.samasa_gate_code.append(world.random.randint(0, 3))

    randomize_shop_order(world)
    randomize_shop_prices(world)
    compute_rupee_requirements(world)

    create_random_rings_pool(world)

    if world.options.linked_heros_cave.value:
        world.dungeon_entrances["d11 entrance"] = "enter d11"


def pick_essences_in_game(world: OracleOfSeasonsWorld) -> None:
    # If the value for "Placed Essences" is lower than "Required Essences" (which can happen when using random
    # values for both), a new random value is automatically picked in the valid range.
    if world.options.required_essences > world.options.placed_essences:
        world.options.placed_essences.value = world.random.randint(world.options.required_essences.value, 8)

    # If some essence pedestal locations were excluded and essences are not shuffled,
    # remove those essences in priority
    if not world.options.shuffle_essences:
        excluded_locations_data = {name: data for name, data in LOCATIONS_DATA.items() if name in world.options.exclude_locations.value}
        for loc_name, loc_data in excluded_locations_data.items():
            if "essence" in loc_data and loc_data["essence"] is True:
                world.essences_in_game.remove(loc_data["vanilla_item"])
        if len(world.essences_in_game) < world.options.required_essences:
            raise ValueError("Too many essence pedestal locations were excluded, seed will be unbeatable")

    # If we need to remove more essences, pick them randomly
    world.random.shuffle(world.essences_in_game)
    world.essences_in_game = world.essences_in_game[0:world.options.placed_essences]


def restrict_non_local_items(world: OracleOfSeasonsWorld) -> None:
    # Restrict non_local_items option in cases where it's incompatible with other options that enforce items
    # to be placed locally (e.g. dungeon items with keysanity off)
    if not world.options.keysanity_small_keys:
        world.options.non_local_items.value -= world.item_name_groups["Small Keys"]
        world.options.non_local_items.value -= world.item_name_groups["Master Keys"]
    if not world.options.keysanity_boss_keys:
        world.options.non_local_items.value -= world.item_name_groups["Boss Keys"]
    if not world.options.keysanity_maps_compasses:
        world.options.non_local_items.value -= world.item_name_groups["Dungeon Maps"]
        world.options.non_local_items.value -= world.item_name_groups["Compasses"]


def randomize_default_seasons(world: OracleOfSeasonsWorld) -> None:
    if world.options.default_seasons == "randomized":
        seasons_pool = SEASONS
    elif world.options.default_seasons.current_key.endswith("singularity"):
        single_season = world.options.default_seasons.current_key.replace("_singularity", "")
        if single_season == "random":
            single_season = world.random.choice(SEASONS)
        else:
            single_season = next(byte for byte, name in SEASON_NAMES.items() if name == single_season)
        seasons_pool = [single_season]
    else:
        return

    for region in world.default_seasons:
        if region == "HORON_VILLAGE" and not world.options.normalize_horon_village_season:
            continue
        world.default_seasons[region] = world.random.choice(seasons_pool)


def randomize_old_men(world: OracleOfSeasonsWorld) -> None:
    if world.options.shuffle_old_men == OracleOfSeasonsOldMenShuffle.option_shuffled_values:
        shuffled_rupees = list(world.old_man_rupee_values.values())
        world.random.shuffle(shuffled_rupees)
        world.old_man_rupee_values = dict(zip(world.old_man_rupee_values, shuffled_rupees))
    elif world.options.shuffle_old_men == OracleOfSeasonsOldMenShuffle.option_random_values:
        for key in world.old_man_rupee_values.keys():
            sign = world.random.choice([-1, 1])
            world.old_man_rupee_values[key] = world.random.choice(get_old_man_values_pool()) * sign
    elif world.options.shuffle_old_men == OracleOfSeasonsOldMenShuffle.option_random_positive_values:
        for key in world.old_man_rupee_values.keys():
            world.old_man_rupee_values[key] = world.random.choice(get_old_man_values_pool())
    else:
        # Remove the old man values from the pool so that they don't count negative when they are shuffled as items
        world.old_man_rupee_values = {}


def randomize_shop_order(world: OracleOfSeasonsWorld) -> None:
    world.shop_order = [
        ["horonShop1", "horonShop2", "horonShop3"],
        ["memberShop1", "memberShop2", "memberShop3"],
        ["syrupShop1", "syrupShop2", "syrupShop3"]
    ]
    if world.options.advance_shop:
        world.shop_order.append(["advanceShop1", "advanceShop2", "advanceShop3"])
    if world.options.shuffle_business_scrubs:
        world.shop_order.extend([["spoolSwampScrub"], ["samasaCaveScrub"], ["d2Scrub"], ["d4Scrub"]])
    world.random.shuffle(world.shop_order)


def randomize_shop_prices(world: OracleOfSeasonsWorld) -> None:
    if world.options.shop_prices == "vanilla":
        if world.options.enforce_potion_in_shop:
            world.shop_prices["horonShop3"] = 300
        return
    if world.options.shop_prices == "free":
        world.shop_prices = {k: 0 for k in world.shop_prices}
        return

    # Prices are randomized, get a random price that follow set options for each shop location.
    # Values must be rounded to nearest valid rupee amount.
    average = AVERAGE_PRICE_PER_LOCATION[world.options.shop_prices.current_key]
    deviation = min(19 * (average / 50), 100)
    for i, shop in enumerate(world.shop_order):
        shop_price_factor = (i / len(world.shop_order)) + 0.5
        for location_code in shop:
            value = world.random.gauss(average, deviation) * shop_price_factor
            world.shop_prices[location_code] = min(VALID_RUPEE_PRICE_VALUES, key=lambda x: abs(x - value))
    # Subrosia market special cases
    for i in range(2, 6):
        value = world.random.gauss(average, deviation) * 0.5
        world.shop_prices[f"subrosianMarket{i}"] = min(VALID_RUPEE_PRICE_VALUES, key=lambda x: abs(x - value))


def compute_rupee_requirements(world: OracleOfSeasonsWorld) -> None:
    # Compute global rupee requirements for each shop, based on shop order and item prices
    cumulated_requirement = 0
    for shop in world.shop_order:
        if shop[0].startswith("advance") and not world.options.advance_shop:
            continue
        if shop[0].endswith("Scrub") and not world.options.shuffle_business_scrubs:
            continue
        # Add the price of each shop location in there to the requirement
        for shop_location in shop:
            cumulated_requirement += world.shop_prices[shop_location]
        # Deduce the shop name from the code of the first location
        shop_name = shop[0]
        if not shop_name.endswith("Scrub"):
            shop_name = shop_name[:-1]
        world.shop_rupee_requirements[shop_name] = cumulated_requirement


def create_random_rings_pool(world: OracleOfSeasonsWorld) -> None:
    # Get a subset of as many rings as needed, with a potential filter depending on chosen options
    ring_names = [name for name, idata in ITEMS_DATA.items() if "ring" in idata]

    # Remove required rings because they'll be added later anyway
    ring_names = [name for name in ring_names if name not in world.options.required_rings.value and name not in world.options.excluded_rings.value]

    world.random.shuffle(ring_names)
    world.random_rings_pool = ring_names
