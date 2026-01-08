import csv
from typing import Dict, List, NamedTuple

from . import resources

class MinishootRegionData(NamedTuple):
    name: str
    locations: List[str]
    outgoing_transitions: List[str]
    ingoing_transitions: List[str]

region_table: Dict[str, MinishootRegionData]={}

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files  # noqa

with files(resources).joinpath('regions.csv').open() as file:
    reader = csv.reader(file)
    for line, row in enumerate(reader):
        if line == 0:
            continue
        region_data = MinishootRegionData(
            name=row[0],
            locations=row[1].split(','),
            outgoing_transitions=row[2].split(','),
            ingoing_transitions=row[3].split(',')
        )
        region_table[region_data.name] = region_data
