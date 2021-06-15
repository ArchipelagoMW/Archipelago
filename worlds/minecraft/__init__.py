from .Items import MinecraftItem, item_table, item_frequencies
from .Locations import MinecraftAdvancement, advancement_table, exclusion_table, events_table
from .Regions import mc_regions, link_minecraft_structures
from .Rules import set_rules

from BaseClasses import Region, Entrance
from Options import minecraft_options
from ..AutoWorld import World

client_version = (0, 3)

class MinecraftWorld(World):
    game: str = "Minecraft"


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
        link_minecraft_structures(self.world, self.player)

        pool = []
        for item_name, item_data in item_table.items():
            for count in range(item_frequencies.get(item_name, 1)):
                pool.append(MinecraftItem(item_name, item_data.progression, item_data.code, self.player))

        prefill_pool = {}
        prefill_pool.update(events_table)
        exclusion_pools = ['hard', 'insane', 'postgame']
        for key in exclusion_pools:
            if not getattr(self.world, f"include_{key}_advancements")[self.player]:
                prefill_pool.update(exclusion_table[key])

        for loc_name, item_name in prefill_pool.items():
            item_data = item_table[item_name]
            location = self.world.get_location(loc_name, self.player)
            item = MinecraftItem(item_name, item_data.progression, item_data.code, self.player)
            self.world.push_item(location, item, collect=False)
            pool.remove(item)
            location.event = item_data.progression
            location.locked = True

        self.world.itempool += pool


    def set_rules(self):
        set_rules(self.world, self.player)


    def create_regions(self):
        def MCRegion(region_name: str, exits=[]):
            ret = Region(region_name, None, region_name, self.player)
            ret.world = self.world
            ret.locations = [ MinecraftAdvancement(self.player, loc_name, loc_data.id, ret) 
                for loc_name, loc_data in advancement_table.items() 
                if loc_data.region == region_name ]
            for exit in exits: 
                ret.exits.append(Entrance(self.player, exit, ret))
            return ret

        self.world.regions += [MCRegion(*r) for r in mc_regions]


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
