from dataclasses import dataclass, field

from .game_item import Source
from ..strings.animal_names import Animal as AnimalName

assert AnimalName


@dataclass(frozen=True)
class Animal:
    name: str
    required_building: str = field(kw_only=True)
    sources: tuple[Source, ...] = field(kw_only=True)


@dataclass(frozen=True)
class IncubatorSource(Source):
    egg_item: str


@dataclass(frozen=True)
class OstrichIncubatorSource(Source):
    egg_item: str
