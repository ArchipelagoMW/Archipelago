
from typing import ChainMap
from . import buildings, island_buildings, mechanics, misc
from .. import ItemData, PointsItemData

# ID domains:
# buildings < 1000
# island buildings 1xxx
# mechanics 2xxx
# task lines 3xxx
# operator lines 4xxx
# research points 5xxx
# platforms 6xxx


class RewardType:
    building = 0
    island_building = 1
    mechanic = 2
    platforms = 3
    blueprint_points = 4
    research_points = 5


all_items = ChainMap[str, ItemData | PointsItemData](
    buildings.always,
    buildings.starting,
    buildings.simple_processors,
    buildings.sandbox,
    island_buildings.always,
    island_buildings.starting,
    island_buildings.miners,
    mechanics.always,
    mechanics.starting,
    mechanics.special,
    misc.task_lines,
    misc.operator_lines,
    misc.research_points,
    misc.platforms,
    misc.blueprint_points,
)

all_standard_items = ChainMap[str, ItemData](
    buildings.always,
    buildings.starting,
    buildings.simple_processors,
    buildings.sandbox,
    island_buildings.always,
    island_buildings.starting,
    island_buildings.miners,
    mechanics.always,
    mechanics.starting,
    mechanics.special,
    misc.task_lines,
    misc.operator_lines,
)

all_points_items = ChainMap[str, PointsItemData](
    misc.research_points,
    misc.platforms,
    misc.blueprint_points,
)
