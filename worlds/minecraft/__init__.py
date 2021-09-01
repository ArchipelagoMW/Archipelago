import os
import json
from base64 import b64encode, b64decode
from math import ceil

from .Items import MinecraftItem, item_table, required_items, junk_weights
from .Locations import MinecraftAdvancement, advancement_table, exclusion_table, events_table
from .Regions import mc_regions, link_minecraft_structures, default_connections
from .Rules import set_rules
from worlds.generic.Rules import exclusion_rules

from BaseClasses import Region, Entrance, Item
from .Options import minecraft_options
from ..AutoWorld import World

client_version = 6

class MinecraftWorld(World):
    """
    Minecraft is a game about creativity. In a world made entirely of cubes, you explore, discover, mine,
    craft, and try not to explode. Delve deep into the earth and discover abandoned mines, ancient
    structures, and materials to create a portal to another world. Defeat the Ender Dragon, and claim
    victory!
    """
    game: str = "Minecraft"
    options = minecraft_options
    topology_present = True

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.id for name, data in advancement_table.items()}

    data_version = 3

    def _get_mc_data(self):
        exits = [connection[0] for connection in default_connections]
        return {
            'world_seed': self.world.slot_seeds[self.player].getrandbits(32),
            'seed_name': self.world.seed_name,
            'player_name': self.world.get_player_name(self.player),
            'player_id': self.player,
            'client_version': client_version,
            'structures': {exit: self.world.get_entrance(exit, self.player).connected_region.name for exit in exits},
            'advancement_goal': self.world.advancement_goal[self.player],
            'egg_shards_required': self.world.egg_shards_required[self.player],
            'egg_shards_available': self.world.egg_shards_available[self.player],
            'MC35': bool(self.world.send_defeated_mobs[self.player]),
            'race': self.world.is_race
        }

    def generate_basic(self):

        # Generate item pool
        itempool = []
        junk_pool = junk_weights.copy()
        # Add all required progression items
        for (name, num) in required_items.items():
            itempool += [name] * num
        # Add structure compasses if desired
        if self.world.structure_compasses[self.player]:
            structures = [connection[1] for connection in default_connections]
            for struct_name in structures:
                itempool.append(f"Structure Compass ({struct_name})")
        # Add dragon egg shards
        itempool += ["Dragon Egg Shard"] * self.world.egg_shards_available[self.player]
        # Add bee traps if desired
        bee_trap_quantity = ceil(self.world.bee_traps[self.player] * (len(self.location_names)-len(itempool)) * 0.01)
        itempool += ["Bee Trap (Minecraft)"] * bee_trap_quantity
        # Fill remaining items with randomly generated junk
        itempool += self.world.random.choices(list(junk_pool.keys()), weights=list(junk_pool.values()), k=len(self.location_names)-len(itempool))
        # Convert itempool into real items
        itempool = [item for item in map(lambda name: self.create_item(name), itempool)]

        # Choose locations to automatically exclude based on settings
        exclusion_pool = set()
        exclusion_types = ['hard', 'insane', 'postgame']
        for key in exclusion_types:
            if not getattr(self.world, f"include_{key}_advancements")[self.player]:
                exclusion_pool.update(exclusion_table[key])
        exclusion_rules(self.world, self.player, exclusion_pool)

        # Prefill event locations with their events
        self.world.get_location("Blaze Spawner", self.player).place_locked_item(self.create_item("Blaze Rods"))
        self.world.get_location("Ender Dragon", self.player).place_locked_item(self.create_item("Victory"))

        self.world.itempool += itempool

    def set_rules(self):
        set_rules(self.world, self.player)

    def create_regions(self):
        def MCRegion(region_name: str, exits=[]):
            ret = Region(region_name, None, region_name, self.player, self.world)
            ret.locations = [MinecraftAdvancement(self.player, loc_name, loc_data.id, ret)
                for loc_name, loc_data in advancement_table.items()
                if loc_data.region == region_name]
            for exit in exits:
                ret.exits.append(Entrance(self.player, exit, ret))
            return ret

        self.world.regions += [MCRegion(*r) for r in mc_regions]
        link_minecraft_structures(self.world, self.player)

    def generate_output(self, output_directory: str):
        data = self._get_mc_data()
        filename = f"AP_{self.world.seed_name}_P{self.player}_{self.world.get_player_name(self.player)}.apmc"
        with open(os.path.join(output_directory, filename), 'wb') as f:
            f.write(b64encode(bytes(json.dumps(data), 'utf-8')))

    def fill_slot_data(self):
        slot_data = self._get_mc_data()
        for option_name in minecraft_options:
            option = getattr(self.world, option_name)[self.player]
            slot_data[option_name] = int(option.value)
        return slot_data

    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        item = MinecraftItem(name, item_data.progression, item_data.code, self.player)
        nonexcluded_items = ["Sharpness III Book", "Infinity Book", "Looting III Book"]
        if name in nonexcluded_items:  # prevent books from going on excluded locations
            item.never_exclude = True
        return item

def mc_update_output(raw_data, server, port):
    data = json.loads(b64decode(raw_data))
    data['server'] = server
    data['port'] = port
    return b64encode(bytes(json.dumps(data), 'utf-8'))
