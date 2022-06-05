import json
from pathlib import Path
from typing import Dict, Set, NamedTuple, List

from BaseClasses import Location, Region


class LocationPositionData(NamedTuple):
    x: float
    y: float
    z: float


class LocationData(NamedTuple):
    name: str
    code: int
    instanceId: str
    itemName: str
    itemQuantity: int
    itemType: int
    sceneId: int
    sceneName: str
    itemNearestExit: str
    chestId: int
    itemContainerName: str
    itemContainerPosition: LocationPositionData


class TunicLocationWrapper (Location):
    game: str = "Tunic"


class TunicLocations:
    _location_table: List[LocationData] = []
    _location_table_lookup: Dict[str, LocationData] = {}

    def _populate_location_table_from_data(self):
        base_path = Path(__file__).parent
        file_path = (base_path / "data/ItemLocations.json").resolve()
        with open(file_path) as file:
            exported_locations = json.load(file)

            for tunic_location in exported_locations:
                curr_location_quantity = 0
                if "itemName" in tunic_location:
                    curr_location_name = f"{tunic_location['itemName']} x {tunic_location['itemQuantity']} " \
                                         f"({tunic_location['itemType']}) [{tunic_location['instanceId']}]"
                    curr_location_quantity = tunic_location['itemQuantity']
                elif 'moneyQuantity' in tunic_location and tunic_location['moneyQuantity'] > 0:
                    curr_location_name = f"{tunic_location['moneyQuantity']}$ " \
                                         f"({tunic_location['itemType']}) [{tunic_location['instanceId']}]"
                    curr_location_quantity = tunic_location['moneyQuantity']
                else:
                    curr_location_name = f"Empty chest " \
                                         f"({tunic_location['itemType']}) [{tunic_location['instanceId']}]"
                curr_location = LocationData(
                    curr_location_name,
                    tunic_location["numericId"],
                    tunic_location["instanceId"],
                    tunic_location["itemName"] if "itemName" in tunic_location else "",
                    curr_location_quantity,
                    tunic_location["itemType"],
                    tunic_location["sceneId"],
                    tunic_location["sceneName"],
                    tunic_location["itemNearestExit"],
                    tunic_location["chestId"],
                    tunic_location["itemContainerName"],
                    LocationPositionData(
                        tunic_location["itemContainerPosition"]["x"],
                        tunic_location["itemContainerPosition"]["y"],
                        tunic_location["itemContainerPosition"]["z"],
                    )
                )
                self._location_table.append(curr_location)
                self._location_table_lookup[curr_location_name] = curr_location

    def _get_location_table(self) -> List[LocationData]:
        if not self._location_table or not self._location_table_lookup:
            self._populate_location_table_from_data()
        return self._location_table

    def _get_location_table_lookup(self) -> Dict[str, LocationData]:
        if not self._location_table or not self._location_table_lookup:
            self._populate_location_table_from_data()
        return self._location_table_lookup

    def get_location_names_per_category(self) -> Dict[str, Set[str]]:
        categories: Dict[str, Set[str]] = {}

        for location in self._get_location_table():
            categories.setdefault(location.itemType, set()).add(location.name)

        return categories

    def generate_location(self, name: str, player: int) -> Location:
        location = self._get_location_table_lookup().get(name)
        return TunicLocationWrapper(player, name, location.code)

    def generate_area_locations(self, area: str, player: int, region: Region) -> [TunicLocationWrapper]:
        if not self._location_table or not self._location_table_lookup:
            self._populate_location_table_from_data()
        ret_value = []
        for tunic_location in self._location_table:
            if tunic_location.sceneName == area:
                ret_value.append((player, tunic_location.name, tunic_location.code, tunic_location.sceneName))
        if ret_value:
            return [TunicLocationWrapper(val[0], val[1], val[2], region) for val in ret_value]
        return []

    def get_location_name_to_code_dict(self) -> Dict[str, int]:
        return {name: location.code for name, location in self._get_location_table_lookup().items()}

    def get_location(self, name: str) -> LocationData:
        return self._get_location_table_lookup()[name]
