from typing import Dict, Set


from .Items import MinecraftItem, item_table, item_frequencies
from .Locations import MinecraftAdvancement, advancement_table, exclusion_table, events_table
from .Regions import mc_regions, link_minecraft_structures
from .Rules import set_rules
from worlds.generic.Rules import exclusion_rules

from BaseClasses import Region, Entrance, Item
from .Options import minecraft_options
from ..AutoWorld import World

client_version = (0, 5)

class MinecraftWorld(World):
    game: str = "Minecraft"
    options = minecraft_options
    topology_present = True
    item_names = frozenset(item_table)
    location_names = frozenset(advancement_table)

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.id for name, data in advancement_table.items()}

    data_version = 2

    def _get_mc_data(self):
        exits = ["Overworld Structure 1", "Overworld Structure 2", "Nether Structure 1", "Nether Structure 2",
                 "The End Structure"]
        return {
            'world_seed': self.world.slot_seeds[self.player].getrandbits(32),
            # consistent and doesn't interfere with other generation
            'seed_name': self.world.seed_name,
            'player_name': self.world.get_player_names(self.player),
            'player_id': self.player,
            'client_version': client_version,
            'structures': {exit: self.world.get_entrance(exit, self.player).connected_region.name for exit in exits}
        }

    def generate_basic(self):

        # Generate item pool
        itempool = []
        pool_counts = item_frequencies.copy()
        if getattr(self.world, "bee_traps")[self.player]: # replace Rotten Flesh by bee traps
            pool_counts.update({"Rotten Flesh": 0, "Bee Trap (Minecraft)": 4})
        # Add needed structure compasses to the pool, replacing 50 XP
        for entrance_name in ["Overworld Structure 1", "Overworld Structure 2"]:
            struct_name = self.world.get_entrance(entrance_name, self.player).connected_region.name
            pool_counts[f"Structure Compass ({struct_name})"] = 1
            pool_counts["50 XP"] -= 1
        for item_name in item_table:
            for count in range(pool_counts.get(item_name, 1)):
                itempool.append(self.create_item(item_name))

        # Choose locations to automatically exclude based on settings
        exclusion_pool = set()
        exclusion_types = ['hard', 'insane', 'postgame']
        for key in exclusion_types:
            if not getattr(self.world, f"include_{key}_advancements")[self.player]:
                exclusion_pool.update(exclusion_table[key])
        exclusion_rules(self.world, self.player, exclusion_pool)

        # Prefill the Ender Dragon with the completion condition
        completion = self.create_item("Victory")
        self.world.get_location("Ender Dragon", self.player).place_locked_item(completion)
        itempool.remove(completion)
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

    def generate_output(self):
        import json
        from base64 import b64encode
        from Utils import output_path

        data = self._get_mc_data()
        filename = f"AP_{self.world.seed_name}_P{self.player}_{self.world.get_player_names(self.player)}.apmc"
        with open(output_path(filename), 'wb') as f:
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
        nonexcluded_items = ["Sharpness III Book", "Infinity Book", "Looting III Book", "Saddle"]
        if name in nonexcluded_items:  # prevent these items from going on excluded locations
            item.can_be_excluded = False
        return item
