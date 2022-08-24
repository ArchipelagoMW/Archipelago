import os
import typing
import math
import threading


from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification
from ..AutoWorld import WebWorld, World
from .Items import MMBN3Item, ItemData, item_table
from .Locations import MMBN3Location, all_locations, setup_locations


class MMBN3Web(WebWorld):
    theme = "ice"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the MegaMan Battle Network 3 Randomizer connected to an Archipelago Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["digiholic","XKirby"]
    )
    tutorials = [setup_en]


class MMBN3World(World):
    """
    Play as Lan and MegaMan to stop the evil organization WWW led by the nefarious
    Dr. Wily in their plans to take over the Net! Collect BattleChips, Customize your Navi,
    and utilize powerful Style Changes to grow strong enough to take on the greatest
    threat the Internet has ever faced!
    """
    game: str = "MegaMan Battle Network 3"

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = all_locations

    active_level_list: typing.List[str]
    web = MMBN3Web()

    def __init__(self, world: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(world, player)

    def create_item(self, name: str) -> "Item":
        pass
