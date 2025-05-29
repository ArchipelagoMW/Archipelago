from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Optional

from ...data.hats_data import HatItem, HatDifficulty

location_prefix = "Wear "


def to_location_name(hat: str) -> str:
    return location_prefix + hat


def extract_hat_from_location_name(location_name: str) -> Optional[str]:
    if not location_name.startswith(location_prefix):
        return None

    return location_name[len(location_prefix):]


@dataclass(frozen=True)
class HatsanityFeature(ABC):
    is_enabled: ClassVar[bool]

    to_location_name = staticmethod(to_location_name)
    extract_hat_from_location_name = staticmethod(extract_hat_from_location_name)

    @abstractmethod
    def is_included(self, hat: HatItem) -> bool:
        ...


class HatsanityNone(HatsanityFeature):
    is_enabled = False

    def is_included(self, hat: HatItem) -> bool:
        return False


class HatsanityEasy(HatsanityFeature):
    is_enabled = True

    def is_included(self, hat: HatItem) -> bool:
        return hat.difficulty == HatDifficulty.easy


class HatsanityTailoring(HatsanityFeature):
    is_enabled = True

    def is_included(self, hat: HatItem) -> bool:
        return hat.difficulty == HatDifficulty.tailoring


class HatsanityEasyTailoring(HatsanityFeature):
    is_enabled = True

    def is_included(self, hat: HatItem) -> bool:
        return hat.difficulty < HatDifficulty.medium


class HatsanityMedium(HatsanityFeature):
    is_enabled = True

    def is_included(self, hat: HatItem) -> bool:
        return hat.difficulty <= HatDifficulty.medium


class HatsanityDifficult(HatsanityFeature):
    is_enabled = True

    def is_included(self, hat: HatItem) -> bool:
        return hat.difficulty <= HatDifficulty.difficult_or_rng


class HatsanityNearPerfection(HatsanityFeature):
    is_enabled = True

    def is_included(self, hat: HatItem) -> bool:
        return hat.difficulty <= HatDifficulty.near_perfection


class HatsanityPostPerfection(HatsanityFeature):
    is_enabled = True

    def is_included(self, hat: HatItem) -> bool:
        return hat.difficulty <= HatDifficulty.post_perfection
