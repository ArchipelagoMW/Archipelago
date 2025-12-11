from dataclasses import dataclass


@dataclass
class Event:
    pass


@dataclass
class LocationClearedEvent(Event):
    location_id: int


@dataclass
class MathProblemStarted(Event):
    pass


@dataclass
class MathProblemSolved(Event):
    pass


@dataclass
class VictoryEvent(Event):
    pass


@dataclass
class LocationalEvent(Event):
    x: int
    y: int


@dataclass
class ConfettiFired(LocationalEvent):
    pass
