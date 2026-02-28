"""Shop price generation functionality for Archipelago DK64."""

from random import Random

from randomizer import Spoiler
from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Types import Types
from randomizer.Enums.VendorType import VendorType
from randomizer.Lists.Item import ItemList as DK64RItemList
from randomizer.Lists.Location import SharedShopLocations
from archipelago.Options import DK64Options, ShopPrices

# Progressive moves configuration (item: count)
PROGRESSIVE_MOVES = {
    "ProgressiveSlam": 3,
    "ProgressiveAmmoBelt": 2,
    "ProgressiveInstrumentUpgrade": 3,
}


def _get_price_weights(shop_prices_value: int) -> tuple[float, int, int]:
    """Get the parameters for the price distribution."""
    if shop_prices_value == ShopPrices.option_high:
        return (6.5, 3, 12)
    elif shop_prices_value == ShopPrices.option_medium:
        return (4.5, 2, 9)
    elif shop_prices_value == ShopPrices.option_low:
        return (2.5, 1, 6)
    elif shop_prices_value == ShopPrices.option_free:
        return (0, 0, 0)


def _generate_random_price(random: Random, avg: float, stddev: float, upper_limit: int) -> int:
    """Generate a random price using normal distribution."""
    if avg == 0:  # Free prices
        return 0

    price = round(random.normalvariate(avg, stddev))
    return max(1, min(price, upper_limit))


def _get_shared_shop_vendors(spoiler: Spoiler, options: DK64Options, random: Random) -> tuple[set[tuple[Levels, VendorType]], set[Locations]]:
    """Identify vendor/level combinations that have shared shops."""
    shared_shop_vendors: set[tuple[Levels, VendorType]] = set()

    if not options.enable_shared_shops.value:
        if not hasattr(spoiler.settings, "selected_shared_shops"):
            spoiler.settings.selected_shared_shops = set()
        return shared_shop_vendors, set()

    # Get or create the set of available shared shops
    if hasattr(spoiler.settings, "selected_shared_shops") and spoiler.settings.selected_shared_shops:
        available_shared_shops: set[Locations] = spoiler.settings.selected_shared_shops
    else:
        all_shared_shops = list(SharedShopLocations)
        random.shuffle(all_shared_shops)
        available_shared_shops = set(all_shared_shops[:10])
        spoiler.settings.selected_shared_shops = available_shared_shops

    # Build set of vendor/level combinations
    for location_id, location in spoiler.LocationList.items():
        if location.type == Types.Shop and location.kong == Kongs.any:
            if location_id in available_shared_shops:
                shared_shop_vendors.add((location.level, location.vendor))

    return shared_shop_vendors, available_shared_shops


def _categorize_shop_locations(
    spoiler: Spoiler, options: DK64Options, shared_shop_vendors: set[tuple[Levels, VendorType]], available_shared_shops: set[Locations]
) -> tuple[list[Locations], list[Locations], dict[Kongs, int]]:
    """Categorize shops into included and excluded based on settings."""
    shop_locations: list[Locations] = []
    excluded_shop_locations: list[Locations] = []
    shops_per_kong: dict[Kongs, int] = {kong: 0 for kong in Kongs}

    for location_id, location in spoiler.LocationList.items():
        if location.type != Types.Shop:
            continue

        # Check if shop is excluded by smaller_shops setting
        if hasattr(location, "smallerShopsInaccessible") and location.smallerShopsInaccessible and options.smaller_shops.value:
            excluded_shop_locations.append(location_id)
            continue

        # Check if shared shop is excluded
        if location.kong == Kongs.any:
            if not options.enable_shared_shops.value or location_id not in available_shared_shops:
                excluded_shop_locations.append(location_id)
                continue

        # Check if kong shop is blocked by a shared shop at same vendor/level
        if location.kong != Kongs.any and options.enable_shared_shops.value:
            if (location.level, location.vendor) in shared_shop_vendors:
                excluded_shop_locations.append(location_id)
                continue

        # Shop is included
        shop_locations.append(location_id)
        if location.kong != Kongs.any:
            shops_per_kong[location.kong] += 1

    return shop_locations, excluded_shop_locations, shops_per_kong


def _generate_individual_prices(random: Random, shop_locations: list[Locations], avg: float, stddev: int, upper_limit: int) -> dict[Items | Locations, int | list[int]]:
    """Generate random individual prices for shops and progressive items."""
    individual_prices: dict[Items | Locations, int | list[int]] = {}

    # Generate shop prices - simple random price per shop
    for location_id in shop_locations:
        individual_prices[location_id] = _generate_random_price(random, avg, stddev, upper_limit)

    # Progressive items get their own price list
    for item_name, count in PROGRESSIVE_MOVES.items():
        item_enum = getattr(Items, item_name)
        individual_prices[item_enum] = []
        for _ in range(count):
            individual_prices[item_enum].append(_generate_random_price(random, avg, stddev, upper_limit))

    return individual_prices


def _convert_to_cumulative_prices(
    spoiler: Spoiler, random: Random, individual_prices: dict[Items | Locations, int | list[int]], shop_locations: list[Locations]
) -> dict[Items | Locations, int | list[int]]:
    """Convert individual prices to cumulative running totals per kong."""
    price_assignment = []

    # Build list of price assignments
    for key, value in individual_prices.items():
        if isinstance(value, list):
            # Progressive move - add multiple entries
            for price in value:
                price_assignment.append({"is_prog": True, "cost": price, "item": key, "kong": Kongs.any})
        elif key in shop_locations:
            # Shop location
            location = spoiler.LocationList[key]
            price_assignment.append({"is_prog": False, "cost": value, "item": key, "kong": location.kong})

    # Shuffle and calculate cumulative prices
    random.shuffle(price_assignment)
    total_cost = [0] * 5
    cumulative_prices = {}

    for assignment in price_assignment:
        kong = assignment["kong"]
        written_price = assignment["cost"]

        if kong == Kongs.any:
            # Progressive item - add to all kongs, price is average of current totals
            current_kong_total = 0
            for kong_index in range(5):
                current_kong_total += total_cost[kong_index]
                total_cost[kong_index] += written_price
            written_price = int(current_kong_total / 5)
        else:
            # Kong-specific shop - add to that kong's total
            total_cost[kong] += written_price
            written_price = total_cost[kong]

        # Store cumulative price
        key = assignment["item"]
        if assignment["is_prog"]:
            if key not in cumulative_prices:
                cumulative_prices[key] = []
            cumulative_prices[key].append(written_price)
        else:
            cumulative_prices[key] = written_price

    return cumulative_prices


def generate_prices(spoiler: Spoiler, options: DK64Options, random: Random) -> None:
    """Generate custom shop prices for Archipelago."""
    # Get price distribution parameters (matches standalone)
    shopprices = options.shop_prices.value
    avg, stddev, upper_limit = _get_price_weights(shopprices)

    # Categorize shops
    shared_shop_vendors, available_shared_shops = _get_shared_shop_vendors(spoiler, options, random)
    shop_locations, excluded_shop_locations, shops_per_kong = _categorize_shop_locations(spoiler, options, shared_shop_vendors, available_shared_shops)

    # Generate individual prices using standalone algorithm
    individual_prices = _generate_individual_prices(random, shop_locations, avg, stddev, upper_limit)

    # Add 0 prices for non-shop items and excluded shops
    for item_id in DK64RItemList.keys():
        if item_id not in individual_prices:
            individual_prices[item_id] = 0

    for location_id in excluded_shop_locations:
        individual_prices[location_id] = 0

    # Store original prices
    spoiler.settings.original_prices = individual_prices.copy()

    if shopprices > 0:
        # Convert to cumulative prices
        cumulative_prices = _convert_to_cumulative_prices(spoiler, random, individual_prices, shop_locations)

        # Add 0 prices for items not in shops
        for item_id in DK64RItemList.keys():
            if item_id not in cumulative_prices:
                cumulative_prices[item_id] = 0

        # Add 0 prices for all location IDs not already priced
        for location_id in spoiler.LocationList.keys():
            if location_id not in cumulative_prices:
                cumulative_prices[location_id] = 0

        for location_id in excluded_shop_locations:
            cumulative_prices[location_id] = 0

        spoiler.settings.prices = cumulative_prices
    else:
        # Free prices - ensure all locations exist with 0 cost
        for location_id in spoiler.LocationList.keys():
            if location_id not in individual_prices:
                individual_prices[location_id] = 0
        spoiler.settings.prices = individual_prices.copy()
