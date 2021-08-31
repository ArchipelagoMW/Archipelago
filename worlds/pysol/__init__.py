import logging
from typing import Set

logger = logging.getLogger("PySolFC")

from .Locations import lookup_name_to_id as locations_lookup_name_to_id
from .Items import lookup_name_to_item
from .Items import lookup_name_to_id as items_lookup_name_to_id

from .Regions import create_regions
from .Rules import set_rules

from BaseClasses import Region, Entrance, Location, MultiWorld, Item
from ..AutoWorld import World


class PySolFCWorld(World):
    game: str = "PySolFC"

    item_name_to_id = items_lookup_name_to_id
    location_name_to_id = locations_lookup_name_to_id

    def generate_basic(self):
        # Link regions
        self.world.get_entrance('Startup', self.player).connect(self.world.get_region('Games Menu', self.player))

        # Generate item pool
        pool = []
        for item in lookup_name_to_item:
            for i in range(item["count"]):
                pysol_item = PySolFCItem(item["name"], item["progression"], item["id"], player = self.player)
                pool.append(pysol_item)
        self.world.itempool += pool

    def set_rules(self):
        set_rules(self.world, self.player)


    def create_regions(self):
        create_regions(self.world, self.player)


    def generate_output(self, output_directory: str):
        pass


    def fill_slot_data(self): 
        slot_data = {}
        return slot_data


def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    ret = Region(name, None, name, player)
    ret.world = world
    if locations:
        for location in locations:
            loc_id = locations_lookup_name_to_id.get(location, 0)
            location = PySolFCLocation(player, location, loc_id, ret)
            ret.locations.append(location)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, exit, ret))

    return ret


class PySolFCLocation(Location):
    game: str = "PySolFC"

    def __init__(self, player: int, name: str, address=None, parent=None):
        super(PySolFCLocation, self).__init__(player, name, address, parent)


class PySolFCItem(Item):
    game = "PySolFC"

    def __init__(self, name, advancement, code, player: int = None):
        super(PySolFCItem, self).__init__(name, advancement, code, player)
