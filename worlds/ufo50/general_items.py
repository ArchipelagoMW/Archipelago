from typing import Dict, Set

from .constants import game_ids, BASE_ID

cartridge_items: Dict[str, int] = {f"{name} Cartridge": BASE_ID + num for name, num in game_ids.items()
                                   if name != "Main Menu"}
cartridge_item_group: Dict[str, Set[str]] = {"Cartridges": {name for name in cartridge_items.keys()}}
