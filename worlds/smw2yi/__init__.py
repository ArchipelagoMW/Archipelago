import os
import typing
import math
import threading

from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification
from .Items import YoshiItem, ItemData, item_table
from .Locations import YILocation, all_locations, setup_locations
from .Options import yoshi_options
from .Regions import create_regions, connect_regions
from .Rules import set_rules
from ..generic.Rules import add_rule
from .Names import ItemName, LocationName
from ..AutoWorld import WebWorld, World
from .Rom import get_base_rom_path

class YIWeb(WebWorld):
    theme = "grass"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "test",
        "ill",
        "write",
        "this",
        "later"
    )

    tutorials = [setup_en]


class YIWorld(World):
    """this is a game"""
    game: str = "Yoshis Island"
    option_definitions = yoshi_options
    topology_present = False
    data_version = 0
    required_client_version = (0, 3, 5)

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = all_locations

    web = YIWeb()

    def __init__(self, world: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(world, player)

    @classmethod
    def stage_assert_generate(cls, world):
        rom_file = get_base_rom_path()

    def _get_slot_data(self):
        return {
            #"death_link": self.world.death_link[self.player].value,
        }

    
    def _create_items(self, name: str):
        data = item_table[name]
        return [self.create_item(name)] * data.quantity


    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()
        for option_name in yoshi_options:
            option = getattr(self.world, option_name) [self.player]
            slot_data[option_name] = option.value

        return slot_data

    def generate_basic(self):
        itempool: typing.List[YoshiItem] = []
        
        
        total_required_locations = 1

        itempool += [self.create_item(ItemName.spring_ball)]
        itempool += [self.create_item(ItemName.large_spring)]
        itempool += [self.create_item(ItemName.push_switch)]


        self.world.itempool += itempool

    

    def create_regions(self):
        location_table = setup_locations(self.world, self.player)
        create_regions(self.world, self.player, location_table)




    def create_item(self, name: str, force_non_progression=False) -> Item:
        data = item_table[name]

        if force_non_progression:
            classification = ItemClassification.filler
        elif data.progression:
            classification = ItemClassification.progression
        else:
            classification = ItemClassification.filler

        created_item = YoshiItem(name, classification, data.code, self.player)

        return created_item

    

    def set_rules(self):
        set_rules(self.world, self.player)