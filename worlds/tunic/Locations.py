from pathlib import Path
from typing import Dict, Set, NamedTuple, List
from BaseClasses import Location
import csv


class TunicLocationData:
    id: str
    region_name: str
    scene_name: str
    position: int
    name: str
    code: int


class TunicLocations:
    locations: List[TunicLocationData] = []
    locations_lookup: Dict[str, TunicLocationData] = {}

    def populate_locations(self):
        locations_file_path = (Path(__file__).parent / "data/Locations2.csv").resolve()
        location_id = 3000
        with open(locations_file_path) as location_file:
            csv_file = csv.reader(location_file)
            csv_file.__next__()
            for line in csv_file:
                location: TunicLocationData = TunicLocationData()
                location.id = line[2]
                location.region_name = line[0]
                location.scene_name = line[1]
                location.position = line[3]
                location.name = line[4]
                location.code = len(self.locations) + location_id
                self.locations.append(location)
                self.locations_lookup[line[4]] = location
