from abc import ABC
from dataclasses import dataclass
from typing import ClassVar

from ...strings.building_names import Building
from .base import FeatureBase

progressive_house = "Progressive House"

# Even if you start with the farmhouse, we keep all the logic and code the same. We just place one farmhouse in your start inventory. it's much simpler this way.
progressive_house_by_upgrade_name = {
    Building.farm_house: 1,
    Building.kitchen: 2,
    Building.kids_room: 3,
    Building.cellar: 4,
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
