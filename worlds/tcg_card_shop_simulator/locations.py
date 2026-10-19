from collections import defaultdict
from typing import TYPE_CHECKING

from BaseClasses import Location, Region, LocationProgressType
from Options import OptionError
from .constants import ITEMS_LICENSE_OFFSET
from .data import GeneratedLocationData, RegionTypeEnum, ItemTypeEnum
from .data.helpers.card_types import Difficulty
from .data.locations import CardAchievementFamily, generate_level_locations, generate_card_sanity_locations, \
    generate_event_locations, EventFormat, generate_license_locations, ShopProduct
from .data.locations.achievements import generate_open_achievement_locations, generate_sell_achievement_locations, \
    generate_grade_achievement_locations
from .data.regions.entrances import Entrances, LevelEntrances, PackEntrances, pack_regions
from .data.regions.regions import DefaultRegions, get_level_region, LevelRegions, GenericRegions
from .data.items.shop_licenses import BoosterPackItems, AccessoriesItems, FigurineItems, TableTopItems, \
    TETRAMON_BASE_PACK_ITEMS, TETRAMON_DESTINY_PACK_ITEMS

if TYPE_CHECKING:
    from . import TCGSimulatorWorld


# def create_location(world, data: GeneratedLocationData):
#     region = world.get_region(data.region.value)
#     location = Location(world.player, data.name, data.location_id, region)
#     location.progress_type = data.progress_type
#     # location.item_rule = data.item_rule
#     region.locations.append(location)
#     world.set_rule(location, data.rule)
#
#     #check if location should be filled with junk from any TCG in multiworld
#     if data.location_id & (1 << 51):
#         if data.progress_type == LocationProgressType.EXCLUDED:
#             world.sanity_fill_locations.append(location)
#         else:
#             world.backup_sanity_fill_locations.append(location)

def create_region(world: "TCGSimulatorWorld", region_type: RegionTypeEnum, locations_by_region: dict[RegionTypeEnum, list[GeneratedLocationData]] | None = None):
    region = Region(region_type.value, world.player, world.multiworld)
    world.multiworld.regions.append(region)
    world.created_region_types.add(region_type)
    if locations_by_region is None:
        return region

    for data in locations_by_region[region_type]:
        location = Location(world.player, data.name, data.location_id, region)
        location.progress_type = data.progress_type
        # location.item_rule = data.item_rule
        region.locations.append(location)
        world.set_rule(location, data.rule)

        if data.location_id & (1 << 51):
            if data.progress_type == LocationProgressType.EXCLUDED:
                world.sanity_fill_locations.append(location)
            else:
                world.backup_sanity_fill_locations.append(location)
    return region

def create_regions(world: "TCGSimulatorWorld"):
    menu = create_region(world, DefaultRegions.MENU)

    locations_by_region: dict[RegionTypeEnum, list[GeneratedLocationData]] = defaultdict(list)

    for family in CardAchievementFamily:
        for _location in  generate_open_achievement_locations(
                family,
                Difficulty(world.options.checks_opening_difficulty.value)
        ):
            locations_by_region[_location.region].append(_location)

        for _location in generate_sell_achievement_locations(
                family,
                Difficulty(world.options.checks_selling_difficulty.value)
        ):
            locations_by_region[_location.region].append(_location)

        for _location in generate_grade_achievement_locations(
                family,
                Difficulty(world.options.checks_grading_difficulty.value)
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

    #always have 4 starting items
    remaining = world.total_licenses - 4
    booster_items_to_skip = 0

    pack_types = [
        required_items
        for required_items, _, _ in pack_regions.values()
    ]
    #Collection builder start is super restrictive on low max level
    if world.options.goal.value == world.options.goal.option_collection_builder and world.options.max_level.value == 10:

        starting_pack_type = world.random.choice(pack_types)
        starting_pack = world.random.choice(starting_pack_type)
        booster_pack_items.remove(starting_pack)
        starting_license_items.append(starting_pack)

        accessories_items.remove(AccessoriesItems.PROGRESSIVE_CLEANSER)
        starting_license_items.append(AccessoriesItems.PROGRESSIVE_CLEANSER)
        starting_license_items.append(figurine_items.pop())
        starting_license_items.append(tabletop_items.pop())

        for pack_type in pack_types:
            if any(item in starting_license_items for item in pack_type):
                continue

            available = [
                item
                for item in pack_type
                if item in booster_pack_items
            ]
            chosen = world.random.choice(available)

            booster_pack_items.remove(chosen)
            license_items.append(chosen)
            remaining -= 1
    else:
        for shop in shops:
            starting_license_items.append(shop.pop())

        if AccessoriesItems.PROGRESSIVE_CLEANSER not in starting_license_items:
            accessories_items.remove(AccessoriesItems.PROGRESSIVE_CLEANSER)
            license_items.append(AccessoriesItems.PROGRESSIVE_CLEANSER)
            remaining -= 1

        if world.options.goal.value == world.options.goal.option_collection_builder:
            booster_items_to_skip = 8
            for pack_type in pack_types:
                if any(item in starting_license_items for item in pack_type):
                    booster_items_to_skip -= 1
                    continue

                available = [
                    item
                    for item in pack_type
                    if item in booster_pack_items
                ]

                chosen = world.random.choice(available)

                booster_pack_items.remove(chosen)
                license_items.append(chosen)
                remaining -= 1


    if remaining < 0:
        raise OptionError(
            "Not enough licenses available for the selected goal."
        )

    while remaining > 0:
        for shop in shops:

            if remaining == 0:
                break
            if shop == booster_pack_items and booster_items_to_skip > 0:
                booster_items_to_skip -=1
                continue

            if not shop:
                continue

            license_items.append(shop.pop())
            remaining -= 1

        if all(not shop for shop in shops):
            break

    if world.is_ut:
        license_items = world.license_items
        starting_license_items = world.starting_license_items

    for item in license_items:
        for _location in generate_license_locations(ShopProduct(item.item_id-ITEMS_LICENSE_OFFSET), world.options.sell_check_amount.value):
            locations_by_region[_location.region].append(_location)
    for item in starting_license_items:
        for _location in generate_license_locations(ShopProduct(item.item_id-ITEMS_LICENSE_OFFSET), world.options.sell_check_amount.value):
            locations_by_region[_location.region].append(_location)

    available_licenses = set(license_items) | set(starting_license_items)

    if world.options.bulk_box.value:
        if available_licenses & TETRAMON_BASE_PACK_ITEMS:
            for _location in generate_license_locations(ShopProduct.BULKBOX_TETRAMON, world.options.sell_check_amount.value):
                locations_by_region[_location.region].append(_location)
        if available_licenses & TETRAMON_DESTINY_PACK_ITEMS:
            for _location in generate_license_locations(ShopProduct.BULKBOX_DESTINY, world.options.sell_check_amount.value):
                locations_by_region[_location.region].append(_location)

    for region in GenericRegions:
        create_region(world, region, locations_by_region)

    create_region(
        world,
        LevelRegions.LEVELS_1_TO_4,
        locations_by_region,
    )

    for level in range(5, world.options.max_level.value + 1, 5):
        create_region(
            world,
            get_level_region(level),
            locations_by_region,
        )

    for open_region, (required_items, sell_region, grade_region) in pack_regions.items():
        if not any(item in available_licenses for item in required_items):
            continue

        for region in (open_region, sell_region, grade_region):
            create_region(world, region, locations_by_region)

    return license_items, starting_license_items


def create_entrances(world: "TCGSimulatorWorld"):
    for entrance in (*Entrances, *LevelEntrances, *PackEntrances):

        if entrance.exiting_region not in world.created_region_types or entrance.entering_region not in world.created_region_types:
            continue

        world.create_entrance(
            world.get_region(entrance.exiting_region.value),
            world.get_region(entrance.entering_region.value),
            rule=entrance.rule,
            name=entrance.value,
            force_creation=True,
        )