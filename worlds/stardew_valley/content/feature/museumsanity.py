from abc import ABC
from dataclasses import dataclass
from typing import ClassVar

from .base import FeatureBase
from ...data.requirement import MuseumCompletionRequirement


@dataclass(frozen=True)
class MuseumsanityFeature(FeatureBase, ABC):
    is_enabled: ClassVar[bool]


class MuseumsanityNone(MuseumsanityFeature):
    is_enabled = False

    @staticmethod
    def _disable_museum_completion_requirement(requirement: MuseumCompletionRequirement) -> bool:
        return True


@dataclass(frozen=True)
class MuseumsanityMilestones(MuseumsanityFeature):
    is_enabled = True


@dataclass(frozen=True)
class MuseumsanityRandomized(MuseumsanityFeature):
    is_enabled = True
    amount_of_randomized_donations: int = 40

    def _disable_museum_completion_requirement(self, requirement: MuseumCompletionRequirement) -> bool:
        return requirement.number_donated > self.amount_of_randomized_donations


@dataclass(frozen=True)
class MuseumsanityAll(MuseumsanityFeature):
    is_enabled = True
