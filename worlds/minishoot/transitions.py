import csv
from typing import Dict, NamedTuple

from . import resources

class MinishootTransitionData(NamedTuple):
    name: str
    origin: str
    destination: str
    logic_rule: str

transition_table: Dict[str, MinishootTransitionData]={}

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files  # noqa

with files(resources).joinpath('transitions.csv').open() as file:
    reader = csv.reader(file)
    for line, row in enumerate(reader):
        if line == 0:
            continue
        transition_data = MinishootTransitionData(
            name=row[0],
            origin=row[1],
            destination=row[2],
            logic_rule=row[3]
        )
        transition_table[transition_data.name] = transition_data
