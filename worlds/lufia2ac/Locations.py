from typing import Dict

from BaseClasses import Location

start_id: int = 0xAC0000
l2ac_location_name_to_id: Dict[str, int] = {f"Blue chest {i + 1}": (start_id + i) for i in range(88)}


class L2ACLocation(Location):
    game: str = "Lufia II Ancient Cave"
