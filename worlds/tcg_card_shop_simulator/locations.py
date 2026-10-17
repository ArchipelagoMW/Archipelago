from collections import defaultdict
from typing import TYPE_CHECKING

from BaseClasses import Location, Region
from .constants import ITEMS_LICENSE_OFFSET
from .data import GeneratedLocationData, RegionTypeEnum, ItemTypeEnum
from .data.helpers.card_types import Difficulty
from .data.locations import CardAchievementFamily, generate_level_locations, generate_card_sanity_locations, \
    generate_event_locations, EventFormat, generate_license_locations, ShopProduct
from .data.locations.achievements import generate_open_achievement_locations, generate_sell_achievement_locations, \
    generate_grade_achievement_locations
from .data.regions.entrances import Entrances, LevelEntrances, PackEntrances
from .data.regions.regions import DefaultRegions, Regions, get_level_region
from .data.items.shop_licenses import BoosterPackItems, AccessoriesItems, FigurineItems, TableTopItems

if TYPE_CHECKING:
    from . import TCGSimulatorWorld


def create_location(world, data: GeneratedLocationData):
    region = world.get_region(data.region.value)
    location = Location(world.player, data.name, data.location_id, region)
    location.progress_type = data.progress_type
    # location.item_rule = data.item_rule
    region.locations.append(location)
    world.set_rule(location, data.rule)

def create_region(world: "TCGSimulatorWorld", region_type: RegionTypeEnum, locations_by_region: dict[RegionTypeEnum, list[GeneratedLocationData]] | None = None):
    region = Region(region_type.value, world.player, world.multiworld)
    world.multiworld.regions.append(region)

    if locations_by_region is None:
        return region

    for data in locations_by_region[region_type]:
        location = Location(world.player, data.name, data.location_id, region)
        location.progress_type = data.progress_type
        # location.item_rule = data.item_rule
        region.locations.append(location)
        world.set_rule(location, data.rule)

    return region

def create_regions(world: "TCGSimulatorWorld"):
    menu = create_region(world, DefaultRegions.MENU)

    locations_by_region: dict[RegionTypeEnum, list[GeneratedLocationData]] = defaultdict(list)

    for family in CardAchievementFamily:
        for _location in  generate_open_achievement_locations(
                family,
                Difficulty(world.options.checks_opening_difficulty.option_impossible)
        ):
            locations_by_region[_location.region].append(_location)

        for _location in generate_sell_achievement_locations(
                family,
                Difficulty(world.options.checks_selling_difficulty.option_impossible)
        ):
            locations_by_region[_location.region].append(_location)

        for _location in generate_grade_achievement_locations(
                family,
                Difficulty(world.options.checks_grading_difficulty.option_impossible)
        ):
            locations_by_region[_location.region].append(_location)


    for _location in generate_level_locations(2, world.options.max_level.value):
        locations_by_region[_location.region].append(_location)

    if world.options.card_sanity.value != world.options.card_sanity.option_disabled:
        for _location in generate_card_sanity_locations(
                world.options.card_sanity.value == world.options.card_sanity.option_uniqueFoils,
                world.options.card_sanity_percentage.value/100,
            world
        ):
            locations_by_region[_location.region].append(_location)

    if world.options.no_formats.value:
        for _location in generate_event_locations([EventFormat.NO_FORMAT], world.options.play_table_checks.value):
            locations_by_region[_location.region].append(_location)
    else:
        for _location in generate_event_locations(list(EventFormat), world.options.play_table_checks.value):
            locations_by_region[_location.region].append(_location)

    booster_pack_items: list[ItemTypeEnum] = sorted(list(BoosterPackItems), key=lambda x: x.value)
    accessories_items: list[ItemTypeEnum] = sorted(list(AccessoriesItems), key=lambda x: x.value)
    figurine_items: list[ItemTypeEnum] = sorted(list(FigurineItems), key=lambda x: x.value)
    tabletop_items: list[ItemTypeEnum] = sorted(list(TableTopItems), key=lambda x: x.value)

    shops = [
        booster_pack_items,
        accessories_items,
        figurine_items,
        tabletop_items,
    ]

    license_items: list[ItemTypeEnum] = []
    starting_license_items: list[ItemTypeEnum] = []

    for shop in shops:
        world.random.shuffle(shop)

    for shop in shops:
        starting_license_items.append(shop.pop())

    remaining = world.total_licenses - len(starting_license_items)

    if AccessoriesItems.PROGRESSIVE_CLEANSER not in starting_license_items:
        accessories_items.remove(AccessoriesItems.PROGRESSIVE_CLEANSER)
        license_items.append(AccessoriesItems.PROGRESSIVE_CLEANSER)
        remaining -= 1

    while remaining > 0:
        for shop in shops:
            if remaining == 0:
                break

            if not shop:
                continue

            license_items.append(shop.pop())
            remaining -= 1

        if all(not shop for shop in shops):
            break

    if world.is_ut:
        license_items = world.license_items

    for item in license_items:
        for _location in generate_license_locations(ShopProduct(item.item_id-ITEMS_LICENSE_OFFSET), world.options.sell_check_amount.value):
            locations_by_region[_location.region].append(_location)

    for region in Regions:
        create_region(world, region, locations_by_region)

    return license_items, starting_license_items


def create_entrances(world: "TCGSimulatorWorld"):

    for entrance in Entrances:
        world.create_entrance(world.get_region(entrance.exiting_region.value), world.get_region(entrance.entering_region.value), rule=entrance.rule, name=entrance.value, force_creation=True)

    for entrance in LevelEntrances:
        world.create_entrance(world.get_region(entrance.exiting_region.value), world.get_region(entrance.entering_region.value), rule=entrance.rule, name=entrance.value, force_creation=True)

    for entrance in PackEntrances:
        world.create_entrance(world.get_region(entrance.exiting_region.value), world.get_region(entrance.entering_region.value), rule=entrance.rule, name=entrance.value, force_creation=True)