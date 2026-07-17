from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from collections import defaultdict
from dataclasses import dataclass
from BaseClasses import Location, LocationProgressType
from rule_builder.rules import Has, Rule

from . import constants
from . import items
from .constants import Regions, Items, Locations
from .items import ItemHandler
from .events import EventHandler, Started, Cleared

if TYPE_CHECKING:
    from .world import TombaWorld


def get_name(name: str, region: str):
    return f"{name} ({region})"


@dataclass
class LocationData:
    _id_counter: ClassVar[int] = 1  # ID 0 is reserved

    id: int
    name: str
    region: str
    item_id: int
    progress_type: LocationProgressType
    area_id: int | None
    section_id: int | None
    rule: Rule | None

    def __init__(
        self,
        name: str,
        region: str,
        item_name: str,
        area_id: int | None = None,
        section_id: int | None = None,
        progress_type: LocationProgressType = LocationProgressType.DEFAULT,
        rule: Rule | None = None,
    ):
        self.id = LocationData._id_counter
        LocationData._id_counter += 1

        self.name = get_name(name, region)
        self.region = region
        self.progress_type = progress_type

        item = ItemHandler.by_name.get(item_name, None)
        if item is not None:
            self.item_id = item.id

        self.area_id = area_id
        self.section_id = section_id
        self.rule = rule

    def __repr__(self) -> str:
        return self.name


class LocationHandler:
    location_table: list[LocationData] = [
        LocationData(Locations.MAILBOX, Regions.VILLAGE_OF_ALL_BEGINNINGS, Items.FURIOUS_TORNADO),
        LocationData("Peach Flower Gas", Regions.VILLAGE_OF_ALL_BEGINNINGS, Items.BABY_PIG),
        LocationData("Kokka Egg in the Village", Regions.VILLAGE_OF_ALL_BEGINNINGS, Items.CHICK, 0x00, 0x00),
        LocationData(
            "100 Year Chest in the Tree",
            Regions.VILLAGE_OF_ALL_BEGINNINGS,
            Items.HUNDRED_YEAR_OLD_BELL,
            rule=Has(Items.HUNDRED_YEAR_OLD_KEY),
        ),
        LocationData("Kokka Egg near the elevator", Regions.FOREST_OF_ALL_BEGINNINGS, Items.CHICK, 0x00, 0x01),
        LocationData("Kokka Egg near the Hut 1", Regions.FOREST_OF_ALL_BEGINNINGS, Items.CHICK, 0x00, 0x02),
        LocationData("Kokka Egg near the Hut 2", Regions.FOREST_OF_ALL_BEGINNINGS, Items.CHICK, 0x00, 0x02),
        LocationData("Bitting Plant", Regions.FOREST_OF_ALL_BEGINNINGS, Items.BITTING_PLANT_FLOWER),
        LocationData("100 Year Old Reward", Regions.FOREST_OF_ALL_BEGINNINGS, Items.HUNDRED_YEAR_OLD_KEY),
        LocationData(
            "100 Year Chest near the Hut",
            Regions.FOREST_OF_ALL_BEGINNINGS,
            Items.CHARITY_WINGS,
            0x00,
            0x02,
            rule=Has(Items.HUNDRED_YEAR_OLD_KEY),
        ),
        LocationData("Drown", Regions.OL_POND, Items.BANANAS),
        *[
            LocationData(f"Leaf Butterfly {index}", Regions.FOREST_OF_100_FLOWERS, Items.LEAF_BUTTERFLY)
            for index in range(1, 30)
        ],
        LocationData("Campfire", Regions.FOREST_OF_100_FLOWERS, Items.BAKED_YAM, rule=Has(Items.BUCKET_OF_WATER)),
        LocationData(
            "On Top of the Spikes",
            Regions.FOREST_OF_100_FLOWERS,
            Items.WOOD_BOOMERANG,
            rule=Has(Items.HUNDRED_YEAR_OLD_KEY),
        ),
        LocationData(
            "1,000 Year Chest",
            Regions.FOREST_OF_100_FLOWERS,
            Items.CHARITY_WINGS,
            0x02,
            0x00,
            rule=Has(Items.THOUSAND_YEAR_OLD_KEY),
        ),
        LocationData("Top of Watch Tower", Regions.WATCH_TOWER, Items.TELESCOPE),
        LocationData("Push the Boulder", Regions.WATCH_TOWER, Items.DIRTY_MIRROR),
        LocationData("Under the Boulder", Regions.WATCH_TOWER, Items.FLOWER_SEEDS),
        LocationData("100 Year Chest", Regions.WATCH_TOWER, Items.JUMPING_PANTS, rule=Has(Items.HUNDRED_YEAR_OLD_KEY)),
        LocationData(
            "Million Year Chest", Regions.WATCH_TOWER, Items.ORANGE_EVIL_PIG_BAG, rule=Has(Items.MILLION_YEAR_OLD_KEY)
        ),
        LocationData("Fill the Bucket", Regions.WATCH_TOWER, Items.BUCKET_OF_WATER, rule=Has(Items.BUCKET)),
        LocationData("On top of the Pole", Regions.WOBBLY_WHARF, Items.BUCKET),
        LocationData("Fire Starter", Regions.DWARF_VILLAGE, Items.TORCH),
        LocationData("Meet the Dwarf Elder", Regions.DWARF_VILLAGE, Items.BLUE_EVIL_PIG_BAG),
        LocationData("Jail", Regions.DWARF_VILLAGE, Items.BROKEN_VASE),
        LocationData("AP Box", Regions.MUSHROOM_FOREST, Items.ORDINARY_MUSHROOM, rule=Has(Locations.AP_150_000)),
        LocationData(
            "1,000 Year Chest 1",
            Regions.MUSHROOM_FOREST,
            Items.THOUSAND_YEAR_OLD_BELL,
            rule=Has(Items.THOUSAND_YEAR_OLD_KEY),
        ),
        LocationData(
            "1,000 Year Chest 2",
            Regions.MUSHROOM_FOREST,
            Items.MYSTERIOUS_MUSHROOM,
            rule=Has(Items.THOUSAND_YEAR_OLD_KEY),
        ),
        # LocationData("1,000 Year Chest 3", Regions.MUSHROOM_FOREST, Items.CHARITY_WINGS, 0x??, 0x??,
        #             rule=Has(Items.THOUSAND_YEAR_OLD_KEY)),
        # LocationData("10,000 Year Chest", Regions.MUSHROOM_FOREST, Items.CHARITY_WINGS, 0x??, 0x??,
        #             rule=Has(Items.TEN_THOUSAND_YEAR_OLD_KEY)),
        # LocationData("100 Year Chest", Regions.MUSHROOM_FOREST, Items.CHARITY_WINGS, 0x??, 0x??,
        #             rule=Has(Items.HUNDRED_YEAR_OLD_KEY)),
        LocationData("Monster Fight", Regions.MUSHROOM_FOREST, Items.RISE_AND_SHINE_POWDER),
    ]

    @staticmethod
    def filter(item_id: int, area_id: int, section_id: int) -> list[int]:
        return [
            location.id
            for location in LocationHandler.location_table
            if location.item_id == item_id
            and (location.area_id is None or location.area_id == area_id)
            and (location.section_id is None or location.section_id == section_id)
        ]

    by_name = {}
    by_region = defaultdict(list)
    by_item_id = defaultdict(list)
    name_to_id = {}

    for location in location_table:
        by_name[location.name] = location
        by_region[location.region].append(location)

        if hasattr(location, "item_id"):
            by_item_id[location.item_id].append(location.id)

        name_to_id[location.name] = location.id


class TombaLocation(Location):
    game = constants.GAME


def create_all_locations(world: TombaWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: TombaWorld) -> None:
    for name, locations in LocationHandler.by_region.items():
        region = world.get_region(name)
        region.add_locations({location.name: location.id for location in locations}, TombaLocation)

    # Force furious tornado to be on Mailbox
    # TODO: Fix crash when using Tornado and mailbox still has the animation
    MAILBOX = world.get_location(get_name(Locations.MAILBOX, Regions.VILLAGE_OF_ALL_BEGINNINGS))
    MAILBOX.place_locked_item(ItemHandler.create_item(world, Items.FURIOUS_TORNADO))


def create_events(world: TombaWorld) -> None:
    """Those event are considered cleared once the logic reach the specific region they are in"""
    for event in EventHandler.event_table:
        started_region = world.get_region(event.started_region)
        started_region.add_event(
            Started(event.name), location_type=TombaLocation, item_type=items.TombaItem, show_in_spoiler=False
        )

        cleared_region = started_region
        if event.cleared_region != event.started_region:
            cleared_region = world.get_region(event.cleared_region)

        cleared_region.add_event(
            Cleared(event.name), location_type=TombaLocation, item_type=items.TombaItem, show_in_spoiler=False
        )

    VILLAGE_OF_ALL_BEGINNINGS = world.get_region(Regions.VILLAGE_OF_ALL_BEGINNINGS)
    VILLAGE_OF_ALL_BEGINNINGS.add_event(Locations.AP_150_000, location_type=TombaLocation, item_type=items.TombaItem)
