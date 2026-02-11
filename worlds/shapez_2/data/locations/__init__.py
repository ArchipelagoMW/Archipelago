from typing import ChainMap
from .. import LocationData
from . import milestones, tasks, operator_levels

# ID domains:
# milestones < 10000
# tasks 1xxxx
# operator levels 2xxxx

all_locations = ChainMap[str, LocationData](
    milestones.locations,
    tasks.locations,
    operator_levels.locations,
)
