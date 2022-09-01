from typing import Dict
from BaseClasses import Location
from .Options import TotalLocations


class RiskOfRainLocation(Location):
    game: str = "Risk of Rain 2"


# 37006 - 37506
item_pickups: Dict[str, int] = {
    f"ItemPickup{i+1}": 37000+i for i in range(TotalLocations.range_end)
}
