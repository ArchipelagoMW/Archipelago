import logging

logger = logging.getLogger("Hollow Knight")

from .Locations import lookup_name_to_id
from .Items import item_table
from .Regions import create_regions
from .Rules import set_rules

from BaseClasses import Region, Entrance, Location, MultiWorld, Item


def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    ret = Region(name, None, name, player)
    ret.world = world
    if locations:
        for location in locations:
            loc_id = lookup_name_to_id.get(location, 0)
            location = HKLocation(player, location, loc_id, ret)
            ret.locations.append(location)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, exit, ret))

    return ret

class HKLocation(Location):
    game: str = "Hollow Knight"

    def __init__(self, player: int, name: str, address=None, parent=None):
        super(HKLocation, self).__init__(player, name, address, parent)

class HKItem(Item):
    game = "Hollow Knight"

    def __init__(self, name, advancement, code, player: int = None):
        super(HKItem, self).__init__(name, advancement, code, player)


def gen_hollow(world: MultiWorld, player: int):
    link_regions(world, player)
    gen_items(world, player)
    set_rules(world, player)




def link_regions(world: MultiWorld, player: int):
    world.get_entrance('Hollow Nest S&Q', player).connect(world.get_region('Hollow Nest', player))


def gen_items(world: MultiWorld, player: int):
    pool = []
    for item_name, item_data in item_table.items():

        item = HKItem(item_name, item_data.advancement, item_data.id, player=player)

        if item_data.type == "Event":
            event_location = world.get_location(item_name, player)
            world.push_item(event_location, item)
            event_location.event = True
            event_location.locked = True
            if item.name == "King's_Pass":
                world.push_precollected(item)
        elif item_data.type == "Fake":
            pass
        else:
            pool.append(item)

    world.itempool += pool



