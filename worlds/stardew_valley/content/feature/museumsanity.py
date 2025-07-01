from abc import ABC
from dataclasses import dataclass
from typing import Tuple, ClassVar

from ...data.game_item import Source, Requirement
from ...data.requirement import MuseumCompletionRequirement


@dataclass(frozen=True)
class MuseumsanityFeature(ABC):
    is_enabled: ClassVar[bool]
    disabled_sources: ClassVar[Tuple[type[Source], ...]] = ()
    disabled_requirements: ClassVar[Tuple[type[Requirement], ...]] = ()


class MuseumsanityNone(MuseumsanityFeature):
    is_enabled = False
    disabled_requirements = (MuseumCompletionRequirement,)


@dataclass(frozen=True)
class MuseumsanityMilestones(MuseumsanityFeature):
    is_enabled = True


@dataclass(frozen=True)
class MuseumsanityRandomized(MuseumsanityFeature):
    is_enabled = True


@dataclass(frozen=True)
class MuseumsanityAll(MuseumsanityFeature):
    is_enabled = True
