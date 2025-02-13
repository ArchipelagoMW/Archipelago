from typing import Dict, NamedTuple, Optional

from BaseClasses import Location
from .Names import LocationName


celeste_base_id: int = 0xCA1000


class CelesteLocation(Location):
    game = "Celeste"


class CelesteLocationData(NamedTuple):
    region: str
    address: Optional[int] = None


strawberry_location_data_table: Dict[str, CelesteLocationData] = {
    LocationName.strawberry_1:  CelesteLocationData("Forsaken City", celeste_base_id + 0x00),
}

location_data_table: Dict[str, CelesteLocationData] = {**strawberry_location_data_table}

location_table = {name: data.address for name, data in location_data_table.items() if data.address is not None}
