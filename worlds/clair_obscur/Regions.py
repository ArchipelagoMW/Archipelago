from typing import Dict, Tuple, List

from BaseClasses import Region
from worlds.clair_obscur import ClairObscurWorld
from worlds.clair_obscur.Data import data
from worlds.generic.Rules import set_rule


def create_regions(world: ClairObscurWorld) -> dict[str, Region]:
    regions: Dict[str, Region] = {}
    regions["Menu"] = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(regions["Menu"])

    for region_name, region_data in data.regions.items():
        new_region = Region(region_name, world.player, world.multiworld)

        regions[region_name] = new_region
        world.multiworld.regions.append(new_region)
        parent = world.multiworld.get_region(region_data.parent_map, world.player)
        entrance = parent.connect(new_region)
        if region_data.condition:
            for cond in region_data.condition.keys():
                amount = region_data.condition[cond]
                set_rule(entrance, lambda state: state.has(cond, world.player, amount))

    return regions