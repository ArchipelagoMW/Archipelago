import csv
from typing import Dict, NamedTuple

from . import resources

from worlds.minishoot.pool import MinishootPool, get_item_pool

class MinishootLocationData(NamedTuple):
    name: str
    vanilla_item_name: str
    pool: MinishootPool
    region: str
    logic_rule: str

# Chosen completely arbitrarily. Is there a better way to do this?
location_base_id = 519346400

location_table: Dict[str, MinishootLocationData] = {}
location_name_to_id: Dict[str, int] = {}

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files  # noqa

with files(resources).joinpath('locations.csv').open() as file:
    reader = csv.reader(file)
    for line, row in enumerate(reader):
        if line == 0:
            continue
        location_data = MinishootLocationData(
            name=row[0],
            vanilla_item_name=row[1],
            pool=get_item_pool(row[2]),
            region=row[3],
            logic_rule=row[4]
        )
        location_table[location_data.name] = location_data
        location_name_to_id[location_data.name] = location_base_id + line
