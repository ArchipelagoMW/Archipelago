from typing import Dict, NamedTuple, Optional
from BaseClasses import Location
from .Constants import YTGV_BASE_ID
from .Names import LocationName, RegionName

class YTGVLocation(Location):
    game = "Yellow Taxi Goes Vroom"

class YTGVLocationData(NamedTuple):
    region: str
    id: Optional[int]

location_data_table: Dict[str, YTGVLocationData] = {
    LocationName.MORIOS_LAB_INTO: YTGVLocationData(
        region = RegionName.MORIOS_LAB,
        id = YTGV_BASE_ID + 0,
    ),
    LocationName.MORIOS_LAB_MARIOS_HOME_PORTAL: YTGVLocationData(
        region = RegionName.MORIOS_LAB,
        id = YTGV_BASE_ID + 1,
    ),
    LocationName.GRANNY: YTGVLocationData(
        region = RegionName.MOON,
        id = None,
    )
}

name_to_id = {
    location_name: location_data.id for location_name, location_data in location_data_table.items()
}
