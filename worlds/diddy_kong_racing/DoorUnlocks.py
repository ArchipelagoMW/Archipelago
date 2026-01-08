from __future__ import annotations

import math
import re
from typing import TYPE_CHECKING

from BaseClasses import Location
from .Names import ItemName, LocationName

if TYPE_CHECKING:
    from . import DiddyKongRacingWorld
else:
    DiddyKongRacingWorld = object


class DoorUnlockInfo:
    def __init__(self, item: str, location: str, requirement: int):
        self.item = item
        self.location = location
        self.requirement = requirement


vanilla_door_unlock_info_list: list[DoorUnlockInfo] = [
    DoorUnlockInfo(ItemName.DINO_DOMAIN_UNLOCK, LocationName.WORLD_1_UNLOCK, 1),
    DoorUnlockInfo(ItemName.SNOWFLAKE_MOUNTAIN_UNLOCK, LocationName.WORLD_2_UNLOCK, 2),
    DoorUnlockInfo(ItemName.SHERBET_ISLAND_UNLOCK, LocationName.WORLD_3_UNLOCK, 10),
    DoorUnlockInfo(ItemName.DRAGON_FOREST_UNLOCK, LocationName.WORLD_4_UNLOCK, 16),
    DoorUnlockInfo(ItemName.ANCIENT_LAKE_DOOR_1_UNLOCK, LocationName.RACE_1_1_UNLOCK, 1),
    DoorUnlockInfo(ItemName.ANCIENT_LAKE_DOOR_2_UNLOCK, LocationName.RACE_1_2_UNLOCK, 6),
    DoorUnlockInfo(ItemName.FOSSIL_CANYON_DOOR_1_UNLOCK, LocationName.RACE_2_1_UNLOCK, 2),
    DoorUnlockInfo(ItemName.FOSSIL_CANYON_DOOR_2_UNLOCK, LocationName.RACE_2_2_UNLOCK, 7),
    DoorUnlockInfo(ItemName.JUNGLE_FALLS_DOOR_1_UNLOCK, LocationName.RACE_3_1_UNLOCK, 3),
    DoorUnlockInfo(ItemName.JUNGLE_FALLS_DOOR_2_UNLOCK, LocationName.RACE_3_2_UNLOCK, 8),
    DoorUnlockInfo(ItemName.HOT_TOP_VOLCANO_DOOR_1_UNLOCK, LocationName.RACE_4_1_UNLOCK, 5),
    DoorUnlockInfo(ItemName.HOT_TOP_VOLCANO_DOOR_2_UNLOCK, LocationName.RACE_4_2_UNLOCK, 10),
    DoorUnlockInfo(ItemName.EVERFROST_PEAK_DOOR_1_UNLOCK, LocationName.RACE_5_1_UNLOCK, 2),
    DoorUnlockInfo(ItemName.EVERFROST_PEAK_DOOR_2_UNLOCK, LocationName.RACE_5_2_UNLOCK, 10),
    DoorUnlockInfo(ItemName.WALRUS_COVE_DOOR_1_UNLOCK, LocationName.RACE_6_1_UNLOCK, 3),
    DoorUnlockInfo(ItemName.WALRUS_COVE_DOOR_2_UNLOCK, LocationName.RACE_6_2_UNLOCK, 11),
    DoorUnlockInfo(ItemName.SNOWBALL_VALLEY_DOOR_1_UNLOCK, LocationName.RACE_7_1_UNLOCK, 6),
    DoorUnlockInfo(ItemName.SNOWBALL_VALLEY_DOOR_2_UNLOCK, LocationName.RACE_7_2_UNLOCK, 14),
    DoorUnlockInfo(ItemName.FROSTY_VILLAGE_DOOR_1_UNLOCK, LocationName.RACE_8_1_UNLOCK, 9),
    DoorUnlockInfo(ItemName.FROSTY_VILLAGE_DOOR_2_UNLOCK, LocationName.RACE_8_2_UNLOCK, 16),
    DoorUnlockInfo(ItemName.WHALE_BAY_DOOR_1_UNLOCK, LocationName.RACE_9_1_UNLOCK, 10),
    DoorUnlockInfo(ItemName.WHALE_BAY_DOOR_2_UNLOCK, LocationName.RACE_9_2_UNLOCK, 17),
    DoorUnlockInfo(ItemName.CRESCENT_ISLAND_DOOR_1_UNLOCK, LocationName.RACE_10_1_UNLOCK, 11),
    DoorUnlockInfo(ItemName.CRESCENT_ISLAND_DOOR_2_UNLOCK, LocationName.RACE_10_2_UNLOCK, 18),
    DoorUnlockInfo(ItemName.PIRATE_LAGOON_DOOR_1_UNLOCK, LocationName.RACE_11_1_UNLOCK, 13),
    DoorUnlockInfo(ItemName.PIRATE_LAGOON_DOOR_2_UNLOCK, LocationName.RACE_11_2_UNLOCK, 20),
    DoorUnlockInfo(ItemName.TREASURE_CAVES_DOOR_1_UNLOCK, LocationName.RACE_12_1_UNLOCK, 16),
    DoorUnlockInfo(ItemName.TREASURE_CAVES_DOOR_2_UNLOCK, LocationName.RACE_12_2_UNLOCK, 22),
    DoorUnlockInfo(ItemName.WINDMILL_PLAINS_DOOR_1_UNLOCK, LocationName.RACE_13_1_UNLOCK, 16),
    DoorUnlockInfo(ItemName.WINDMILL_PLAINS_DOOR_2_UNLOCK, LocationName.RACE_13_2_UNLOCK, 23),
    DoorUnlockInfo(ItemName.GREENWOOD_VILLAGE_DOOR_1_UNLOCK, LocationName.RACE_14_1_UNLOCK, 17),
    DoorUnlockInfo(ItemName.GREENWOOD_VILLAGE_DOOR_2_UNLOCK, LocationName.RACE_14_2_UNLOCK, 24),
    DoorUnlockInfo(ItemName.BOULDER_CANYON_DOOR_1_UNLOCK, LocationName.RACE_15_1_UNLOCK, 20),
    DoorUnlockInfo(ItemName.BOULDER_CANYON_DOOR_2_UNLOCK, LocationName.RACE_15_2_UNLOCK, 30),
    DoorUnlockInfo(ItemName.HAUNTED_WOODS_DOOR_1_UNLOCK, LocationName.RACE_16_1_UNLOCK, 22),
    DoorUnlockInfo(ItemName.HAUNTED_WOODS_DOOR_2_UNLOCK, LocationName.RACE_16_2_UNLOCK, 37),
    DoorUnlockInfo(ItemName.SPACEDUST_ALLEY_DOOR_1_UNLOCK, LocationName.RACE_17_1_UNLOCK, 39),
    DoorUnlockInfo(ItemName.SPACEDUST_ALLEY_DOOR_2_UNLOCK, LocationName.RACE_17_2_UNLOCK, 43),
    DoorUnlockInfo(ItemName.DARKMOON_CAVERNS_DOOR_1_UNLOCK, LocationName.RACE_18_1_UNLOCK, 40),
    DoorUnlockInfo(ItemName.DARKMOON_CAVERNS_DOOR_2_UNLOCK, LocationName.RACE_18_2_UNLOCK, 44),
    DoorUnlockInfo(ItemName.SPACEPORT_ALPHA_DOOR_1_UNLOCK, LocationName.RACE_19_1_UNLOCK, 41),
    DoorUnlockInfo(ItemName.SPACEPORT_ALPHA_DOOR_2_UNLOCK, LocationName.RACE_19_2_UNLOCK, 45),
    DoorUnlockInfo(ItemName.STAR_CITY_DOOR_1_UNLOCK, LocationName.RACE_20_1_UNLOCK, 42),
    DoorUnlockInfo(ItemName.STAR_CITY_DOOR_2_UNLOCK, LocationName.RACE_20_2_UNLOCK, 46)
]

vanilla_door_unlock_info_sorted_by_requirement: list[DoorUnlockInfo] = sorted(vanilla_door_unlock_info_list,
                                                                              key=lambda x: x.requirement)
cached_door_requirement_progression: list[int] | None = None

DOOR_UNLOCK_ITEM_PATTERN = re.compile("(\\d+) balloon\\(s\\) \\(.* Unlock\\)")


def get_door_requirement_progression(world: DiddyKongRacingWorld) -> list[int]:
    global cached_door_requirement_progression
    if cached_door_requirement_progression:
        return cached_door_requirement_progression

    if world.options.door_requirement_progression == 0:  # Vanilla
        door_requirement_progression = [x.requirement for x in vanilla_door_unlock_info_sorted_by_requirement]
    elif world.options.door_requirement_progression == 1:  # Linear
        door_unlock_requirement_interval = ((world.options.maximum_door_requirement - 1)
                                            / (len(vanilla_door_unlock_info_list) - 1))
        door_requirement_progression = []
        door_unlock_requirement = 1
        for _ in range(len(vanilla_door_unlock_info_list)):
            door_requirement_progression.append(math.floor(door_unlock_requirement))
            door_unlock_requirement += door_unlock_requirement_interval
    else:  # Exponential
        door_requirement_progression = []
        ratio = world.options.maximum_door_requirement / 46
        for i in range(len(vanilla_door_unlock_info_list) - 1):
            door_requirement_progression.append(max(1, math.floor(ratio * 3.31 * math.exp(0.0628 * i) - 2)))

        door_requirement_progression.append(int(world.options.maximum_door_requirement))

    cached_door_requirement_progression = door_requirement_progression
    return door_requirement_progression


def shuffle_door_unlock_items(world: DiddyKongRacingWorld) -> None:
    race_1_unlock_to_race_2_unlock = {
        ItemName.ANCIENT_LAKE_DOOR_1_UNLOCK: ItemName.ANCIENT_LAKE_DOOR_2_UNLOCK,
        ItemName.FOSSIL_CANYON_DOOR_1_UNLOCK: ItemName.FOSSIL_CANYON_DOOR_2_UNLOCK,
        ItemName.JUNGLE_FALLS_DOOR_1_UNLOCK: ItemName.JUNGLE_FALLS_DOOR_2_UNLOCK,
        ItemName.HOT_TOP_VOLCANO_DOOR_1_UNLOCK: ItemName.HOT_TOP_VOLCANO_DOOR_2_UNLOCK,
        ItemName.EVERFROST_PEAK_DOOR_1_UNLOCK: ItemName.EVERFROST_PEAK_DOOR_2_UNLOCK,
        ItemName.WALRUS_COVE_DOOR_1_UNLOCK: ItemName.WALRUS_COVE_DOOR_2_UNLOCK,
        ItemName.SNOWBALL_VALLEY_DOOR_1_UNLOCK: ItemName.SNOWBALL_VALLEY_DOOR_2_UNLOCK,
        ItemName.FROSTY_VILLAGE_DOOR_1_UNLOCK: ItemName.FROSTY_VILLAGE_DOOR_2_UNLOCK,
        ItemName.WHALE_BAY_DOOR_1_UNLOCK: ItemName.WHALE_BAY_DOOR_2_UNLOCK,
        ItemName.CRESCENT_ISLAND_DOOR_1_UNLOCK: ItemName.CRESCENT_ISLAND_DOOR_2_UNLOCK,
        ItemName.PIRATE_LAGOON_DOOR_1_UNLOCK: ItemName.PIRATE_LAGOON_DOOR_2_UNLOCK,
        ItemName.TREASURE_CAVES_DOOR_1_UNLOCK: ItemName.TREASURE_CAVES_DOOR_2_UNLOCK,
        ItemName.WINDMILL_PLAINS_DOOR_1_UNLOCK: ItemName.WINDMILL_PLAINS_DOOR_2_UNLOCK,
        ItemName.GREENWOOD_VILLAGE_DOOR_1_UNLOCK: ItemName.GREENWOOD_VILLAGE_DOOR_2_UNLOCK,
        ItemName.BOULDER_CANYON_DOOR_1_UNLOCK: ItemName.BOULDER_CANYON_DOOR_2_UNLOCK,
        ItemName.HAUNTED_WOODS_DOOR_1_UNLOCK: ItemName.HAUNTED_WOODS_DOOR_2_UNLOCK,
        ItemName.SPACEDUST_ALLEY_DOOR_1_UNLOCK: ItemName.SPACEDUST_ALLEY_DOOR_2_UNLOCK,
        ItemName.DARKMOON_CAVERNS_DOOR_1_UNLOCK: ItemName.DARKMOON_CAVERNS_DOOR_2_UNLOCK,
        ItemName.SPACEPORT_ALPHA_DOOR_1_UNLOCK: ItemName.SPACEPORT_ALPHA_DOOR_2_UNLOCK,
        ItemName.STAR_CITY_DOOR_1_UNLOCK: ItemName.STAR_CITY_DOOR_2_UNLOCK
    }

    dino_domain_race_1_unlocks = (
        ItemName.ANCIENT_LAKE_DOOR_1_UNLOCK,
        ItemName.FOSSIL_CANYON_DOOR_1_UNLOCK,
        ItemName.JUNGLE_FALLS_DOOR_1_UNLOCK,
        ItemName.HOT_TOP_VOLCANO_DOOR_1_UNLOCK
    )
    snowflake_mountain_race_1_unlocks = (
        ItemName.EVERFROST_PEAK_DOOR_1_UNLOCK,
        ItemName.WALRUS_COVE_DOOR_1_UNLOCK,
        ItemName.SNOWBALL_VALLEY_DOOR_1_UNLOCK,
        ItemName.FROSTY_VILLAGE_DOOR_1_UNLOCK
    )
    sherbet_island_race_1_unlocks = (
        ItemName.WHALE_BAY_DOOR_1_UNLOCK,
        ItemName.CRESCENT_ISLAND_DOOR_1_UNLOCK,
        ItemName.PIRATE_LAGOON_DOOR_1_UNLOCK,
        ItemName.TREASURE_CAVES_DOOR_1_UNLOCK
    )
    dragon_forest_race_1_unlocks = (
        ItemName.WINDMILL_PLAINS_DOOR_1_UNLOCK,
        ItemName.GREENWOOD_VILLAGE_DOOR_1_UNLOCK,
        ItemName.BOULDER_CANYON_DOOR_1_UNLOCK,
        ItemName.HAUNTED_WOODS_DOOR_1_UNLOCK
    )
    future_fun_land_race_1_unlocks = (
        ItemName.SPACEDUST_ALLEY_DOOR_1_UNLOCK,
        ItemName.DARKMOON_CAVERNS_DOOR_1_UNLOCK,
        ItemName.SPACEPORT_ALPHA_DOOR_1_UNLOCK,
        ItemName.STAR_CITY_DOOR_1_UNLOCK
    )

    if world.options.open_worlds:
        available_doors = [
            *dino_domain_race_1_unlocks,
            *snowflake_mountain_race_1_unlocks,
            *sherbet_island_race_1_unlocks,
            *dragon_forest_race_1_unlocks,
            *future_fun_land_race_1_unlocks
        ]
    else:
        available_doors = [
            ItemName.DINO_DOMAIN_UNLOCK,
            ItemName.SNOWFLAKE_MOUNTAIN_UNLOCK,
            ItemName.SHERBET_ISLAND_UNLOCK,
            ItemName.DRAGON_FOREST_UNLOCK
        ]

    door_unlock_item_to_index = {door_unlock_info.item: index for index, door_unlock_info in
                                 enumerate(vanilla_door_unlock_info_list)}

    race_2_unlock_count = 0

    for door_unlock_info, requirement in zip(vanilla_door_unlock_info_sorted_by_requirement,
                                             get_door_requirement_progression(world)):
        if not (world.options.open_worlds and door_unlock_info.location in LocationName.WORLD_UNLOCK_LOCATIONS):
            world.random.shuffle(available_doors)
            door_unlock_item = available_doors.pop()
            door_unlock_item_index = door_unlock_item_to_index[door_unlock_item]
            world.door_unlock_requirements[door_unlock_item_index] = requirement

            if door_unlock_item == ItemName.DINO_DOMAIN_UNLOCK:
                available_doors.extend(dino_domain_race_1_unlocks)
            elif door_unlock_item == ItemName.SNOWFLAKE_MOUNTAIN_UNLOCK:
                available_doors.extend(snowflake_mountain_race_1_unlocks)
            elif door_unlock_item == ItemName.SHERBET_ISLAND_UNLOCK:
                available_doors.extend(sherbet_island_race_1_unlocks)
            elif door_unlock_item == ItemName.DRAGON_FOREST_UNLOCK:
                available_doors.extend(dragon_forest_race_1_unlocks)
            elif door_unlock_item in race_1_unlock_to_race_2_unlock:
                available_doors.append(race_1_unlock_to_race_2_unlock[door_unlock_item])
            elif not world.options.open_worlds:
                race_2_unlock_count += 1
                if race_2_unlock_count == 16:
                    available_doors.extend(future_fun_land_race_1_unlocks)


def place_vanilla_door_unlock_items(world: DiddyKongRacingWorld) -> None:
    for door_num, door_unlock_info in enumerate(vanilla_door_unlock_info_list):
        if not (world.options.open_worlds and door_unlock_info.location in LocationName.WORLD_UNLOCK_LOCATIONS):
            world.door_unlock_requirements[door_num] = door_unlock_info.requirement


def place_door_unlock_items(world: DiddyKongRacingWorld) -> None:
    filled_door_unlock_locations = set()
    if world.options.open_worlds:
        filled_door_unlock_locations.update(LocationName.WORLD_UNLOCK_LOCATIONS)

    origin_region = world.get_region(world.origin_region_name)

    for item_door_unlock_info, item_door_unlock_requirement in zip(vanilla_door_unlock_info_list,
                                                                   world.door_unlock_requirements):
        if not (world.options.open_worlds and item_door_unlock_info.location in LocationName.WORLD_UNLOCK_LOCATIONS):
            for location_door_unlock_info, location_door_unlock_requirement in \
                    zip(vanilla_door_unlock_info_sorted_by_requirement, get_door_requirement_progression(world)):
                base_location_name = location_door_unlock_info.location
                if item_door_unlock_requirement == location_door_unlock_requirement and base_location_name not in filled_door_unlock_locations:
                    location_name = build_door_unlock_location_name(location_door_unlock_info.location,
                                                                    item_door_unlock_requirement)
                    origin_region.add_locations({location_name: None})
                    world.place_locked_item(location_name, world.create_event_item(item_door_unlock_info.item))
                    filled_door_unlock_locations.add(base_location_name)
                    break


def build_door_unlock_location_name(door_unlock_location_base_name: str, door_unlock_requirement: int) -> str:
    return str(door_unlock_requirement) + " balloon(s) (" + door_unlock_location_base_name + ")"


def is_door_unlock_location(location: Location):
    return DOOR_UNLOCK_ITEM_PATTERN.match(location.name)


def get_door_unlock_requirement(location: Location):
    return int(DOOR_UNLOCK_ITEM_PATTERN.match(location.name).group(1))
