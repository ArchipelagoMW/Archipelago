from typing import Optional, Dict

from BaseClasses import Location

from .Constants import *


class SavingPrincessLocation(Location):
    game: str = GAME_NAME


class LocData:
    code: Optional[int]

    def __init__(self, code: Optional[int] = None):
        if code is not None:
            self.code = code + BASE_ID
        else:
            self.code = None


location_dict_base: Dict[str, LocData] = {
    LOCATION_CAVE_AMMO:         LocData(0),
    LOCATION_CAVE_RELOAD:       LocData(1),
    LOCATION_CAVE_HEALTH:       LocData(2),
    LOCATION_CAVE_WEAPON:       LocData(3),
    LOCATION_VOLCANIC_RELOAD:   LocData(4),
    LOCATION_VOLCANIC_HEALTH:   LocData(5),
    LOCATION_VOLCANIC_AMMO:     LocData(6),
    LOCATION_VOLCANIC_WEAPON:   LocData(7),
    LOCATION_ARCTIC_AMMO:       LocData(8),
    LOCATION_ARCTIC_RELOAD:     LocData(9),
    LOCATION_ARCTIC_HEALTH:     LocData(10),
    LOCATION_ARCTIC_WEAPON:     LocData(11),
    LOCATION_JACKET:            LocData(12),
    LOCATION_HUB_AMMO:          LocData(13),
    LOCATION_HUB_HEALTH:        LocData(14),
    LOCATION_HUB_RELOAD:        LocData(15),
    LOCATION_SWAMP_AMMO:        LocData(16),
    LOCATION_SWAMP_HEALTH:      LocData(17),
    LOCATION_SWAMP_RELOAD:      LocData(18),
    LOCATION_SWAMP_SPECIAL:     LocData(19),
    LOCATION_ELECTRICAL_RELOAD: LocData(20),
    LOCATION_ELECTRICAL_HEALTH: LocData(21),
    LOCATION_ELECTRICAL_AMMO:   LocData(22),
    LOCATION_ELECTRICAL_WEAPON: LocData(23),
}

location_dict_expanded: Dict[str, LocData] = {
    **location_dict_base,
    EP_LOCATION_CAVE_MINIBOSS:          LocData(24),
    EP_LOCATION_CAVE_BOSS:              LocData(25),
    EP_LOCATION_VOLCANIC_BOSS:          LocData(26),
    EP_LOCATION_ARCTIC_BOSS:            LocData(27),
    EP_LOCATION_HUB_CONSOLE:            LocData(28),
    EP_LOCATION_HUB_NINJA_SCARE:        LocData(29),
    EP_LOCATION_SWAMP_BOSS:             LocData(30),
    EP_LOCATION_ELEVATOR_NINJA_FIGHT:   LocData(31),
    EP_LOCATION_ELECTRICAL_EXTRA:       LocData(32),
    EP_LOCATION_ELECTRICAL_MINIBOSS:    LocData(33),
    EP_LOCATION_ELECTRICAL_BOSS:        LocData(34),
    EP_LOCATION_ELECTRICAL_FINAL_BOSS:  LocData(35),
}

location_dict_event_expanded: Dict[str, LocData] = {
    EVENT_LOCATION_VICTORY: LocData(),
}

# most event locations are only relevant without expanded pool
location_dict_events: Dict[str, LocData] = {
    EVENT_LOCATION_GUARD_GONE:      LocData(),
    EVENT_LOCATION_CLIFF_GONE:      LocData(),
    EVENT_LOCATION_ACE_GONE:        LocData(),
    EVENT_LOCATION_SNAKE_GONE:      LocData(),
    EVENT_LOCATION_POWER_ON:        LocData(),
    **location_dict_event_expanded,
}

location_dict: Dict[str, LocData] = {
    **location_dict_expanded,
    **location_dict_events,
}
