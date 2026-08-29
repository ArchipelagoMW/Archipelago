from abc import ABC
from dataclasses import dataclass
from typing import ClassVar

from .base import FeatureBase
from ...strings.building_names import Building

progressive_house = "Progressive House"

# This assumes that the farm house is always available, which might not be true forever...
progressive_house_by_upgrade_name = {
    Building.farm_house: 0,
    Building.kitchen: 1,
    Building.kids_room: 2,
    Building.cellar: 3
}


def to_progressive_item(building: str) -> tuple[str, int]:
    """Return the name of the progressive item and its quantity required to unlock the building.
    """
    if building in [Building.coop, Building.barn, Building.shed]:
        return f"Progressive {building}", 1
    elif building.startswith("Big"):
        return f"Progressive {building[building.index(' ') + 1:]}", 2
    elif building.startswith("Deluxe"):
        return f"Progressive {building[building.index(' ') + 1:]}", 3
    elif building in progressive_house_by_upgrade_name:
        return progressive_house, progressive_house_by_upgrade_name[building]

    return building, 1


def to_location_name(building: str) -> str:
    return f"{building} Blueprint"


@dataclass(frozen=True)
class BuildingProgressionFeature(FeatureBase, ABC):
    is_progressive: ClassVar[bool]
    starting_buildings: set[str]

    to_progressive_item = staticmethod(to_progressive_item)
    progressive_house = progressive_house

    to_location_name = staticmethod(to_location_name)


class BuildingProgressionVanilla(BuildingProgressionFeature):
    is_progressive = False


class BuildingProgressionProgressive(BuildingProgressionFeature):
    is_progressive = True
