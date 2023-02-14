import os
import json
from base64 import b64encode, b64decode
from math import ceil

from .Items import MinecraftItem, item_table, required_items, junk_weights
from .Locations import MinecraftAdvancement, advancement_table, exclusion_table, get_postgame_advancements
from .Regions import mc_regions, link_minecraft_structures, default_connections
from .Rules import set_advancement_rules, set_completion_rules
from worlds.generic.Rules import exclusion_rules

from BaseClasses import Region, Entrance, Item, Tutorial, ItemClassification
from .Options import minecraft_options
from ..AutoWorld import World, WebWorld

client_version = 9

class MinecraftWebWorld(WebWorld):
    theme = "jungle"
    bug_report_page = "https://github.com/KonoTyran/Minecraft_AP_Randomizer/issues/new?assignees=&labels=bug&template=bug_report.yaml&title=%5BBug%5D%3A+Brief+Description+of+bug+here"

    setup = Tutorial(
        "Multiworld Setup Tutorial",
        "A guide to setting up the Archipelago Minecraft software on your computer. This guide covers"
        "single-player, multiworld, and related software.",
        "English",
        "minecraft_en.md",
        "minecraft/en",
        ["Kono Tyran"]
    )

    setup_es = Tutorial(
        setup.tutorial_name,
        setup.description,
        "Español",
        "minecraft_es.md",
        "minecraft/es",
        ["Edos"]
    )

    setup_sv = Tutorial(
        setup.tutorial_name,
        setup.description,
        "Swedish",
        "minecraft_sv.md",
        "minecraft/sv",
        ["Albinum"]
    )

    tutorials = [setup, setup_es, setup_sv]


class MinecraftWorld(World):
    """
    Minecraft is a game about creativity. In a world made entirely of cubes, you explore, discover, mine,
    craft, and try not to explode. Delve deep into the earth and discover abandoned mines, ancient
    structures, and materials to create a portal to another world. Defeat the Ender Dragon, and claim
    victory!
    """
    game: str = "Minecraft"
    option_definitions = minecraft_options
    topology_present = True
    web = MinecraftWebWorld()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.id for name, data in advancement_table.items()}

    data_version = 7

    def _get_mc_data(self):
        exits = [connection[0] for connection in default_connections]
        return {
            'world_seed': self.multiworld.per_slot_randoms[self.player].getrandbits(32),
            'seed_name': self.multiworld.seed_name,
            'player_name': self.multiworld.get_player_name(self.player),
            'player_id': self.player,
            'client_version': client_version,
            'structures': {exit: self.multiworld.get_entrance(exit, self.player).connected_region.name for exit in exits},
            'advancement_goal': self.multiworld.advancement_goal[self.player].value,
            'egg_shards_required': min(self.multiworld.egg_shards_required[self.player].value,
                                       self.multiworld.egg_shards_available[self.player].value),
            'egg_shards_available': self.multiworld.egg_shards_available[self.player].value,
            'required_bosses': self.multiworld.required_bosses[self.player].current_key,
            'MC35': bool(self.multiworld.send_defeated_mobs[self.player].value),
            'death_link': bool(self.multiworld.death_link[self.player].value),
            'starting_items': str(self.multiworld.starting_items[self.player].value),
            'race': self.multiworld.is_race,
        }

    def generate_basic(self):

        # Generate item pool
        itempool = []
        junk_pool = junk_weights.copy()
        # Add all required progression items
        for (name, num) in required_items.items():
            itempool += [name] * num
        # Add structure compasses if desired
        if self.multiworld.structure_compasses[self.player]:
            structures = [connection[1] for connection in default_connections]
            for struct_name in structures:
                itempool.append(f"Structure Compass ({struct_name})")
        # Add dragon egg shards
        if self.multiworld.egg_shards_required[self.player] > 0:
            itempool += ["Dragon Egg Shard"] * self.multiworld.egg_shards_available[self.player]
        # Add bee traps if desired
        bee_trap_quantity = ceil(self.multiworld.bee_traps[self.player] * (len(self.location_names) - len(itempool)) * 0.01)
        itempool += ["Bee Trap"] * bee_trap_quantity
        # Fill remaining items with randomly generated junk
        itempool += self.multiworld.random.choices(list(junk_pool.keys()), weights=list(junk_pool.values()), k=len(self.location_names) - len(itempool))
        # Convert itempool into real items
        itempool = [item for item in map(lambda name: self.create_item(name), itempool)]

        # Choose locations to automatically exclude based on settings
        exclusion_pool = set()
        exclusion_types = ['hard', 'unreasonable']
        for key in exclusion_types:
            if not getattr(self.multiworld, f"include_{key}_advancements")[self.player]:
                exclusion_pool.update(exclusion_table[key])
        # For postgame advancements, check with the boss goal
        exclusion_pool.update(get_postgame_advancements(self.multiworld.required_bosses[self.player].current_key))
        exclusion_rules(self.multiworld, self.player, exclusion_pool)

        # Prefill event locations with their events
        self.multiworld.get_location("Blaze Spawner", self.player).place_locked_item(self.create_item("Blaze Rods"))
        self.multiworld.get_location("Ender Dragon", self.player).place_locked_item(self.create_item("Defeat Ender Dragon"))
        self.multiworld.get_location("Wither", self.player).place_locked_item(self.create_item("Defeat Wither"))

        self.multiworld.itempool += itempool

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choices(list(junk_weights.keys()), weights=list(junk_weights.values()))[0]

    def set_rules(self):
        set_advancement_rules(self.multiworld, self.player)
        set_completion_rules(self.multiworld, self.player)

    def create_regions(self):
        def MCRegion(region_name: str, exits=[]):
            ret = Region(region_name, self.player, self.multiworld)
            ret.locations = [MinecraftAdvancement(self.player, loc_name, loc_data.id, ret)
                for loc_name, loc_data in advancement_table.items()
                if loc_data.region == region_name]
            for exit in exits:
                ret.exits.append(Entrance(self.player, exit, ret))
            return ret

        self.multiworld.regions += [MCRegion(*r) for r in mc_regions]
        link_minecraft_structures(self.multiworld, self.player)

    def generate_output(self, output_directory: str):
        data = self._get_mc_data()
        filename = f"AP_{self.multiworld.get_out_file_name_base(self.player)}.apmc"
        with open(os.path.join(output_directory, filename), 'wb') as f:
            f.write(b64encode(bytes(json.dumps(data), 'utf-8')))

    def fill_slot_data(self):
        slot_data = self._get_mc_data()
        for option_name in minecraft_options:
            option = getattr(self.multiworld, option_name)[self.player]
            if slot_data.get(option_name, None) is None and type(option.value) in {str, int}:
                slot_data[option_name] = int(option.value)
        return slot_data

    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        if name == "Bee Trap":
            classification = ItemClassification.trap
            # prevent books from going on excluded locations
        elif name in ("Sharpness III Book", "Infinity Book", "Looting III Book"):
            classification = ItemClassification.useful
        elif item_data.progression:
            classification = ItemClassification.progression
        else:
            classification = ItemClassification.filler
        item = MinecraftItem(name, classification, item_data.code, self.player)

        return item

def mc_update_output(raw_data, server, port):
    data = json.loads(b64decode(raw_data))
    data['server'] = server
    data['port'] = port
    return b64encode(bytes(json.dumps(data), 'utf-8'))
