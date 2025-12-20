# Python standard libraries
from collections import defaultdict
from math import ceil
from random import choice
from typing import Any, ClassVar, Callable, Union, cast

# Archipelago imports
import settings
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import components, Component, launch_subprocess, Type, icon_paths
from BaseClasses import (Item,
                         ItemClassification as ItemClass,
                         Tutorial,
                         CollectionState)
from Options import OptionGroup
from .data.additions import ADDITIONS
from .data.equipment import EQUIPMENT

# LoD imports
from .options import LegendOfDragoonOptions, lod_option_groups

from .locations import SHOP_LOCATIONS
from .data.items import ITEMS, ItemType
from .data.shops import ShopType

class LegendOfDragoonWebWorld(WebWorld):
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up ArchiDragoon (Archipelago on Severed Chains)",
        "English",
        "en_setup.md",
        "setup/en",
        ["pkolb-dev"]
    )

    tutorials = [setup_en]
    bug_report_page = "https://github.com/pkolb-dev/Archipelago/issues"
    option_groups = lod_option_groups
    options_presets = {}

class LegendOfDragoonWorld(World):
    """
    The Legend of Dragoon is a role-playing game developed and published by Sony Computer Entertainment for the video game console PlayStation.
    It was first released in Japan on December 2, 1999, in North America on June 11, 2000, and on January 19, 2001 in Europe.
    It was re-released in PlayStation Network December 22, 2010 in Japan and May 1, 2012 in North America.
    The game follows a young man, Dart Feld, on his journey through a world of magic, where ancient dragon warriors
    called Dragoons exist, to fight against evil forces who are threatening to destroy the world. 
    """
    
    # ID, name, version
    game = "The Legend of Dragoon"
    required_client_version = (0, 6, 0)

    # Web world
    web = LegendOfDragoonWebWorld()

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Severed Chains.",
        "English",
        "setup_en.md",
        "setup/en",
        ["pkolb-dev"]
    )

    tutorials = [setup_en]

    # Options
    options_dataclass = options.LegendOfDragoonOptions
    options: options.LegendOfDragoonOptions

    item_name_to_id = {item.name: item.key for item in ITEMS}
    location_name_to_id = {location.name: location.key for location in SHOP_LOCATIONS} # swap to LOCATIONS, rather than SHOP_LOCATIONS

    def create_items(self) -> None:
        items_made: int = 0
        for item_name in self.item_name_to_id:
            item_id = self.item_name_to_id[item_name]

    def get_filler_item_name(self) -> str:
        return ''

    def __init__(self, multiworld, player):
        super(LegendOfDragoonWorld, self).__init__(multiworld, player)
        self.randomized_shop_items = {}
        self.slots_by_shop = defaultdict(list)
        for loc in SHOP_LOCATIONS:
            self.slots_by_shop[loc.key].append(loc)

    def generate_shop_randomization(self, settings):
        healing_items = [item for item in ITEMS if item.item_type == ItemType.HEALING]
        attack_items = [item for item in ITEMS if item.item_type == ItemType.ATTACK]
        status_items = [item for item in ITEMS if item.item_type == ItemType.STATUS]

        for key, slots in self.slots_by_shop.items():
            for loc in slots:
                if loc.shop_type == ShopType.EQUIPMENT:
                    item = choice(attack_items)
                elif loc.shop_type == ShopType.ITEM:
                    item = choice(healing_items + status_items)
                else:
                    item = choice(ITEMS)

                self.randomized_shop_items[loc.id] = item

    def get_item_for_slot(self, shop_location_id):
        return self.randomized_shop_items.get(shop_location_id)
