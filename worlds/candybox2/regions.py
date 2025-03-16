from BaseClasses import Region, MultiWorld
from .locations import candy_box_locations, CandyBox2Location, village_shop_locations, village_house_1_locations, \
    village_locations
from .options import CandyBox2Options


class CandyBox2Region(Region):
    pass

def create_regions(world: MultiWorld, options: CandyBox2Options, player: int):
    candy_box = populate_region(world, player, CandyBox2Region("Menu", player, world, "The Candy Box"), candy_box_locations, None)
    village = populate_region(world, player, CandyBox2Region("Village", player, world, "The Village"), village_locations, candy_box)
    populate_region(world, player, CandyBox2Region("Village Shop", player, world, "The shop in the village"), village_shop_locations, village)
    populate_region(world, player, CandyBox2Region("Village House 1", player, world, "The house next to the forge in the village"), village_house_1_locations, village)

def populate_region(world: MultiWorld, player: int, region: CandyBox2Region, locations: dict[str, int], parent: Region | None):
    region.locations += [CandyBox2Location(player, location_name, locations[location_name], region) for location_name in locations]
    world.regions.append(region)
    if parent is not None:
        parent.connect(region)

    return region