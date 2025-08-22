from math import ceil
from typing import Dict, Tuple, List

from BaseClasses import Region
from worlds.clair_obscur import ClairObscurWorld
from worlds.clair_obscur.Data import data
from worlds.generic.Rules import set_rule, add_rule


def create_regions(world: ClairObscurWorld) -> dict[str, Region]:
    regions: Dict[str, Region] = {}

    #Create menu region
    menu = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu)

    #Create regions and add to multiworld
    for region_name, region_data in data.regions.items():
        new_region = Region(region_name, world.player, world.multiworld)
        regions[region_name] = new_region
        world.multiworld.regions.append(new_region)

    return regions

def connect_regions(world: ClairObscurWorld):
    player = world.player

    for connection in data.connections:
        origin = world.multiworld.get_region(connection.origin_region, player)
        destination = world.multiworld.get_region(connection.destination_region, player)
        entrance = origin.connect(destination)

        #Connection condition: usually area item or rock count, but sometimes barrier breaker or painted power
        if connection.condition:
            for cond in connection.condition.keys():
                amount = connection.condition[cond]
                add_rule(entrance, lambda state, con = cond, pl = player, am=amount: state.has(con, pl, am))

        #Pictos amount condition
        if connection.pictos_level > 1:
            pictos_amount = world.convert_pictos(connection.pictos_level)
            add_rule(entrance, lambda state, pl = player, pic = pictos_amount: state.has_group(
                "Picto", pl, pic))
