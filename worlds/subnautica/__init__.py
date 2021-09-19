import logging

logger = logging.getLogger("Subnautica")

from .Locations import lookup_name_to_id as locations_lookup_name_to_id
from .Items import item_table, lookup_name_to_item, advancement_item_names
from .Items import lookup_name_to_id as items_lookup_name_to_id

from .Regions import create_regions
from .Rules import set_rules
from .Options import options

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
    options = options

    def generate_basic(self):
        # Link regions
        self.world.get_entrance('Lifepod 5', self.player).connect(self.world.get_region('Planet 4546B', self.player))

        # Generate item pool
        pool = []
        neptune_launch_platform = None
        extras = 0
        for item in item_table:
            for i in range(item["count"]):
                subnautica_item = self.create_item(item["name"])
                if item["name"] == "Neptune Launch Platform":
                    neptune_launch_platform = subnautica_item
                elif not item["progression"] and self.world.item_pool[self.player] == "valuable":
                    self.world.push_precollected(subnautica_item)
                    extras += 1
                else:
                    pool.append(subnautica_item)
        for item_name in self.world.random.choices(sorted(advancement_item_names - {"Neptune Launch Platform"}),
                                                   k=extras):
            pool.append(self.create_item(item_name))

        self.world.itempool += pool

        # Victory item
        self.world.get_location("Aurora - Captain Data Terminal", self.player).place_locked_item(
            neptune_launch_platform)
        self.world.get_location("Neptune Launch", self.player).place_locked_item(
            SubnauticaItem("Victory", True, None, player=self.player))

    def set_rules(self):
        set_rules(self.world, self.player)

    def create_regions(self):
        create_regions(self.world, self.player)

    def fill_slot_data(self):
        slot_data = {}
        return slot_data

    def create_item(self, name: str) -> Item:
        item = lookup_name_to_item[name]
        return SubnauticaItem(name, item["progression"], item["id"], player=self.player)


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


class SubnauticaItem(Item):
    game = "Subnautica"
