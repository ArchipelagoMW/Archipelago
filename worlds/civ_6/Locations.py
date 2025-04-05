from collections import defaultdict
from dataclasses import dataclass
from typing import Optional, Dict
from BaseClasses import Location, Region

from .Data import get_boosts_data, get_new_civics_data, get_new_techs_data

from .Enum import CivVICheckType, EraType

CIV_VI_AP_LOCATION_ID_BASE = 5041000

# Locs that should not have progression items
GOODY_HUT_LOCATION_NAMES = [
    "GOODY_HUT_1",
    "GOODY_HUT_2",
    "GOODY_HUT_3",
    "GOODY_HUT_4",
    "GOODY_HUT_5",
    "GOODY_HUT_6",
    "GOODY_HUT_7",
    "GOODY_HUT_8",
    "GOODY_HUT_9",
    "GOODY_HUT_10",
]


@dataclass
class CivVILocationData:
    name: str
    cost: int
    uiTreeRow: int
    civ_id: int
    era_type: str
    location_type: CivVICheckType

    game: str = "Civilization VI"

    @property
    def code(self):
        return self.civ_id + CIV_VI_AP_LOCATION_ID_BASE


class CivVILocation(Location):
    game: str = "Civilization VI"
    location_type: CivVICheckType

    def __init__(
        self,
        player: int,
        name: str = "",
        address: Optional[int] = None,
        parent: Optional[Region] = None,
    ):
        super().__init__(player, name, address, parent)
        category = name.split("_")[0]
        if "victory" in category:
            self.location_type = CivVICheckType.EVENT
        else:
            self.location_type = CivVICheckType(category)


def generate_flat_location_table() -> Dict[str, CivVILocationData]:
    """
    Generates a flat location table in the following format:
    {
      "TECH_AP_ANCIENT_00": CivVILocationData,
      "TECH_AP_ANCIENT_01": CivVILocationData,
      "CIVIC_AP_ANCIENT_00": CivVILocationData,
      ...
    }
    """
    era_locations = generate_era_location_table()
    flat_locations: Dict[str, CivVILocationData] = {}
    for locations in era_locations.values():
        for location_id, location_data in locations.items():
            flat_locations[location_id] = location_data
    return flat_locations


def generate_era_location_table() -> Dict[str, Dict[str, CivVILocationData]]:
    """
    Uses the data from existing_tech.json to generate a location table in the following format:
    {
      "ERA_ANCIENT": {
        "TECH_AP_ANCIENT_00": CivVILocationData,
        "TECH_AP_ANCIENT_01": CivVILocationData,
        "CIVIC_AP_ANCIENT_00": CivVILocationData,
      },
      ...
    }
    """

    new_techs = get_new_techs_data()
    era_locations: Dict[str, Dict[str, CivVILocationData]] = defaultdict(dict)
    id_base = 0
    # Techs
    for data in new_techs:
        era_type = data["EraType"]
        era_locations[era_type][data["Type"]] = CivVILocationData(
            data["Type"],
            data["Cost"],
            data["UITreeRow"],
            id_base,
            era_type,
            CivVICheckType.TECH,
        )
        id_base += 1
    # Civics
    new_civics = get_new_civics_data()

    for data in new_civics:
        era_type = data["EraType"]
        era_locations[era_type][data["Type"]] = CivVILocationData(
            data["Type"],
            data["Cost"],
            data["UITreeRow"],
            id_base,
            era_type,
            CivVICheckType.CIVIC,
        )
        id_base += 1

    # Eras
    for era in EraType:

        if era == EraType.ERA_ANCIENT:
            continue

        era_locations[era.name][era.name] = CivVILocationData(
            era.name, 0, 0, id_base, era.name, CivVICheckType.ERA
        )
        id_base += 1

    # Goody Huts, defaults to 10 goody huts as location checks (rarely will a player get more than this)
    for i in range(10):
        era_locations[EraType.ERA_ANCIENT.value]["GOODY_HUT_" + str(i + 1)] = (
            CivVILocationData(
                "GOODY_HUT_" + str(i + 1),
                0,
                0,
                id_base,
                EraType.ERA_ANCIENT.value,
                CivVICheckType.GOODY,
            )
        )
        id_base += 1
    # Boosts
    boosts = get_boosts_data()
    for boost in boosts:
        location = CivVILocationData(
            boost.Type, 0, 0, id_base, boost.EraType, CivVICheckType.BOOST
        )
        era_locations["ERA_ANCIENT"][boost.Type] = location
        id_base += 1

    return era_locations
