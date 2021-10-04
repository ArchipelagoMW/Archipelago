import os


from .Items import TerrariaItem, item_table, item_frequencies
from .Locations import TerrariaAchievement, achievement_table, exclusion_table, events_table
from .Regions import terraria_regions, link_terraria_structures, default_connections
from .Rules import set_rules
from worlds.generic.Rules import exclusion_rules

from BaseClasses import Region, Entrance, Item
from .Options import terraria_options
from ..AutoWorld import World

client_version = 5

class TerrariaWorld(World):
    game: str = "Terraria"
    options = terraria_options
    topology_present = True

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.id for name, data in achievement_table.items()}

    data_version = 2

    def _get_terraria_data(self):
        exits = [connection[0] for connection in default_connections]
        return {
            'world_seed': self.world.slot_seeds[self.player].getrandbits(32),
            # consistent and doesn't interfere with other generation
            'seed_name': self.world.seed_name,
            'player_name': self.world.get_player_name(self.player),
            'player_id': self.player,
            'client_version': client_version,
            'race': self.world.is_race
        }

    def generate_basic(self):

        # Generate item pool
        itempool = []
        pool_counts = item_frequencies.copy()
        for item_name in item_table:
            for count in range(pool_counts.get(item_name, 1)):
                itempool.append(self.create_item(item_name))

        # Choose locations to automatically exclude based on settings
        exclusion_pool = set()
        exclusion_types = ['hardmode', 'insane', 'postgame']
        for key in exclusion_types:
            if not getattr(self.world, f"include_{key}_achievements")[self.player]:
                exclusion_pool.update(exclusion_table[key])
        exclusion_rules(self.world, self.player, exclusion_pool)

        # Prefill the Wall of Flesh with the completion condition
        completion = self.create_item("Victory")
        self.world.get_location("Still Hungry", self.player).place_locked_item(completion)
        itempool.remove(completion)
        self.world.itempool += itempool

    def set_rules(self):
        set_rules(self.world, self.player)

    def create_regions(self):
        def TerrariaRegion(region_name: str, exits=[]):
            ret = Region(region_name, None, region_name, self.player, self.world)
            ret.locations = [TerrariaAchievement(self.player, loc_name, loc_data.id, ret)
                for loc_name, loc_data in achievement_table.items() 
                if loc_data.region == region_name]
            for exit in exits: 
                ret.exits.append(Entrance(self.player, exit, ret))
            return ret

        self.world.regions += [TerrariaRegion(*r) for r in terraria_regions]
        link_terraria_structures(self.world, self.player)

    def generate_output(self, output_directory: str):
        import json
        from base64 import b64encode

        data = self._get_terraria_data()
        filename = f"AP_{self.world.seed_name}_P{self.player}_{self.world.get_player_name(self.player)}.apterra"
        with open(os.path.join(output_directory, filename), 'wb') as f:
            f.write(b64encode(bytes(json.dumps(data), 'utf-8')))

    def fill_slot_data(self): 
        slot_data = self._get_terraria_data()
        for option_name in terraria_options:
            option = getattr(self.world, option_name)[self.player]
            slot_data[option_name] = int(option.value)
        return slot_data

    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        item = TerrariaItem(name, item_data.progression, item_data.code, self.player)
        nonexcluded_items = []
        if name in nonexcluded_items:  # prevent books from going on excluded locations
            item.never_exclude = True
        return item
