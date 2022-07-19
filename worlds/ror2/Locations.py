from typing import Dict
from BaseClasses import Location
from .Options import TotalLocations


class RiskOfRainLocation(Location):
    game: str = "Risk of Rain 2"


# 37000 - 38000
base_location_table = {
    "Victory": None,
}
# 37006 - 37506
item_pickups = {
    f"ItemPickup{i+1}": 37000+i for i in range(TotalLocations.range_end)
}

location_table = {**base_location_table, **item_pickups}

lookup_id_to_name: Dict[int, str] = {id: name for name, id in location_table.items()}
