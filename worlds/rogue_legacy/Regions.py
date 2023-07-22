from typing import Callable, Dict, List, NamedTuple

from BaseClasses import CollectionState
from .Rules import can_access_secret_room, can_afford_tier2, can_afford_tier3, can_afford_tier4, \
    can_cheat_cheapskate_elf, can_open_door, has_defeated_castle, has_defeated_forest, has_defeated_tower, \
    has_fairy_progression

__all__ = ["RegionExit", "region_table"]


class RegionExit(NamedTuple):
    region: str
    access_rule: Callable[[CollectionState, int], bool] = lambda state, player: True


region_table: Dict[str, List[RegionExit]] = {
    # Start
    "Menu": [RegionExit("Manor - Tier 1"), RegionExit("Castle Hamson")],

    # Manor Renovation
    "Manor - Tier 1": [RegionExit("Manor - Tier 2", can_afford_tier2)],
    "Manor - Tier 2": [RegionExit("Manor - Tier 3", can_afford_tier3)],
    "Manor - Tier 3": [RegionExit("Manor - Tier 4", can_afford_tier4)],
    "Manor - Tier 4": [],

    # Main Zones
    "Castle Hamson": [
        RegionExit("Forest Abkhazia", has_defeated_castle),
        RegionExit("The Maya", has_defeated_forest),
        RegionExit("The Land of Darkness", has_defeated_tower),
        RegionExit("The Fountain Room", can_open_door),
        RegionExit("Castle Fairy Chests", has_fairy_progression),
        RegionExit("Cheapskate Elf", can_cheat_cheapskate_elf),
        RegionExit("The Secret Room", can_access_secret_room),
    ],
    "Forest Abkhazia": [RegionExit("Forest Fairy Chests", has_fairy_progression)],
    "The Maya": [RegionExit("Tower Fairy Chests", has_fairy_progression)],
    "The Land of Darkness": [RegionExit("Dungeon Fairy Chests", has_fairy_progression)],
    "The Fountain Room": [],

    # Fairy Chests
    "Castle Fairy Chests": [],
    "Forest Fairy Chests": [],
    "Tower Fairy Chests": [],
    "Dungeon Fairy Chests": [],

    # Special Areas
    "Cheapskate Elf": [],
    "The Secret Room": [],
}
