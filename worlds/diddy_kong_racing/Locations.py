from __future__ import annotations

from typing import NamedTuple

from BaseClasses import Location
from .Names import LocationName


class DiddyKongRacingLocation(Location):
    game: str = "Diddy Kong Racing"


class LocationData(NamedTuple):
    dkr_id: int | None = 0


TIMBERS_ISLAND_LOCATION_TABLE: dict[str, LocationData] = {
    LocationName.BRIDGE_BALLOON: LocationData(1616100),
    LocationName.WATERFALL_BALLOON: LocationData(1616101),
    LocationName.RIVER_BALLOON: LocationData(1616102),
    LocationName.OCEAN_BALLOON: LocationData(1616103),
    LocationName.TAJ_CAR_RACE: LocationData(1616104),
    LocationName.TAJ_HOVERCRAFT_RACE: LocationData(1616105),
    LocationName.TAJ_PLANE_RACE: LocationData(1616106)
}

DINO_DOMAIN_LOCATION_TABLE: dict[str, LocationData] = {
    LocationName.ANCIENT_LAKE_1: LocationData(1616200),
    LocationName.ANCIENT_LAKE_2: LocationData(1616201),
    LocationName.FOSSIL_CANYON_1: LocationData(1616202),
    LocationName.FOSSIL_CANYON_2: LocationData(1616203),
    LocationName.JUNGLE_FALLS_1: LocationData(1616204),
    LocationName.JUNGLE_FALLS_2: LocationData(1616205),
    LocationName.HOT_TOP_VOLCANO_1: LocationData(1616206),
    LocationName.HOT_TOP_VOLCANO_2: LocationData(1616207),
    LocationName.FIRE_MOUNTAIN_KEY: LocationData(1616208),
    LocationName.FIRE_MOUNTAIN: LocationData(1616209),
    LocationName.TRICKY_2: LocationData(1616210)
}

SNOWFLAKE_MOUNTAIN_LOCATION_TABLE: dict[str, LocationData] = {
    LocationName.EVERFROST_PEAK_1: LocationData(1616300),
    LocationName.EVERFROST_PEAK_2: LocationData(1616301),
    LocationName.WALRUS_COVE_1: LocationData(1616302),
    LocationName.WALRUS_COVE_2: LocationData(1616303),
    LocationName.SNOWBALL_VALLEY_1: LocationData(1616304),
    LocationName.SNOWBALL_VALLEY_2: LocationData(1616305),
    LocationName.FROSTY_VILLAGE_1: LocationData(1616306),
    LocationName.FROSTY_VILLAGE_2: LocationData(1616307),
    LocationName.ICICLE_PYRAMID_KEY: LocationData(1616308),
    LocationName.ICICLE_PYRAMID: LocationData(1616309),
    LocationName.BLUEY_2: LocationData(1616310)
}

SHERBET_ISLAND_LOCATION_TABLE: dict[str, LocationData] = {
    LocationName.WHALE_BAY_1: LocationData(1616400),
    LocationName.WHALE_BAY_2: LocationData(1616401),
    LocationName.CRESCENT_ISLAND_1: LocationData(1616402),
    LocationName.CRESCENT_ISLAND_2: LocationData(1616403),
    LocationName.PIRATE_LAGOON_1: LocationData(1616404),
    LocationName.PIRATE_LAGOON_2: LocationData(1616405),
    LocationName.TREASURE_CAVES_1: LocationData(1616406),
    LocationName.TREASURE_CAVES_2: LocationData(1616407),
    LocationName.DARKWATER_BEACH_KEY: LocationData(1616408),
    LocationName.DARKWATER_BEACH: LocationData(1616409),
    LocationName.BUBBLER_2: LocationData(1616410)
}

DRAGON_FOREST_LOCATION_TABLE: dict[str, LocationData] = {
    LocationName.WINDMILL_PLAINS_1: LocationData(1616500),
    LocationName.WINDMILL_PLAINS_2: LocationData(1616501),
    LocationName.GREENWOOD_VILLAGE_1: LocationData(1616502),
    LocationName.GREENWOOD_VILLAGE_2: LocationData(1616503),
    LocationName.BOULDER_CANYON_1: LocationData(1616504),
    LocationName.BOULDER_CANYON_2: LocationData(1616505),
    LocationName.HAUNTED_WOODS_1: LocationData(1616506),
    LocationName.HAUNTED_WOODS_2: LocationData(1616507),
    LocationName.SMOKEY_CASTLE_KEY: LocationData(1616508),
    LocationName.SMOKEY_CASTLE: LocationData(1616509),
    LocationName.SMOKEY_2: LocationData(1616510)
}

FUTURE_FUN_LAND_LOCATION_TABLE: dict[str, LocationData] = {
    LocationName.SPACEDUST_ALLEY_1: LocationData(1616600),
    LocationName.SPACEDUST_ALLEY_2: LocationData(1616601),
    LocationName.DARKMOON_CAVERNS_1: LocationData(1616602),
    LocationName.DARKMOON_CAVERNS_2: LocationData(1616603),
    LocationName.SPACEPORT_ALPHA_1: LocationData(1616604),
    LocationName.SPACEPORT_ALPHA_2: LocationData(1616605),
    LocationName.STAR_CITY_1: LocationData(1616606),
    LocationName.STAR_CITY_2: LocationData(1616607)
}

ALL_LOCATION_TABLE: dict[str, LocationData] = {
    **TIMBERS_ISLAND_LOCATION_TABLE,
    **DINO_DOMAIN_LOCATION_TABLE,
    **SNOWFLAKE_MOUNTAIN_LOCATION_TABLE,
    **SHERBET_ISLAND_LOCATION_TABLE,
    **DRAGON_FOREST_LOCATION_TABLE,
    **FUTURE_FUN_LAND_LOCATION_TABLE
}
