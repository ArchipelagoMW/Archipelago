from abc import ABC, abstractmethod
from typing import ClassVar

from .base import FeatureBase
from ...data.game_item import GameItem, ItemTag
from ...strings.seed_names import Seed

location_prefix = "Harvest "


def to_location_name(crop: str) -> str:
    return location_prefix + crop


def to_prog_item_name(seed_name: str) -> str:
    if seed_name == Seed.coffee_starter:
        return Seed.coffee
    return seed_name


def extract_crop_from_location_name(location_name: str) -> str | None:
    if not location_name.startswith(location_prefix):
        return None

    return location_name[len(location_prefix):]


class CropsanityFeature(FeatureBase, ABC):
    is_enabled: ClassVar[bool]

    to_location_name = staticmethod(to_location_name)
    to_prog_item_name = staticmethod(to_prog_item_name)
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
