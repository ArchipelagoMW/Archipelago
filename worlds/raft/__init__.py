import logging
import typing
import random

from .Locations import location_table, lookup_name_to_id as locations_lookup_name_to_id
from .Items import item_table, lookup_name_to_item, advancement_item_names
from .Items import lookup_name_to_id as items_lookup_name_to_id
from .Progressives import lookup_item_to_progressive, progressive_item_list

from .Regions import create_regions, getConnectionName
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

    item_name_to_id = items_lookup_name_to_id.copy()
    lastItemId = max(filter(lambda val: val is not None, item_name_to_id.values()))
    for progressiveItemName in progressive_item_list.keys():
        lastItemId += 1
        item_name_to_id[progressiveItemName] = lastItemId
    location_name_to_id = locations_lookup_name_to_id
    options = options

    possible_resource_packs = [ #TODO: Figure out a more dynamic way of setting these
            ("Plank", 1, 5),
            ("Plastic", 1, 5),
            ("Clay", 1, 5),
            ("Stone", 1, 5),
            ("Rope", 1, 5),
            ("Scrap", 1, 5),
            ("SeaVine", 1, 5),
            ("Thatch", 1, 5),
            ("Sand", 1, 5),
            ("Beet", 1, 5)
        ]

    for resourcePack in possible_resource_packs:
        for i in range(resourcePack[1], resourcePack[2] + 1):
            lastItemId += 1
            item_name_to_id["Resource Pack: " + str(i) + " " + resourcePack[0]] = lastItemId
    

    data_version = 11

    def generate_basic(self):
        # Generate item pool
        pool = []
        extras = len(location_table) - len(item_table)
        if extras < 0:
            extras = 0
        for item in item_table:
            raft_item = self.create_item(item["name"])
            pool.append(raft_item)

        print(lookup_name_to_item)
        while extras > 0:
            pack_seed = self.possible_resource_packs[random.randrange(0, len(self.possible_resource_packs))]
            pack = self.create_item("Resource Pack: " + str(random.randrange(pack_seed[1], pack_seed[2] + 1)) + " " + pack_seed[0])
            pool.append(pack)
            extras -= 1

        self.world.itempool += pool

    def set_rules(self):
        set_rules(self.world, self.player)

    def create_regions(self):
        create_regions(self.world, self.player)

    def fill_slot_data(self):
        slot_data = {}
        return slot_data

    def create_item(self, name: str) -> Item:
        if len(name) >= 14 and name[0:14] == "Resource Pack:": #TODO: Make this less evil and hacky
            return RaftItem(name, False, self.item_name_to_id[name], player=self.player)
        item = lookup_name_to_item[name]
        if name in lookup_item_to_progressive:
            name = lookup_item_to_progressive[name]
        return RaftItem(name, item["progression"], self.item_name_to_id[name], player=self.player)
    
    def collect_item(self, state, item, remove=False):
        if item.name in progressive_item_list:
            prog_table = progressive_item_list[item.name]
            if remove:
                for item_name in reversed(prog_table):
                    if state.has(item_name, item.player):
                        return item_name
            else:
                for item_name in prog_table:
                    if not state.has(item_name, item.player):
                        return item_name

        return super(RaftWorld, self).collect_item(state, item, remove)

    def get_required_client_version(self) -> typing.Tuple[int, int, int]:
        return max((0, 2, 0), super(RaftWorld, self).get_required_client_version())
    
    def pre_fill(self):
        # Victory item
        self.world.get_location("Tangaroa Next Frequency", self.player).place_locked_item(
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
