from typing import Dict, List, NamedTuple, Optional

from BaseClasses import Location

start_id: int = 0xAC0000


class L2ACLocation(Location):
    game: str = "Lufia II Ancient Cave"


class LocationData(NamedTuple):
    region: str
    name: str
    code: Optional[int]


l2ac_location_table: List[LocationData] = [
    LocationData("AncientDungeon", f"Blue chest {i + 1}", i) for i in range(256)
]

l2ac_location_name_to_id: Dict[str, int] = {location.name: start_id + location.code for location in l2ac_location_table}
