from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar

from .base import FeatureBase
from ...data.fish_data import FishItem
from ...strings.fish_names import Fish

location_prefix = "Fishsanity: "


def to_location_name(fish: str) -> str:
    return location_prefix + fish


def extract_fish_from_location_name(location_name: str) -> str | None:
    if not location_name.startswith(location_prefix):
        return None

    return location_name[len(location_prefix):]


@dataclass(frozen=True)
class FishsanityFeature(FeatureBase, ABC):
    is_enabled: ClassVar[bool]

    randomization_ratio: float = 1

    to_location_name = staticmethod(to_location_name)
    extract_fish_from_location_name = staticmethod(extract_fish_from_location_name)

    @property
    def is_randomized(self) -> bool:
        return self.randomization_ratio != 1

    @abstractmethod
    def is_included(self, fish: FishItem) -> bool:
        ...


class FishsanityNone(FishsanityFeature):
    is_enabled = False

    def is_included(self, fish: FishItem) -> bool:
        return False


class FishsanityLegendaries(FishsanityFeature):
    is_enabled = True

    def is_included(self, fish: FishItem) -> bool:
        return fish.legendary


class FishsanitySpecial(FishsanityFeature):
    is_enabled = True

    included_fishes = {
        Fish.angler,
        Fish.crimsonfish,
        Fish.glacierfish,
        Fish.legend,
        Fish.mutant_carp,
        Fish.blobfish,
        Fish.lava_eel,
        Fish.octopus,
        Fish.scorpion_carp,
        Fish.ice_pip,
        Fish.super_cucumber,
        Fish.dorado
    }

    def is_included(self, fish: FishItem) -> bool:
        return fish.name in self.included_fishes


class FishsanityAll(FishsanityFeature):
    is_enabled = True

    def is_included(self, fish: FishItem) -> bool:
        return True


class FishsanityExcludeLegendaries(FishsanityFeature):
    is_enabled = True

    def is_included(self, fish: FishItem) -> bool:
        return not fish.legendary


class FishsanityExcludeHardFish(FishsanityFeature):
    is_enabled = True

    def is_included(self, fish: FishItem) -> bool:
        return fish.difficulty < 80


class FishsanityOnlyEasyFish(FishsanityFeature):
    is_enabled = True

    def is_included(self, fish: FishItem) -> bool:
        return fish.difficulty < 50
