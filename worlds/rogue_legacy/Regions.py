from typing import Callable, Dict, List, NamedTuple

from BaseClasses import CollectionState
from .Rules import can_open_door, has_defeated_castle, has_defeated_forest, has_defeated_tower, \
    has_fairy_progression, has_upgrades_percentage

__all__ = ["RLRegionData", "region_table"]


class RLRegionData(NamedTuple):
    exits: List[str] = []
    rules: Callable[[CollectionState, int], bool] = lambda state, player: True


region_table: Dict[str, RLRegionData] = {
    # Start
    "Menu":                 RLRegionData(
        exits=["Manor - Tier 1", "Castle Hamson"],
    ),

    # Manor Renovation
    "Manor - Tier 1":       RLRegionData(
        exits=["Manor - Tier 2"],
    ),
    "Manor - Tier 2":       RLRegionData(
        exits=["Manor - Tier 3"],
        rules=lambda state, player: state.can_reach("Forest Abkhazia", "Region", player),
    ),
    "Manor - Tier 3":       RLRegionData(
        exits=["Manor - Tier 4"],
        rules=lambda state, player: state.can_reach("The Maya", "Region", player),
    ),
    "Manor - Tier 4":       RLRegionData(
        rules=lambda state, player: state.can_reach("The Land of Darkness", "Region", player),
    ),

    # Castle Hamson Zones
    "Castle Hamson":        RLRegionData(
        exits=[
            "Forest Abkhazia",
            "The Maya",
            "The Land of Darkness",
            "The Fountain Room",
            "Castle Fairy Chests",
            "Cheapskate Elf",
            "The Secret Room",
        ],
    ),
    "Forest Abkhazia":      RLRegionData(
        exits=["Forest Fairy Chests"],
        rules=lambda state, player: has_upgrades_percentage(state, player, 15) and has_defeated_castle(state, player),
    ),
    "The Maya":             RLRegionData(
        exits=["Tower Fairy Chests"],
        rules=lambda state, player: has_upgrades_percentage(state, player, 30) and has_defeated_forest(state, player),
    ),
    "The Land of Darkness": RLRegionData(
        exits=["Dungeon Fairy Chests"],
        rules=lambda state, player: has_upgrades_percentage(state, player, 45) and has_defeated_tower(state, player),
    ),
    "The Fountain Room":    RLRegionData(
        rules=lambda state, player: has_upgrades_percentage(state, player, 60) and can_open_door(state, player),
    ),

    # Fairy Chests
    "Castle Fairy Chests":  RLRegionData(
        rules=lambda state, player: has_fairy_progression(state, player),
    ),
    "Forest Fairy Chests":  RLRegionData(
        rules=lambda state, player: has_fairy_progression(state, player),
    ),
    "Tower Fairy Chests":   RLRegionData(
        rules=lambda state, player: has_fairy_progression(state, player),
    ),
    "Dungeon Fairy Chests": RLRegionData(
        rules=lambda state, player: has_fairy_progression(state, player),
    ),

    # Special Areas
    "Cheapskate Elf":       RLRegionData(
        rules=lambda state, player: state.has("Nerdy Glasses Shrine", player),
    ),
    "The Secret Room":      RLRegionData(
        rules=lambda state, player: state.has("Calypso's Compass Shrine", player),
    ),
}
