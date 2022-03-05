import os
import json
from base64 import b64encode, b64decode
from math import ceil

from .Items import ChecksFinderItem, item_table, required_items
from .Locations import ChecksFinderAdvancement, advancement_table, exclusion_table
from .Regions import checksfinder_regions, link_checksfinder_structures, default_connections
from .Rules import set_rules, set_completion_rules
from worlds.generic.Rules import exclusion_rules

from BaseClasses import Region, Entrance, Item
from .Options import checksfinder_options
from ..AutoWorld import World

client_version = 7

class ChecksFinderWorld(World):
    """
    ChecksFinder is a game where you avoid mines and find checks inside the board
    with the mines! You win when you get all your items and beat the board!
    """
    game: str = "ChecksFinder"
    options = checksfinder_options
    topology_present = True

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.id for name, data in advancement_table.items()}

    data_version = 4

    def _get_checksfinder_data(self):
        return {
            'world_seed': self.world.slot_seeds[self.player].getrandbits(32),
            'seed_name': self.world.seed_name,
            'player_name': self.world.get_player_name(self.player),
            'player_id': self.player,
            'client_version': client_version,
            'max_width': self.world.max_width[self.player],
            'max_height': self.world.max_height[self.player],
            'max_bombs': self.world.max_bombs[self.player],
            'race': self.world.is_race,
        }

    def generate_basic(self):

        # Generate item pool
        itempool = []
        # Add all required progression items
        for (name, num) in required_items.items():
            itempool += [name] * num
        # Add the map width and height stuff
        itempool += ["Map Width"] * (self.world.max_width[self.player]-5)
        itempool += ["Map Height"] * (self.world.max_height[self.player]-5)
        # Add the map bombs
        itempool += ["Map Bombs"] * (self.world.max_bombs[self.player]-5)
        # Convert itempool into real items
        itempool = [item for item in map(lambda name: self.create_item(name), itempool)]

        # Choose locations to automatically exclude based on settings
        exclusion_pool = set()

        self.world.itempool += itempool

    def set_rules(self):
        set_rules(self.world, self.player)
        set_completion_rules(self.world, self.player)

    def create_regions(self):
        def ChecksFinderRegion(region_name: str, exits=[]):
            ret = Region(region_name, None, region_name, self.player, self.world)
            ret.locations = [ChecksFinderAdvancement(self.player, loc_name, loc_data.id, ret)
                for loc_name, loc_data in advancement_table.items()
                if loc_data.region == region_name]
            for exit in exits:
                ret.exits.append(Entrance(self.player, exit, ret))
            return ret

        self.world.regions += [ChecksFinderRegion(*r) for r in checksfinder_regions]
        link_checksfinder_structures(self.world, self.player)

    def generate_output(self, output_directory: str):
        data = self._get_checksfinder_data()
        filename = f"AP_{self.world.seed_name}_P{self.player}_{self.world.get_player_name(self.player)}.apcf"
        with open(os.path.join(output_directory, filename), 'wb') as f:
            f.write(b64encode(bytes(json.dumps(data), 'utf-8')))

    def fill_slot_data(self):
        slot_data = self._get_mc_data()
        for option_name in checksfinder_options:
            option = getattr(self.world, option_name)[self.player]
            if slot_data.get(option_name, None) is None and type(option.value) in {str, int}:
                slot_data[option_name] = int(option.value)
        return slot_data

    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        item = ChecksFinderItem(name, item_data.progression, item_data.code, self.player)
        return item


def ChecksFinder_update_output(raw_data, server, port):
    data = json.loads(b64decode(raw_data))
    data['server'] = server
    data['port'] = port
    return b64encode(bytes(json.dumps(data), 'utf-8'))
