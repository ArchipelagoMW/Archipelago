import logging
import typing

from .Locations import location_table, lookup_name_to_id as locations_lookup_name_to_id
from .Items import item_table, lookup_name_to_item, advancement_item_names
from .Items import lookup_name_to_id as items_lookup_name_to_id

from .Regions import create_regions, regionMap, getConnectionName
from .Rules import set_rules
from .Options import options

from BaseClasses import Region, RegionType, Entrance, Location, MultiWorld, Item
from ..AutoWorld import World


class RaftWorld(World):
    """
    Raft is a flooded world exploration game. You're stranded on a small raft in the middle of the
    ocean, and you must survive on trash floating by you on the top of the water and around/on any
    islands that you come across.
    """
    game: str = "Raft"

    item_name_to_id = items_lookup_name_to_id
    location_name_to_id = locations_lookup_name_to_id
    options = options

    data_version = 2

    def generate_basic(self):
        # Generate item pool
        pool = []
        extras = len(location_table) - len(item_table) - 1
        if extras < 0:
            extras = 0
        for item in item_table:
            raft_item = self.create_item(item["name"])
            for i in range(item["count"]):
                pool.append(raft_item)

        for item_name in self.world.random.choices(sorted(advancement_item_names), k=extras):
            item = self.create_item(item_name)
            item.advancement = False  # as it's an extra, just fast-fill it somewhere (is this actually correct...?)
            pool.append(item)

        self.world.itempool += pool

    def set_rules(self):
        set_rules(self.world, self.player)

    def create_regions(self):
        create_regions(self.world, self.player)

    def fill_slot_data(self):
        slot_data = {}
        return slot_data

    def create_item(self, name: str) -> Item:
        item = lookup_name_to_item[name]
        return RaftItem(name, item["progression"], item["id"], player=self.player)

    def get_required_client_version(self) -> typing.Tuple[int, int, int]:
        return max((0, 2, 0), super(RaftWorld, self).get_required_client_version())
    
    def pre_fill(self):
        # Victory item
        self.world.get_location("RadioTowerRadioTranscriptionLOC", self.player).place_locked_item( #TODO: Add actual victory location
            RaftItem("Victory", True, None, player=self.player))


def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    ret = Region(name, RegionType.Generic, name, player)
    ret.world = world
    if locations:
        for location in locations:
            loc_id = locations_lookup_name_to_id.get(location, 0)
            locationObj = RaftLocation(player, location, loc_id, ret)
            ret.locations.append(locationObj)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, getConnectionName(name, exit), ret))

    return ret


class RaftLocation(Location):
    game = "Raft"


class RaftItem(Item):
    game = "Raft"
