import logging

logger = logging.getLogger("Hollow Knight")

from .Locations import locations, lookup_name_to_id
from .Items import items

from BaseClasses import Region, Entrance, Location, MultiWorld, Item


class HKLocation(Location):
    game: str = "Hollow Knight"

    def __init__(self, player: int, name: str, address=None, parent=None):
        super(HKLocation, self).__init__(player, name, address, parent)

class HKItem(Item):
    def __init__(self, name, advancement, code, player: int = None):
        super(HKItem, self).__init__(name, advancement, code, player)

def gen_hollow(world: MultiWorld, player: int):
    logger.info("Doing buggy things.")
    gen_regions(world, player)
    link_regions(world, player)
    gen_items(world, player)
    world.clear_location_cache()
    world.clear_entrance_cache()


def gen_regions(world: MultiWorld, player: int):
    world.regions += [
        create_region(world, player, 'Menu', None, ['Hollow Nest S&Q']),
        create_region(world, player, 'Hollow Nest', [location["name"] for location in locations.values()])
    ]


def link_regions(world: MultiWorld, player: int):
    world.get_entrance('Hollow Nest S&Q', player).connect(world.get_region('Hollow Nest', player))


def gen_items(world: MultiWorld, player: int):
    pool = []
    for item_id, item_data in items.items():
        name = item_data["name"]
        item = HKItem(name, item_data["advancement"], item_id, player=player)
        item.game = "Hollow Knight"
        pool.append(item)
    world.itempool += pool


def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    ret = Region(name, None, name, player)
    ret.world = world
    if locations:
        for location in locations:
            loc_id = lookup_name_to_id[location]
            location = HKLocation(player, location, loc_id, ret)
            ret.locations.append(location)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, exit, ret))

    return ret
