from dataclasses import dataclass, field

Event = tuple[int, str, str]


@dataclass
class Goals:
    """ choices made for objective rando """
    objectives: list[Event] = field(default_factory=list)
    map_station_order: list[int] = field(default_factory=list)
