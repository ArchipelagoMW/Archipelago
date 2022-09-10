from typing import Dict
from BaseClasses import Location
from .Options import TotalLocations


class RiskOfRainLocation(Location):
    game: str = "Risk of Rain 2"


# 38006 - 38506
item_pickups: Dict[str, int] = {
    f"ItemPickup{i+1}": 38000+i for i in range(TotalLocations.range_end)
}
