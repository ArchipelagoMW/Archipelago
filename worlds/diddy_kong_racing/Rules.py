from typing import TYPE_CHECKING, Callable

from BaseClasses import CollectionState
from worlds.generic.Rules import set_rule
from .DoorUnlocks import get_door_unlock_requirement, is_door_unlock_location
from .Names import ItemName, LocationName, RegionName
from .Regions import convert_region_name_to_entrance_name

# Allows type hinting without circular imports
if TYPE_CHECKING:
    from . import DiddyKongRacingWorld
else:
    DiddyKongRacingWorld = object

VANILLA_RACE_2_LOCATIONS: list[list[str]] = [
    [LocationName.ANCIENT_LAKE_2, LocationName.FIRE_MOUNTAIN_KEY],
    [LocationName.FOSSIL_CANYON_2],
    [LocationName.JUNGLE_FALLS_2],
    [LocationName.HOT_TOP_VOLCANO_2],
    [LocationName.EVERFROST_PEAK_2],
    [LocationName.WALRUS_COVE_2],
    [LocationName.SNOWBALL_VALLEY_2, LocationName.ICICLE_PYRAMID_KEY],
    [LocationName.FROSTY_VILLAGE_2],
    [LocationName.WHALE_BAY_2],
    [LocationName.CRESCENT_ISLAND_2, LocationName.DARKWATER_BEACH_KEY],
    [LocationName.PIRATE_LAGOON_2],
    [LocationName.TREASURE_CAVES_2],
    [LocationName.WINDMILL_PLAINS_2],
    [LocationName.GREENWOOD_VILLAGE_2],
    [LocationName.BOULDER_CANYON_2, LocationName.SMOKEY_CASTLE_KEY],
    [LocationName.HAUNTED_WOODS_2],
    [LocationName.SPACEDUST_ALLEY_2],
    [LocationName.DARKMOON_CAVERNS_2],
    [LocationName.SPACEPORT_ALPHA_2],
    [LocationName.STAR_CITY_2]
]


def set_rules(world: DiddyKongRacingWorld) -> None:
    # Skip for Universal Tracker, these will be called from interpret_slot_data as they depend on slot data
    if not hasattr(world.multiworld, "generation_is_fake"):
        set_region_access_rules(world)
        set_door_unlock_rules(world)
        set_race_2_location_rules(world)

    set_overworld_balloon_rules(world)
    set_amulet_rules(world)

    world.multiworld.completion_condition[world.player] = lambda state: state.has(ItemName.VICTORY, world.player)


def set_region_access_rules(world: DiddyKongRacingWorld) -> None:
    region_access_rules = {
        # Timber's Island
        RegionName.DINO_DOMAIN: dino_domain(world),
        RegionName.SNOWFLAKE_MOUNTAIN: snowflake_mountain(world),
        RegionName.SHERBET_ISLAND: sherbet_island(world),
        RegionName.DRAGON_FOREST: dragon_forest(world),
        RegionName.WIZPIG_1: wizpig_1(world),
        RegionName.FUTURE_FUN_LAND: future_fun_land(world),
        # Dino Domain
        RegionName.ANCIENT_LAKE: ancient_lake_door_1(world),
        RegionName.FOSSIL_CANYON: fossil_canyon_door_1(world),
        RegionName.JUNGLE_FALLS: jungle_falls_door_1(world),
        RegionName.HOT_TOP_VOLCANO: hot_top_volcano_door_1(world),
        RegionName.FIRE_MOUNTAIN: fire_mountain(world),
        RegionName.TRICKY: tricky_1(world),
        # Snowflake Mountain
        RegionName.EVERFROST_PEAK: everfrost_peak_door_1(world),
        RegionName.WALRUS_COVE: walrus_cove_door_1(world),
        RegionName.SNOWBALL_VALLEY: snowball_valley_door_1(world),
        RegionName.FROSTY_VILLAGE: frosty_village_door_1(world),
        RegionName.ICICLE_PYRAMID: icicle_pyramid(world),
        RegionName.BLUEY: bluey_1(world),
        # Sherbet Island
        RegionName.WHALE_BAY: whale_bay_door_1(world),
        RegionName.CRESCENT_ISLAND: crescent_island_door_1(world),
        RegionName.PIRATE_LAGOON: pirate_lagoon_door_1(world),
        RegionName.TREASURE_CAVES: treasure_caves_door_1(world),
        RegionName.DARKWATER_BEACH: darkwater_beach(world),
        RegionName.BUBBLER: bubbler_1(world),
        # Dragon Forest
        RegionName.WINDMILL_PLAINS: windmill_plains_door_1(world),
        RegionName.GREENWOOD_VILLAGE: greenwood_village_door_1(world),
        RegionName.BOULDER_CANYON: boulder_canyon_door_1(world),
        RegionName.HAUNTED_WOODS: haunted_woods_door_1(world),
        RegionName.SMOKEY_CASTLE: smokey_castle(world),
        RegionName.SMOKEY: smokey_1(world),
        # Future Fun Land
        RegionName.SPACEDUST_ALLEY: spacedust_alley_door_1(world),
        RegionName.DARKMOON_CAVERNS: darkmoon_caverns_door_1(world),
        RegionName.SPACEPORT_ALPHA: spaceport_alpha_door_1(world),
        RegionName.STAR_CITY: star_city_door_1(world)
    }

    if world.options.victory_condition.value == 1:
        region_access_rules[RegionName.WIZPIG_2] = wizpig_2(world)

    for region, rule in region_access_rules.items():
        entrance_name = convert_region_name_to_entrance_name(region)
        entrance = world.get_entrance(entrance_name)
        set_rule(entrance, rule)


def set_door_unlock_rules(world: DiddyKongRacingWorld) -> None:
    for location in world.get_region(world.origin_region_name).get_locations():
        if is_door_unlock_location(location):
            door_unlock_requirement = get_door_unlock_requirement(location)
            set_rule(location, door_unlock(world, door_unlock_requirement))


def set_overworld_balloon_rules(world: DiddyKongRacingWorld) -> None:
    overworld_balloon_rules = {
        LocationName.BRIDGE_BALLOON: bridge_balloon(world),
        LocationName.WATERFALL_BALLOON: waterfall_balloon(world),
        LocationName.RIVER_BALLOON: river_balloon(world),
        LocationName.OCEAN_BALLOON: ocean_balloon(world),
        LocationName.TAJ_CAR_RACE: tag_car_race(world),
        LocationName.TAJ_HOVERCRAFT_RACE: taj_hovercraft_race(world),
        LocationName.TAJ_PLANE_RACE: taj_plane_race(world)
    }

    for location, rule in overworld_balloon_rules.items():
        set_location_rule(world, location, rule)


def set_race_2_location_rules(world: DiddyKongRacingWorld) -> None:
    race_door_2_rules = [
        ancient_lake_door_2(world),
        fossil_canyon_door_2(world),
        jungle_falls_door_2(world),
        hot_top_volcano_door_2(world),
        everfrost_peak_door_2(world),
        walrus_cove_door_2(world),
        snowball_valley_door_2(world),
        frosty_village_door_2(world),
        whale_bay_door_2(world),
        crescent_island_door_2(world),
        pirate_lagoon_door_2(world),
        treasure_caves_door_2(world),
        windmill_plains_door_2(world),
        greenwood_village_door_2(world),
        boulder_canyon_door_2(world),
        haunted_woods_door_2(world),
        spacedust_alley_door_2(world),
        darkmoon_caverns_door_2(world),
        spaceport_alpha_door_2(world),
        star_city_door_2(world)
    ]

    for door_num, entrance_num in enumerate(world.entrance_order):
        race_door_2_rule = race_door_2_rules[door_num]
        for location in VANILLA_RACE_2_LOCATIONS[entrance_num]:
            set_location_rule(world, location, race_door_2_rule)


def set_amulet_rules(world: DiddyKongRacingWorld) -> None:
    amulet_rules = {
        LocationName.TRICKY_2: tricky_2(world),
        LocationName.BLUEY_2: bluey_2(world),
        LocationName.BUBBLER_2: bubbler_2(world),
        LocationName.SMOKEY_2: smokey_2(world)
    }

    for location, rule in amulet_rules.items():
        set_location_rule(world, location, rule)


def dino_domain(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: world.options.open_worlds or state.has(ItemName.DINO_DOMAIN_UNLOCK, world.player)


def snowflake_mountain(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: world.options.open_worlds or state.has(ItemName.SNOWFLAKE_MOUNTAIN_UNLOCK, world.player)


def sherbet_island(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: world.options.open_worlds or state.has(ItemName.SHERBET_ISLAND_UNLOCK, world.player)


def dragon_forest(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: world.options.open_worlds or state.has(ItemName.DRAGON_FOREST_UNLOCK, world.player)


def future_fun_land(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: (
            world.options.open_worlds.value
            or (
                    wizpig_1(world)(state)
                    and (
                            world.options.skip_trophy_races.value
                            or (
                                    tricky_2(world)(state)
                                    and bluey_2(world)(state)
                                    and bubbler_2(world)(state)
                                    and smokey_2(world)(state)
                            )
                    )
            )
    )


def bridge_balloon(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: True


def waterfall_balloon(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: True


def river_balloon(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: True


def ocean_balloon(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: True


def tag_car_race(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: has_total_balloon_count(world, state, 5)


def taj_hovercraft_race(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: has_total_balloon_count(world, state, 10)


def taj_plane_race(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: has_total_balloon_count(world, state, 18)


def ancient_lake_door_1(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: state.has(ItemName.ANCIENT_LAKE_DOOR_1_UNLOCK, world.player)


def ancient_lake_door_2(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: (state.has(ItemName.ANCIENT_LAKE_DOOR_2_UNLOCK, world.player)
                          and tricky_1(world)(state))


def fossil_canyon_door_1(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: state.has(ItemName.FOSSIL_CANYON_DOOR_1_UNLOCK, world.player)


def fossil_canyon_door_2(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: (state.has(ItemName.FOSSIL_CANYON_DOOR_2_UNLOCK, world.player)
                          and tricky_1(world)(state))


def jungle_falls_door_1(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: state.has(ItemName.JUNGLE_FALLS_DOOR_1_UNLOCK, world.player)


def jungle_falls_door_2(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: (state.has(ItemName.JUNGLE_FALLS_DOOR_2_UNLOCK, world.player)
                          and tricky_1(world)(state))


def hot_top_volcano_door_1(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: state.has(ItemName.HOT_TOP_VOLCANO_DOOR_1_UNLOCK, world.player)


def hot_top_volcano_door_2(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: (state.has(ItemName.HOT_TOP_VOLCANO_DOOR_2_UNLOCK, world.player)
                          and tricky_1(world)(state))


def everfrost_peak_door_1(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: state.has(ItemName.EVERFROST_PEAK_DOOR_1_UNLOCK, world.player)


def everfrost_peak_door_2(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: (state.has(ItemName.EVERFROST_PEAK_DOOR_2_UNLOCK, world.player)
                          and bluey_1(world)(state))


def walrus_cove_door_1(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: state.has(ItemName.WALRUS_COVE_DOOR_1_UNLOCK, world.player)


def walrus_cove_door_2(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: (state.has(ItemName.WALRUS_COVE_DOOR_2_UNLOCK, world.player)
                          and bluey_1(world)(state))


def snowball_valley_door_1(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: state.has(ItemName.SNOWBALL_VALLEY_DOOR_1_UNLOCK, world.player)


def snowball_valley_door_2(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: (state.has(ItemName.SNOWBALL_VALLEY_DOOR_2_UNLOCK, world.player)
                          and bluey_1(world)(state))


def frosty_village_door_1(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: state.has(ItemName.FROSTY_VILLAGE_DOOR_1_UNLOCK, world.player)


def frosty_village_door_2(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: (state.has(ItemName.FROSTY_VILLAGE_DOOR_2_UNLOCK, world.player)
                          and bluey_1(world)(state))


def whale_bay_door_1(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: state.has(ItemName.WHALE_BAY_DOOR_1_UNLOCK, world.player)


def whale_bay_door_2(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: (state.has(ItemName.WHALE_BAY_DOOR_2_UNLOCK, world.player)
                          and bubbler_1(world)(state))


def crescent_island_door_1(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: state.has(ItemName.CRESCENT_ISLAND_DOOR_1_UNLOCK, world.player)


def crescent_island_door_2(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: (state.has(ItemName.CRESCENT_ISLAND_DOOR_2_UNLOCK, world.player)
                          and bubbler_1(world)(state))


def pirate_lagoon_door_1(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: state.has(ItemName.PIRATE_LAGOON_DOOR_1_UNLOCK, world.player)


def pirate_lagoon_door_2(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: (state.has(ItemName.PIRATE_LAGOON_DOOR_2_UNLOCK, world.player)
                          and bubbler_1(world)(state))


def treasure_caves_door_1(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: state.has(ItemName.TREASURE_CAVES_DOOR_1_UNLOCK, world.player)


def treasure_caves_door_2(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: (state.has(ItemName.TREASURE_CAVES_DOOR_2_UNLOCK, world.player)
                          and bubbler_1(world)(state))


def windmill_plains_door_1(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: state.has(ItemName.WINDMILL_PLAINS_DOOR_1_UNLOCK, world.player)


def windmill_plains_door_2(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: (state.has(ItemName.WINDMILL_PLAINS_DOOR_2_UNLOCK, world.player)
                          and smokey_1(world)(state))


def greenwood_village_door_1(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: state.has(ItemName.GREENWOOD_VILLAGE_DOOR_1_UNLOCK, world.player)


def greenwood_village_door_2(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: (state.has(ItemName.GREENWOOD_VILLAGE_DOOR_2_UNLOCK, world.player)
                          and smokey_1(world)(state))


def boulder_canyon_door_1(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: state.has(ItemName.BOULDER_CANYON_DOOR_1_UNLOCK, world.player)


def boulder_canyon_door_2(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: (state.has(ItemName.BOULDER_CANYON_DOOR_2_UNLOCK, world.player)
                          and smokey_1(world)(state))


def haunted_woods_door_1(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: state.has(ItemName.HAUNTED_WOODS_DOOR_1_UNLOCK, world.player)


def haunted_woods_door_2(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: (state.has(ItemName.HAUNTED_WOODS_DOOR_2_UNLOCK, world.player)
                          and smokey_1(world)(state))


def spacedust_alley_door_1(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: state.has(ItemName.SPACEDUST_ALLEY_DOOR_1_UNLOCK, world.player)


def spacedust_alley_door_2(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: state.has(ItemName.SPACEDUST_ALLEY_DOOR_2_UNLOCK, world.player)


def darkmoon_caverns_door_1(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: state.has(ItemName.DARKMOON_CAVERNS_DOOR_1_UNLOCK, world.player)


def darkmoon_caverns_door_2(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: state.has(ItemName.DARKMOON_CAVERNS_DOOR_2_UNLOCK, world.player)


def spaceport_alpha_door_1(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: state.has(ItemName.SPACEPORT_ALPHA_DOOR_1_UNLOCK, world.player)


def spaceport_alpha_door_2(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: state.has(ItemName.SPACEPORT_ALPHA_DOOR_2_UNLOCK, world.player)


def star_city_door_1(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: state.has(ItemName.STAR_CITY_DOOR_1_UNLOCK, world.player)


def star_city_door_2(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: state.has(ItemName.STAR_CITY_DOOR_2_UNLOCK, world.player)


def fire_mountain(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: state.has(ItemName.FIRE_MOUNTAIN_KEY, world.player)


def icicle_pyramid(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: state.has(ItemName.ICICLE_PYRAMID_KEY, world.player)


def darkwater_beach(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: state.has(ItemName.DARKWATER_BEACH_KEY, world.player)


def smokey_castle(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: state.has(ItemName.SMOKEY_CASTLE_KEY, world.player)


def tricky_1(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: can_access_boss_1(world, state, ItemName.DINO_DOMAIN_BALLOON)


def tricky_2(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: can_access_boss_2(world, state, ItemName.DINO_DOMAIN_BALLOON)


def bluey_1(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: can_access_boss_1(world, state, ItemName.SNOWFLAKE_MOUNTAIN_BALLOON)


def bluey_2(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: can_access_boss_2(world, state, ItemName.SNOWFLAKE_MOUNTAIN_BALLOON)


def bubbler_1(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: can_access_boss_1(world, state, ItemName.SHERBET_ISLAND_BALLOON)


def bubbler_2(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: can_access_boss_2(world, state, ItemName.SHERBET_ISLAND_BALLOON)


def smokey_1(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: can_access_boss_1(world, state, ItemName.DRAGON_FOREST_BALLOON)


def smokey_2(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: can_access_boss_2(world, state, ItemName.DRAGON_FOREST_BALLOON)


def wizpig_1(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: state.has(ItemName.WIZPIG_AMULET_PIECE, world.player,
                                   world.options.wizpig_1_amulet_pieces.value)


def wizpig_2(world: DiddyKongRacingWorld) -> Callable[[object], bool]:
    return lambda state: (state.has(ItemName.TT_AMULET_PIECE, world.player, world.options.wizpig_2_amulet_pieces.value)
                          and has_total_balloon_count(world, state, world.options.wizpig_2_balloons.value))


def door_unlock(world: DiddyKongRacingWorld, requirement: int) -> Callable[[object], bool]:
    return lambda state: has_total_balloon_count(world, state, requirement)


def set_location_rule(world: DiddyKongRacingWorld, location_name: str, rule: Callable[[object], bool]) -> None:
    location = world.get_location(location_name)
    set_rule(location, rule)


def has_total_balloon_count(world: DiddyKongRacingWorld, state: CollectionState, balloon_count: int) -> bool:
    collected_balloon_count = state.count_from_list(
        [
            ItemName.TIMBERS_ISLAND_BALLOON,
            ItemName.DINO_DOMAIN_BALLOON,
            ItemName.SNOWFLAKE_MOUNTAIN_BALLOON,
            ItemName.SHERBET_ISLAND_BALLOON,
            ItemName.DRAGON_FOREST_BALLOON,
            ItemName.FUTURE_FUN_LAND_BALLOON
        ],
        world.player
    )

    return collected_balloon_count >= balloon_count


def can_access_boss_1(world: DiddyKongRacingWorld, state: CollectionState, regional_balloon_item_name: str) -> bool:
    return state.has(regional_balloon_item_name, world.player, world.options.boss_1_regional_balloons.value)


def can_access_boss_2(world: DiddyKongRacingWorld, state: CollectionState, regional_balloon_item_name: str) -> bool:
    return state.has(regional_balloon_item_name, world.player, world.options.boss_2_regional_balloons.value)
