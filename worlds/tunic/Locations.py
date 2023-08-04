from pathlib import Path
from typing import Dict, List
import csv


class TunicLocationData:
    region: str
    name: str


class TunicLocations:
    locations: List[TunicLocationData] = []
    locations_lookup: Dict[str, TunicLocationData] = {}

    def populate_locations(self):
        locations_file_path = (Path(__file__).parent / "data/Locations.csv").resolve()
        with open(locations_file_path) as location_file:
            csv_file = csv.reader(location_file)
            csv_file.__next__()
            for line in csv_file:
                location: TunicLocationData = TunicLocationData()
                location.region = line[0]
                location.name = line[1]
                self.locations.append(location)
                self.locations_lookup[line[1]] = location
