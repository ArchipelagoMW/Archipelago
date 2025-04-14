from typing import List, Optional, Callable, NamedTuple
from BaseClasses import CollectionState
from .Options import CrystalProjectOptions

EventId: Optional[int] = None


class LocationData(NamedTuple):
    region: str
    name: str
    code: Optional[int]
    rule: Optional[Callable[[CollectionState], bool]] = None


def get_location_datas(player: Optional[int], options: Optional[CrystalProjectOptions]) -> List[LocationData]:

    # 1337000 - 1337155 Generic locations
    # 1337171 - 1337175 New Pickup checks
    # 1337246 - 1337249 Ancient Pyramid
    location_table: List[LocationData] = [
        # Present item locations
        LocationData('Spawning Meadow', 'Spawning Meadow First Chest',  0)
        ]
 
    return location_table
