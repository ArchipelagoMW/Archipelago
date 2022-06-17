import os

from .Items import Psychonauts2Item, item_table, item_frequencies
from .Locations import Psychonauts2Location, location_table
from .Regions import link_psychonauts2_entrances, psychonauts2_regions, default_connections
from .Rules import set_location_rules
from worlds.generic.Rules import exclusion_rules

from BaseClasses import Region, Entrance, Item, RegionType
from .Options import psychonauts2_options
from ..AutoWorld import World, WebWorld

# notes: https://docs.google.com/spreadsheets/d/1aP80hPwEHRQsEVVwZS3T5nIn2mBdIs7XwgPsFk5uqkw/edit#gid=0

client_version = 0

class Psychonauts2World(World):
    """Psychonauts 2 is a platform-adventure game about using psychic powers to explore people's minds. Explore crazy environments and search for clues while a mole is loose in the Psychonauts!"""
    game: str = "Psychonauts 2"
    options = psychonauts2_options
    topology_present = False
    remote_items: bool = True
    remote_start_inventory: bool = True

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.id for name, data in location_table.items()}

    data_version = 0

    def _get_psychonauts2_data(self):
        exits = [connection[0] for connection in default_connections]
        return {
            'world_seed': self.world.slot_seeds[self.player].getrandbits(32),
            'seed_name': self.world.seed_name,
            'player_name': self.world.get_player_name(self.player),
            'player_id': self.player,
            'client_version': client_version,
            'structures': {exit: self.world.get_entrance(exit, self.player).connected_region.name for exit in exits},
            #'death_link': bool(self.world.death_link[self.player].value),
            'starting_items': str(self.world.starting_items[self.player].value),
            'race': self.world.is_race,
        }

    def generate_basic(self):
        # place "Victory" at Maligula Boss Fight and set collection as win condition
        self.world.get_location("Defeat Maligula", self.player)\
            .place_locked_item(self.create_event("Victory"))
        self.world.completion_condition[self.player] = \
            lambda state: state.has("Victory", self.player)

        # Generate item pool
        itempool = []

        for (name, num) in item_frequencies.items():
            itempool += [name] * (num-1)

        for (name, value) in item_table.items():
            if name in item_table.items():
                itempool += value

        itempool = [item for item in map(lambda name: self.create_item(name), itempool)]

        self.world.itempool += itempool

        """ pool_counts = item_frequencies.copy()
        for item_name in item_table:
            for count in range(pool_counts.get(item_name, 1)):
                itempool.append(self.create_item(item_name)) """

    def set_rules(self):
        set_location_rules(self.world, self.player)

    def create_regions(self):
        def psychonauts2region(region_name: str, exits=[]):
            ret = Region(region_name, RegionType.Generic, region_name, self.player, self.world)
            ret.locations = [Psychonauts2Location(self.player, loc_name, loc_data.id, ret)
                for loc_name, loc_data in location_table.items()
                if loc_data.region == region_name]
            for exit in exits:
                ret.exits.append(Entrance(self.player, exit, ret))
            return ret

        self.world.regions += [psychonauts2region(*r) for r in psychonauts2_regions]
        link_psychonauts2_entrances(self.world, self.player)

    def create_item (self, name: str) -> Item:
        item_data = item_table[name]
        item = Psychonauts2Item(name, item_data.progression, item_data.code, self.player)
        return item

    def create_event (self, event: str):
        return Psychonauts2Item(event, True, None, self.player)

    

