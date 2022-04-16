import os
import json
from base64 import b64encode, b64decode
from math import ceil

from .Items import UndertaleItem, item_table, required_items, junk_weights
from .Locations import UndertaleAdvancement, advancement_table, exclusion_table
from .Regions import undertale_regions, link_undertale_structures
from .Rules import set_rules, set_completion_rules
from worlds.generic.Rules import exclusion_rules

from BaseClasses import Region, Entrance, Item
from .Options import undertale_options
from ..AutoWorld import World

client_version = 7


def data_path(*args):
    return os.path.join(os.path.dirname(__file__), 'data', *args)


class UndertaleWorld(World):
    """
    Undertale is an RPG where every choice you make matters. You could choose to hurt all the enemies, eventually
    causing genocide of the monster species. Or you can spare all the enemies, befriending them and freeing them
    from their underground prison.
    """
    game: str = "Undertale"
    options = undertale_options
    topology_present = True

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.id for name, data in advancement_table.items()}

    data_version = 4

    def _get_undertale_data(self):
        return {
            'world_seed': self.world.slot_seeds[self.player].getrandbits(32),
            'seed_name': self.world.seed_name,
            'player_name': self.world.get_player_name(self.player),
            'player_id': self.player,
            'client_version': client_version,
            'race': self.world.is_race,
            'route': self.world.route_required[self.player].current_key,
            'temy_armor_include': bool(self.world.temy_include[self.player].value),
        }

    def generate_basic(self):

        # Generate item pool
        itempool = []
        junk_pool = junk_weights.copy()
        # Add all required progression items
        for (name, num) in required_items.items():
            itempool += [name] * num
        if self.world.route_required[self.player].current_key == "genocide":
            itempool += ["Instant Noodles"]
        if self.world.route_required[self.player].current_key == "pacifist":
            itempool += ["Undyne Letter EX"]
        if self.world.temy_include[self.player].value == 1:
            itempool += ["temy armor"]

        # Choose locations to automatically exclude based on settings
        exclusion_pool = set()
        exclusion_pool.update(exclusion_table[self.world.route_required[self.player].current_key])

        # Fill remaining items with randomly generated junk
        itempool += self.world.random.choices(list(junk_pool.keys()), weights=list(junk_pool.values()), k=len(self.location_names)-len(itempool)-len(exclusion_pool))
        # Convert itempool into real items
        itempool = [item for item in map(lambda name: self.create_item(name), itempool)]

        self.world.random.shuffle(itempool)

        self.world.itempool += itempool

    def set_rules(self):
        set_rules(self.world, self.player)
        set_completion_rules(self.world, self.player)

    def create_regions(self):
        def UndertaleRegion(region_name: str, exits=[]):
            ret = Region(region_name, None, region_name, self.player, self.world)
            ret.locations = [UndertaleAdvancement(self.player, loc_name, loc_data.id, ret)
                for loc_name, loc_data in advancement_table.items()
                if loc_data.region == region_name and not loc_name in exclusion_table[self.world.route_required[self.player].current_key]]
            for exit in exits:
                ret.exits.append(Entrance(self.player, exit, ret))
            return ret

        self.world.regions += [UndertaleRegion(*r) for r in undertale_regions]
        link_undertale_structures(self.world, self.player)

    def fill_slot_data(self):
        slot_data = self._get_undertale_data()
        for option_name in undertale_options:
            option = getattr(self.world, option_name)[self.player]
            if slot_data.get(option_name, None) is None and type(option.value) in {str, int}:
                slot_data[option_name] = int(option.value)
        return slot_data

    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        item = UndertaleItem(name, item_data.progression, item_data.code, self.player)
        return item
