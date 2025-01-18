from abc import ABC, abstractmethod
from typing import ClassVar, Optional

from ...data.game_item import GameItem, ItemTag

location_prefix = "Harvest "


def to_location_name(crop: str) -> str:
    return location_prefix + crop


def extract_crop_from_location_name(location_name: str) -> Optional[str]:
    if not location_name.startswith(location_prefix):
        return None

    return location_name[len(location_prefix):]


class CropsanityFeature(ABC):
    is_enabled: ClassVar[bool]

    to_location_name = staticmethod(to_location_name)
    extract_crop_from_location_name = staticmethod(extract_crop_from_location_name)

    @abstractmethod
    def is_included(self, crop: GameItem) -> bool:
        ...


class CropsanityDisabled(CropsanityFeature):
    is_enabled = False

    def is_included(self, crop: GameItem) -> bool:
        return False


class CropsanityEnabled(CropsanityFeature):
    is_enabled = True

    def is_included(self, crop: GameItem) -> bool:
        return ItemTag.CROPSANITY_SEED in crop.tags
