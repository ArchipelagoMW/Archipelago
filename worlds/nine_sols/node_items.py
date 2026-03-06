from enum import IntEnum
from random import Random

from .options import NineSolsGameOptions, FirstRootNode


class MapSide(IntEnum):
    LEFT = 1  # past Cortex Center's Charged Strike statue
    CENTER = 2
    RIGHT = 3  # past Central Hall's Tai-Chi Kick statue


spawn_to_mapside: dict[int, MapSide] = {
    # we use the same alphabetical order as the option class so it's easy to verify that every value is mapped
    FirstRootNode.option_agrarian_hall: MapSide.RIGHT,
    FirstRootNode.option_apeman_facility_depths: MapSide.CENTER,
    FirstRootNode.option_apeman_facility_monitoring: MapSide.CENTER,
    FirstRootNode.option_central_transport_hub: MapSide.CENTER,
    FirstRootNode.option_factory_great_hall: MapSide.LEFT,
    FirstRootNode.option_factory_underground: MapSide.LEFT,
    FirstRootNode.option_galactic_dock: MapSide.CENTER,
    FirstRootNode.option_outer_warehouse: MapSide.LEFT,
    FirstRootNode.option_grotto_of_scriptures_entry: MapSide.RIGHT,
    FirstRootNode.option_grotto_of_scriptures_east: MapSide.RIGHT,
    FirstRootNode.option_grotto_of_scriptures_west: MapSide.RIGHT,
    FirstRootNode.option_inner_warehouse: MapSide.LEFT,
    FirstRootNode.option_lake_yaochi_ruins: MapSide.RIGHT,
    FirstRootNode.option_power_reservoir_east: MapSide.CENTER,
    FirstRootNode.option_power_reservoir_west: MapSide.CENTER,
    FirstRootNode.option_radiant_pagoda: MapSide.CENTER,
    FirstRootNode.option_yinglong_canal: MapSide.RIGHT,
}


leftside_node_items = [
    "Outer Warehouse Root Node",
    "Factory (Great Hall) Root Node",
]
center_node_items = [
    "Apeman Facility (Depths) Root Node",
    "Power Reservoir (East) Root Node",
    "Radiant Pagoda Root Node",
]
rightside_node_items = [
    "Lake Yaochi Ruins Root Node",
    "Grotto of Scriptures (East) Root Node",
]


def select_node_item_names(random: Random, options: NineSolsGameOptions) -> list[str]:
    spawnside = spawn_to_mapside[options.first_root_node.value]

    items = []
    if spawnside != MapSide.LEFT:
        items.append(random.choice(leftside_node_items))
    if spawnside != MapSide.CENTER:
        items.append(random.choice(center_node_items))
    if spawnside != MapSide.RIGHT:
        items.append(random.choice(rightside_node_items))

    return items
