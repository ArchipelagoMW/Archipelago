from typing import Dict
from BaseClasses import Location
from .Options import TotalLocations


class NoitaLocation(Location):
    game: str = "Noita"


# 110000 - 110500
item_pickups: Dict[str, int] = {
    f"Chest{i+1}": 110000+i for i in range(TotalLocations.range_end)
}