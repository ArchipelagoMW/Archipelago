from __future__ import annotations
from typing import Callable, Dict, List, NamedTuple, TYPE_CHECKING

from BaseClasses import CollectionState
from .Names import RegionName, ItemName
from . import Locations

if TYPE_CHECKING:
    from . import YTGVWorld

class YTGVRegionData(NamedTuple):
    exits: List[str] = []
    rules: Dict[str, Callable[[CollectionState], bool]] = {}

def create_region_data_table(world: YTGVWorld) -> Dict[str, YTGVRegionData]:
    return {
        RegionName.MENU: YTGVRegionData([
            RegionName.MORIOS_LAB,
            # Only true in the intro of the game
            # RegionName.grannys_island
        ]),
        RegionName.MORIOS_LAB: YTGVRegionData(
            exits = [
                RegionName.GRANNYS_ISLAND,
                RegionName.TOSLA_HQ,
            ],
            rules = {
                RegionName.TOSLA_HQ: lambda state: state.has(ItemName.GEAR, world.player, 2)
            },
        ),
        RegionName.GRANNYS_ISLAND: YTGVRegionData([
            RegionName.MORIOS_LAB,
        ]),
        RegionName.TOSLA_HQ: YTGVRegionData([
            RegionName.MORIOS_LAB,
            RegionName.MOON,
        ]),
        RegionName.MOON: YTGVRegionData([
            RegionName.MORIOS_LAB
        ])
    }

region_name_to_locations = {}

for location_name, location_data in Locations.location_data_table.items():
    items = region_name_to_locations.setdefault(location_data.region, {})
    items[location_name] = location_data.id

from pprint import pprint
print("##### DEBUG: region_name_to_locations:")
pprint(region_name_to_locations)