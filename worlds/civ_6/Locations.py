from typing import List, Optional, Dict, Union
from BaseClasses import Location, LocationProgressType, Region

from .Data import CivicPrereqData, TechPrereqData, get_boosts_data, get_new_civics_data, get_new_techs_data

from .Enum import CivVICheckType, EraType

CIV_VI_AP_LOCATION_ID_BASE = 5041000

# Locs that should not have progression items
EXCLUDED_LOCATIONS = [
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


class CivVILocationData:
    game: str = "Civilization VI"
    name: str
    cost: int
    uiTreeRow: int
    civ_id: int
    code: int
    era_type: str
    location_type: CivVICheckType
    pre_reqs: Optional[List[Union[CivicPrereqData, TechPrereqData]]]

    def __init__(self, name: str, cost: int, uiTreeRow: int, id: int, era_type: str, location_type: CivVICheckType):
        self.name = name
        self.cost = cost
        self.uiTreeRow = uiTreeRow
        self.civ_id = id
        self.code = id + CIV_VI_AP_LOCATION_ID_BASE
        self.era_type = era_type
        self.location_type = location_type


class CivVILocation(Location):
    game: str = "Civilization VI"
    location_type: CivVICheckType

    def __init__(self, player: int, name: str = "", address: Optional[int] = None, parent: Optional[Region] = None):
        super().__init__(player, name, address, parent)
        if name.split("_")[0] == "TECH":
            self.location_type = CivVICheckType.TECH
        elif name.split("_")[0] == "CIVIC":
            self.location_type = CivVICheckType.CIVIC
        elif name.split("_")[0] == "ERA":
            self.location_type = CivVICheckType.ERA
        elif name.split("_")[0] == "GOODY":
            self.location_type = CivVICheckType.GOODY
        elif name.split("_")[0] == "BOOST":
            self.location_type = CivVICheckType.BOOST
        else:
            self.location_type = CivVICheckType.EVENT

        if self.name in EXCLUDED_LOCATIONS:
            self.progress_type = LocationProgressType.EXCLUDED

        if self.location_type == CivVICheckType.BOOST:
            boost_data_list = get_boosts_data()
            boost_data = next((boost for boost in boost_data_list if boost.Type == name), None)
            if boost_data and boost_data.Classification == "EXCLUDED":
                self.progress_type = LocationProgressType.EXCLUDED


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
    era_locations: Dict[str, Dict[str, CivVILocationData]] = {}
    id_base = 0
# Techs
    for data in new_techs:
        era_type = data["EraType"]
        if era_type not in era_locations:
            era_locations[era_type] = {}

        era_locations[era_type][data["Type"]] = CivVILocationData(
            data["Type"], data["Cost"], data["UITreeRow"], id_base, era_type, CivVICheckType.TECH)
        id_base += 1
# Civics
    new_civics = get_new_civics_data()

    for data in new_civics:
        era_type = data["EraType"]
        if era_type not in era_locations:
            era_locations[era_type] = {}
        era_locations[era_type][data["Type"]] = CivVILocationData(
            data["Type"], data["Cost"], data["UITreeRow"], id_base, era_type, CivVICheckType.CIVIC)
        id_base += 1

# Eras
    eras = list(EraType)
    for i in range(len(EraType)):
        location_era = eras[i].name

        if location_era == "ERA_ANCIENT":
            continue

        era_locations[location_era][location_era] = CivVILocationData(
            location_era, 0, 0, id_base, location_era, CivVICheckType.ERA)
        id_base += 1
# Goody Huts, defaults to 10 goody huts as location checks (rarely will a player get more than this)
    for i in range(10):
        era_locations[EraType.ERA_ANCIENT.value]["GOODY_HUT_" + str(i + 1)] = CivVILocationData(
            "GOODY_HUT_" + str(i + 1), 0, 0, id_base, EraType.ERA_ANCIENT.value, CivVICheckType.GOODY)
        id_base += 1
# Boosts
    boosts = get_boosts_data()
    for boost in boosts:
        location = CivVILocationData(
            boost.Type, 0, 0, id_base, boost.EraType, CivVICheckType.BOOST)
        era_locations["ERA_ANCIENT"][boost.Type] = location
        id_base += 1

    return era_locations
