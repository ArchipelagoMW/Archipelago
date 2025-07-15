from typing import Dict, Tuple, List

from BaseClasses import Region
from worlds.clair_obscur import ClairObscurWorld
from worlds.clair_obscur.Data import data


def create_regions(world: ClairObscurWorld) -> dict[str, Region]:
    regions: Dict[str, Region] = {}


    for region_name, region_data in data.regions.items():
        new_region = Region(region_name, world.player, world.multiworld)

        regions[region_name] = new_region
        world.multiworld.regions.append(new_region)


    for region_name in regions:
        region_data = regions[region_name]
        if region_name == "World Map":
            continue
        region_data.connect(regions["World Map"], f"{region_name} -> World Map")
        regions["World Map"].connect(region_data, f"World Map -> {region_name}")


    regions["Menu"] = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(regions["Menu"])
    regions["Menu"].connect(regions["World Map"])
    regions["World Map"].connect(regions["Menu"])

    return regions