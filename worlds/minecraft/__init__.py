import os
import json
import settings
import typing
from base64 import b64encode, b64decode
from typing import Dict, Any

from BaseClasses import Region, Entrance, Item, Tutorial, ItemClassification, Location
from worlds.AutoWorld import World, WebWorld

from . import Constants
from .Options import minecraft_options
from .Structures import shuffle_structures
from .ItemPool import build_item_pool, get_junk_item_names
from .Rules import set_rules

client_version = 9


class MinecraftSettings(settings.Group):
    class ForgeDirectory(settings.OptionalUserFolderPath):
        pass

    class ReleaseChannel(str):
        """
        release channel, currently "release", or "beta"
        any games played on the "beta" channel have a high likelihood of no longer working on the "release" channel.
        """

    forge_directory: ForgeDirectory = ForgeDirectory("Minecraft Forge server")
    max_heap_size: str = "2G"
    release_channel: ReleaseChannel = ReleaseChannel("release")


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

    setup_fr = Tutorial(
        setup.tutorial_name,
        setup.description,
        "Français",
        "minecraft_fr.md",
        "minecraft/fr",
        ["TheLynk"]
    )

    tutorials = [setup, setup_es, setup_sv, setup_fr]


class MinecraftWorld(World):
    """
    Minecraft is a game about creativity. In a world made entirely of cubes, you explore, discover, mine,
    craft, and try not to explode. Delve deep into the earth and discover abandoned mines, ancient
    structures, and materials to create a portal to another world. Defeat the Ender Dragon, and claim
    victory!
    """
    game: str = "Minecraft"
    option_definitions = minecraft_options
    settings: typing.ClassVar[MinecraftSettings]
    topology_present = True
    web = MinecraftWebWorld()

    item_name_to_id = Constants.item_name_to_id
    location_name_to_id = Constants.location_name_to_id

    data_version = 7

    def _get_mc_data(self) -> Dict[str, Any]:
        exits = [connection[0] for connection in Constants.region_info["default_connections"]]
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

    def create_item(self, name: str) -> Item:
        item_class = ItemClassification.filler
        if name in Constants.item_info["progression_items"]:
            item_class = ItemClassification.progression
        elif name in Constants.item_info["useful_items"]:
            item_class = ItemClassification.useful
        elif name in Constants.item_info["trap_items"]:
            item_class = ItemClassification.trap

        return MinecraftItem(name, item_class, self.item_name_to_id.get(name, None), self.player)

    def create_event(self, region_name: str, event_name: str) -> None:
        region = self.multiworld.get_region(region_name, self.player)
        loc = MinecraftLocation(self.player, event_name, None, region)
        loc.place_locked_item(self.create_event_item(event_name))
        region.locations.append(loc)

    def create_event_item(self, name: str) -> None:
        item = self.create_item(name)
        item.classification = ItemClassification.progression
        return item

    def create_regions(self) -> None:
        # Create regions
        for region_name, exits in Constants.region_info["regions"]:
            r = Region(region_name, self.player, self.multiworld)
            for exit_name in exits:
                r.exits.append(Entrance(self.player, exit_name, r))
            self.multiworld.regions.append(r)

        # Bind mandatory connections
        for entr_name, region_name in Constants.region_info["mandatory_connections"]:
            e = self.multiworld.get_entrance(entr_name, self.player)
            r = self.multiworld.get_region(region_name, self.player)
            e.connect(r)

        # Add locations
        for region_name, locations in Constants.location_info["locations_by_region"].items():
            region = self.multiworld.get_region(region_name, self.player)
            for loc_name in locations:
                loc = MinecraftLocation(self.player, loc_name,
                    self.location_name_to_id.get(loc_name, None), region)
                region.locations.append(loc)

        # Add events
        self.create_event("Nether Fortress", "Blaze Rods")
        self.create_event("The End", "Ender Dragon")
        self.create_event("Nether Fortress", "Wither")

        # Shuffle the connections
        shuffle_structures(self)

    def create_items(self) -> None:
        self.multiworld.itempool += build_item_pool(self)

    set_rules = set_rules

    def generate_output(self, output_directory: str) -> None:
        data = self._get_mc_data()
        filename = f"{self.multiworld.get_out_file_name_base(self.player)}.apmc"
        with open(os.path.join(output_directory, filename), 'wb') as f:
            f.write(b64encode(bytes(json.dumps(data), 'utf-8')))

    def fill_slot_data(self) -> dict:
        slot_data = self._get_mc_data()
        for option_name in minecraft_options:
            option = getattr(self.multiworld, option_name)[self.player]
            if slot_data.get(option_name, None) is None and type(option.value) in {str, int}:
                slot_data[option_name] = int(option.value)
        return slot_data

    def get_filler_item_name(self) -> str:
        return get_junk_item_names(self.multiworld.random, 1)[0]


class MinecraftLocation(Location):
    game = "Minecraft"

class MinecraftItem(Item):
    game = "Minecraft"


def mc_update_output(raw_data, server, port):
    data = json.loads(b64decode(raw_data))
    data['server'] = server
    data['port'] = port
    return b64encode(bytes(json.dumps(data), 'utf-8'))
