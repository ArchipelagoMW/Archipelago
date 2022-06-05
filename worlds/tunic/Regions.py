"""
Areas.json:
"sceneName":"Atoll Redux",
"areaExits":[
     {
        "destinationSceneName":"Frog Stairs",
        "destinationLocation":"mouth"
     },
     {
        "destinationSceneName":"Shop",
        "destinationLocation":""
     },
     {
        "destinationSceneName":"Transit",
        "destinationLocation":"teleporter_atoll"
     }
]
Becomes regions: ("Atoll Redux",
    [
        "Go to Frog Stairs_mouth",
        "Go to Shop from Atoll Redux",
        "Go to Transit_teleporter_atoll"
    ])
Becomes connections:
    [
        ("Go to Frog Stairs_mouth", "Frog Stairs"),
        ("Go to Shop from Atoll Redux", "Shop"),
        ("Go to Transit_teleporter_atoll", "Transit"),
    ]
"""
import json
from pathlib import Path
from typing import NamedTuple, List


class TunicArea(NamedTuple):
    name: str
    exits: List[str]


class TunicConnections(NamedTuple):
    exit: str
    destination: str


TUNIC_CONNECTION_PREPEND = "Go to"
TUNIC_CONNECTION_FROM_TEXT_IF_LOCATION_NOT_FOUND = "from"


class TunicRegions:
    _tunic_regions = []
    _tunic_connections = []

    def _populate_region_table_from_data(self):
        base_path = Path(__file__).parent
        file_path = (base_path / "data/Areas.json").resolve()
        with open(file_path) as file:
            exported_region_data = json.load(file)
            for exported_region_item in exported_region_data:
                curr_region_name = exported_region_item["sceneName"]
                curr_region_exits = []
                for exported_exit in exported_region_item["areaExits"]:
                    if "destinationSceneName" in exported_exit:
                        exit_denomination = TUNIC_CONNECTION_PREPEND + " " + exported_exit["destinationSceneName"]
                        if exported_exit["destinationLocation"]:
                            exit_denomination += "_" + exported_exit["destinationLocation"]
                        else:
                            exit_denomination += " " + TUNIC_CONNECTION_FROM_TEXT_IF_LOCATION_NOT_FOUND\
                                                 + " " + curr_region_name
                        curr_region_exits.append(exit_denomination)
                        if "destinationSceneName" in exported_exit:
                            self._tunic_connections.append(TunicConnections(exit_denomination,
                                                                            exported_exit["destinationSceneName"]))
                self._tunic_regions.append(TunicArea(curr_region_name, curr_region_exits))

    def get_tunic_regions(self) -> [TunicArea]:
        if not self._tunic_regions or not self._tunic_connections:
            self._populate_region_table_from_data()
        return self._tunic_regions

    def get_tunic_connections(self) -> [TunicConnections]:
        if not self._tunic_regions or not self._tunic_connections:
            self._populate_region_table_from_data()
        return self._tunic_connections
