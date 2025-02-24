
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Tutorial
from .Locations import location_table
from .Items import item_table
from typing import Any, Dict
from .client import BKClient


class BanjoKazooieWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Banjo-Kazooie randomizer connected to an Archipelago multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["JadeCurtiss90"]
    )]


class BanjoKazooieWorld(World):
    """
    Banjo-Kazooie is a 3D platforming game. You control Banjo the bear and Kazooie the bird on their quest to save
    Banjo's sister Tooty from the evil witch Gruntilda. Climb Grunty's Lair, explore 9 unique worlds, and defeat
    the evil witch!
    """
    web = BanjoKazooieWeb()

    game = "Banjo-Kazooie"
    topology_present = True

    data_version = 0
    required_client_version = (0, 3, 8)

    item_name_to_id = {name: data.ap_code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in location_table.items()}

    level_entrances = [
        ["Mumbo's Mountain", 1],
        ["Treasure Trove Cove", 2],
        ["Clanker's Cavern", 3],
        ["Bubblegloop Swamp", 4],
        ["Freezeezy Peak", 5],
        ["Gobi's Valley", 6],
        ["Mad Monster Mansion", 7],
        ["Rusty Bucket Bay", 8],
        ["Click Clock Wood", 9],
    ]

    def create_item(self, name: str):
        pass

    def create_items(self) -> None:
        pass

    def create_regions(self) -> None:
        pass

    def generate_early(self) -> None:
        pass

    def set_rules(self) -> None:
        pass
