from typing import Optional, List, NamedTuple
from .enums import MAIN_MENU_STRING, WORLD_2_STRING, WorldName, LocationName


class Spelunky2RegionData(NamedTuple):
    exits: Optional[List[str]] = None


region_data_table = {
    # Primary Regions
    MAIN_MENU_STRING: Spelunky2RegionData([WorldName.DWELLING]),  # Add connections to Olmec's Lair and Ice Caves when shortcuts are added # noqa: E128
    WorldName.DWELLING.value: Spelunky2RegionData([WorldName.JUNGLE.value, WorldName.VOLCANA.value, WORLD_2_STRING,]),
    WorldName.JUNGLE.value: Spelunky2RegionData([WorldName.OLMECS_LAIR.value, LocationName.BLACK_MARKET]),
    WorldName.VOLCANA.value: Spelunky2RegionData([WorldName.OLMECS_LAIR.value, LocationName.VLADS_CASTLE]),
    WorldName.OLMECS_LAIR.value: Spelunky2RegionData([WorldName.TIDE_POOL.value, WorldName.TEMPLE]),
    WorldName.TIDE_POOL.value: Spelunky2RegionData([WorldName.ICE_CAVES.value, LocationName.ABZU]),
    WorldName.TEMPLE.value: Spelunky2RegionData([WorldName.ICE_CAVES.value, LocationName.CITY_OF_GOLD]),
    WorldName.ICE_CAVES.value: Spelunky2RegionData([WorldName.NEO_BABYLON.value, LocationName.MOTHERSHIP]),
    WorldName.NEO_BABYLON.value: Spelunky2RegionData([WorldName.SUNKEN_CITY]),
    WorldName.SUNKEN_CITY.value: Spelunky2RegionData([WorldName.COSMIC_OCEAN.value, WorldName.EGGPLANT]),
    WorldName.COSMIC_OCEAN.value: Spelunky2RegionData(),

    # Secondary Regions
    WORLD_2_STRING:       Spelunky2RegionData(),
    LocationName.BLACK_MARKET.value:   Spelunky2RegionData(),
    LocationName.VLADS_CASTLE.value:   Spelunky2RegionData(),
    LocationName.ABZU.value:           Spelunky2RegionData(),
    LocationName.CITY_OF_GOLD.value:   Spelunky2RegionData([LocationName.DUAT]),
    LocationName.DUAT.value:           Spelunky2RegionData(),
    LocationName.MOTHERSHIP.value:     Spelunky2RegionData(),
    WorldName.EGGPLANT.value:          Spelunky2RegionData(),
}
