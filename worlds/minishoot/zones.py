from typing import Dict, List, NamedTuple
import csv

from . import resources

class MinishootZoneData(NamedTuple):
    """Data for a Minishoot zone. Zones are aggregations of regions on a macro level."""
    name: str
    regions: List[str] = []
    locations: List[str] = []

zone_table: Dict[str, MinishootZoneData]={}

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files  # noqa

with files(resources).joinpath('zones.csv').open() as file:
    reader = csv.reader(file)
    for line, row in enumerate(reader):
        if line == 0:
            continue
        zone_data_name = name=row[0]
        zone_data_regions = []
        zone_data_locations = []
        if (row[1] != ''):
            zone_data_regions.extend(row[1].split(','))
        if (row[2] != ''):
            zone_data_locations.extend(row[2].split(','))
        zone_data = MinishootZoneData(zone_data_name, zone_data_regions, zone_data_locations)
        zone_table[zone_data.name] = zone_data
