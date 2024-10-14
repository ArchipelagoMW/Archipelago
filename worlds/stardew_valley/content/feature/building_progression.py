from abc import ABC
from dataclasses import dataclass
from typing import ClassVar, Set


@dataclass(frozen=True)
class BuildingProgressionFeature(ABC):
    is_progressive: ClassVar[bool]
    starting_buildings: Set[str]
    price_multiplier: float = 1.0


class BuildingProgressionVanilla(BuildingProgressionFeature):
    is_progressive = False


class BuildingProgressionProgressive(BuildingProgressionFeature):
    is_progressive = True
