from typing import Dict

from BaseClasses import Location
from .Options import BlueChestCount

start_id: int = 0xAC0000

l2ac_location_name_to_id: Dict[str, int] = {
    **{f"Blue chest {i + 1}": (start_id + i) for i in range(BlueChestCount.range_end + 7 + 6)},
    **{f"Iris treasure {i + 1}": (start_id + 0x039C + i) for i in range(9)},
    "Boss": start_id + 0x01C2,
}


class L2ACLocation(Location):
    game: str = "Lufia II Ancient Cave"
