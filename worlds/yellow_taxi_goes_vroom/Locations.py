from typing import Dict, NamedTuple, Optional
from BaseClasses import Location
from .RegionInfo import region_info_list
from .Constants import YTGV_BASE_ID
from .Names import LocationName, RegionName

class YTGVLocation(Location):
    game = "Yellow Taxi Goes Vroom"

class YTGVLocationData(NamedTuple):
    region: str
    id: Optional[int]
    is_gear: bool = False

def calculate_gear_id(level_id: int, gear_id):
    return YTGV_BASE_ID + (100 * level_id) + gear_id

location_data_table: Dict[str, YTGVLocationData] = {}

for region_info in region_info_list:
    for gear_index, gear_id in enumerate(region_info.gear_ids):
        location_name = f"{region_info.local_area_name} | Gear {gear_index + 1}"
        location_data = YTGVLocationData(
            region = region_info.local_area_name,
            id = calculate_gear_id(region_info.level_id, gear_id),
            is_gear = True,
        )
        location_data_table[location_name] = location_data

location_data_table[LocationName.MUSK] = YTGVLocationData(
    region = RegionName.TOSLA_HQ,
    id = None,
)

location_data_table[LocationName.GRANNY] = YTGVLocationData(
    region = RegionName.MOON,
    id = None,
)

name_to_id = {
    location_name: location_data.id for location_name, location_data in location_data_table.items()
}
