from typing import Dict, List
from . import data
import csv


class TunicLocationData:
    region: str
    name: str


class TunicLocations:
    locations: List[TunicLocationData] = []
    locations_lookup: Dict[str, TunicLocationData] = {}

    def populate_locations(self):
        from importlib.resources import files
        with files(data).joinpath("Locations.csv").open() as location_file:
            csv_file = csv.reader(location_file)
            csv_file.__next__()
            for line in csv_file:
                location: TunicLocationData = TunicLocationData()
                location.region = line[0]
                location.name = line[1]
                self.locations.append(location)
                self.locations_lookup[line[1]] = location
