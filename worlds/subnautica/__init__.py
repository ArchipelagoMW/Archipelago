import logging
from typing import Set

logger = logging.getLogger("Subnautica")

from .Locations import lookup_name_to_id as locations_lookup_name_to_id
from .Items import item_table
from .Items import lookup_name_to_id as items_lookup_name_to_id

from .Regions import create_regions
from .Rules import set_rules

from BaseClasses import Region, Entrance, Location, MultiWorld, Item
from ..AutoWorld import World


class SubnauticaWorld(World):
    """
    Subnautica is an undersea exploration game. Stranded on an alien world, you become infected by
    an unknown bacteria. The planet's automatic quarantine will shoot you down if you try to leave.
    You must find a cure for yourself, build an escape rocket, and leave the planet.
    """
    game: str = "Subnautica"

    item_name_to_id = items_lookup_name_to_id
    location_name_to_id = locations_lookup_name_to_id

    def generate_basic(self):
        # Link regions
        self.world.get_entrance('Lifepod 5', self.player).connect(self.world.get_region('Planet 4546B', self.player))

        # Generate item pool
        pool = []
        neptune_launch_platform = None
        for item in item_table:
            for i in range(item["count"]):
                subnautica_item = SubnauticaItem(item["name"], item["progression"], item["id"], player = self.player)
                if item["name"] == "Neptune Launch Platform":
                    neptune_launch_platform = subnautica_item
                else:
                    pool.append(subnautica_item)
        self.world.itempool += pool

        # Victory item
        self.world.get_location("Aurora - Captain Data Terminal", self.player).place_locked_item(neptune_launch_platform)
        self.world.get_location("Neptune Launch", self.player).place_locked_item(SubnauticaItem("Victory", True, None, player = self.player))


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
            location = SubnauticaLocation(player, location, loc_id, ret)
            ret.locations.append(location)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, exit, ret))

    return ret


class SubnauticaLocation(Location):
    game: str = "Subnautica"

    def __init__(self, player: int, name: str, address=None, parent=None):
        super(SubnauticaLocation, self).__init__(player, name, address, parent)


class SubnauticaItem(Item):
    game = "Subnautica"

    def __init__(self, name, advancement, code, player: int = None):
        super(SubnauticaItem, self).__init__(name, advancement, code, player)
