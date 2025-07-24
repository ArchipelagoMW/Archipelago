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
        # parent = world.multiworld.get_region(region_data.parent_map, world.player)
        # parent.connect(new_region)
        # parent.create_exit(region_name)
        world.multiworld.regions.append(new_region)

    #After all regions are added, connect them
    for region_name, region_data in data.regions.items():
        from_reg = world.multiworld.get_region(region_data.parent_map, world.player)
        to_reg = world.multiworld.get_region(region_name, world.player)
        connection = from_reg.connect(to_reg)
        if region_data.condition:
            for cond in region_data.condition.keys():
                amount = region_data.condition[cond]
                add_rule(connection, lambda state, con=cond, pl=world.player, am=amount: state.has(con, pl, am))

    return regions