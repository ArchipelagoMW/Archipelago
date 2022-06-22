import os
import json
from base64 import b64encode, b64decode
from math import ceil

from .Items import MinecraftItem, item_table, required_items, junk_weights
from .Locations import MinecraftAdvancement, advancement_table, exclusion_table, get_postgame_advancements
from .Regions import mc_regions, link_minecraft_structures, default_connections
from .Rules import set_advancement_rules, set_completion_rules
from worlds.generic.Rules import exclusion_rules

from BaseClasses import Region, Entrance, Item, Tutorial
from .Options import minecraft_options
from ..AutoWorld import World, WebWorld

client_version = 8

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

    def modify_tracker(self, tracker):
        tracker.icons = {
            "Wooden Pickaxe": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/d/d2/Wooden_Pickaxe_JE3_BE3.png",
            "Stone Pickaxe": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c4/Stone_Pickaxe_JE2_BE2.png",
            "Iron Pickaxe": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/d/d1/Iron_Pickaxe_JE3_BE2.png",
            "Diamond Pickaxe": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/e/e7/Diamond_Pickaxe_JE3_BE3.png",
            "Wooden Sword": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/d/d5/Wooden_Sword_JE2_BE2.png",
            "Stone Sword": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/b/b1/Stone_Sword_JE2_BE2.png",
            "Iron Sword": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/8/8e/Iron_Sword_JE2_BE2.png",
            "Diamond Sword": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/4/44/Diamond_Sword_JE3_BE3.png",
            "Leather Tunic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/b/b7/Leather_Tunic_JE4_BE2.png",
            "Iron Chestplate": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/31/Iron_Chestplate_JE2_BE2.png",
            "Diamond Chestplate": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/e/e0/Diamond_Chestplate_JE3_BE2.png",
            "Iron Ingot": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/fc/Iron_Ingot_JE3_BE2.png",
            "Block of Iron": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7e/Block_of_Iron_JE4_BE3.png",
            "Brewing": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/fa/Brewing_Stand.png",
            "Ender Pearls": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/f6/Ender_Pearl_JE3_BE2.png",
            "Bucket": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/fc/Bucket_JE2_BE2.png",
            "Archery": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/a/ab/Bow_%28Pull_2%29_JE1_BE1.png",
            "Shield": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c6/Shield_JE2_BE1.png",
            "Bed": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/6/6a/Red_Bed_%28N%29.png",
            "Netherite Scrap": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/33/Netherite_Scrap_JE2_BE1.png",
            "Flint and Steel": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/9/94/Flint_and_Steel_JE4_BE2.png",
            "Enchanting": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/31/Enchanting_Table.gif",
            "Fishing Rod": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7f/Fishing_Rod_JE2_BE2.png",
            "Campfire": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/9/91/Campfire_JE2_BE2.gif",
            "Bottle": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/75/Water_Bottle_JE2_BE2.png",
            "Spyglass": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c1/Spyglass_JE2_BE1.png",
        }

        tracker.progressive_items = [
            "Progressive Tools", "Progressive Weapons", "Progressive Armor", "Progressive Resource Crafting",
            "Brewing", "Ender Pearls", "Bucket", "Archery", "Shield", "Bed", "Bottle", "Netherite Scrap",
            "Flint and Steel", "Enchanting", "Fishing Rod", "Campfire", "Spyglass"
        ]

        tracker.progressive_names = {
            "Progressive Tools": ["Wooden Pickaxe", "Stone Pickaxe", "Iron Pickaxe", "Diamond Pickaxe"],
            "Progressive Weapons": ["Wooden Sword", "Stone Sword", "Iron Sword", "Diamond Sword"],
            "Progressive Armor": ["Leather Tunic", "Iron Chestplate", "Diamond Chestplate"],
            "Progressive Resource Crafting": ["Iron Ingot", "Iron Ingot", "Block of Iron"]
        }

        tracker.regions = {
            "Story": ["Minecraft", "Stone Age", "Getting an Upgrade", "Acquire Hardware", "Suit Up",
                      "Not Today, Thank You", "Isn't It Iron Pick", "Diamonds!", "Cover Me With Diamonds", "Enchanter",
                      "Hot Stuff", "Ice Bucket Challenge", "We Need to Go Deeper", "Zombie Doctor", "Eye Spy", "The End?"],

            "Nether": ["Nether", "Return to Sender", "Uneasy Alliance", "Those Were the Days", "War Pigs",
                       "Hidden in the Depths", "Country Lode, Take Me Home", "Cover Me in Debris", "Subspace Bubble",
                       "A Terrible Fortress", "Spooky Scary SKeleton", "This Boat Has Legs", "Hot Tourist Destinations"],

            "The End": ["The End", "Free the End", "The Next Generation", "Remote Getaway",
                        "The City at the End of the Game", "Sky's the Limit", "Great View From Up Here",
                        "The End... Again...", "You Need a Mint"],

            "Adventure": ["Adventure", "Voluntary Exile", "Is It a Bird?", "Is It a Balloon?", "Is It a Plane?",
                          "Hero of the Village", "Monster Hunter", "A Throwaway Joke", "Very Very Frightening",
                          "Take Aim", "Sniper Duel", "Bullseye", "Monsters Hunted", "Postmortal", "What a Deal!",
                          "Hired Help", "Sticky Situation", "Ol' Betsy", "Two Birds, One Arrow",
                          "Who's the Pillager Now?", "Arbalistic", "Sweet Dreams", "Adventuring Time", "Surge Protector",
                          "Light as a Rabbit"],

            "Husbandry": ["Husbandry", "Bee Our Guest", "The Parrots and the Bats", "Two by Two", "Best Friends Forever",
                          "A Complete Catalogue", "Fishy Business", "Tactical Fishing", "Total Beelocation",
                          "A Seedy Place", "A Balanced Diet", "Serious Dedication", "Whatever Floats Your Goat!",
                          "Glow and Behold!", "Wax On", "Wax Off", "The Cutest Predator",
                          "The Healing Power of Friendship"],

            "Archipelago": ["Getting Wood", "Time to Mine!", "Hot Topic", "Bake Bread", "The Lie", "On a Rail",
                            "Time to Strike!", "Cow Tipper", "When Pigs Fly", "Overkill", "Librarian", "Overpowered"]
        }


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
    web = MinecraftWebWorld()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.id for name, data in advancement_table.items()}

    data_version = 5

    def _get_mc_data(self):
        exits = [connection[0] for connection in default_connections]
        return {
            'world_seed': self.world.slot_seeds[self.player].getrandbits(32),
            'seed_name': self.world.seed_name,
            'player_name': self.world.get_player_name(self.player),
            'player_id': self.player,
            'client_version': client_version,
            'structures': {exit: self.world.get_entrance(exit, self.player).connected_region.name for exit in exits},
            'advancement_goal': self.world.advancement_goal[self.player].value,
            'egg_shards_required': min(self.world.egg_shards_required[self.player].value,
                                       self.world.egg_shards_available[self.player].value),
            'egg_shards_available': self.world.egg_shards_available[self.player].value,
            'required_bosses': self.world.required_bosses[self.player].current_key,
            'MC35': bool(self.world.send_defeated_mobs[self.player].value),
            'death_link': bool(self.world.death_link[self.player].value),
            'starting_items': str(self.world.starting_items[self.player].value),
            'race': self.world.is_race,
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
        if self.world.egg_shards_required[self.player] > 0:
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
        exclusion_types = ['hard', 'unreasonable']
        for key in exclusion_types:
            if not getattr(self.world, f"include_{key}_advancements")[self.player]:
                exclusion_pool.update(exclusion_table[key])
        # For postgame advancements, check with the boss goal
        exclusion_pool.update(get_postgame_advancements(self.world.required_bosses[self.player].current_key))
        exclusion_rules(self.world, self.player, exclusion_pool)

        # Prefill event locations with their events
        self.world.get_location("Blaze Spawner", self.player).place_locked_item(self.create_item("Blaze Rods"))
        self.world.get_location("Ender Dragon", self.player).place_locked_item(self.create_item("Defeat Ender Dragon"))
        self.world.get_location("Wither", self.player).place_locked_item(self.create_item("Defeat Wither"))

        self.world.itempool += itempool

    def get_filler_item_name(self) -> str:
        return self.world.random.choices(list(junk_weights.keys()), weights=list(junk_weights.values()))[0]

    def set_rules(self):
        set_advancement_rules(self.world, self.player)
        set_completion_rules(self.world, self.player)

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
        filename = f"AP_{self.world.seed_name}_P{self.player}_{self.world.get_file_safe_player_name(self.player)}.apmc"
        with open(os.path.join(output_directory, filename), 'wb') as f:
            f.write(b64encode(bytes(json.dumps(data), 'utf-8')))

    def fill_slot_data(self):
        slot_data = self._get_mc_data()
        for option_name in minecraft_options:
            option = getattr(self.world, option_name)[self.player]
            if slot_data.get(option_name, None) is None and type(option.value) in {str, int}:
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
