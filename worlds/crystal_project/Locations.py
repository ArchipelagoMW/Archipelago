from typing import List, Optional, Callable, NamedTuple
from BaseClasses import CollectionState

class LocationData(NamedTuple):
    region: str
    name: str
    code: Optional[int]

def get_locations(world: "CrystalProjectWorld") -> List[LocationData]:

    location_table: List[LocationData] = [
        LocationData("Spawning Meadow", "SM - Chest 1", 1)
    ]

    return location_table